# 🥗 NutriBot — Food Nutrition Chatbot Using NLP

<p align="center">
  <strong>An NLP-powered chatbot for exploring food nutrition information.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-red?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/NLP-Query%20Processing-purple" alt="NLP">
  <img src="https://img.shields.io/badge/Data-USDA%20FoodData%20Central-green" alt="USDA FoodData Central">
</p>

## 📌 About NutriBot

**NutriBot** is a food nutrition chatbot developed using Python, Natural Language Processing (NLP), and Streamlit. It allows users to enter food names and food-related questions in natural language and explore nutritional information.

The application connects to the **USDA FoodData Central API** to retrieve food records and provide nutrition information. It also includes food matching, spelling-error handling, and quantity-based analysis for supported inputs.

## 📑 Table of Contents

- [Features](#-features)
- [Application Screenshots](#-application-screenshots)
- [Example Queries](#-example-queries)
- [How It Works](#️-how-it-works)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Data Source](#-data-source)
- [Author](#️-author)

## ✨ Features

- **Natural Language Queries:** Enter food-related questions using everyday language.
- **Food Search:** Search food records through USDA FoodData Central.
- **Spelling Error Handling:** Attempt to handle common typing mistakes in food names.
- **Nutrition Analysis:** Retrieve calories, protein, carbohydrates, fats, and other available nutrients.
- **Quantity-Based Analysis:** Calculate nutrition for supported quantities and portions.
- **Interactive Interface:** Explore nutrition information through a Streamlit web application.

## 📸 Application Screenshots

### 🏠 1. NutriBot Dashboard

The main interface for entering food queries and interacting with the chatbot.

![NutriBot Dashboard](results/screenshots/Dashboard.png)

### 🥗 2. Full Nutrition Details

A detailed view of the nutritional information returned for a selected food.

![Full Nutrition Details](results/screenshots/Full%20Details.png)

### 📊 3. Nutrition Results

An example of the nutrition analysis displayed by the application.

![Nutrition Results](results/screenshots/Nutrition%20Results.png)

## 💬 Example Queries

| User Query | Purpose |
|---|---|
| `chicken` | Search for a matching food record |
| `2 bananas` | Analyze a supported food quantity |
| `I ate 150 grams of chicken` | Request nutrition for a specified quantity |
| `How much protein is in chicken?` | Ask about a specific nutrient |
| `brocolli` | Test spelling-error handling |

Actual results depend on the selected food record, available USDA data, and the application's supported quantity handling.

## ⚙️ How It Works

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
Nutrition Data Processing
       |
       v
Chatbot Response
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| NLP | Natural-language query processing |
| USDA FoodData Central API | Nutrition data retrieval |
| Requests | API communication |
| python-dotenv | Environment variable management |

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
├── results/
│   └── screenshots/
│       ├── Dashboard.png
│       ├── Full Details.png
│       └── Nutrition Results.png
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

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API Key

Create a `.env` file in the project root and add your own API key:

```env
USDA_API_KEY=your_api_key_here
```

Get an API key from the [USDA FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/).

**Security:** Keep your actual API key private. Do not commit your `.env` file to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

On Windows, you can also start the application using `RUN_NUTRIBOT.bat`.

## 🧪 Testing

The project includes the following test files:

- `test_api.py` — API-related checks
- `test_matcher.py` — food-matching checks
- `test_nlp.py` — NLP processing checks

Run the relevant test files from your activated virtual environment.

## 🔮 Future Enhancements

- Meal-wise nutrition summaries
- Nutrition history and visualizations
- Improved food recognition and matching
- Additional user-interface improvements
- Online deployment

## 📚 Data Source

Nutrition data is retrieved from [USDA FoodData Central](https://fdc.nal.usda.gov/).

## 👩‍💻 Author

**Keerthi Thokala**

[GitHub Profile](https://github.com/KeerthiThokala029)

---

<p align="center">
  <strong>🥗 NutriBot</strong><br>
  <em>Making nutrition information easier to explore, one query at a time.</em>
</p>