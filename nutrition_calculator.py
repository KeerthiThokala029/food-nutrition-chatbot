class NutritionCalculator:
    """
    Calculates nutrition values from USDA FoodData Central records.

    Handles both:
    - Normalized USDA nutrient dictionaries
    - Raw USDA API records containing FOODNUTRIENTS
    """

    NUTRIENT_MAP = {
        "energy": ["energy", "energy kcal", "calories", "kcal"],
        "protein": ["protein"],
        "carbohydrates": [
            "carbohydrates",
            "carbohydrate",
            "carbohydrate by difference",
            "carbohydrate, by difference",
            "carbs",
        ],
        "fat": [
            "fat",
            "total lipid",
            "total lipid fat",
            "total lipid (fat)",
        ],
        "fiber": [
            "fiber",
            "dietary fiber",
            "fiber total dietary",
            "fiber, total dietary",
        ],
        "sugars": [
            "sugars",
            "total sugars",
            "sugar",
        ],
        "sodium": [
            "sodium",
            "sodium na",
            "sodium, na",
        ],
        "calcium": [
            "calcium",
            "calcium ca",
            "calcium, ca",
        ],
        "iron": [
            "iron",
            "iron fe",
            "iron, fe",
        ],
        "magnesium": [
            "magnesium",
            "magnesium mg",
            "magnesium, mg",
        ],
        "phosphorus": [
            "phosphorus",
            "phosphorus p",
            "phosphorus, p",
        ],
        "potassium": [
            "potassium",
            "potassium k",
            "potassium, k",
        ],
        "zinc": [
            "zinc",
            "zinc zn",
            "zinc, zn",
        ],
        "vitamin a": [
            "vitamin a",
            "vitamin a rae",
        ],
        "vitamin c": [
            "vitamin c",
            "vitamin c total ascorbic acid",
            "vitamin c, total ascorbic acid",
        ],
        "vitamin d": [
            "vitamin d",
            "vitamin d d2 d3",
            "vitamin d (d2 + d3)",
        ],
        "vitamin e": [
            "vitamin e",
            "vitamin e alpha tocopherol",
            "vitamin e (alpha-tocopherol)",
        ],
        "vitamin k": [
            "vitamin k",
            "vitamin k phylloquinone",
            "vitamin k (phylloquinone)",
        ],
        "vitamin b1": [
            "vitamin b1",
            "thiamin",
            "thiamine",
        ],
        "vitamin b2": [
            "vitamin b2",
            "riboflavin",
        ],
        "vitamin b3": [
            "vitamin b3",
            "niacin",
        ],
        "vitamin b6": [
            "vitamin b6",
            "vitamin b 6",
            "vitamin b-6",
        ],
        "vitamin b12": [
            "vitamin b12",
            "vitamin b 12",
            "vitamin b-12",
        ],
        "folate": [
            "folate",
            "folate total",
            "folate, total",
            "folate food",
            "folate, food",
            "folate dfe",
            "folate, dfe",
            "folic acid",
        ],
    }

    DISPLAY_NAMES = {
        "energy": "Energy",
        "protein": "Protein",
        "carbohydrates": "Carbohydrates",
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
        "vitamin a": "Vitamin A",
        "vitamin c": "Vitamin C",
        "vitamin d": "Vitamin D",
        "vitamin e": "Vitamin E",
        "vitamin k": "Vitamin K",
        "vitamin b1": "Vitamin B1",
        "vitamin b2": "Vitamin B2",
        "vitamin b3": "Vitamin B3",
        "vitamin b6": "Vitamin B6",
        "vitamin b12": "Vitamin B12",
        "folate": "Folate",
    }

    DEFAULT_NUTRIENTS = [
        "energy",
        "protein",
        "carbohydrates",
        "fat",
        "fiber",
        "sugars",
        "sodium",
        "calcium",
        "iron",
        "magnesium",
        "phosphorus",
        "potassium",
        "zinc",
        "vitamin a",
        "vitamin c",
        "vitamin d",
        "vitamin e",
        "vitamin k",
        "vitamin b1",
        "vitamin b2",
        "vitamin b3",
        "vitamin b6",
        "vitamin b12",
        "folate",
    ]

    def _normalize_name(self, value):
        if value is None:
            return ""

        text = str(value).lower().strip()

        for char in [
            "_",
            "-",
            ",",
            "(",
            ")",
            "+",
        ]:
            text = text.replace(char, " ")

        return " ".join(text.split())

    def _to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _get_raw_nutrients(self, food_details):
        """
        Extract raw USDA nutrient rows.

        Supports the structure visible in your current output:
        FOODNUTRIENTS -> NUTRIENTNAME / UNITNAME / VALUE
        """

        if not isinstance(food_details, dict):
            return []

        nutrients = (
            food_details.get("FOODNUTRIENTS")
            or food_details.get("foodNutrients")
            or food_details.get("nutrients")
            or []
        )

        if not isinstance(nutrients, list):
            return []

        return nutrients

    def _find_raw_nutrient(self, raw_nutrients, nutrient_name):
        """
        Find the best USDA nutrient row for a requested nutrient.
        """

        aliases = self.NUTRIENT_MAP.get(
            nutrient_name,
            [nutrient_name]
        )

        normalized_aliases = {
            self._normalize_name(alias)
            for alias in aliases
        }

        # Exact normalized match first
        for nutrient in raw_nutrients:
            if not isinstance(nutrient, dict):
                continue

            name = (
                nutrient.get("NUTRIENTNAME")
                or nutrient.get("nutrientName")
                or nutrient.get("name")
                or nutrient.get("description")
                or ""
            )

            normalized_name = self._normalize_name(name)

            if normalized_name in normalized_aliases:
                value = (
                    nutrient.get("VALUE")
                    if nutrient.get("VALUE") is not None
                    else nutrient.get("value")
                )

                number = self._to_float(value)

                if number is not None:
                    return {
                        "value": number,
                        "unit": (
                            nutrient.get("UNITNAME")
                            or nutrient.get("unitName")
                            or nutrient.get("unit")
                            or ""
                        ),
                    }

        # Partial matching
        for nutrient in raw_nutrients:
            if not isinstance(nutrient, dict):
                continue

            name = (
                nutrient.get("NUTRIENTNAME")
                or nutrient.get("nutrientName")
                or nutrient.get("name")
                or ""
            )

            normalized_name = self._normalize_name(name)

            for alias in normalized_aliases:
                if alias and (
                    alias in normalized_name
                    or normalized_name in alias
                ):
                    value = (
                        nutrient.get("VALUE")
                        if nutrient.get("VALUE") is not None
                        else nutrient.get("value")
                    )

                    number = self._to_float(value)

                    if number is not None:
                        return {
                            "value": number,
                            "unit": (
                                nutrient.get("UNITNAME")
                                or nutrient.get("unitName")
                                or nutrient.get("unit")
                                or ""
                            ),
                        }

        return None

    def extract_nutrients(self, food_details):
        """
        Convert USDA data into a clean dictionary.

        Values are kept at the USDA reference amount,
        normally 100 g.
        """

        if not isinstance(food_details, dict):
            return {}

        raw_nutrients = self._get_raw_nutrients(food_details)

        result = {}

        # ---------------------------------------------------------
        # RAW USDA FORMAT
        # ---------------------------------------------------------
        if raw_nutrients:
            for nutrient_name in self.DEFAULT_NUTRIENTS:

                found = self._find_raw_nutrient(
                    raw_nutrients,
                    nutrient_name
                )

                if found is not None:
                    result[self.DISPLAY_NAMES[nutrient_name]] = {
                        "value": found["value"],
                        "unit": found["unit"],
                    }

            return result

        # ---------------------------------------------------------
        # ALREADY NORMALIZED FORMAT
        # ---------------------------------------------------------
        for nutrient_name in self.DEFAULT_NUTRIENTS:

            aliases = self.NUTRIENT_MAP.get(
                nutrient_name,
                [nutrient_name]
            )

            found = None
            found_unit = ""

            for key, value in food_details.items():

                normalized_key = self._normalize_name(key)

                for alias in aliases:

                    if normalized_key == self._normalize_name(alias):

                        if isinstance(value, dict):
                            found = self._to_float(
                                value.get("value")
                                if value.get("value") is not None
                                else value.get("amount")
                            )

                            found_unit = value.get(
                                "unit",
                                ""
                            )
                        else:
                            found = self._to_float(value)

                        break

                if found is not None:
                    break

            if found is not None:
                result[self.DISPLAY_NAMES[nutrient_name]] = {
                    "value": found,
                    "unit": found_unit,
                }

        return result

    def calculate(self, food_details, grams):
        """
        Calculate nutrition for a specified number of grams.

        USDA reference values are generally per 100 g.
        """

        try:
            grams = float(grams)
        except (TypeError, ValueError):
            return {}

        if grams <= 0:
            return {}

        base_nutrients = self.extract_nutrients(food_details)

        if not base_nutrients:
            return {}

        multiplier = grams / 100.0

        result = {}

        for nutrient_name, nutrient_data in base_nutrients.items():

            if isinstance(nutrient_data, dict):

                value = self._to_float(
                    nutrient_data.get("value")
                )

                unit = nutrient_data.get(
                    "unit",
                    ""
                )

            else:
                value = self._to_float(
                    nutrient_data
                )

                unit = ""

            if value is None:
                continue

            result[nutrient_name] = {
                "value": value * multiplier,
                "unit": unit,
            }

        # Internal helper used by the chatbot
        result["_grams"] = grams

        return result

    def calculate_from_food_details(self, food_details, portion):
        """
        Compatibility method for PortionResolver output.
        """

        if not isinstance(portion, dict):
            return {}

        grams = (
            portion.get("grams")
            or portion.get("weight_grams")
            or portion.get("calculated_grams")
            or portion.get("amount_grams")
        )

        if grams is None:
            return {}

        return self.calculate(
            food_details,
            grams
        )

    def get_nutrient(self, nutrition, nutrient_name):
        """
        Get one requested nutrient.
        """

        if not isinstance(nutrition, dict):
            return None

        target = self._normalize_name(
            nutrient_name
        )

        for key, value in nutrition.items():

            if self._normalize_name(key) == target:
                return value

        return None

    def format_nutrition(self, nutrition):
        """
        Convert calculated nutrition into readable text.
        """

        if not nutrition:
            return "Nutrition information unavailable."

        lines = []

        for nutrient_name, data in nutrition.items():

            if nutrient_name == "_grams":
                continue

            if isinstance(data, dict):

                value = data.get("value")
                unit = data.get("unit", "")

                if value is None:
                    continue

                lines.append(
                    f"{nutrient_name}: "
                    f"{self._format_number(value)}"
                    f"{unit}"
                )

            else:
                lines.append(
                    f"{nutrient_name}: {data}"
                )

        return "\n".join(lines)

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
    print("NutritionCalculator loaded successfully.")