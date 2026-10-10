class ResponseGenerator:

    def __init__(self):
        pass

    def generate(self, result):

        if result is None:
            return "Sorry, I could not process that request."

        if result.get("error"):
            return result.get(
                "message",
                "Sorry, I could not find nutrition information."
            )

        # ---------------------------------------------------------
        # FOOD NAME
        # ---------------------------------------------------------

        food_name = (
            result.get("food_name")
            or result.get("food")
            or result.get("matched_food")
            or "Unknown food"
        )

        # If the entire USDA dictionary was accidentally passed
        # as food_name, extract the description instead.
        if isinstance(food_name, dict):

            food_name = (
                food_name.get("DESCRIPTION")
                or food_name.get("description")
                or food_name.get("foodName")
                or food_name.get("foodDescription")
                or "Unknown food"
            )

        food_name = str(food_name)

        # ---------------------------------------------------------
        # AMOUNT
        # ---------------------------------------------------------

        amount = result.get("amount")

        if amount is None:
            amount = result.get("quantity")

        unit = result.get("unit") or ""

        calculated_grams = (
            result.get("calculated_grams")
            or result.get("grams")
            or result.get("amount_grams")
        )

        # ---------------------------------------------------------
        # NUTRITION
        # ---------------------------------------------------------

        nutrition = (
            result.get("nutrition")
            or result.get("nutrients")
            or {}
        )

        requested_nutrient = (
            result.get("requested_nutrient")
            or result.get("nutrient")
        )

        lines = []

        lines.append(
            f"### 🥗 Nutrition for {food_name.upper()}"
        )

        # ---------------------------------------------------------
        # SPELLING CORRECTION
        # ---------------------------------------------------------

        if result.get("spelling_corrected"):

            original = result.get("original_query")
            corrected = result.get("corrected_query")

            if original and corrected:
                lines.append(
                    f"💡 Interpreted **{original}** as "
                    f"**{corrected}**."
                )

        # ---------------------------------------------------------
        # AMOUNT
        # ---------------------------------------------------------

        if amount is not None:

            if unit:
                lines.append(
                    f"**Amount:** "
                    f"{self._format_number(amount)} {unit}"
                )
            else:
                lines.append(
                    f"**Amount:** "
                    f"{self._format_number(amount)}"
                )

        if calculated_grams is not None:

            lines.append(
                f"**Calculated amount:** "
                f"{self._format_number(calculated_grams)} g"
            )

        # ---------------------------------------------------------
        # REQUESTED NUTRIENT
        # ---------------------------------------------------------

        if requested_nutrient and nutrition:

            requested_value = self._find_nutrient(
                nutrition,
                requested_nutrient
            )

            if requested_value is not None:

                lines.append("")
                lines.append("### 🎯 Requested Nutrient")

                lines.append(
                    f"**{self._display_name(requested_nutrient)}:** "
                    f"{self._format_value(requested_value)}"
                )

        # ---------------------------------------------------------
        # FULL NUTRITION
        # ---------------------------------------------------------

        if nutrition:

            lines.append("")
            lines.append("### 📊 Nutrition Information")

            ordered = [
                "Energy",
                "Protein",
                "Carbohydrates",
                "Fat",
                "Fiber",
                "Sugars",
                "Sodium",
                "Calcium",
                "Iron",
                "Magnesium",
                "Phosphorus",
                "Potassium",
                "Zinc",
                "Vitamin A",
                "Vitamin C",
                "Vitamin D",
                "Vitamin E",
                "Vitamin K",
                "Vitamin B1",
                "Vitamin B2",
                "Vitamin B3",
                "Vitamin B6",
                "Vitamin B12",
                "Folate",
            ]

            displayed = set()

            for nutrient in ordered:

                value = self._find_nutrient(
                    nutrition,
                    nutrient
                )

                if value is not None:

                    lines.append(
                        f"- **{nutrient}:** "
                        f"{self._format_value(value)}"
                    )

                    displayed.add(
                        self._normalize(nutrient)
                    )

            # Extra nutrients
            for key, value in nutrition.items():

                if key == "_grams":
                    continue

                if self._normalize(key) in displayed:
                    continue

                if value is None:
                    continue

                lines.append(
                    f"- **{key}:** "
                    f"{self._format_value(value)}"
                )

        else:

            lines.append("")
            lines.append(
                "⚠️ Nutrition values were unavailable."
            )

        lines.append("")
        lines.append(
            "**Source:** USDA FoodData Central"
        )

        return "\n".join(lines)

    # =============================================================
    # HELPERS
    # =============================================================

    def _normalize(self, value):

        return (
            str(value)
            .lower()
            .strip()
            .replace("_", " ")
            .replace("-", " ")
            .replace(",", "")
        )

    def _find_nutrient(self, nutrition, requested):

        if not isinstance(nutrition, dict):
            return None

        target = self._normalize(
            requested
        )

        aliases = {
            "energy": [
                "energy",
                "calories"
            ],
            "protein": [
                "protein"
            ],
            "carbohydrates": [
                "carbohydrates",
                "carbohydrate",
                "carbs"
            ],
            "fat": [
                "fat",
                "total lipid fat"
            ],
            "fiber": [
                "fiber",
                "dietary fiber"
            ],
            "sugars": [
                "sugars",
                "sugar"
            ],
            "vitamin b1": [
                "vitamin b1",
                "thiamin"
            ],
            "vitamin b2": [
                "vitamin b2",
                "riboflavin"
            ],
            "vitamin b3": [
                "vitamin b3",
                "niacin"
            ],
            "vitamin b6": [
                "vitamin b6",
                "vitamin b 6"
            ],
            "vitamin b12": [
                "vitamin b12",
                "vitamin b 12"
            ],
        }

        possible = aliases.get(
            target,
            [requested]
        )

        possible = [
            self._normalize(x)
            for x in possible
        ]

        for key, value in nutrition.items():

            normalized_key = self._normalize(
                key
            )

            if normalized_key in possible:
                return value

        return None

    def _display_name(self, value):

        mapping = {
            "protein": "Protein",
            "energy": "Energy",
            "calories": "Calories",
            "carbohydrates": "Carbohydrates",
            "carbs": "Carbohydrates",
            "fat": "Fat",
            "fiber": "Fiber",
            "sugars": "Sugars",
            "sodium": "Sodium",
            "calcium": "Calcium",
            "iron": "Iron",
            "magnesium": "Magnesium",
            "phosphorus": "Phosphorus",
            "potassium": "Potassium",
            "zinc": "Zinc",
        }

        return mapping.get(
            self._normalize(value),
            str(value).title()
        )

    def _format_value(self, value):

        if isinstance(value, dict):

            number = value.get("value")

            if number is None:
                number = value.get("amount")

            unit = value.get(
                "unit",
                ""
            )

            if number is not None:

                formatted = self._format_number(
                    number
                )

                if unit:
                    return f"{formatted} {unit}"

                return formatted

        if isinstance(value, (int, float)):

            return self._format_number(
                value
            )

        return str(value)

    def _format_number(self, value):

        try:

            number = float(value)

            if number.is_integer():
                return str(int(number))

            return (
                f"{number:.2f}"
                .rstrip("0")
                .rstrip(".")
            )

        except (TypeError, ValueError):

            return str(value)


if __name__ == "__main__":

    generator = ResponseGenerator()

    sample = {
        "food_name": "Chicken",
        "calculated_grams": 100,
        "nutrition": {
            "Energy": {
                "value": 215,
                "unit": "KCAL"
            },
            "Protein": {
                "value": 19.4,
                "unit": "G"
            }
        }
    }

    print(
        generator.generate(sample)
    )