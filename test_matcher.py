"""
Test Food Matcher with live USDA data.
"""

from nutrition_database import NutritionDatabase
from food_matcher import FoodMatcher


db = NutritionDatabase()

matcher = FoodMatcher()


test_inputs = [
    "chicken",
    "chiken",
    "broccoli",
    "brocolli",
    "banana",
    "bananna",
    "tomato",
    "tomatto",
    "apple",
    "aple",
    "fried chicken",
    "chicken breast",
]


for user_input in test_inputs:

    print()
    print("=" * 70)

    print(
        "USER INPUT:",
        user_input
    )

    corrected = matcher.correct_spelling(
        user_input
    )

    print(
        "CORRECTED:",
        corrected
    )

    # Search using corrected spelling.
    search_results = db.search_food(
        corrected,
        page_size=20
    )

    print(
        "USDA RESULTS:",
        len(search_results)
    )

    if not search_results:

        print(
            "No USDA results found."
        )

        continue

    match = matcher.find_best_match(
        corrected,
        search_results
    )

    if not match:

        print(
            "NO RELIABLE MATCH"
        )

        continue

    print()
    print(
        "BEST USDA MATCH:"
    )

    print(
        "Food:",
        match["food"]
    )

    print(
        "Similarity:",
        match["similarity"]
    )

    print(
        "Score:",
        match["score"]
    )

    print(
        "Food ID:",
        match["fdc_id"]
    )

    print(
        "Data Type:",
        match["data_type"]
    )