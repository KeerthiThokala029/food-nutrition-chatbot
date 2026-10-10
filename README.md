# 🥗 NutriBot — Food Nutrition Chatbot Using NLP

<p align="center">
  <strong>An NLP-powered chatbot for exploring food nutrition information.</strong>
</p>

<p align="center">
  ![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
  ![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
  ![USDA](https://img.shields.io/badge/Data-USDA%20FoodData%20Central-green)
</p>

## 📌 About the Project

NutriBot is a food nutrition chatbot developed using Python, Natural Language Processing (NLP), and Streamlit. It allows users to enter food-related queries in natural language and retrieve nutritional information through the USDA FoodData Central API.

The application combines food search, spelling correction, and quantity-based analysis for supported inputs in a simple, interactive interface.

## 📑 Table of Contents

- [✨ Features](#-features)
- [📸 Application Screenshots](#-application-screenshots)
- [⚙️ How It Works](#️-how-it-works)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Installation and Setup](#-installation-and-setup)
- [📂 Project Structure](#-project-structure)
- [🔮 Future Enhancements](#-future-enhancements)
- [📚 Data Source](#-data-source)
- [👩‍💻 Author](#-author)

## ✨ Features

- 💬 **Natural Language Queries** — process everyday food-related questions.
- 🔍 **Food Search** — find relevant food records using the USDA API.
- ✏️ **Spelling Correction** — handle common food-name typing errors.
- 🥗 **Nutrition Analysis** — display calories, protein, carbohydrates, fats, and other available nutrients.
- ⚖️ **Quantity-Based Analysis** — calculate nutrition for supported quantities and portions.
- 🖥️ **Interactive Interface** — explore nutrition information through Streamlit.

## 📸 Application Screenshots

### 🏠 Dashboard

The main interface for interacting with NutriBot.

![NutriBot Dashboard](results/screenshots/Dashboard.png)

### 📊 Nutrition Results

An example of the application's nutrition analysis output.

![Nutrition Results](results/screenshots/Nutrition%20Results.pngNutrition%20Results.png)

### 🥗 Full Nutrition Details

A detailed view of the nutrition information returned by the application.

![Full Nutrition Details](results/screenshots/Full%20Details.png)
## ⚙️ How It Works

```text
💬 User Query
     ↓
🧠 NLP Processing
     ↓
🔍 Food and Quantity Matching
     ↓
🌐 USDA FoodData Central API
     ↓
🧮 Nutrition Processing
     ↓
📊 Chatbot Response
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Application logic |
| 🎨 Streamlit | Web interface |
| 🧠 NLP | Query processing |
| 🌐 USDA FoodData Central API | Nutrition data retrieval |
| 🔗 Requests | API communication |
| 🔐 python-dotenv | Environment configuration |

## 🚀 Installation and Setup

### Prerequisites

- Python 3.12 or a compatible version
- Git
- USDA FoodData Central API key

### 1. Clone the repository

```bash
git clone https://github.com/KeerthiThokala029/food-nutrition-chatbot.git
cd food-nutrition-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
USDA_API_KEY=your_api_key_here
```

Get your API key from the [USDA FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/).

🔒 Keep your API key private. Do not upload your `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Alternatively, launch `RUN_NUTRIBOT.bat` on Windows.

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
│   ├── Dashboard.png
│   ├── Full Details.png
│   └── Nutrition Results.png
└── README.md
```

## 🔮 Future Enhancements

- 📅 Meal-wise nutrition summaries
- 📈 Nutrition history and visualizations
- 🔎 Improved food matching
- ☁️ Online deployment

## 📚 Data Source

Nutrition information is retrieved from [USDA FoodData Central](https://fdc.nal.usda.gov/).

## 👩‍💻 Author

**Keerthi Thokala**

[GitHub Profile](https://github.com/KeerthiThokala029)

---

<p align="center">
  🥗 <strong>NutriBot</strong><br>
  <em>Making nutrition information easier to explore.</em>
</p>