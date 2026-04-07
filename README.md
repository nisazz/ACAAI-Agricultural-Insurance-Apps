# 🌾 ACAAI – Automated Compensation Assessment for Agricultural Insurance

## 📌 Overview
ACAAI (Automated Compensation Assessment for Agricultural Insurance) is a data-driven system designed to modernize agricultural insurance by automating claim validation using weather index data.

Traditional agricultural insurance systems rely heavily on manual field assessments, resulting in delays, high operational costs, and limited transparency. This project introduces a **rule-based automated system** that leverages rainfall data to improve efficiency, accuracy, and accessibility for farmers.

---

## 🚀 Key Features
- 📊 Processed and analyzed **10 years of rainfall data**
- ⚙️ Built **Python-based ETL pipelines** for data cleaning and transformation
- 🌧️ Implemented **Rainfall Anomaly Index (RAI)** and **Standardised Precipitation Index (SPI)**
- 🤖 Automated **insurance claim validation using rule-based logic**
- 🔗 Integrated **real-time and historical weather data via API**
- 📱 Designed for integration with a **mobile application**

---

## 🧠 Problem Statement
Agricultural insurance systems in Malaysia face several challenges:
- Manual and time-consuming claim validation processes  
- High operational and transaction costs  
- Delays in compensation payouts  
- Lack of transparency in decision-making  

These issues reduce the effectiveness of insurance in protecting farmers against climate-related risks.

---

## 💡 Solution
This project introduces a **weather index-based insurance model** that:
- Uses rainfall indices (RAI & SPI) to determine compensation eligibility  
- Automates claim assessment without field inspection  
- Reduces human error and bias  
- Speeds up compensation for farmers  

---

## 🏗️ System Architecture
<img width="400" height="315" alt="image" src="https://github.com/user-attachments/assets/06eca09e-e9bd-4d9f-baca-9602cc4f61de" />

## Compensation Assessment Flowchart
<img width="371" height="835" alt="image" src="https://github.com/user-attachments/assets/0c231fd6-1785-4073-9d18-6ba47ddee596" />


---

## 📊 Data Pipeline
The data pipeline includes:
- Data ingestion from API and historical datasets  
- Data cleaning (handling missing values, normalization)  
- Feature engineering (RAI & SPI calculations)  
- Data storage and integration with application backend  

---

## 🧮 Index Calculations
- **RAI (Rainfall Anomaly Index)**: Measures deviation of rainfall from normal conditions  
- **SPI (Standardised Precipitation Index)**: Identifies drought and excessive rainfall conditions  

These indices are used to trigger insurance claims  

---

## 🛠️ Tech Stack

### 📱 Frontend (Mobile Application)
- **React Native (JavaScript)**  
  Used to develop a cross-platform mobile application (iOS & Android) with a user-friendly interface.  
  Modules implemented include:
  - User Authentication (registration & login)
  - Main Menu Dashboard
  - Policy Management (purchase, claim, appeal)
  - Support & Inquiry features

### ⚙️ Backend & API
- **Flask (Python)**  
  Lightweight backend framework used to:
  - Process weather data
  - Compute RAI & SPI indices
  - Implement rule-based claim validation
  - Expose RESTful APIs for frontend integration

### 📊 Data Engineering & Processing
- **Python (pandas, NumPy, Matplotlib)**  
  Used for:
  - Building ETL pipelines (Extract, Transform, Load)
  - Data cleaning and preprocessing
  - Rainfall data analysis
  - RAI & SPI calculations
  - Data visualization during development

### ☁️ Database & Authentication
- **Firebase (Google Cloud)**  
  Used as the backend-as-a-service for:
  - User authentication and account management
  - Real-time database for storing user data, policies, and claims
  - Application hosting and integration support

### 🌦️ Data Source
- **Open-Meteo API**  
  Provides:
  - Historical rainfall data (10 years) for baseline modeling
  - Recent rainfall data (30 days) for claim validation
  - Reliable, real-time weather data via API integration

### 🧑‍💻 Development Tools
- **Visual Studio Code**  
  Primary development environment for:
  - Python backend development
  - React Native mobile application
  - API integration and testing

### 📌 Methodology
- **Solo Scrum (Agile Development)**  
  Development was structured into multiple sprints:
  - UI Development
  - User Account Module
  - Main Menu Module
  - Policy Module
  - Support Module
  - Assessment Module  

  Each sprint focused on delivering a functional component within a 2-week cycle.
---

## 📈 Impact
- ⏱️ Faster insurance claim processing  
- 💰 Reduced operational costs  
- 🔍 Improved transparency and fairness  
- 🌱 Supports farmers facing climate risks  

---

## 🔮 Future Improvements
- Machine learning models for predictive risk analysis  
- Integration with satellite or IoT weather data  
- Expansion to additional climate variables (temperature, humidity)  
- Full deployment of mobile application

---

## Youtube Video
Link: https://youtu.be/Bmiec-TPJes

---

## 👩‍💻 Author
**Hanisah Zainuddin**  

