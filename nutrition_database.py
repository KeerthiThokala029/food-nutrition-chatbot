
import os
import re
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from rapidfuzz import fuzz


load_dotenv()


class NutritionDatabase:
    """
    USDA FoodData Central API wrapper.

    Responsibilities:
    1. Search USDA foods.
    2. Fetch detailed nutrition data for an FDC ID.
    3. Extract normalized nutrient values.
    4. Provide robust matching for common food queries.
    """

    BASE_URL = "https://api.nal.usda.gov/fdc/v1"

    CANONICAL_QUERIES = {
        "apple": "apple raw",
        "apples": "apple raw",
        "banana": "banana raw",
        "bananas": "banana raw",
        "orange": "orange raw",
        "oranges": "orange raw",
        "broccoli": "broccoli raw",
        "brocolli": "broccoli raw",
        "tomato": "tomato raw",
        "tomatoes": "tomato raw",
        "tomatto": "tomato raw",
        "chicken": "chicken meat only raw",
        "chickens": "chicken meat only raw",
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
        "bananas": "banana",
        "oranges": "orange",
        "chikcen": "chicken",
        "chiken": "chicken",
        "chickn": "chicken",
    }

    SPECIALIZED_TERMS = {
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
        "sauce",
        "sauces",
        "fried",
        "roasted",
        "roasting",
        "baked",
        "boiled",
        "cooked",
        "grilled",
        "canned",
        "dried",
        "dehydrated",
        "chips",
        "powder",
        "burger",
        "pizza",
        "pasta",
        "cheese",
        "cream",
        "drink",
        "bar",
        "mix",
        "blend",
        "fat",
        "spread",
        "casserole",
        "soup",
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
        "white",
    }

    def __init__(self):
        self.api_key = os.getenv("USDA_API_KEY")

        if not self.api_key:
            raise ValueError(
                "USDA_API_KEY was not found. "
                "Make sure your .env file contains USDA_API_KEY=your_key"
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Food-Nutrition-Chatbot/1.0"
            }
        )

    # ============================================================
    # BASIC HELPERS
    # ============================================================

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = str(text or "").lower().strip()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def correct_spelling(self, text: str) -> str:
        words = self._normalize_text(text).split()

        corrected = [
            self.SPELLING_CORRECTIONS.get(word, word)
            for word in words
        ]

        return " ".join(corrected)

    @staticmethod
    def _singularize(word: str) -> str:
        word = word.lower()

        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"

        if word.endswith("oes") and len(word) > 4:
            return word[:-2]

        if word.endswith("es") and len(word) > 4:
            return word[:-2]

        if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
            return word[:-1]

        return word

    def _tokens(self, text: str) -> List[str]:
        return [
            self._singularize(word)
            for word in self._normalize_text(text).split()
            if word
        ]

    # ============================================================
    # USDA SEARCH
    # ============================================================

    def search_food(
        self,
        query: str,
        page_size: int = 25,
    ) -> List[Dict[str, Any]]:
        """
        Search USDA FoodData Central.

        Returns the USDA food records from the search endpoint.
        """

        if not query:
            return []

        corrected = self.correct_spelling(query)

        canonical = self.CANONICAL_QUERIES.get(
            corrected,
            corrected,
        )

        url = f"{self.BASE_URL}/foods/search"

        params = {
            "api_key": self.api_key,
            "query": canonical,
            "pageSize": page_size,
        }

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=20,
            )

            response.raise_for_status()

            data = response.json()

            foods = data.get("foods", [])

            if not isinstance(foods, list):
                return []

            return foods

        except requests.RequestException as exc:
            print(f"USDA search error: {exc}")
            return []

        except ValueError as exc:
            print(f"USDA returned invalid JSON: {exc}")
            return []

    # ============================================================
    # MATCHING
    # ============================================================

    def is_valid_chicken(self, description: str) -> bool:
        text = self._normalize_text(description)

        if "chicken" not in text:
            return False

        forbidden = [
            "wing",
            "wings",
            "breast",
            "thigh",
            "leg",
            "drumstick",
            "liver",
            "heart",
            "gizzard",
            "neck",
            "skin",
            "feet",
            "sausage",
            "soup",
            "salad",
            "sandwich",
            "burger",
            "pizza",
            "casserole",
            "stew",
        ]

        return not any(word in text.split() for word in forbidden)

    def is_bad_generic_match(
        self,
        query: str,
        description: str,
    ) -> bool:
        query_tokens = set(self._tokens(query))
        desc_tokens = set(self._tokens(description))

        if not query_tokens:
            return False

        # Specialized terms that weren't requested.
        for term in self.SPECIALIZED_TERMS:
            if term in desc_tokens and term not in query_tokens:
                return True

        # For a simple food query, avoid unrelated compound foods.
        if len(query_tokens) == 1:
            food = next(iter(query_tokens))

            if food not in desc_tokens:
                return True

            if len(desc_tokens) > 6:
                return True

        return False

    def score_candidate(
        self,
        query: str,
        food: Dict[str, Any],
    ) -> float:
        description = (
            food.get("description")
            or food.get("lowercaseDescription")
            or ""
        )

        if not description:
            return -10000

        query_corrected = self.correct_spelling(query)

        query_tokens = set(self._tokens(query_corrected))
        desc_tokens = set(self._tokens(description))

        score = 0.0

        data_type = str(
            food.get("dataType")
            or food.get("datatype")
            or ""
        ).lower()

        if data_type == "foundation":
            score += 500

        elif data_type == "sr legacy":
            score += 480

        elif data_type == "survey (fndds)":
            score += 350

        elif data_type == "branded":
            score -= 1000

        # Exact normalized description.
        if self._normalize_text(description) == self._normalize_text(
            query_corrected
        ):
            score += 5000

        # Exact token equality.
        if query_tokens == desc_tokens:
            score += 4000

        matched = query_tokens.intersection(desc_tokens)
        missing = query_tokens.difference(desc_tokens)

        score += len(matched) * 500
        score -= len(missing) * 1000

        # Prefer raw food when the user did not request cooking.
        if "raw" in desc_tokens:
            score += 100

        # Penalize unrelated specialized forms.
        if self.is_bad_generic_match(query_corrected, description):
            score -= 3000

        # Chicken needs special protection from wings/breast/etc.
        if "chicken" in query_tokens:
            if self.is_valid_chicken(description):
                score += 1000
            else:
                score -= 5000

        # Prefer short, simple descriptions for simple queries.
        if len(desc_tokens) <= len(query_tokens) + 2:
            score += 200

        score += fuzz.token_set_ratio(
            self._normalize_text(query_corrected),
            self._normalize_text(description),
        ) * 2

        return score

    def find_best_food(
        self,
        query: str,
        candidates: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        if candidates is None:
            candidates = self.search_food(query)

        if not candidates:
            return None

        scored = []

        for food in candidates:
            score = self.score_candidate(query, food)

            item = dict(food)
            item["_match_score"] = score
            item["_original_query"] = query
            item["_corrected_query"] = self.correct_spelling(query)

            scored.append(item)

        scored.sort(
            key=lambda item: item.get("_match_score", -999999),
            reverse=True,
        )

        return scored[0]

    # ============================================================
    # FOOD DETAILS
    # ============================================================

    def get_food_details(
        self,
        fdc_id: Any,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch the complete USDA food record.

        USDA's Food Details endpoint is:
        /food/{fdcId}
        """

        if not fdc_id:
            return None

        url = f"{self.BASE_URL}/food/{fdc_id}"

        params = {
            "api_key": self.api_key,
        }

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=20,
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                return None

            return data

        except requests.HTTPError as exc:
            print(
                f"USDA food details HTTP error "
                f"for FDC ID {fdc_id}: {exc}"
            )
            return None

        except requests.RequestException as exc:
            print(
                f"USDA food details request error "
                f"for FDC ID {fdc_id}: {exc}"
            )
            return None

        except ValueError as exc:
            print(
                f"USDA food details returned invalid JSON "
                f"for FDC ID {fdc_id}: {exc}"
            )
            return None

    # ============================================================
    # NUTRIENT NAME NORMALIZATION
    # ============================================================

    @staticmethod
    def normalize_nutrient_name(name: str) -> str:
        text = str(name or "").lower().strip()

        replacements = {
            "energy": "energy",
            "energy (atwater general factors)": "energy",
            "energy (atwater specific factors)": "energy",
            "protein": "protein",
            "total lipid (fat)": "fat",
            "total lipid": "fat",
            "fat": "fat",
            "carbohydrate, by difference": "carbohydrates",
            "carbohydrate": "carbohydrates",
            "fiber, total dietary": "fiber",
            "dietary fiber": "fiber",
            "sugars, total including nlea": "sugars",
            "total sugars": "sugars",
            "sodium, na": "sodium",
            "sodium": "sodium",
            "calcium, ca": "calcium",
            "calcium": "calcium",
            "iron, fe": "iron",
            "iron": "iron",
            "potassium, k": "potassium",
            "potassium": "potassium",
            "magnesium, mg": "magnesium",
            "magnesium": "magnesium",
            "phosphorus, p": "phosphorus",
            "phosphorus": "phosphorus",
            "zinc, zn": "zinc",
            "zinc": "zinc",
            "vitamin c, total ascorbic acid": "vitamin c",
            "vitamin c": "vitamin c",
            "vitamin a, rae": "vitamin a",
            "vitamin a": "vitamin a",
            "vitamin e (alpha-tocopherol)": "vitamin e",
            "vitamin e": "vitamin e",
            "vitamin d (d2 + d3)": "vitamin d",
            "vitamin d": "vitamin d",
            "vitamin k (phylloquinone)": "vitamin k",
            "vitamin k": "vitamin k",
        }

        if text in replacements:
            return replacements[text]

        if "energy" in text:
            return "energy"

        if "protein" in text:
            return "protein"

        if "lipid" in text or text == "fat":
            return "fat"

        if "carbohydrate" in text:
            return "carbohydrates"

        if "fiber" in text:
            return "fiber"

        if "sugar" in text:
            return "sugars"

        if "sodium" in text:
            return "sodium"

        if "calcium" in text:
            return "calcium"

        if "iron" in text:
            return "iron"

        if "potassium" in text:
            return "potassium"

        if "magnesium" in text:
            return "magnesium"

        if "phosphorus" in text:
            return "phosphorus"

        if "zinc" in text:
            return "zinc"

        if "vitamin c" in text:
            return "vitamin c"

        if "vitamin a" in text:
            return "vitamin a"

        if "vitamin e" in text:
            return "vitamin e"

        if "vitamin d" in text:
            return "vitamin d"

        if "vitamin k" in text:
            return "vitamin k"

        return text

    # ============================================================
    # NUTRIENT EXTRACTION
    # ============================================================

    def extract_nutrients(
        self,
        food_details: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:
        """
        Convert USDA foodNutrients into a simple normalized dictionary.

        Example:

        {
            "energy": {
                "value": 52.0,
                "unit": "kcal",
                "original_name": "Energy"
            },
            "protein": {
                "value": 0.26,
                "unit": "g",
                "original_name": "Protein"
            }
        }
        """

        result: Dict[str, Dict[str, Any]] = {}

        nutrients = food_details.get("foodNutrients", [])

        if not isinstance(nutrients, list):
            return result

        for nutrient_item in nutrients:
            if not isinstance(nutrient_item, dict):
                continue

            # USDA API records may expose the nutrient name/unit in
            # slightly different nested structures depending on data type.
            nutrient_info = nutrient_item.get("nutrient")

            if isinstance(nutrient_info, dict):
                name = (
                    nutrient_info.get("name")
                    or nutrient_info.get("nutrientName")
                    or ""
                )

                unit = (
                    nutrient_info.get("unitName")
                    or nutrient_info.get("unit")
                    or ""
                )

            else:
                name = (
                    nutrient_item.get("nutrientName")
                    or nutrient_item.get("name")
                    or ""
                )

                unit = (
                    nutrient_item.get("unitName")
                    or nutrient_item.get("unitName")
                    or nutrient_item.get("unit")
                    or ""
                )

            # Value may be under amount or value.
            value = nutrient_item.get("amount")

            if value is None:
                value = nutrient_item.get("value")

            # Some API records expose nutrient amount inside a nested object.
            if value is None and isinstance(
                nutrient_item.get("nutrient"),
                dict,
            ):
                value = nutrient_item["nutrient"].get("amount")

            if not name or value is None:
                continue

            try:
                value = float(value)
            except (TypeError, ValueError):
                continue

            normalized = self.normalize_nutrient_name(name)

            if not normalized:
                continue

            normalized_unit = str(unit or "").lower().strip()

            # Energy is special: USDA may report kcal or kJ.
            if normalized == "energy":
                if "kcal" in normalized_unit:
                    normalized_unit = "kcal"
                elif normalized_unit == "kj" or "kilojoule" in normalized_unit:
                    normalized_unit = "kJ"

            result[normalized] = {
                "value": value,
                "unit": normalized_unit,
                "original_name": name,
            }

        return result

    # ============================================================
    # COMPLETE FOOD LOOKUP
    # ============================================================

    def lookup_food(
        self,
        query: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Search + select best food + fetch full USDA details.
        """

        candidates = self.search_food(query)

        if not candidates:
            return None

        best = self.find_best_food(
            query,
            candidates,
        )

        if not best:
            return None

        fdc_id = (
            best.get("fdcId")
            or best.get("fdcID")
            or best.get("fdc_id")
        )

        if not fdc_id:
            return None

        details = self.get_food_details(fdc_id)

        if not details:
            return None

        nutrients = self.extract_nutrients(details)

        if not nutrients:
            print(
                f"USDA returned food details but no usable nutrients "
                f"for FDC ID {fdc_id}"
            )
            return None

        details["_match_score"] = best.get("_match_score", 0)
        details["_original_query"] = query
        details["_corrected_query"] = best.get(
            "_corrected_query",
            query,
        )
        details["_matched_description"] = (
            details.get("description")
            or best.get("description")
            or query
        )
        details["_nutrients"] = nutrients

        return details


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":
    db = NutritionDatabase()

    test_foods = [
        "chicken",
        "orange",
        "apple",
        "banana",
        "brocolli",
    ]

    print("\n" + "=" * 70)
    print("USDA DATABASE TEST")
    print("=" * 70)

    for query in test_foods:
        print(f"\nSEARCH: {query}")

        candidates = db.search_food(query)

        if not candidates:
            print("No USDA search results.")
            continue

        best = db.find_best_food(query, candidates)

        if not best:
            print("No best match.")
            continue

        print(
            f"BEST MATCH: "
            f"{best.get('description')} "
            f"| FDC ID={best.get('fdcId')} "
            f"| score={best.get('_match_score', 0):.2f}"
        )

        details = db.get_food_details(
            best.get("fdcId")
        )

        if not details:
            print("DETAILS FAILED")
            continue

        print(
            f"DETAILS OK: "
            f"{details.get('description')}"
        )

        nutrients = db.extract_nutrients(details)

        print(
            f"NUTRIENTS FOUND: {len(nutrients)}"
        )

        for nutrient_name in [
            "energy",
            "protein",
            "carbohydrates",
            "fat",
            "fiber",
            "sugars",
            "sodium",
            "calcium",
            "iron",
            "potassium",
            "magnesium",
            "phosphorus",
            "zinc",
        ]:
            if nutrient_name in nutrients:
                item = nutrients[nutrient_name]

                print(
                    f"  {nutrient_name}: "
                    f"{item['value']} {item['unit']}"
                )
