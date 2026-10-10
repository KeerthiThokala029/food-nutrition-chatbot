import re
from typing import Any, Dict, List, Optional


class FoodMatcher:
    """
    Selects the best food from USDA search results.

    This layer is intentionally strict for simple food queries.

    Examples:

        chicken
            -> generic chicken

        orange
            -> oranges, raw

        apple
            -> apple, raw

        banana
            -> bananas, raw

        brocolli
            -> broccoli, raw

    It avoids selecting things such as:

        chicken -> chicken feet
        orange  -> orange peel
        orange  -> orange tomatoes
        apple   -> rose-apples
        chicken -> fat, chicken
    """

    SPECIALIZED_TERMS = {
        "feet",
        "foot",
        "wing",
        "wings",
        "breast",
        "thigh",
        "thighs",
        "leg",
        "legs",
        "drumstick",
        "drumsticks",
        "liver",
        "heart",
        "gizzard",
        "neck",
        "skin",
        "peel",
        "juice",
        "nectar",
        "syrup",
        "jam",
        "jelly",
        "sauce",
        "spread",
        "soup",
        "stew",
        "curry",
        "salad",
        "cake",
        "pie",
        "cookie",
        "biscuit",
        "chips",
        "fries",
        "fried",
        "roasted",
        "roast",
        "grilled",
        "baked",
        "boiled",
        "steamed",
        "dried",
        "canned",
        "frozen",
        "pickled",
        "sweetened",
        "unsweetened",
        "flavored",
        "flavour",
        "breaded",
        "stuffed",
        "tender",
        "tenders",
        "nugget",
        "nuggets",
        "sausage",
        "frankfurter",
        "sandwich",
        "burger",
        "pizza",
        "pasta",
        "macaroni",
        "cheese",
        "sherbet",
        "cream",
        "drink",
        "beverage",
        "bar",
        "mix",
        "blend",
        "fat",
        "spread",
    }

    HARMLESS_DESCRIPTORS = {
        "raw",
        "fresh",
        "ripe",
        "slightly",
        "unripe",
        "plain",
        "whole",
        "large",
        "medium",
        "small",
        "red",
        "green",
        "yellow",
    }

    SPELLING_CORRECTIONS = {
        "brocolli": "broccoli",
        "brocoli": "broccoli",
        "broccolli": "broccoli",
        "tomatto": "tomato",
        "tomatos": "tomatoes",
        "aple": "apple",
        "appel": "apple",
        "bananna": "banana",
        "chiken": "chicken",
        "chickn": "chicken",
        "oranges": "orange",
        "bananas": "banana",
        "apples": "apple",
        "potatos": "potato",
        "potatoe": "potato",
        "carot": "carrot",
        "spinich": "spinach",
        "strawbery": "strawberry",
        "graps": "grape",
        "pineaple": "pineapple",
    }

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # TEXT NORMALIZATION
    # ------------------------------------------------------------------

    @staticmethod
    def normalize_text(text: str) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @staticmethod
    def tokens(text: str) -> List[str]:

        normalized = FoodMatcher.normalize_text(
            text
        )

        if not normalized:
            return []

        return normalized.split()

    @staticmethod
    def singular(word: str) -> str:

        if len(word) <= 3:
            return word

        if word.endswith("ies"):
            return word[:-3] + "y"

        if word.endswith("es") and not word.endswith("ses"):
            return word[:-2]

        if word.endswith("s"):
            return word[:-1]

        return word

    def correct_spelling(
        self,
        text: str,
    ) -> str:

        words = self.tokens(text)

        corrected = []

        for word in words:

            corrected.append(
                self.SPELLING_CORRECTIONS.get(
                    word,
                    word,
                )
            )

        return " ".join(corrected)

    # ------------------------------------------------------------------
    # FOOD DESCRIPTION HELPERS
    # ------------------------------------------------------------------

    def _normalized_description(
        self,
        food: Dict[str, Any],
    ) -> str:

        return self.normalize_text(
            food.get("description", "")
        )

    def _food_tokens(
        self,
        food: Dict[str, Any],
    ) -> List[str]:

        return self.tokens(
            food.get("description", "")
        )

    def _singular_tokens(
        self,
        words: List[str],
    ) -> List[str]:

        return [
            self.singular(word)
            for word in words
        ]

    # ------------------------------------------------------------------
    # EXACT MATCH
    # ------------------------------------------------------------------

    def _exact_match(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:

        normalized_query = self.correct_spelling(
            query
        )

        query_tokens = self._singular_tokens(
            self.tokens(normalized_query)
        )

        query_set = set(query_tokens)

        exact_candidates = []

        for candidate in candidates:

            description = self._normalized_description(
                candidate
            )

            if not description:
                continue

            description_tokens = (
                self._singular_tokens(
                    self.tokens(description)
                )
            )

            description_set = set(
                description_tokens
            )

            # Exact normalized description.
            if description == normalized_query:

                exact_candidates.append(
                    candidate
                )
                continue

            # Exact token-equivalent description.
            if description_set == query_set:

                exact_candidates.append(
                    candidate
                )

        if not exact_candidates:
            return None

        # Prefer Foundation, then SR Legacy,
        # then Survey.
        priority = {
            "Foundation": 3,
            "SR Legacy": 2,
            "Survey (FNDDS)": 1,
            "Branded": 0,
        }

        exact_candidates.sort(
            key=lambda food: priority.get(
                food.get("dataType"),
                0,
            ),
            reverse=True,
        )

        return exact_candidates[0]

    # ------------------------------------------------------------------
    # SCORE
    # ------------------------------------------------------------------

    def _score_candidate(
        self,
        query: str,
        candidate: Dict[str, Any],
    ) -> float:

        corrected_query = self.correct_spelling(
            query
        )

        query_tokens = self._singular_tokens(
            self.tokens(corrected_query)
        )

        description = self._normalized_description(
            candidate
        )

        description_tokens = self._singular_tokens(
            self.tokens(description)
        )

        if not query_tokens or not description_tokens:
            return -10000

        query_set = set(query_tokens)
        description_set = set(description_tokens)

        score = 0.0

        data_type = str(
            candidate.get("dataType", "")
        )

        # --------------------------------------------------------------
        # USDA DATA TYPE
        # --------------------------------------------------------------

        type_priority = {
            "Foundation": 500,
            "SR Legacy": 480,
            "Survey (FNDDS)": 350,
            "Branded": -1000,
        }

        score += type_priority.get(
            data_type,
            0,
        )

        # --------------------------------------------------------------
        # EXACT MATCH
        # --------------------------------------------------------------

        if description == corrected_query:
            score += 5000

        if description_set == query_set:
            score += 4000

        # --------------------------------------------------------------
        # REQUESTED WORDS
        # --------------------------------------------------------------

        matched = query_set.intersection(
            description_set
        )

        score += len(matched) * 500

        missing = query_set - description_set

        score -= len(missing) * 1000

        # --------------------------------------------------------------
        # EXTRA WORDS
        # --------------------------------------------------------------

        extra = (
            description_set - query_set
        )

        # A basic query like "orange" should not match
        # "tomatoes, orange, raw".
        for word in extra:

            if word in self.HARMLESS_DESCRIPTORS:
                score += 10
            else:
                score -= 350

        # --------------------------------------------------------------
        # SPECIALIZED TERMS
        # --------------------------------------------------------------

        for word in self.SPECIALIZED_TERMS:

            if word in description_set:

                # User explicitly requested it.
                if word in query_set:
                    score += 100

                else:
                    score -= 800

        # --------------------------------------------------------------
        # RAW FOOD PREFERENCE
        # --------------------------------------------------------------

        if "raw" in description_tokens:
            score += 100

        # --------------------------------------------------------------
        # SHORT GENERIC DESCRIPTION PREFERENCE
        # --------------------------------------------------------------

        if len(description_tokens) <= 3:
            score += 80

        elif len(description_tokens) <= 5:
            score += 30

        # --------------------------------------------------------------
        # SIMPLE QUERY SAFETY
        # --------------------------------------------------------------

        if len(query_set) == 1:

            requested_word = next(
                iter(query_set)
            )

            # The requested word should be the actual food,
            # not merely an adjective describing another food.
            #
            # Example:
            #   orange -> tomatoes, orange, raw
            # should lose heavily.
            if requested_word in description_set:

                non_harmless = [
                    word
                    for word in description_set
                    if word != requested_word
                    and word
                    not in self.HARMLESS_DESCRIPTORS
                ]

                score -= (
                    len(non_harmless) * 500
                )

        return score

    # ------------------------------------------------------------------
    # PUBLIC MATCH
    # ------------------------------------------------------------------

    def find_best_match(
        self,
        food_query: str,
        candidates: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:

        if not food_query:
            return None

        if not candidates:
            return None

        # --------------------------------------------------------------
        # 1. Exact generic match.
        # --------------------------------------------------------------

        exact = self._exact_match(
            food_query,
            candidates,
        )

        if exact:

            result = dict(exact)

            result["_match_score"] = 99999.0
            result["_original_query"] = food_query
            result["_corrected_query"] = (
                self.correct_spelling(food_query)
            )

            result["_spelling_corrected"] = (
                result["_corrected_query"]
                != self.normalize_text(food_query)
            )

            return result

        # --------------------------------------------------------------
        # 2. Score all candidates.
        # --------------------------------------------------------------

        scored = []

        for candidate in candidates:

            score = self._score_candidate(
                food_query,
                candidate,
            )

            item = dict(candidate)

            item["_match_score"] = score

            item["_original_query"] = food_query

            item["_corrected_query"] = (
                self.correct_spelling(food_query)
            )

            item["_spelling_corrected"] = (
                item["_corrected_query"]
                != self.normalize_text(food_query)
            )

            scored.append(item)

        # --------------------------------------------------------------
        # 3. Sort.
        # --------------------------------------------------------------

        scored.sort(
            key=lambda item: item["_match_score"],
            reverse=True,
        )

        # --------------------------------------------------------------
        # 4. Return best candidate.
        # --------------------------------------------------------------

        if not scored:
            return None

        return scored[0]

    # ------------------------------------------------------------------
    # DEBUG
    # ------------------------------------------------------------------

    def debug_match(
        self,
        food_query: str,
        candidates: List[Dict[str, Any]],
        limit: int = 10,
    ):

        print()
        print("=" * 90)
        print(
            f"FOOD MATCHER DEBUG: {food_query}"
        )
        print("=" * 90)

        scored = []

        for candidate in candidates:

            score = self._score_candidate(
                food_query,
                candidate,
            )

            scored.append(
                (
                    score,
                    candidate,
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        for index, (
            score,
            candidate,
        ) in enumerate(
            scored[:limit],
            start=1,
        ):

            print(
                f"{index}. "
                f"{candidate.get('description')} | "
                f"{candidate.get('dataType')} | "
                f"score={score:.2f}"
            )


# ----------------------------------------------------------------------
# TEST
# ----------------------------------------------------------------------

if __name__ == "__main__":

    matcher = FoodMatcher()

    test_candidates = [
        {
            "description": "Chicken, meat, raw",
            "dataType": "Foundation",
            "fdcId": 1,
        },
        {
            "description": "Chicken feet, raw",
            "dataType": "SR Legacy",
            "fdcId": 2,
        },
        {
            "description": "Fat, chicken",
            "dataType": "SR Legacy",
            "fdcId": 3,
        },
        {
            "description": "Oranges, raw",
            "dataType": "Foundation",
            "fdcId": 4,
        },
        {
            "description": "Tomatoes, orange, raw",
            "dataType": "SR Legacy",
            "fdcId": 5,
        },
        {
            "description": "Apple, raw, with skin",
            "dataType": "Foundation",
            "fdcId": 6,
        },
        {
            "description": "Rose-apples, raw",
            "dataType": "SR Legacy",
            "fdcId": 7,
        },
        {
            "description": "Bananas, raw",
            "dataType": "SR Legacy",
            "fdcId": 8,
        },
        {
            "description": "Broccoli, raw",
            "dataType": "Foundation",
            "fdcId": 9,
        },
    ]

    tests = [
        "chicken",
        "orange",
        "apple",
        "banana",
        "brocolli",
    ]

    for query in tests:

        best = matcher.find_best_match(
            query,
            test_candidates,
        )

        print()
        print(
            f"QUERY: {query}"
        )

        if best:

            print(
                f"BEST: "
                f"{best.get('description')}"
            )

            print(
                f"TYPE: "
                f"{best.get('dataType')}"
            )

            print(
                f"SCORE: "
                f"{best.get('_match_score')}"
            )

        else:

            print(
                "NO MATCH"
            )