import re

from nlp_processor import NLPProcessor
from nutrition_database import NutritionDatabase
from portion_resolver import PortionResolver


class FoodNutritionChatbot:

    # ========================================================
    # COMMON FOOD SPELLING CORRECTIONS
    # ========================================================

    SPELLING_CORRECTIONS = {
        "aple": "apple",
        "appel": "apple",
        "apples": "apple",

        "bananna": "banana",
        "bananas": "banana",

        "brocolli": "broccoli",
        "brocoli": "broccoli",
        "broccolli": "broccoli",
        "brocoly": "broccoli",

        "chiken": "chicken",
        "chickn": "chicken",
        "chiken": "chicken",

        "tomatto": "tomato",
        "tomatos": "tomato",

        "oranges": "orange",

        "potatos": "potato",
        "potatoes": "potato",

        "carots": "carrot",
        "carrots": "carrot",

        "spinich": "spinach",

        "straberry": "strawberry",
        "strawbery": "strawberry",
        "strawberries": "strawberry",

        "mangoes": "mango",
        "mangos": "mango",

        "grapes": "grape",
    }

    # ========================================================
    # SPECIALIZED USDA TERMS
    # ========================================================

    SPECIALIZED_TERMS = {
        "pepper",
        "juice",
        "sauce",
        "chips",
        "powder",
        "cake",
        "bread",
        "pudding",
        "smoothie",
        "nectar",
        "split",
        "burger",
        "sandwich",
        "pizza",
        "salad",
        "soup",
        "stew",
        "casserole",
        "wings",
        "breast",
        "thigh",
        "drumstick",
        "leg",
        "liver",
        "heart",
        "gizzard",
        "neck",
        "feet",
        "skin",
        "cheese",
        "cream",
        "drink",
        "beverage",
        "spread",
        "fat",
        "mix",
        "blend",
        "bar",
        "strudel",
        "marmalade",
        "roasted",
        "fried",
        "boiled",
        "grilled",
    }

    SIMPLE_FOODS = {
        "banana",
        "apple",
        "orange",
        "broccoli",
        "chicken",
        "tomato",
        "potato",
        "carrot",
        "spinach",
        "mango",
        "grape",
        "strawberry",
    }

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        self.nlp = NLPProcessor()

        self.database = NutritionDatabase()

        self.portion_resolver = PortionResolver()

    # ========================================================
    # HELPERS
    # ========================================================

    def _get_value(
        self,
        obj,
        key,
        default=None,
    ):

        if isinstance(obj, dict):

            return obj.get(
                key,
                default,
            )

        return getattr(
            obj,
            key,
            default,
        )

    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    def _normalize_text(
        self,
        text,
    ):

        if text is None:
            return ""

        text = str(text).lower().strip()

        text = re.sub(
            r"[^a-z0-9\s-]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # ========================================================
    # CORRECT SPELLING
    # ========================================================

    def _correct_food_spelling(
        self,
        food_name,
    ):

        food_name = self._normalize_text(
            food_name
        )

        if not food_name:
            return food_name

        words = food_name.split()

        corrected_words = []

        for word in words:

            corrected_words.append(
                self.SPELLING_CORRECTIONS.get(
                    word,
                    word,
                )
            )

        return " ".join(
            corrected_words
        )

    # ========================================================
    # CLEAN FOOD NAME
    # ========================================================

    def _clean_food_name(
        self,
        food_name,
    ):

        if not food_name:
            return ""

        food_name = str(
            food_name
        ).strip().lower()

        removable_words = {
            "of",
            "the",
            "some",
            "food",
            "please",
            "tell",
            "me",
            "about",
            "nutrition",
            "nutritional",
        }

        words = food_name.split()

        words = [
            word
            for word in words
            if word not in removable_words
        ]

        cleaned = " ".join(words)

        return self._correct_food_spelling(
            cleaned
        )

    # ========================================================
    # NLP
    # ========================================================

    def _process_nlp(
        self,
        user_input,
    ):

        if hasattr(
            self.nlp,
            "process",
        ):

            return self.nlp.process(
                user_input
            )

        if hasattr(
            self.nlp,
            "parse",
        ):

            return self.nlp.parse(
                user_input
            )

        if hasattr(
            self.nlp,
            "process_text",
        ):

            return self.nlp.process_text(
                user_input
            )

        raise AttributeError(
            "NLPProcessor does not have "
            "a supported processing method."
        )

    # ========================================================
    # FOOD SELECTION
    # ========================================================

    def _select_food(
        self,
        food_query,
        candidates,
    ):

        if not candidates:
            return None

        query = self._correct_food_spelling(
            food_query
        )

        query = self._normalize_text(
            query
        )

        query_words = set(
            query.split()
        )

        # Singular normalization
        normalized_query_words = set()

        for word in query_words:

            normalized_query_words.add(
                word
            )

            if word.endswith("s"):

                normalized_query_words.add(
                    word[:-1]
                )

        query_words = normalized_query_words

        scored = []

        for candidate in candidates:

            description = self._get_value(
                candidate,
                "description",
                "",
            )

            if not description:
                continue

            description = str(
                description
            )

            normalized_description = (
                self._normalize_text(
                    description
                )
            )

            description_words = set(
                normalized_description.split()
            )

            # Normalize plural candidate words
            candidate_words = set(
                description_words
            )

            for word in list(
                description_words
            ):

                if word.endswith("s"):

                    candidate_words.add(
                        word[:-1]
                    )

            score = 0

            # ------------------------------------------------
            # Exact description
            # ------------------------------------------------

            if (
                normalized_description
                == query
            ):

                score += 20000

            # ------------------------------------------------
            # Exact generic food
            # ------------------------------------------------

            generic_words = {
                word
                for word in candidate_words
                if word not in {
                    "raw",
                    "fresh",
                    "plain",
                    "whole",
                    "ripe",
                    "unripe",
                    "medium",
                    "large",
                    "small",
                    "red",
                    "green",
                    "yellow",
                    "california",
                    "florida",
                    "navel",
                    "commercial",
                    "varieties",
                }
            }

            if generic_words == query_words:

                score += 12000

            # ------------------------------------------------
            # Query words
            # ------------------------------------------------

            matched_words = (
                query_words
                & candidate_words
            )

            score += (
                len(matched_words)
                * 1500
            )

            # ------------------------------------------------
            # Raw food preference
            # ------------------------------------------------

            if "raw" in description_words:

                score += 500

            # ------------------------------------------------
            # Specialized food penalty
            # ------------------------------------------------

            for term in (
                self.SPECIALIZED_TERMS
            ):

                if term in description_words:

                    if term not in query_words:

                        score -= 5000

            # ------------------------------------------------
            # Simple food protection
            # ------------------------------------------------

            if query in self.SIMPLE_FOODS:

                # Generic description should be short.
                extra_words = (
                    len(candidate_words)
                    - len(query_words)
                )

                if extra_words == 0:

                    score += 5000

                elif extra_words <= 2:

                    score += 1500

                else:

                    score -= (
                        extra_words
                        * 500
                    )

            # ------------------------------------------------
            # Data type
            # ------------------------------------------------

            data_type = str(
                self._get_value(
                    candidate,
                    "dataType",
                    "",
                )
            ).lower()

            if data_type == "foundation":

                score += 700

            elif data_type == "sr legacy":

                score += 600

            elif data_type == "survey":

                score += 300

            elif data_type == "branded":

                score -= 3000

            # ------------------------------------------------
            # Preserve candidate
            # ------------------------------------------------

            candidate_copy = dict(
                candidate
            )

            candidate_copy[
                "_chatbot_score"
            ] = score

            scored.append(
                candidate_copy
            )

        if not scored:

            return candidates[0]

        scored.sort(
            key=lambda item: item.get(
                "_chatbot_score",
                -999999,
            ),
            reverse=True,
        )

        return scored[0]

    # ========================================================
    # PORTION
    # ========================================================

    def _resolve_portion(
        self,
        food_name,
        quantity,
        unit,
        food_details=None,
    ):

        try:

            return (
                self.portion_resolver
                .resolve_portion(
                    food_name=food_name,
                    quantity=quantity,
                    unit=unit,
                    food_details=food_details,
                )
            )

        except TypeError:

            try:

                return (
                    self.portion_resolver
                    .resolve_portion(
                        food_name,
                        quantity,
                        unit,
                        food_details,
                    )
                )

            except TypeError:

                return (
                    self.portion_resolver
                    .resolve_portion(
                        food_name,
                        quantity,
                        unit,
                    )
                )

    # ========================================================
    # ENERGY CONVERSION
    # ========================================================

    def _convert_energy_to_kcal(
        self,
        value,
        unit,
    ):

        try:

            value = float(value)

        except (
            TypeError,
            ValueError,
        ):

            return value, unit

        if not unit:

            return value, "kcal"

        unit_lower = str(
            unit
        ).lower()

        if unit_lower in {
            "kj",
            "kilojoule",
            "kilojoules",
        }:

            return (
                value / 4.184,
                "kcal",
            )

        return value, unit

    # ========================================================
    # NUTRITION CALCULATION
    # ========================================================

    def _calculate_nutrition(
        self,
        nutrients,
        grams,
    ):

        if not nutrients:
            return {}

        try:

            grams = float(
                grams
            )

        except (
            TypeError,
            ValueError,
        ):

            grams = 100.0

        multiplier = (
            grams / 100.0
        )

        calculated = {}

        for nutrient_name, data in (
            nutrients.items()
        ):

            value = None
            unit = ""

            if isinstance(
                data,
                dict,
            ):

                value = data.get(
                    "value",
                    data.get(
                        "amount",
                        data.get(
                            "quantity"
                        ),
                    ),
                )

                unit = data.get(
                    "unit",
                    "",
                )

            else:

                value = data

            if value is None:
                continue

            try:

                value = (
                    float(value)
                    * multiplier
                )

            except (
                TypeError,
                ValueError,
            ):

                continue

            # Energy conversion
            if (
                nutrient_name
                == "energy"
            ):

                value, unit = (
                    self._convert_energy_to_kcal(
                        value,
                        unit,
                    )
                )

            calculated[
                nutrient_name
            ] = {
                "value": value,
                "unit": unit,
            }

        return calculated

    # ========================================================
    # NUMBER FORMAT
    # ========================================================

    def _format_number(
        self,
        value,
    ):

        try:

            value = float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return str(value)

        if abs(value) >= 100:

            return f"{value:.1f}"

        if abs(value) >= 10:

            return f"{value:.2f}"

        return f"{value:.2f}"

    # ========================================================
    # NUTRIENT FORMAT
    # ========================================================

    def _format_nutrient(
        self,
        nutrients,
        key,
        label,
        default_unit,
    ):

        data = nutrients.get(
            key
        )

        if not data:
            return None

        if isinstance(
            data,
            dict,
        ):

            value = data.get(
                "value"
            )

            unit = data.get(
                "unit",
                default_unit,
            )

        else:

            value = data

            unit = default_unit

        if value is None:

            return None

        if not unit:

            unit = default_unit

        return (
            f"{label}: "
            f"{self._format_number(value)} "
            f"{unit}"
        )

    # ========================================================
    # RESPONSE
    # ========================================================

    def _build_response(
        self,
        food_name,
        portion,
        nutrients,
        selected_food,
    ):

        description = self._get_value(
            selected_food,
            "description",
            food_name,
        )

        grams = portion.get(
            "grams"
        )

        lines = []

        lines.append(
            f"### Nutrition for {description}"
        )

        lines.append("")

        lines.append(
            f"**Reference amount: "
            f"{self._format_number(grams)} g**"
        )

        lines.append("")

        nutrient_order = [
            (
                "energy",
                "Energy",
                "kcal",
            ),
            (
                "protein",
                "Protein",
                "g",
            ),
            (
                "carbohydrates",
                "Carbohydrates",
                "g",
            ),
            (
                "fat",
                "Fat",
                "g",
            ),
            (
                "fiber",
                "Fiber",
                "g",
            ),
            (
                "sugars",
                "Sugars",
                "g",
            ),
            (
                "sodium",
                "Sodium",
                "mg",
            ),
            (
                "calcium",
                "Calcium",
                "mg",
            ),
            (
                "iron",
                "Iron",
                "mg",
            ),
            (
                "potassium",
                "Potassium",
                "mg",
            ),
            (
                "magnesium",
                "Magnesium",
                "mg",
            ),
            (
                "phosphorus",
                "Phosphorus",
                "mg",
            ),
            (
                "zinc",
                "Zinc",
                "mg",
            ),
            (
                "vitamin_a",
                "Vitamin A",
                "µg",
            ),
            (
                "vitamin_c",
                "Vitamin C",
                "mg",
            ),
            (
                "vitamin_d",
                "Vitamin D",
                "µg",
            ),
            (
                "vitamin_e",
                "Vitamin E",
                "mg",
            ),
            (
                "vitamin_k",
                "Vitamin K",
                "µg",
            ),
        ]

        for (
            key,
            label,
            default_unit,
        ) in nutrient_order:

            formatted = (
                self._format_nutrient(
                    nutrients,
                    key,
                    label,
                    default_unit,
                )
            )

            if formatted:

                lines.append(
                    formatted
                )

        lines.append("")

        lines.append(
            "Source: **USDA FoodData Central**"
        )

        return "\n".join(
            lines
        )

    # ========================================================
    # MAIN MESSAGE PROCESSOR
    # ========================================================

    def process_message(
        self,
        user_input,
    ):

        if (
            not user_input
            or not str(user_input).strip()
        ):

            return (
                "Please enter a food or "
                "nutrition question."
            )

        # ----------------------------------------------------
        # NLP
        # ----------------------------------------------------

        parsed = self._process_nlp(
            user_input
        )

        food_name = self._get_value(
            parsed,
            "food",
            self._get_value(
                parsed,
                "food_name",
                "",
            ),
        )

        quantity = self._get_value(
            parsed,
            "quantity",
            None,
        )

        unit = self._get_value(
            parsed,
            "unit",
            None,
        )

        # ----------------------------------------------------
        # Clean + spell correction
        # ----------------------------------------------------

        food_name = (
            self._clean_food_name(
                food_name
            )
        )

        if not food_name:

            return (
                "I couldn't identify the food. "
                "Try **2 bananas** or "
                "**150 grams of chicken**."
            )

        # ----------------------------------------------------
        # USDA SEARCH
        # ----------------------------------------------------

        try:

            candidates = (
                self.database.search_food(
                    food_name
                )
            )

        except Exception as error:

            return (
                "I couldn't connect to USDA "
                "FoodData Central.\n\n"
                f"Error: `{error}`"
            )

        if not candidates:

            return (
                f"I couldn't find **{food_name}** "
                "in USDA FoodData Central."
            )

        # ----------------------------------------------------
        # SELECT FOOD
        # ----------------------------------------------------

        selected_food = (
            self._select_food(
                food_name,
                candidates,
            )
        )

        if not selected_food:

            return (
                f"I couldn't find a suitable "
                f"USDA record for **{food_name}**."
            )

        fdc_id = self._get_value(
            selected_food,
            "fdcId",
            self._get_value(
                selected_food,
                "fdc_id",
                None,
            ),
        )

        if fdc_id is None:

            return (
                "The USDA result did not "
                "contain a valid FDC ID."
            )

        # ----------------------------------------------------
        # DETAILS
        # ----------------------------------------------------

        try:

            food_details = (
                self.database.get_food_details(
                    fdc_id
                )
            )

        except Exception as error:

            return (
                "USDA found the food, but I "
                "couldn't retrieve its details.\n\n"
                f"Error: `{error}`"
            )

        if not food_details:

            description = (
                self._get_value(
                    selected_food,
                    "description",
                    food_name,
                )
            )

            return (
                "USDA did not provide usable "
                f"nutrition data for {description}."
            )

        # ----------------------------------------------------
        # NUTRIENTS
        # ----------------------------------------------------

        try:

            nutrients = (
                self.database.extract_nutrients(
                    food_details
                )
            )

        except Exception as error:

            return (
                "I found the food, but couldn't "
                "extract its nutrition information.\n\n"
                f"Error: `{error}`"
            )

        if not nutrients:

            description = (
                self._get_value(
                    selected_food,
                    "description",
                    food_name,
                )
            )

            return (
                "USDA did not provide usable "
                f"nutrition data for {description}."
            )

        # ----------------------------------------------------
        # PORTION
        # ----------------------------------------------------

        try:

            portion = (
                self._resolve_portion(
                    food_name=food_name,
                    quantity=quantity,
                    unit=unit,
                    food_details=food_details,
                )
            )

        except Exception as error:

            return (
                "I couldn't determine the requested "
                "portion.\n\n"
                f"Error: `{error}`"
            )

        if not portion:

            return (
                "I couldn't determine the requested "
                "portion."
            )

        if (
            portion.get("status")
            == "needs_weight"
        ):

            return portion.get(
                "message",
                "Please provide an approximate "
                "weight in grams.",
            )

        grams = portion.get(
            "grams"
        )

        if grams is None:

            return (
                "I couldn't determine the food "
                "weight. Please provide the "
                "amount in grams."
            )

        # ----------------------------------------------------
        # CALCULATE
        # ----------------------------------------------------

        calculated = (
            self._calculate_nutrition(
                nutrients,
                grams,
            )
        )

        if not calculated:

            description = (
                self._get_value(
                    selected_food,
                    "description",
                    food_name,
                )
            )

            return (
                "USDA did not provide usable "
                f"nutrition data for {description}."
            )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return self._build_response(
            food_name=food_name,
            portion=portion,
            nutrients=calculated,
            selected_food=selected_food,
        )


# ============================================================
# NO TEST CODE
# ============================================================