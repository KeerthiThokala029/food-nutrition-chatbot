import re


class PortionResolver:
    """
    Converts user quantities and units into grams.

    Priority:
    1. Direct weight units
    2. Standard count weights for common countable foods
    3. USDA food portions when appropriate
    4. Ambiguous household units are not guessed
    """

    # ---------------------------------------------------------
    # Standard weights for one whole/countable food
    # ---------------------------------------------------------

    COUNT_WEIGHTS = {
        "banana": 118.0,
        "apple": 182.0,
        "orange": 131.0,
        "pear": 178.0,
        "peach": 150.0,
        "plum": 66.0,
        "mango": 200.0,
        "kiwi": 69.0,
        "lemon": 58.0,
        "lime": 67.0,

        "egg": 50.0,

        "tomato": 123.0,
        "potato": 173.0,
        "onion": 110.0,
        "carrot": 61.0,
        "cucumber": 301.0,

        "avocado": 150.0,
        "bell pepper": 119.0,
        "pepper": 119.0,

        "broccoli": 148.0,
        "cauliflower": 575.0,
        "corn": 103.0,
        "sweet potato": 130.0,
    }

    # ---------------------------------------------------------
    # Direct measurable units
    # ---------------------------------------------------------

    UNIT_TO_GRAMS = {
        "g": 1.0,
        "gram": 1.0,
        "grams": 1.0,

        "kg": 1000.0,
        "kilogram": 1000.0,
        "kilograms": 1000.0,

        "mg": 0.001,
        "milligram": 0.001,
        "milligrams": 0.001,

        "oz": 28.3495,
        "ounce": 28.3495,
        "ounces": 28.3495,

        "lb": 453.592,
        "pound": 453.592,
        "pounds": 453.592,

        "tsp": 5.0,
        "teaspoon": 5.0,
        "teaspoons": 5.0,

        "tbsp": 15.0,
        "tablespoon": 15.0,
        "tablespoons": 15.0,

        "cup": 240.0,
        "cups": 240.0,

        "ml": 1.0,
        "milliliter": 1.0,
        "milliliters": 1.0,

        "l": 1000.0,
        "liter": 1000.0,
        "liters": 1000.0,
    }

    # ---------------------------------------------------------
    # Units that cannot safely be converted without food-
    # specific information
    # ---------------------------------------------------------

    AMBIGUOUS_UNITS = {
        "plate",
        "plates",
        "bowl",
        "bowls",
        "serving",
        "servings",
        "portion",
        "portions",
        "glass",
        "glasses",
        "bottle",
        "bottles",
        "packet",
        "packets",
        "piece",
        "pieces",
        "slice",
        "slices",
        "spoon",
        "spoons",
    }

    def __init__(self):
        pass

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def _normalize_food(self, food):
        if not food:
            return ""

        text = str(food).lower().strip()

        text = re.sub(
            r"\b(raw|fresh|ripe|unripe|whole|chopped|sliced|cut)\b",
            "",
            text,
        )

        text = re.sub(r"\s+", " ", text).strip()

        # Simple plural handling.
        if text.endswith("ies"):
            text = text[:-3] + "y"

        elif text.endswith("oes"):
            text = text[:-2]

        elif text.endswith("s") and not text.endswith("ss"):
            text = text[:-1]

        return text

    # =========================================================
    # STANDARD COUNT WEIGHT
    # =========================================================

    def _find_count_weight(self, food):
        normalized = self._normalize_food(food)

        # Exact match.
        if normalized in self.COUNT_WEIGHTS:
            return self.COUNT_WEIGHTS[normalized]

        # Handle common multi-word foods.
        for food_name, weight in self.COUNT_WEIGHTS.items():
            if normalized == food_name:
                return weight

        return None

    # =========================================================
    # USDA PORTION
    # =========================================================

    def _find_usda_count_portion(self, food_details):
        """
        Try to find an individual USDA portion.

        This is a fallback only. Standard count weights are
        preferred for common whole foods because they give
        predictable behavior for inputs such as:

            1 apple
            2 bananas
            1 orange
        """

        if not food_details:
            return None

        portions = food_details.get("foodPortions")

        if not isinstance(portions, list):
            return None

        candidates = []

        for portion in portions:

            if not isinstance(portion, dict):
                continue

            gram_weight = portion.get("gramWeight")

            if gram_weight is None:
                continue

            try:
                gram_weight = float(gram_weight)
            except (TypeError, ValueError):
                continue

            if gram_weight <= 0:
                continue

            modifier = str(
                portion.get("modifier")
                or portion.get("portionDescription")
                or portion.get("measureUnit")
                or ""
            ).lower()

            score = 0

            preferred_words = [
                "small",
                "medium",
                "large",
                "piece",
                "whole",
                "fruit",
                "item",
            ]

            for word in preferred_words:
                if word in modifier:
                    score += 1

            candidates.append(
                (
                    score,
                    gram_weight,
                    modifier,
                )
            )

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        best_score, best_weight, _ = candidates[0]

        if best_score > 0 and 20 <= best_weight <= 1000:
            return best_weight

        return None

    # =========================================================
    # MAIN RESOLVER
    # =========================================================

    def resolve(
        self,
        food,
        quantity=None,
        unit=None,
        food_details=None,
    ):
        result = {
            "grams": None,
            "quantity": quantity,
            "unit": unit,
            "status": "unknown",
            "message": None,
            "source": None,
        }

        # -----------------------------------------------------
        # No quantity
        # -----------------------------------------------------

        if quantity is None:

            result["grams"] = 100.0
            result["status"] = "default"
            result["source"] = "100 g reference amount"

            result["message"] = (
                "No quantity was specified, so nutrition is shown "
                "for a 100 g reference amount."
            )

            return result

        # -----------------------------------------------------
        # Validate quantity
        # -----------------------------------------------------

        try:
            quantity = float(quantity)

        except (TypeError, ValueError):

            result["status"] = "unknown"
            result["message"] = (
                "I could not understand the quantity."
            )

            return result

        if quantity <= 0:

            result["status"] = "unknown"
            result["message"] = (
                "Quantity must be greater than zero."
            )

            return result

        unit_text = str(unit or "").lower().strip()

        # =====================================================
        # 1. DIRECT WEIGHT
        # =====================================================

        if unit_text in self.UNIT_TO_GRAMS:

            grams = (
                quantity
                * self.UNIT_TO_GRAMS[unit_text]
            )

            result["grams"] = grams
            result["status"] = "resolved"
            result["source"] = (
                f"{quantity:g} {unit_text}"
            )

            return result

        # =====================================================
        # 2. COUNT
        # =====================================================

        if unit_text in {
            "count",
            "item",
            "items",
            "",
        }:

            # IMPORTANT:
            # Standard count weights come FIRST.
            #
            # This prevents:
            # 2 bananas -> 450 g
            # 1 apple -> 242 g
            # 1 orange -> 180 g
            #
            # from being selected from arbitrary USDA portions.

            count_weight = self._find_count_weight(food)

            if count_weight is not None:

                result["grams"] = (
                    quantity * count_weight
                )

                result["status"] = "resolved"

                result["source"] = (
                    f"standard count weight: "
                    f"{count_weight:g} g per item"
                )

                return result

            # -------------------------------------------------
            # USDA fallback
            # -------------------------------------------------

            usda_weight = self._find_usda_count_portion(
                food_details
            )

            if usda_weight is not None:

                result["grams"] = (
                    quantity * usda_weight
                )

                result["status"] = "resolved"

                result["source"] = (
                    f"USDA portion: "
                    f"{usda_weight:g} g per item"
                )

                return result

            # -------------------------------------------------
            # Cannot determine count weight
            # -------------------------------------------------

            result["status"] = "needs_weight"

            result["message"] = (
                f"I can identify {food}, but I need an "
                f"approximate weight in grams to calculate "
                f"the quantity accurately."
            )

            return result

        # =====================================================
        # 3. AMBIGUOUS HOUSEHOLD UNIT
        # =====================================================

        if unit_text in self.AMBIGUOUS_UNITS:

            result["status"] = "needs_weight"

            result["message"] = (
                f"'{unit_text}' does not have a universal "
                f"weight for {food}. Please provide an "
                f"approximate weight in grams or use a "
                f"measurable unit."
            )

            return result

        # =====================================================
        # 4. UNKNOWN UNIT
        # =====================================================

        result["status"] = "needs_weight"

        result["message"] = (
            f"I do not have a reliable conversion for "
            f"'{unit_text}'. Please provide the amount "
            f"in grams."
        )

        return result

    # =========================================================
    # COMPATIBILITY METHOD
    # =========================================================

    def resolve_portion(
        self,
        food,
        quantity=None,
        unit=None,
        food_details=None,
    ):
        return self.resolve(
            food=food,
            quantity=quantity,
            unit=unit,
            food_details=food_details,
        )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    resolver = PortionResolver()

    tests = [
        ("banana", 2, "count"),
        ("apple", 1, "count"),
        ("orange", 1, "count"),
        ("chicken", 150, "grams"),
        ("chicken", None, None),
        ("rice", 2, "plates"),
    ]

    print("=" * 60)
    print("PORTION RESOLVER TEST")
    print("=" * 60)

    for food, quantity, unit in tests:

        result = resolver.resolve(
            food=food,
            quantity=quantity,
            unit=unit,
        )

        print()
        print(f"Food: {food}")
        print(f"Quantity: {quantity}")
        print(f"Unit: {unit}")
        print(f"Result: {result}")