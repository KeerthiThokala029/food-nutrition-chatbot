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
  <img src="https://img.shields.io/badge/USDA-Food%20Nutrition-228B22?style=for-the-badge" alt="USDA FoodData Central">
</p>

---

## 📑 Table of Contents

- [About the Project](#-about-the-project)
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
- [Author](#-author)

## 📌 About the Project

**NutriBot** is a food nutrition chatbot developed using Python, Natural Language Processing (NLP), and Streamlit. It allows users to enter food names and food-related questions in natural language and explore nutritional information.

The application connects to the **USDA FoodData Central API** to retrieve food records and nutrition data. It includes food matching, spelling-error handling, and quantity-based analysis for supported inputs.

The project aims to make nutrition information easier to access through a simple, interactive chatbot interface.

## ✨ Features

- **Natural Language Queries:** Enter food-related questions using everyday language.
- **Food Search:** Search food records through the USDA FoodData Central API.
- **Spelling Error Handling:** Attempt to handle common typing mistakes in food names.
- **Nutrition Analysis:** Retrieve calories, protein, carbohydrates, fats, and other available nutrients.
- **Quantity-Based Analysis:** Calculate nutrition for supported quantities and portions.
- **Interactive Interface:** Explore food nutrition information through a Streamlit web application.

## 📸 Application Screenshots

### 🏠 1. Dashboard

The main interface for entering food queries and interacting with NutriBot.

![NutriBot Dashboard](results/screenshots/Dashboard.png)

### 📊 2. Nutrition Results

An overview of the nutrition information returned by the chatbot.

![Nutrition Results](results/screenshots/Nutrition%20Results.png)

### 🥗 3. Full Nutrition Details

A detailed view of the available nutritional information for a selected food.

![Full Nutrition Details](results/screenshots/Full%20Details.png)

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

NutriBot processes a food query and follows these general steps:

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
| Streamlit | Interactive web interface |
| Natural Language Processing | Query processing |
| USDA FoodData Central API | Food and nutrition data retrieval |
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

Before running the project, make sure you have:

- Python 3.12 or a compatible version
- Git
- A USDA FoodData Central API key

### 1. Clone the Repository

Open a terminal and run:

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

Create a `.env` file in the root directory of the project and add your USDA API key:

```env
USDA_API_KEY=your_api_key_here
```

You can obtain an API key through the [USDA FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/).

**Security note:** Replace `your_api_key_here` with your own key. Never publish your actual API key or commit your `.env` file to GitHub.

### 5. Run the Application

Start NutriBot with:

```bash
streamlit run app.py
```

Alternatively, on Windows, run the `RUN_NUTRIBOT.bat` launcher from the project folder.

## 🧪 Testing

The project includes the following test files:

- `test_api.py` — API-related checks
- `test_matcher.py` — food-matching checks
- `test_nlp.py` — NLP processing checks

Run the relevant test file from your activated virtual environment. For example:

```bash
python test_matcher.py
```

## 🔮 Future Enhancements

- Meal-wise nutrition summaries
- Nutrition history and visualizations
- Improved food recognition and matching
- Additional chatbot capabilities
- Online deployment

## 📚 Data Source

NutriBot uses [USDA FoodData Central](https://fdc.nal.usda.gov/) as its food and nutrition data source.

The available nutritional information depends on the USDA record selected and the nutrients provided for that record.

## 👩‍💻 Author

**Keerthi Thokala**

[GitHub Profile](https://github.com/KeerthiThokala029)

**Project Repository:** [NutriBot — Food Nutrition Chatbot Using NLP](https://github.com/KeerthiThokala029/food-nutrition-chatbot)

---

<p align="center">
  <strong>🥗 NutriBot</strong>
  <br>
  <em>Making nutrition information easier to explore, one query at a time.</em>
</p>