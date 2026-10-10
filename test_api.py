from nutrition_database import NutritionDatabase


# Create USDA database connection
db = NutritionDatabase()


# Food entered by the user
user_input = "banana"


# Search USDA
results = db.search_food(
    user_input,
    page_size=20
)


print(f"\nUSDA returned {len(results)} results.")


if not results:
    print("No food results found.")
    exit()


# Select the best food instead of simply taking the first result
food = db.select_best_food(
    results,
    user_input
)


if not food:
    print("Could not select a suitable food.")
    exit()


print("\nBest USDA Match:")
print("Food:", food.get("description"))
print("Food ID:", food.get("fdcId"))
print("Data Type:", food.get("dataType"))


# Get complete nutrition information
food_details = db.get_food_details(
    food.get("fdcId")
)


if not food_details:
    print("Could not retrieve nutrition details.")
    exit()


# Extract nutrients
nutrients = db.extract_nutrients(
    food_details
)


print("\nNutrition Information:\n")


important_nutrients = [
    "Energy",
    "Protein",
    "Carbohydrate, by difference",
    "Total lipid (fat)",
    "Fiber, total dietary",
    "Sugars, total including NLEA",
    "Sodium, Na"
]


for nutrient_name in important_nutrients:

    if nutrient_name in nutrients:

        amount = nutrients[nutrient_name]["amount"]
        unit = nutrients[nutrient_name]["unit"]

        print(
            f"{nutrient_name}: "
            f"{amount} {unit}"
        )