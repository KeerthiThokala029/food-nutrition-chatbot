# 🥗 NutriBot — Food Nutrition Chatbot Using NLP

**From everyday food queries to meaningful nutrition insights.**

NutriBot is a Python-based food nutrition chatbot that combines Natural Language Processing (NLP), food matching, quantity-based calculations, and USDA FoodData Central to help users explore nutritional information through an interactive dashboard.

---

## 📑 Table of Contents

- [🌟 About the Project](#-about-the-project)
- [🎯 Project Objectives](#-project-objectives)
- [✨ Key Features](#-key-features)
- [🖥️ Dashboard Workflow](#️-dashboard-workflow)
- [🥗 Nutrition Information](#-nutrition-information)
- [⚖️ Quantity and Serving Support](#️-quantity-and-serving-support)
- [🔎 Food Matching and Ranking](#-food-matching-and-ranking)
- [🛡️ Safe Handling of Unknown Foods](#️-safe-handling-of-unknown-foods)
- [🏗️ System Architecture](#️-system-architecture)
- [⚙️ Methodology](#️-methodology)
- [📸 Application Screenshots](#-application-screenshots)
- [🛠️ Technology Stack](#️-technology-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Installation and Setup](#-installation-and-setup)
- [▶️ Running the Application](#️-running-the-application)
- [🧪 Testing](#-testing)
- [⚠️ Limitations](#️-limitations)
- [🔮 Future Enhancements](#-future-enhancements)
- [📚 Data Source](#-data-source)
- [👩‍💻 Author and Connect](#-author-and-connect)

---

## 🌟 About the Project

NutriBot is designed to make food nutrition information easier to access and understand.

Users can enter food-related queries through the dashboard. The application processes the input, attempts to identify the food and requested quantity, searches the USDA FoodData Central database, and presents the available nutritional information.

Instead of relying solely on a predefined list of foods, NutriBot uses an external nutrition database and food-matching logic to identify suitable records for supported queries.

The project brings together text processing, food identification, API communication, nutrition calculations, and response generation in a single interactive application.

## 🎯 Project Objectives

- Develop an interactive chatbot for food nutrition queries.
- Process supported food inputs using NLP techniques.
- Retrieve food and nutrient information from USDA FoodData Central.
- Improve food identification through text similarity and spelling-error handling.
- Interpret supported quantities and serving descriptions.
- Calculate nutrition values based on the selected food record.
- Handle unmatched foods without inventing nutrition information.
- Present nutrition results through a user-friendly dashboard.

## ✨ Key Features

### 💬 Natural Language Food Queries

Accepts supported food-related inputs in a simple, conversational format.

### 🔍 Dynamic Food Search

Uses USDA FoodData Central to search food records rather than depending entirely on a fixed food list.

### ✏️ Spelling-Error Handling

Uses text normalization and spelling-recovery techniques to help identify intended food names when possible.

### ⚖️ Quantity and Portion Processing

Attempts to identify quantities, units, and serving information for supported query formats.

### 🧮 Nutrition Calculation

Scales available nutrient values according to the requested quantity when the required data and unit conversions are supported.

### 🏆 Food Matching and Ranking

Evaluates food candidates using text similarity, food descriptions, data types, and other matching criteria.

### 🛡️ Unknown-Food Handling

Avoids presenting fabricated nutrition values when a sufficiently reliable food match cannot be established.

### 🖥️ Interactive Dashboard

Displays the application's nutrition results and detailed food information through Streamlit.

---

## 🖥️ Dashboard Workflow

The dashboard is the main interface through which users interact with NutriBot. When a user submits a food query, the application processes it through several stages before displaying the result.

The example below illustrates the intended workflow for a query such as `I ate 200g banana`.

### 1️⃣ User Input

The user enters a food-related query in the dashboard.

Example:

```text
I ate 200g banana
```

The input may contain a food name, a quantity, a unit, and additional words describing the request.

### 2️⃣ Text Normalization

The application cleans and normalizes the input to make subsequent text processing more consistent.

This may involve trimming unnecessary whitespace and normalizing text for matching.

### 3️⃣ Spelling Recovery

The food-matching process attempts to recover from common spelling errors.

Example:

```text
chickwn → chicken
```

Spelling recovery is algorithmic and does not guarantee a correct result for every misspelling. The resulting candidates still need to be evaluated.

### 4️⃣ Food Extraction

The application identifies the food name that should be used for the nutrition lookup.

Example:

```text
banana
```

The extracted food becomes the search term for the next stage.

### 5️⃣ Quantity Extraction

The application attempts to identify the amount requested by the user.

Example:

```text
200
```

This value is interpreted together with the detected unit and food information.

### 6️⃣ Unit Detection

The application identifies the unit associated with the quantity.

Example:

```text
g
```

The quantity and unit together represent the requested amount:

```text
200 g of banana
```

### 7️⃣ Intent Detection

The query-processing logic determines the type of food-related operation requested, where supported.

For the example query, the intended operation is nutrition lookup.

```text
Intent: nutrition
```

### 8️⃣ USDA Food Retrieval

The application searches USDA FoodData Central using the extracted food name.

The API may return multiple candidate records. NutriBot evaluates the available candidates rather than automatically assuming that the first result is always the best match.

### 9️⃣ Food Selection and Nutrient Extraction

The matching logic selects a suitable food record when possible. The nutrition database module then retrieves detailed information and extracts available nutrient values.

The selected record may differ depending on its description, preparation method, data type, and similarity to the requested food.

### 🔟 Nutrition Calculation

When the requested quantity and the selected food's nutrition basis are compatible, the application scales nutrient values to the requested amount.

For example, if a record provides nutrient values per 100 g, a calculation for 200 g can use a scaling factor of:

\[
\text{Scaling factor}=\frac{200}{100}=2
\]

Each available nutrient value is multiplied by this factor, provided the record and calculation logic support that basis.

### 1️⃣1️⃣ Response Generation

The response-generation component formats the processed information for the dashboard.

The result can include available nutrition values, calculated amounts, and relevant food details.

If a reliable match cannot be established, the application should avoid presenting an unrelated food as a confident match.

---

## 🥗 Nutrition Information

NutriBot extracts available nutrient information from the selected USDA food record. The exact nutrients displayed depend on the data returned by the API and the application's supported output.

| Nutrient | Unit |
|---|---|
| 🔥 Calories / Energy | kcal, where available |
| 💪 Protein | g |
| 🍞 Carbohydrates | g |
| 🥑 Total Fat | g |
| 🌾 Fiber | g |
| 🍬 Sugar | g |
| 🦴 Calcium | mg |
| 🩸 Iron | mg |
| 🧂 Sodium | mg |
| 🍊 Vitamin C | mg |

**Note:** This table describes important nutrients of interest; it does not guarantee that every nutrient is present for every food record. The application should use the units and values supplied by the selected record.

## ⚖️ Quantity and Serving Support

Users may enter food queries in formats such as:

```text
100g banana
200g apple
1 kg rice
2 apples
1 serving
```

Inputs such as `500 mg food` also contain a quantity and unit, but meaningful nutrition calculations depend on whether the unit can be interpreted appropriately for the selected food.

### 🧮 How Quantity-Based Calculation Works

When the nutrition basis is expressed per 100 g, the calculation can be represented as:

\[
\text{Nutrient amount}
=
\text{Nutrient per 100 g}
\times
\frac{\text{Requested grams}}{100}
\]

For example, if a selected record contains 10 g of a nutrient per 100 g, then a supported calculation for 200 g gives:

\[
10\times\frac{200}{100}=20\text{ g}
\]

This is an illustrative calculation, not a measured nutrition value for a particular food.

For serving-based inputs, the application needs suitable serving-weight information or another supported conversion method. It should not assume that every serving has the same weight.

### 📏 Unit and Portion Considerations

- Weight units must be converted consistently before scaling nutrition values.
- Serving-based quantities require an appropriate serving definition.
- Food records may use different nutrient bases.
- Unsupported or ambiguous quantities can lead to uncertain calculations.

The accuracy of the result depends on correct food matching, quantity interpretation, and the nutrition data available for the selected record.

---

## 🔎 Food Matching and Ranking

USDA FoodData Central can return multiple possible records for the same search term. For this reason, NutriBot uses food-matching and ranking logic to help select a suitable candidate.

### 🏆 Candidate Evaluation

The matching process can consider:

- Text similarity between the query and food description
- Similarity after spelling normalization
- Whether the food description starts with the requested name
- USDA data type priority
- Generic versus specialized food descriptions
- Preparation-related terms
- A minimum similarity threshold

The final choice depends on the implemented scoring rules and the candidates returned by the API.

### 🍗 Why Ranking Matters

Consider a generic query:

```text
User: chicken
```

A food database might contain records describing plain chicken, prepared chicken dishes, and branded chicken products.

The system should favor a record that appropriately represents the user's query rather than selecting a record simply because it contains the word “chicken.”

For a generic food query, a plain, relevant food record may be more appropriate than a specialized product. However, the best choice also depends on what the user actually means—for example, raw chicken and cooked chicken do not have identical nutrition profiles.

### ✏️ Spelling Recovery Is Not Final Selection

Spelling recovery and food ranking serve different purposes:

1. Spelling recovery attempts to generate a more useful search query.
2. USDA search retrieves candidate records.
3. Matching logic evaluates the candidates.
4. The selected record supplies the nutrition data.

This separation helps prevent a spelling correction from being treated as proof that the correct food has been found.

---

## 🛡️ Safe Handling of Unknown Foods

Nutrition information should be based on a suitable food record rather than invented values.

For an input such as:

```text
xyzabc food
```

If the application cannot identify a sufficiently reliable match, the appropriate behavior is to report that nutrition information could not be found and ask the user to try a different description.

Example response:

```text
I couldn't find reliable nutrition information for
"xyzabc food" in the current food database.

Please try another food name or provide a more
specific description.
```

This example illustrates the desired behavior; the exact wording depends on the application's response-generation implementation.

### 🔐 Why This Matters

- Prevents unsupported nutrition values from being presented as facts.
- Reduces the risk of selecting unrelated food records.
- Encourages more specific queries when the input is ambiguous.
- Keeps retrieved data separate from estimated or unavailable information.

A similarity score alone does not establish that a match is nutritionally appropriate. The food description and the requested preparation or portion should also be considered.

---

## 🏗️ System Architecture

The architecture describes the main components that work together to process a query and produce a nutrition response.

![NutriBot System Architecture](docs/images/system-architecture.png)

### 🧩 Main Components

**1. Streamlit Dashboard**

Collects user input and displays the resulting nutrition information.

**2. Chatbot Module**

Coordinates the application's query-processing and response workflow.

**3. NLP Processor**

Handles supported natural-language input processing.

**4. Food Matcher**

Evaluates candidate food descriptions and helps select an appropriate record.

**5. Nutrition Database**

Communicates with USDA FoodData Central to search for foods and retrieve detailed nutrition data.

**6. Portion Resolver**

Handles supported quantity and portion interpretation.

**7. Nutrition Calculator**

Calculates nutrition amounts from the selected record when the quantity and nutrition basis are compatible.

**8. Response Generator**

Formats the available nutrition information for presentation.

---

## ⚙️ Methodology

NutriBot organizes the nutrition lookup process into a sequence of stages.

| Stage | Operation | Purpose |
|---|---|---|
| 1 | Input collection | Accept a food-related query |
| 2 | Text normalization | Prepare text for processing |
| 3 | Spelling recovery | Attempt to handle spelling errors |
| 4 | Food extraction | Identify the food search term |
| 5 | Quantity and unit processing | Interpret supported amounts |
| 6 | Intent processing | Determine the requested operation |
| 7 | API search | Retrieve candidate food records |
| 8 | Food ranking | Evaluate possible matches |
| 9 | Nutrient extraction | Retrieve available nutrient values |
| 10 | Nutrition calculation | Scale values for supported quantities |
| 11 | Response generation | Present the result in the dashboard |

The exact execution order and behavior depend on the application's implementation. Some stages may be combined or handled by the same module.

---

## 📸 Application Screenshots

The following screenshots illustrate the main views of NutriBot.

### 🏠 Dashboard

The main interface for entering food queries and interacting with the chatbot.

![NutriBot Dashboard](results/screenshots/Dashboard.png)

### 📊 Nutrition Results

An example of the nutrition information displayed for a selected food.

![Nutrition Results](results/screenshots/Nutrition%20Results.png)

### 🥗 Full Nutrition Details

A detailed view of the available nutrition information for a selected food record.

![Full Nutrition Details](results/screenshots/Full%20Details.png)

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core application logic |
| 🖥️ Streamlit | Interactive dashboard |
| 🧠 NLP techniques | Food-query processing |
| 🌐 USDA FoodData Central API | Food and nutrient retrieval |
| 🔗 Requests | HTTP API communication |
| 🔐 python-dotenv | Environment variable configuration |
| 🔎 RapidFuzz | Text similarity and matching |

---

## 📂 Project Structure

```text
food-nutrition-chatbot/
├── app.py
├── chatbot.py
├── nlp_processor.py
├── food_matcher.py
├── nutrition_database.py
├── nutrition_calculator.py
├── portion_resolver.py
├── response_generator.py
├── train_model.py
├── test_api.py
├── test_matcher.py
├── test_nlp.py
├── requirements.txt
├── RUN_NUTRIBOT.bat
├── .env
├── .gitignore
├── README.md
├── docs/
│   └── images/
│       └── system-architecture.png
└── results/
    └── screenshots/
        ├── Dashboard.png
        ├── Nutrition Results.png
        └── Full Details.png
```

**Important:** `.env` contains your private API key and should not be committed to GitHub. The directory listing above illustrates the local development setup; the private `.env` file should be excluded from the public repository.

---

## 🚀 Installation and Setup

### 📋 Prerequisites

- Python 3.12 or another compatible Python version
- Git
- A USDA FoodData Central API key
- Internet access for API requests

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/KeerthiThokala029/food-nutrition-chatbot.git
cd food-nutrition-chatbot
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows using PowerShell:

```powershell
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the API Key

Create a `.env` file in the project's root directory:

```env
USDA_API_KEY=your_api_key_here
```

Get an API key and review the API documentation at the [USDA FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/).

Replace the placeholder with your own key. Do not share your real API key or commit the `.env` file.

---

## ▶️ Running the Application

Activate your virtual environment and run:

```bash
streamlit run app.py
```

Alternatively, on Windows, run:

```text
RUN_NUTRIBOT.bat
```

Open the local URL shown in the terminal to access the NutriBot dashboard.

---

## 🧪 Testing

NutriBot includes test scripts for checking individual components.

| Test File | Purpose |
|---|---|
| `test_api.py` | API-related checks |
| `test_matcher.py` | Food-matching checks |
| `test_nlp.py` | NLP processing checks |

For example, run the food matcher test with:

```bash
python test_matcher.py
```

Run the tests from the project directory with the virtual environment activated. API-related tests may require a working internet connection and a valid API key.

---

## ⚠️ Limitations

- The available nutrition information depends on USDA FoodData Central records.
- Not all food records provide every nutrient listed in this README.
- Spelling recovery and similarity-based matching cannot guarantee a correct match for every query.
- Raw, cooked, branded, and prepared foods may have different nutrient profiles.
- Quantity calculations depend on supported units and a compatible nutrition basis.
- Serving-based calculations require suitable serving information.
- Live API searches require internet access and valid API configuration.
- Nutrition information should not be treated as medical advice.

## 🔮 Future Enhancements

Possible improvements include:

- 📈 Interactive nutrition charts
- 🍽️ Meal-wise nutrition summaries
- 🗓️ Daily food and nutrition history
- 🧠 More robust food-name and intent recognition
- ⚖️ Expanded serving and unit conversion support
- 🔍 Better handling of ambiguous food matches
- 📱 Improved mobile dashboard layout
- ☁️ Public deployment and hosting

---

## 📚 Data Source

NutriBot uses **[USDA FoodData Central](https://fdc.nal.usda.gov/)** as its external food and nutrition data source.

The API supplies food records and nutrient information. NutriBot uses its food-search and nutrition-processing logic to select records and present the information returned by the database.

---

## 👩‍💻 Author and Connect

### 🔗 Connect

**GitHub:**

[https://github.com/KeerthiThokala029](https://github.com/KeerthiThokala029)

**Project Repository:**

[https://github.com/KeerthiThokala029/food-nutrition-chatbot](https://github.com/KeerthiThokala029/food-nutrition-chatbot)

---

<p align="center">
  <strong>🥗 NutriBot</strong>
  <br>
  <em>Making food nutrition information easier to explore, one query at a time.</em>
</p>