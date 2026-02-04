# Civil-Engineering-Water-Suite
A comprehensive web-based tool for water quality analysis and water supply scheme design. Features automated WHO/NIS compliance checks and detailed project proposal generation with population and demand forecasting.
# 💧 Civil Engineering Water Suite

A professional-grade web application designed for Civil Engineers and Water Quality Analysts. This tool automates the complex calculations involved in water quality assessment and water supply scheme design.

## 🚀 Key Features

### 1. Multi-Parameter Water Analysis
- **Automated Compliance Checks:** Instantly compares lab results against **WHO Guidelines** and **NIS 554:2015** standards.
- **Smart Diagnostics:** Automatically flags unsafe parameters (e.g., pH, Turbidity, E. Coli, Heavy Metals) and suggests specific treatment solutions (e.g., "Aeration required for Iron removal").
- **PDF Reporting:** Generates a professional "Comprehensive Analysis Report" detailing every parameter, violation, and required corrective action.

### 2. Detailed Proposal Generator
- **Population Forecasting:** Calculates future population using **Geometric Progression** (for Cities) or **Arithmetic Progression** (for Villages) with step-by-step mathematical workings shown.
- **Water Demand Estimation:** Computes Average and Maximum Daily Demand based on per capita consumption and peak factors.
- **Treatment System Design:** Proposes customized treatment process flows (e.g., Aeration → Coagulation → Filtration) based on the specific water source (River, Borehole, or Rainwater).
- **Proposal Export:** Downloads a ready-to-print Project Proposal PDF containing design data, calculations, and technical specifications.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Python)
- **Backend Logic:** Python
- **Report Generation:** FPDF
- **Data Storage:** JSON (Customizable parameter database)

## 📦 Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
