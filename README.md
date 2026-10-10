# 🥗 NutriBot — Food Nutrition Chatbot Using NLP

<p align="center">
  <strong>Making food nutrition information simple, accessible, and easy to explore.</strong>
  <br>
  A Python-based food nutrition chatbot using Natural Language Processing and USDA FoodData Central.
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
- [Objectives](#-objectives)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Methodology](#-methodology)
- [Results and Visualization](#-results-and-visualization)
- [Application Screenshots](#-application-screenshots)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Running the Application](#-running-the-application)
- [Testing](#-testing)
- [Limitations](#️-limitations)
- [Future Enhancements](#-future-enhancements)
- [Data Source](#-data-source)
- [Author and Connect](#-author-and-connect)

---

## 📌 About the Project

**NutriBot** is a food nutrition chatbot developed using Python, Natural Language Processing (NLP), and Streamlit. It helps users explore nutritional information by entering food names and supported food-related queries.

The application connects to the **USDA FoodData Central API** to search food records and retrieve available nutrient information. It incorporates food matching, spelling-error handling, and quantity-based nutrition analysis for supported inputs.

NutriBot combines query processing, external nutrition data retrieval, food matching, nutrition calculations, and an interactive web interface in one application.

## 🎯 Objectives

The main objectives of NutriBot are to:

- Provide an interactive interface for exploring food nutrition information.
- Process supported food-related queries written in natural language.
- Retrieve food records and nutrients from USDA FoodData Central.
- Improve food matching when users enter spelling mistakes.
- Calculate nutrition values for supported quantities and portions.
- Present retrieved information in an understandable format.

## ✨ Features

### 💬 Natural Language Query Processing

Processes supported food-related inputs and identifies information needed for nutrition lookup.

### 🔍 Food Search and Matching

Searches USDA FoodData Central and ranks candidate food records to identify a suitable match.

### ✏️ Spelling Error Handling

Uses generic text-processing strategies to attempt recovery from common spelling mistakes without depending exclusively on a fixed list of food-name corrections.

### 🥦 Nutrition Information Retrieval

Retrieves available nutritional information, which may include:

- Energy and calories
- Protein
- Carbohydrates
- Total fat
- Other nutrients provided by the selected record

### ⚖️ Quantity-Based Nutrition Calculation

For supported inputs, interprets a food quantity or portion and calculates nutrition values based on the selected food record.

### 🖥️ Interactive Web Interface

Provides a Streamlit interface where users can enter food queries and view nutrition information.

---

## 🏗️ System Architecture

The system architecture illustrates how NutriBot processes a user query, identifies the requested food and quantity, retrieves nutrition information, calculates nutrient values, and presents the response.

![NutriBot System Architecture](docs/images/system-architecture.png)

### 🧩 Architecture Components

**1. User Interface**

Accepts food names and supported food-related queries through the Streamlit application.

**2. NLP Processing**

Processes the input and helps identify the food-related information required by the application.

**3. Food Matching**

Searches and ranks candidate food records using the application's matching logic.

**4. Nutrition Database Module**

Communicates with USDA FoodData Central to retrieve food records and detailed nutrient information.

**5. Nutrition Calculation**

Processes available nutrient values for supported quantities and portions.

**6. Response Generation**

Formats the processed nutrition information for display to the user.

The processing path depends on the query, the application's logic, and the information returned by the API.

## ⚙️ Methodology

NutriBot follows a sequence of processing stages to convert a food query into a nutrition response.

### 📝 Input Processing

The user enters a food name or supported nutrition query through the application.

### 🔎 Food Identification

The application processes the input and searches for relevant food records. Spelling recovery and similarity-based matching help identify potential candidates.

### 🌐 Nutrition Data Retrieval

The selected food record is retrieved through the USDA FoodData Central API.

### 🧪 Nutrient Extraction

Available nutrient values are extracted from the detailed food record returned by the API.

### 🧮 Quantity-Based Calculation

When a supported quantity or portion is provided, the application calculates the corresponding nutrition values using the selected food record.

### 💬 Response Presentation

The processed nutrition information is formatted and displayed through the Streamlit interface.

---

## 📊 Results and Visualization

The results interface presents nutrition information retrieved and processed by NutriBot. Displayed values depend on the selected food record, the requested quantity, and the nutrient data available from USDA FoodData Central.

### 🥗 Nutrition Metric Analysis

The application can display available nutrition metrics, including:

- Energy
- Calories
- Protein
- Carbohydrates
- Total fat
- Other available nutrients

Not every USDA food record contains the same nutrients, so the information displayed may vary between foods.

### ⚖️ Quantity-Based Nutrition Analysis

For supported inputs, NutriBot uses the interpreted quantity or portion to calculate nutrition values.

Example query formats include:

```text
chicken
2 bananas
150 grams of chicken
```

The results depend on the matched food record, the interpreted quantity, and the available nutrient data.

### 🔍 Food Matching and Spelling Recovery

The food-matching process evaluates candidate records using text similarity and other selection criteria.

Spelling recovery attempts to identify useful alternatives for mistyped food names. It does not guarantee that every misspelled query will produce the intended match.

### 📋 Interpretation

Nutrition results should be interpreted in the context of:

- The selected USDA food record
- Food preparation and description
- The requested quantity or portion
- Nutrients available in the selected record
- The accuracy of food and quantity matching

Nutrition values can vary between food records and preparation methods. The results provide nutrition information for exploration and are not a substitute for professional medical advice.

---

## 📸 Application Screenshots

The following screenshots demonstrate the main interface and nutrition analysis features of NutriBot.

### 🏠 Dashboard

The Dashboard provides the main interface for entering food queries and interacting with the chatbot.

![NutriBot Dashboard](results/screenshots/Dashboard.png)

### 📊 Nutrition Results

The Nutrition Results view presents an example of the nutrition information returned by the application.

The displayed values depend on the selected food record and the available nutrient data.

![Nutrition Results](results/screenshots/Nutrition%20Results.png)

### 🥗 Full Nutrition Details

The Full Nutrition Details view provides a detailed presentation of the available nutritional information for a selected food.

![Full Nutrition Details](results/screenshots/Full%20Details.png)

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Natural Language Processing | Query processing |
| USDA FoodData Central API | Food and nutrition data retrieval |
| Requests | HTTP communication with the API |
| python-dotenv | Environment variable management |
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
├── docs/
│   └── images/
│       └── system-architecture.png
├── results/
│   └── screenshots/
│       ├── Dashboard.png
│       ├── Nutrition Results.png
│       └── Full Details.png
└── README.md
```

## 🚀 Installation and Setup

### 📋 Prerequisites

Before running NutriBot, make sure you have:

- Python 3.12 or a compatible version
- Git
- A USDA FoodData Central API key
- An internet connection for API requests

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/KeerthiThokala029/food-nutrition-chatbot.git
cd food-nutrition-chatbot
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the API Key

Create a `.env` file in the project's root directory and add your USDA API key:

```env
USDA_API_KEY=your_api_key_here
```

Obtain an API key from the [USDA FoodData Central API Guide](https://fdc.nal.usda.gov/api-guide/).

**Security:** Replace the placeholder with your own key. Keep the actual key private and do not commit the `.env` file to GitHub.

## ▶️ Running the Application

After installing the dependencies and configuring the API key, run:

```bash
streamlit run app.py
```

Alternatively, Windows users can launch `RUN_NUTRIBOT.bat` from the project directory.

Streamlit will display a local URL in the terminal that you can open in your browser.

## 🧪 Testing

The project includes test files for checking different components.

| Test File | Purpose |
|---|---|
| `test_api.py` | API-related checks |
| `test_matcher.py` | Food-matching checks |
| `test_nlp.py` | NLP processing checks |

To run a test, activate your virtual environment and execute the relevant file. For example:

```bash
python test_matcher.py
```

Run tests after installing the required dependencies and configuring any necessary environment variables.

## ⚠️ Limitations

- Results depend on the food records available through USDA FoodData Central.
- Nutrient availability varies between food records.
- Spelling recovery and food matching may not identify the intended food in every case.
- Quantity and portion calculations depend on correct input interpretation and supported units.
- An internet connection and a valid API key are required for live USDA API requests.

## 🔮 Future Enhancements

Potential future improvements include:

- Meal-wise nutrition summaries
- Nutrition history and visualizations
- Improved food matching and spelling recovery
- Additional food and quantity query support
- Improved nutrition comparisons
- Online deployment

## 📚 Data Source

NutriBot uses [USDA FoodData Central](https://fdc.nal.usda.gov/) as its external food and nutrition data source.

The API provides food records and nutrient information. The nutrients available depend on the specific record selected.

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