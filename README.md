# Liquidity Vision 
**ML-powered cash flow forecasting system.**

## Overview
This project solves the problem of manual cash flow tracking by automating the process in seconds. It uses Machine Learning to predict the next 6 months of liquidity and provides an early warning system to alert managers before potential cash shortages occur.

## Tech Stack
- **Backend:** Python (Flask, Pandas, Scikit-learn, Prophet)
- **Frontend:** HTML5, CSS3, JavaScript (Chart.js)

## Project Structure
To run this project, ensure your files are organized as follows:
- `liquidity_vision_local.py` (The Python Backend)
- `LiquidityVision_local.html` (The Frontend Dashboard)
- `requirements.txt` (List of necessary libraries)

## How to Run
1. **Install Dependencies:**
   Open your terminal and run:
   ```bash
   pip install -r requirements.txt
 2.  **Start the Backend:**
Run the Python file to start the Flask server:

Bash
python liquidity_vision_local.py
Launch the Dashboard:
Simply double-click LiquidityVision_local.html to open it in your browser and view the interactive charts.

**Core Features**
AI Forecasting: Analyzes historical trends to predict future inflows and outflows.

Interactive Visuals: Dynamic charts that update based on user input.

Scenario Analysis: Adjust interest rates via a slider to see real-time impacts on liquidity.

Smart Alerts: Automated system to detect and warn about potential cash deficits.
