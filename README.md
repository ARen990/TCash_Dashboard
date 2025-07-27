# Hi, My name is ARen 𝄞 .
# Tcash Dashboard

## Description
TCash Dashboard is a web-based data visualization platform built with Streamlit. It allows users to explore and analyze Thai university course and Tuition Fees data with an intuitive and interactive interface.


## Features
- 📊 Interactive Dashboard – Visualize course and university data with dynamic charts (Plotly)

- 🔎 Search & Filter – Quickly find programs by university, faculty, or course name

- 📂 Data Management – Reads and processes data from JSON/CSV files

- 🎨 Custom UI – Styled interface with customized background colors and fonts

## Dataset
The dashboard uses university and course data collected from the TCAS database (https://course.mytcas.com/).
Data is stored in JSON/CSV format in the data/ folder.


## Installation
1. Clone this repository:

```bash
git clone https://github.com/ARen990/miniPROJECT_whatUeat.git
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

For further model modification or retraining:
- `Trainmodelfood.ipynb` (Jupyter Notebook for training and adjusting the model)
- `app.py` (Streamlit script for running the web application)

Ensure TensorFlow and Streamlit are installed:

```bash
pip install tensorflow streamlit numpy pandas
```

## Usage display
1. Run `Dashboard_Tcash.py` using the command:
```bash
streamlit run app.py
```
2. Open a browser and go to `http://localhost:8501`
3. Enter available ingredients (comma-separated), and optionally specify ingredients you dislike or are allergic to.
4. Select the number of recommended dishes.
5. Click to get food recommendations.


## 📬 Contact
- **GitHub:** [ARen990](https://github.com/ARen990)
- **Email:** krittimonp28@gmail.com
- **X:** [Aenijin](https://x.com/Aenijin)

