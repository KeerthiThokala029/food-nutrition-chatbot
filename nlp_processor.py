"""
NLP Processor

Extracts structured information from natural-language food input.

Examples:

    chicken
    I ate chicken
    I ate 2 plates of chicken
    I ate 150 grams of chicken
    2 bananas
    I had a banana
    I ate three pieces of fried chicken
    how much protein is in chicken?
    how many calories are in rice?

The processor does NOT contain a fixed food list.
Food identification is handled later by the USDA food matcher.
"""

import re
from typing import Optional, Dict, Any


class NLPProcessor:
    """Processes natural-language food queries."""

    # ---------------------------------------------------------
    # Number words
    # ---------------------------------------------------------

    NUMBER_WORDS = {
        "zero": 0,
        "a": 1,
        "an": 1,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "half": 0.5,
        "quarter": 0.25,
    }

    # ---------------------------------------------------------
    # Food measurement units
    # ---------------------------------------------------------

    UNITS = {
        "gram": "grams",
        "grams": "grams",
        "g": "grams",

        "kilogram": "kilograms",
        "kilograms": "kilograms",
        "kg": "kilograms",

        "milligram": "milligrams",
        "milligrams": "milligrams",
        "mg": "milligrams",

        "ounce": "ounces",
        "ounces": "ounces",
        "oz": "ounces",

        "pound": "pounds",
        "pounds": "pounds",
        "lb": "pounds",
        "lbs": "pounds",

        "cup": "cups",
        "cups": "cups",

        "tablespoon": "tablespoons",
        "tablespoons": "tablespoons",
        "tbsp": "tablespoons",

        "teaspoon": "teaspoons",
        "teaspoons": "teaspoons",
        "tsp": "teaspoons",

        "plate": "plates",
        "plates": "plates",

        "bowl": "bowls",
        "bowls": "bowls",

        "piece": "pieces",
        "pieces": "pieces",

        "slice": "slices",
        "slices": "slices",

        "serving": "servings",
        "servings": "servings",

        "portion": "portions",
        "portions": "portions",

        "glass": "glasses",
        "glasses": "glasses",

        "bottle": "bottles",
        "bottles": "bottles",

        "packet": "packets",
        "packets": "packets",

        "spoon": "spoons",
        "spoons": "spoons",
    }

    # ---------------------------------------------------------
    # Words that should not become part of the food name
    # ---------------------------------------------------------

    CONTEXT_WORDS = {
        "i",
        "me",
        "my",
        "we",
        "our",

        "ate",
        "eat",
        "eaten",
        "had",
        "have",
        "having",

        "consumed",
        "consume",
        "consuming",

        "want",
        "wanted",

        "give",
        "show",
        "tell",
        "calculate",
        "find",
        "get",
        "know",

        "please",

        "some",
        "of",
        "the",
        "is",
        "are",
        "was",
        "were",

        "in",
        "for",
        "with",
        "about",
        "there",
        "any",

        # Question words
        "what",
        "what's",
        "whats",
        "how",
        "much",
        "many",
        "which",

        # Nutrition words
        "nutrition",
        "nutritional",
        "information",
        "value",

        "calorie",
        "calories",
        "kcal",

        "protein",

        "carbohydrate",
        "carbohydrates",
        "carb",
        "carbs",

        "fat",
        "fats",

        "lipid",
        "lipids",

        "fiber",
        "fibre",

        "sodium",
        "magnesium",
        "calcium",
        "iron",
        "potassium",
        "zinc",
        "phosphorus",

        "vitamin",
        "vitamins",
    }

    # ---------------------------------------------------------
    # Nutrient keywords
    # ---------------------------------------------------------

    NUTRIENT_KEYWORDS = {
        "energy": "energy",

        "calorie": "energy",
        "calories": "energy",
        "kcal": "energy",

        "protein": "protein",

        "carbohydrate": "carbohydrates",
        "carbohydrates": "carbohydrates",
        "carb": "carbohydrates",
        "carbs": "carbohydrates",

        "fat": "fat",
        "fats": "fat",

        "lipid": "fat",
        "lipids": "fat",

        "fiber": "fiber",
        "fibre": "fiber",

        "sodium": "sodium",
        "salt": "sodium",

        "magnesium": "magnesium",
        "calcium": "calcium",
        "iron": "iron",
        "potassium": "potassium",
        "zinc": "zinc",
        "phosphorus": "phosphorus",

        "vitamin": "vitamins",
        "vitamins": "vitamins",
    }

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Main processing method
    # ---------------------------------------------------------

    def process(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Process a user message.

        Returns:

        {
            "original_text": "...",
            "food": "...",
            "quantity": ...,
            "unit": "...",
            "intent": "...",
            "nutrient": "...",
            "normalized_text": "..."
        }
        """

        if not text or not text.strip():

            return self._empty_result()

        original_text = text.strip()

        normalized_text = self._normalize_text(
            original_text
        )

        intent = self._detect_intent(
            normalized_text
        )

        nutrient = self._detect_nutrient(
            normalized_text
        )

        (
            quantity,
            unit,
            remaining_text
        ) = self._extract_quantity_and_unit(
            normalized_text
        )

        food = self._extract_food(
            remaining_text
        )

        return {
            "original_text": original_text,
            "food": food,
            "quantity": quantity,
            "unit": unit,
            "intent": intent,
            "nutrient": nutrient,
            "normalized_text": normalized_text,
        }

    # ---------------------------------------------------------
    # Normalize text
    # ---------------------------------------------------------

    def _normalize_text(
        self,
        text: str
    ) -> str:
        """
        Convert text into a clean normalized form.
        """

        text = text.lower().strip()

        # Replace punctuation with spaces.
        text = re.sub(
            r"[^\w\s.]",
            " ",
            text
        )

        # Remove extra whitespace.
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # ---------------------------------------------------------
    # Detect intent
    # ---------------------------------------------------------

    def _detect_intent(
        self,
        text: str
    ) -> str:
        """
        Detect the user's broad intention.
        """

        words = set(
            text.split()
        )

        comparison_words = {
            "compare",
            "comparison",
            "versus",
            "vs",
            "difference",
            "better",
        }

        if words.intersection(
            comparison_words
        ):
            return "comparison"

        return "nutrition_info"

    # ---------------------------------------------------------
    # Detect nutrient
    # ---------------------------------------------------------

    def _detect_nutrient(
        self,
        text: str
    ) -> Optional[str]:
        """
        Detect whether the user specifically asks
        about a nutrient.
        """

        words = set(
            text.split()
        )

        for (
            keyword,
            nutrient
        ) in self.NUTRIENT_KEYWORDS.items():

            if keyword in words:

                return nutrient

        return None

    # ---------------------------------------------------------
    # Extract quantity and unit
    # ---------------------------------------------------------

    def _extract_quantity_and_unit(
        self,
        text: str
    ):
        """
        Extract quantity and measurement unit.

        Examples:

            2 plates of chicken

            -> 2
            -> plates
            -> chicken


            150 grams of chicken

            -> 150
            -> grams
            -> chicken


            three bananas

            -> 3
            -> count
            -> bananas


            a banana

            -> 1
            -> count
            -> banana
        """

        words = text.split()

        if not words:

            return (
                None,
                None,
                text
            )

        quantity = None
        unit = None

        quantity_index = None
        unit_index = None

        # -----------------------------------------------------
        # Search for numeric quantity
        # -----------------------------------------------------

        for index, word in enumerate(words):

            if re.fullmatch(
                r"\d+(?:\.\d+)?",
                word
            ):

                quantity = float(word)

                if quantity.is_integer():

                    quantity = int(
                        quantity
                    )

                quantity_index = index

                break

        # -----------------------------------------------------
        # Search for number words
        # -----------------------------------------------------

        if quantity is None:

            for index, word in enumerate(words):

                if word in self.NUMBER_WORDS:

                    quantity = (
                        self.NUMBER_WORDS[word]
                    )

                    quantity_index = index

                    break

        # -----------------------------------------------------
        # Search for measurement unit
        # -----------------------------------------------------

        if quantity_index is not None:

            for index in range(
                quantity_index + 1,
                min(
                    quantity_index + 3,
                    len(words)
                )
            ):

                candidate = words[index]

                if candidate in self.UNITS:

                    unit = self.UNITS[
                        candidate
                    ]

                    unit_index = index

                    break

        # -----------------------------------------------------
        # Remove quantity and unit
        # -----------------------------------------------------

        remaining_words = []

        for index, word in enumerate(words):

            if index == quantity_index:

                continue

            if index == unit_index:

                continue

            remaining_words.append(
                word
            )

        remaining_text = " ".join(
            remaining_words
        )

        # -----------------------------------------------------
        # No explicit unit = count
        # -----------------------------------------------------

        if (
            quantity is not None
            and unit is None
        ):

            unit = "count"

        return (
            quantity,
            unit,
            remaining_text
        )

    # ---------------------------------------------------------
    # Extract food name
    # ---------------------------------------------------------

    def _extract_food(
        self,
        text: str
    ) -> str:
        """
        Extract the food phrase.

        This method does NOT use a fixed food list.

        The resulting food phrase will later be sent
        to the USDA food matcher.
        """

        words = text.split()

        cleaned_words = []

        for word in words:

            if word in self.CONTEXT_WORDS:

                continue

            cleaned_words.append(
                word
            )

        food = " ".join(
            cleaned_words
        ).strip()

        return food

    # ---------------------------------------------------------
    # Empty result
    # ---------------------------------------------------------

    def _empty_result(
        self
    ) -> Dict[str, Any]:

        return {
            "original_text": "",
            "food": "",
            "quantity": None,
            "unit": None,
            "intent": "unknown",
            "nutrient": None,
            "normalized_text": "",
        }


# =============================================================
# Standalone testing
# =============================================================

if __name__ == "__main__":

    processor = NLPProcessor()

    test_inputs = [
        "chicken",
        "I ate chicken",
        "I ate 2 plates of chicken",
        "I ate 150 grams of chicken",
        "2 bananas",
        "I had a banana",
        "I ate three pieces of fried chicken",
        "how much protein is in chicken?",
        "how many calories are in rice?",
        "what is the nutrition of broccoli?",
        "tell me the fiber in apple",
        "brocolli",
    ]

    for user_input in test_inputs:

        result = processor.process(
            user_input
        )

        print()
        print("=" * 60)

        print(
            "INPUT:",
            user_input
        )

        print(
            "Food:",
            result["food"]
        )

        print(
            "Quantity:",
            result["quantity"]
        )

        print(
            "Unit:",
            result["unit"]
        )

        print(
            "Intent:",
            result["intent"]
        )

        print(
            "Nutrient:",
            result["nutrient"]
        )