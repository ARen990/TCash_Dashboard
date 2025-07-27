# Hi, My name is ARen 𝄞 .
# Tcash Dashboard

## Description  
TCash Dashboard is a web-based data visualization platform built with Streamlit.  
It allows users to explore and analyze Thai university course and tuition fees data with an intuitive and interactive interface.  

## Features  
- 📊 **Interactive Dashboard** – Visualize course and university data with dynamic charts (Plotly)  
- 🔎 **Search & Filter** – Quickly find programs by university, faculty, or course name  
- 📂 **Data Management** – Reads and processes data from JSON/CSV files  
- 🎨 **Custom UI** – Styled interface with customized background colors and fonts 

## Dataset  
The dashboard uses university and course data collected from the [TCAS database](https://course.mytcas.com/).  
Data is stored in JSON/CSV format in the `data/` folder.  

## Installation
1. Clone this repository:

```bash
git clone https://github.com/ARen990/TCash_Dashboard.git
cd TCash_Dashboard
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```


### Additional Code Information

`Dashboard_Tcash.py`
The entry point for the dashboard. It loads data, handles layout (menus/pages), and renders all visualizations using Streamlit and Plotly.

`data/ folder`
Contains input data files, typically exported from the TCAS database or scraping pipeline. You can add/update files here for use in the dashboard.

`requirements.txt`
has streamlit, pandas, plotly, streamlit-option-menu


## Usage display
1. Run the application:

   ```bash
   streamlit run app.py
   ```
2. Open a browser and go to `http://localhost:8501`
3. Use the menu to navigate through different views:

   * Filter universities and courses
   * View tuition fees and statistics
   * Analyze data with interactive charts

## Project Structure

```
TCash_Dashboard/
├── app.py                 # Main Streamlit app
├── data/                  # Input data (JSON/CSV)
├── requirements.txt       # Dependencies
└── README.md
```


## 📬 Contact
- **GitHub:** [ARen990](https://github.com/ARen990)
- **Email:** krittimonp28@gmail.com
- **X:** [Aenijin](https://x.com/Aenijin)

