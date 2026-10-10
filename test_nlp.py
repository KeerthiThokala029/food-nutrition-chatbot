from nlp_processor import NLPProcessor


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