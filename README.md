# 🥗 NutriBot — Food Nutrition Chatbot Using NLP

<p align="center">
  <strong>Making food nutrition information simple, accessible, and easy to explore.</strong>
  <br>
  A Python-based nutrition chatbot powered by Natural Language Processing and USDA FoodData Central.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/NLP-Text%20Processing-805AD5?style=for-the-badge" alt="NLP">
  <img src="https://img.shields.io/badge/USDA-Food%20Data-228B22?style=for-the-badge" alt="USDA FoodData Central">
</p>

---

## 📑 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [How It Works](#️-how-it-works)
- [Results and Visualization](#-results-and-visualization)
- [Application Screenshots](#-application-screenshots)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Data Source](#-data-source)
- [Author and Connect](#-author-and-connect)

## 📌 About the Project

**NutriBot** is a food nutrition chatbot developed using Python, Natural Language Processing (NLP), and Streamlit. It allows users to enter food names and food-related questions in natural language and explore nutritional information.

The application uses the **USDA FoodData Central API** to search food records and retrieve available nutrient information. It also incorporates food matching, spelling-error handling, and quantity-based nutrition analysis for supported inputs.

The goal of NutriBot is to make food nutrition information easier to explore through a simple, interactive chatbot interface.

## ✨ Features

- **Natural Language Queries:** Enter food-related questions using everyday language.
- **Food Search:** Search food records using the USDA FoodData Central API.
- **Spelling Error Handling:** Attempt to recover from common typing mistakes in food names.
- **Nutrition Analysis:** Retrieve calories, protein, carbohydrates, fats, and other nutrients when available.
- **Quantity-Based Analysis:** Calculate nutrition for supported food quantities and portions.
- **Food Matching:** Rank candidate food records to identify a suitable match.
- **Interactive Interface:** View nutrition information through a Streamlit application.

## ⚙️ How It Works

NutriBot follows a sequence of processing steps to turn a food-related query into a nutrition response.

```text
User Food Query
       |
       v
NLP Processing
       |
       v
Food and Quantity Matching
       |
       v
USDA FoodData Central API
       |
       v
Nutrition Data Extraction
       |
       v
Nutrition Calculation
       |
       v
Chatbot Response
```

The exact processing path depends on the user's query and the food information returned by the API.

## 📊 Results and Visualization

The results interface presents food nutrition information retrieved and processed by NutriBot. The available information depends on the selected USDA food record and the nutrients provided for that record.

### Nutrition Information

The application can present available nutrition values, including:

- Energy and calories
- Protein
- Carbohydrates
- Total fat
- Other available nutrients

The displayed nutrients may differ between food records because USDA records do not all contain identical information.

### Quantity-Based Nutrition Analysis

For supported inputs, NutriBot uses the requested quantity or portion to calculate nutrition values.

Examples of supported query formats may include:

```text
chicken
2 bananas
150 grams of chicken
```

The resulting values depend on the matched food record, the interpreted quantity, and the available nutrition data.

### Food Matching and Spelling Recovery

The application searches USDA FoodData Central for candidate foods and ranks results based on food-description similarity and other selection criteria.

Spelling recovery attempts to handle common typing errors without relying exclusively on a fixed list of food-name corrections. The final match still depends on the available API results and the matching logic.

### Interpretation

Nutrition results should be interpreted in the context of:

- The selected USDA food record
- Food preparation and description
- The requested quantity or portion
- Nutrient availability in the selected record
- The accuracy of food and quantity matching

Nutrition values can vary depending on the specific food record and preparation method. The results are intended to provide nutrition information, not a medical diagnosis.

---

## 📸 Application Screenshots

The following screenshots demonstrate the main interface and nutrition output of NutriBot.

### 🏠 Dashboard

Shows the main interface for entering food queries and interacting with the chatbot.

![NutriBot Dashboard](results/screenshots/Dashboard.png)

### 📊 Nutrition Results

Shows an example of the nutrition results presented by the application.

![Nutrition Results](results/screenshots/Nutrition%20Results.png)

### 🥗 Full Nutrition Details

Shows the detailed nutrition information available for a selected food.

![Full Nutrition Details](results/screenshots/Full%20Details.png)

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| Natural Language Processing | Food-query processing |
| USDA FoodData Central API | Food and nutrition data retrieval |
| Requests | HTTP communication with the API |
| python-dotenv | Loading environment variables |
| RapidFuzz | Text similarity and food matching |

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
├── .gitignore
├── results/
│   └── screenshots/
│       ├── Dashboard.png
│       ├── Nutrition Results.png
│       └── Full Details.png
└── README.md
```

## 🚀 Installation and Setup

### 📋 Prerequisites

- Python 3.12 or a compatible version
- Git
- A USDA FoodData Central API key

### 1. Clone the Repository

```bash
git clone https://github.com/KeerthiThokala029/food-nutrition-chatbot.git
cd food-nutrition-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API Key

Create a `.env` file in the project's root directory and add your own USDA API key:

```env
USDA_API_KEY=your_api_key_here
```

Get an API key through the [USDA FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/).

**Security:** Replace the placeholder with your own key. Do not publish your actual API key or commit your `.env` file to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

Alternatively, on Windows, run `RUN_NUTRIBOT.bat` from the project folder.

## 🧪 Testing

The project includes test files for checking different components:

- `test_api.py` — API-related checks
- `test_matcher.py` — food-matching checks
- `test_nlp.py` — NLP processing checks

To run a test, activate your virtual environment and execute the relevant file. For example:

```bash
python test_matcher.py
```

## 🔮 Future Enhancements

- Meal-wise nutrition summaries
- Nutrition history and visualizations
- Improved food matching and spelling recovery
- Additional food and quantity query support
- Online deployment

## 📚 Data Source

NutriBot uses [USDA FoodData Central](https://fdc.nal.usda.gov/) as its food and nutrition data source.

The availability and accuracy of displayed nutrient values depend on the selected record and the information provided by the API.

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
  <em>Making nutrition information easier to explore, one query at a time.</em>
</p>