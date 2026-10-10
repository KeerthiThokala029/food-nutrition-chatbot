import re
import streamlit as st
import pandas as pd

from chatbot import FoodNutritionChatbot


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Food Nutrition Chatbot",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SIMPLE, SAFE STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        padding: 0.75rem;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        background: rgba(128, 128, 128, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.8rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.35rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHATBOT
# ============================================================

@st.cache_resource
def get_chatbot():
    return FoodNutritionChatbot()


chatbot = get_chatbot()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "queries" not in st.session_state:
    st.session_state.queries = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# NUTRIENTS
# ============================================================

NUTRIENTS = [
    "Carbohydrates",
    "Protein",
    "Energy",
    "Fat",
    "Fiber",
    "Sugars",
    "Sodium",
    "Calcium",
    "Iron",
    "Potassium",
    "Magnesium",
    "Phosphorus",
    "Zinc",
    "Vitamin A",
    "Vitamin B1",
    "Vitamin B2",
    "Vitamin B3",
    "Vitamin B5",
    "Vitamin B6",
    "Vitamin B7",
    "Vitamin B9",
    "Vitamin B12",
    "Vitamin C",
    "Vitamin D",
    "Vitamin E",
    "Vitamin K",
]


NUTRIENT_PATTERN = "|".join(
    re.escape(name)
    for name in sorted(
        NUTRIENTS,
        key=len,
        reverse=True
    )
)


# ============================================================
# RESPONSE CLEANING
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("**", "")
    text = text.replace("__", "")

    return text.strip()


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_response(text):

    clean = clean_text(text)

    result = {
        "food": "",
        "reference": "",
        "nutrients": [],
        "source": "USDA FoodData Central",
    }

    # --------------------------------------------------------
    # FOOD
    # --------------------------------------------------------

    food_match = re.search(
        r"Nutrition\s+for\s+(.+?)(?:\r?\n|$)",
        clean,
        flags=re.IGNORECASE,
    )

    if food_match:

        result["food"] = (
            food_match.group(1).strip()
        )

    # --------------------------------------------------------
    # REFERENCE
    # --------------------------------------------------------

    reference_match = re.search(
        r"Reference\s+amount\s*:\s*(.+?)(?:\r?\n|$)",
        clean,
        flags=re.IGNORECASE,
    )

    if reference_match:

        result["reference"] = (
            reference_match.group(1).strip()
        )

    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    source_match = re.search(
        r"Source\s*:\s*(.+?)(?:\r?\n|$)",
        clean,
        flags=re.IGNORECASE,
    )

    if source_match:

        result["source"] = (
            source_match.group(1).strip()
        )

    # --------------------------------------------------------
    # NUTRIENTS
    # --------------------------------------------------------

    found = []

    # First try normal line-by-line format.
    for line in clean.splitlines():

        line = line.strip()

        match = re.match(
            rf"^({NUTRIENT_PATTERN})\s*:\s*(.+)$",
            line,
            flags=re.IGNORECASE,
        )

        if match:

            found.append(
                (
                    match.group(1).strip(),
                    match.group(2).strip(),
                )
            )

    # --------------------------------------------------------
    # FALLBACK FOR ONE-LINE RESPONSES
    # --------------------------------------------------------

    if not found:

        matches = re.finditer(
            rf"\b({NUTRIENT_PATTERN})\s*:\s*(.*?)(?=\s+\b(?:{NUTRIENT_PATTERN})\s*:|\s+Source\s*:|$)",
            clean,
            flags=re.IGNORECASE | re.DOTALL,
        )

        for match in matches:

            value = match.group(2).strip()

            if value:

                found.append(
                    (
                        match.group(1).strip(),
                        value,
                    )
                )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    seen = set()

    for name, value in found:

        key = name.lower()

        if key in seen:
            continue

        seen.add(key)

        result["nutrients"].append(
            (
                name,
                value,
            )
        )

    return result


# ============================================================
# NUMBER EXTRACTION
# ============================================================

def numeric_value(value):

    if value is None:
        return None

    match = re.search(
        r"-?\d+(?:\.\d+)?",
        str(value),
    )

    if not match:
        return None

    try:

        return float(
            match.group()
        )

    except ValueError:

        return None


# ============================================================
# FIND NUTRIENT
# ============================================================

def find_nutrient(
    nutrients,
    target,
):

    for name, value in nutrients:

        if name.lower() == target.lower():

            return value

    return "0.00"


# ============================================================
# RENDER NUTRITION RESULT
# ============================================================

def render_result(
    response,
    user_query="",
):

    parsed = parse_response(
        response
    )

    # --------------------------------------------------------
    # CHECK
    # --------------------------------------------------------

    if not parsed["nutrients"]:

        st.error(
            "No nutrition values could be read from the response."
        )

        st.write(response)

        return

    food = (
        parsed["food"]
        or "Food"
    )

    reference = (
        parsed["reference"]
        or "100 g"
    )

    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.divider()

    st.subheader(
        "🥗 Nutrition Result"
    )

    if user_query:

        st.caption(
            f"Query: {user_query}"
        )

    st.markdown(
        f"### 🥗 {food}"
    )

    st.caption(
        f"Reference amount: {reference}"
    )

    # ========================================================
    # NUTRITION SUMMARY
    # ========================================================

    st.markdown(
        "### 📊 Nutrition Summary"
    )

    energy = find_nutrient(
        parsed["nutrients"],
        "Energy",
    )

    protein = find_nutrient(
        parsed["nutrients"],
        "Protein",
    )

    carbs = find_nutrient(
        parsed["nutrients"],
        "Carbohydrates",
    )

    fat = find_nutrient(
        parsed["nutrients"],
        "Fat",
    )

    columns = st.columns(4)

    with columns[0]:

        st.metric(
            "🔥 Energy",
            energy,
        )

    with columns[1]:

        st.metric(
            "🥩 Protein",
            protein,
        )

    with columns[2]:

        st.metric(
            "🌾 Carbohydrates",
            carbs,
        )

    with columns[3]:

        st.metric(
            "🥑 Fat",
            fat,
        )

    # ========================================================
    # ADDITIONAL NUTRIENTS
    # ========================================================

    st.markdown(
        "### 🧪 Additional Nutrients"
    )

    fiber = find_nutrient(
        parsed["nutrients"],
        "Fiber",
    )

    sugar = find_nutrient(
        parsed["nutrients"],
        "Sugars",
    )

    sodium = find_nutrient(
        parsed["nutrients"],
        "Sodium",
    )

    vitamin_c = find_nutrient(
        parsed["nutrients"],
        "Vitamin C",
    )

    calcium = find_nutrient(
        parsed["nutrients"],
        "Calcium",
    )

    iron = find_nutrient(
        parsed["nutrients"],
        "Iron",
    )

    potassium = find_nutrient(
        parsed["nutrients"],
        "Potassium",
    )

    magnesium = find_nutrient(
        parsed["nutrients"],
        "Magnesium",
    )

    columns = st.columns(4)

    with columns[0]:

        st.metric(
            "🌿 Fiber",
            fiber,
        )

    with columns[1]:

        st.metric(
            "🍬 Sugars",
            sugar,
        )

    with columns[2]:

        st.metric(
            "🧂 Sodium",
            sodium,
        )

    with columns[3]:

        st.metric(
            "🍊 Vitamin C",
            vitamin_c,
        )

    columns = st.columns(4)

    with columns[0]:

        st.metric(
            "🦴 Calcium",
            calcium,
        )

    with columns[1]:

        st.metric(
            "🔩 Iron",
            iron,
        )

    with columns[2]:

        st.metric(
            "⚡ Potassium",
            potassium,
        )

    with columns[3]:

        st.metric(
            "💊 Magnesium",
            magnesium,
        )

    # ========================================================
    # MACRONUTRIENT CHART
    # ========================================================

    st.markdown(
        "### 📈 Macronutrient Profile"
    )

    chart_data = pd.DataFrame(
        {
            "Nutrient": [
                "Carbohydrates",
                "Protein",
                "Fat",
                "Fiber",
            ],
            "Amount": [
                numeric_value(carbs) or 0,
                numeric_value(protein) or 0,
                numeric_value(fat) or 0,
                numeric_value(fiber) or 0,
            ],
        }
    )

    st.bar_chart(
        chart_data.set_index(
            "Nutrient"
        ),
        height=300,
    )

    # ========================================================
    # FULL DETAILS
    # ========================================================

    st.markdown(
        "### 📋 Full Nutrition Details"
    )

    columns = st.columns(2)

    for index, (
        name,
        value,
    ) in enumerate(
        parsed["nutrients"]
    ):

        with columns[
            index % 2
        ]:

            st.metric(
                name,
                value,
            )

    # ========================================================
    # USDA INFORMATION
    # ========================================================

    st.markdown(
        "### 🌐 USDA Information"
    )

    columns = st.columns(3)

    with columns[0]:

        st.metric(
            "Data Source",
            "USDA",
        )

    with columns[1]:

        st.metric(
            "Database",
            "FoodData Central",
        )

    with columns[2]:

        st.metric(
            "Reference",
            reference,
        )

    st.caption(
        "Nutrition values are retrieved from USDA FoodData Central."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🥗 Food Nutrition Chatbot"
    )

    st.caption(
        "USDA FoodData Central nutrition assistant"
    )

    page = st.radio(
        "Navigate",
        [
            "💬 Chat",
            "📊 Dashboard",
            "⚙️ How It Works",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        "### Quick Examples"
    )

    st.write(
        "🍎 `apple`"
    )

    st.write(
        "🍌 `2 bananas`"
    )

    st.write(
        "🍗 `150 grams of chicken`"
    )

    st.write(
        "✏️ `chiken`"
    )

    st.write(
        "🥦 `brocolli`"
    )


# ============================================================
# CHAT PAGE
# ============================================================

if page == "💬 Chat":

    # ========================================================
    # MAIN TITLE
    #
    # IMPORTANT:
    # Native Streamlit title is used here.
    # No custom HTML header.
    # ========================================================

    st.title(
        "🥗 Food Nutrition Chatbot"
    )

    st.caption(
        "Ask about foods, quantities, nutrients, or spelling mistakes."
    )

    # ========================================================
    # TRY MESSAGE
    # ========================================================

    st.info(
        "Try: `apple` • `2 bananas` • "
        "`150 grams of chicken` • `chiken`"
    )

    # ========================================================
    # EXAMPLES
    # ========================================================

    st.markdown(
        "### Try an Example"
    )

    columns = st.columns(3)

    with columns[0]:

        st.write(
            "🍎 **apple**"
        )

    with columns[1]:

        st.write(
            "🍌 **2 bananas**"
        )

    with columns[2]:

        st.write(
            "🍗 **150 grams of chicken**"
        )

    st.divider()

    # ========================================================
    # LAST RESULT
    # ========================================================

    if st.session_state.last_result:

        render_result(
            st.session_state.last_result[
                "response"
            ],
            st.session_state.last_result[
                "query"
            ],
        )

    # ========================================================
    # HISTORY
    # ========================================================

    if st.session_state.messages:

        with st.expander(
            "💬 Conversation History"
        ):

            for message in (
                st.session_state.messages
            ):

                if (
                    message["role"]
                    == "user"
                ):

                    st.markdown(
                        f"**You:** "
                        f"{message['content']}"
                    )

                else:

                    parsed = parse_response(
                        message["content"]
                    )

                    if parsed["food"]:

                        st.markdown(
                            f"**Bot:** "
                            f"{parsed['food']} — "
                            f"{parsed['reference']}"
                        )

                    else:

                        st.write(
                            message["content"]
                        )

    # ========================================================
    # CHAT INPUT
    # ========================================================

    user_input = st.chat_input(
        "Ask about a food or nutrition..."
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        st.session_state.queries.append(
            user_input
        )

        with st.spinner(
            "Checking USDA FoodData Central..."
        ):

            try:

                response = (
                    chatbot.process_message(
                        user_input
                    )
                )

            except Exception as error:

                response = (
                    "Sorry, I could not process "
                    "that request.\n\n"
                    f"Error: {error}"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        st.session_state.last_result = {
            "query": user_input,
            "response": response,
        }

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.title(
        "📊 Nutrition Dashboard"
    )

    st.caption(
        "Nutrition analysis powered by USDA FoodData Central."
    )

    columns = st.columns(4)

    with columns[0]:

        st.metric(
            "Queries",
            len(
                st.session_state.queries
            ),
        )

    with columns[1]:

        st.metric(
            "Data Source",
            "USDA",
        )

    with columns[2]:

        st.metric(
            "Nutrients",
            "13+",
        )

    with columns[3]:

        st.metric(
            "NLP",
            "Enabled",
        )

    st.divider()

    st.markdown(
        "### Project Capabilities"
    )

    left, right = st.columns(2)

    with left:

        st.info(
            "🔎 **Dynamic Food Search**\n\n"
            "Searches USDA FoodData Central instead of "
            "using a small fixed food list."
        )

        st.info(
            "✏️ **Spelling Recovery**\n\n"
            "Handles inputs such as `chiken`, `bananna`, "
            "and other common spelling variations."
        )

        st.info(
            "⚖️ **Portion Resolution**\n\n"
            "Supports grams, kilograms, countable foods, "
            "and USDA reference portions."
        )

    with right:

        st.info(
            "🧠 **Natural Language Processing**\n\n"
            "Understands food names, quantities, units, "
            "and nutrition questions."
        )

        st.info(
            "📊 **Nutrition Analysis**\n\n"
            "Calculates calories, macronutrients, fiber, "
            "minerals, and available vitamins."
        )

        st.info(
            "🌐 **USDA Data**\n\n"
            "Nutrition information comes from USDA "
            "FoodData Central."
        )

    if st.session_state.queries:

        st.divider()

        st.markdown(
            "### Recent Queries"
        )

        for query in reversed(
            st.session_state.queries[-10:]
        ):

            st.write(
                f"• {query}"
            )


# ============================================================
# HOW IT WORKS
# ============================================================

elif page == "⚙️ How It Works":

    st.title(
        "⚙️ How It Works"
    )

    steps = [
        (
            "1. User Input",
            "The user enters a natural-language food request.",
        ),
        (
            "2. NLP Processor",
            "Extracts food name, quantity, unit, and intent.",
        ),
        (
            "3. USDA Search",
            "Searches USDA FoodData Central for candidate foods.",
        ),
        (
            "4. Food Matching",
            "Ranks the most appropriate USDA food.",
        ),
        (
            "5. Portion Resolver",
            "Converts the requested portion into grams.",
        ),
        (
            "6. Nutrition Calculator",
            "Scales USDA nutrients to the requested amount.",
        ),
        (
            "7. Response Generator",
            "Creates the nutrition result shown in the application.",
        ),
    ]

    for title, description in steps:

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {title}"
            )

            st.write(
                description
            )

    st.divider()

    st.markdown(
        "### Example"
    )

    st.code(
        """User:
I ate 2 bananas

↓

NLP:
food = banana
quantity = 2
unit = count

↓

USDA FoodData Central

↓

Portion Resolver:
2 bananas ≈ 236 g

↓

Nutrition Calculator

↓

Nutrition Result""",
        language="text",
    )


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.title(
        "ℹ️ About"
    )

    st.markdown(
        "### Food Nutrition Chatbot Using NLP"
    )

    st.write(
        "This project combines NLP, fuzzy food matching, "
        "portion resolution, nutrition calculation, and "
        "USDA FoodData Central."
    )

    st.markdown(
        "### Technologies"
    )

    left, right = st.columns(2)

    with left:

        st.write("🐍 Python")
        st.write("🧠 NLP")
        st.write("🔎 RapidFuzz")
        st.write("🌐 USDA FoodData Central API")

    with right:

        st.write("📊 Streamlit")
        st.write("📦 Requests")
        st.write("🔐 python-dotenv")
        st.write("🥗 Nutrition calculation")

    st.divider()

    st.write(
        "The application dynamically searches USDA nutrition "
        "data rather than depending on a small hard-coded "
        "food database."
    )