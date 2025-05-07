import streamlit as st
import csv

# Change background color and styling
st.markdown(
    '''
    <style>
    body {
        background-color: #e8f4f8;
        color: #333333;
        font-family: Arial, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #d1e7ec;
    }
    .stButton button {
        background-color: #4caf50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #f2f2f2;
    }
    </style>
    '''
    , unsafe_allow_html=True
)

# Load dataset without Pandas
def load_dataset(uploaded_file):
    data = []
    uploaded_file.seek(0)
    reader = csv.reader(uploaded_file.read().decode("utf-8").splitlines())
    headers = next(reader)
    for row in reader:
        data.append(dict(zip(headers, row)))
    return headers, data

# Filter data
def get_filtered_data(data, age_range, glucose_range, hypertension, smoking, dietary, alcohol, stress, sleep, family_history, education, income, region):
    filtered_data = []
    for row in data:
        age = int(row['Age'])
        glucose = float(row['Average Glucose Level'])
        sleep_hours = float(row['Sleep Hours'])
        if (age_range[0] <= age <= age_range[1] and 
            glucose_range[0] <= glucose <= glucose_range[1] and
            (row['Hypertension'] == hypertension or hypertension == 'All') and
            (row['Smoking Status'] == smoking or smoking == 'All') and
            (row['Dietary Habits'] == dietary or dietary == 'All') and
            (row['Alcohol Consumption'] == alcohol or alcohol == 'All') and
            (row['Chronic Stress'] == stress or stress == 'All') and
            (sleep_hours >= sleep[0] and sleep_hours <= sleep[1]) and
            (row['Family History of Stroke'] == family_history or family_history == 'All') and
            (row['Education Level'] == education or education == 'All') and
            (row['Income Level'] == income or income == 'All') and
            (row['Region'] == region or region == 'All')):
            filtered_data.append(row)
    return filtered_data

st.title("Enhanced Stroke Data Analytics Dashboard")
uploaded_file = st.file_uploader("Upload Stroke Dataset (CSV)", type=["csv"])

if uploaded_file:
    headers, data = load_dataset(uploaded_file)
    st.sidebar.header("Filter Data")
    age_range = st.sidebar.slider("Select Age Range", 0, 100, (30, 60))
    glucose_range = st.sidebar.slider("Select Glucose Level Range", 50.0, 300.0, (80.0, 180.0))
    hypertension = st.sidebar.selectbox("Hypertension", ['All', '0', '1'])
    smoking = st.sidebar.selectbox("Smoking Status", ['All', 'Formerly smoked', 'Never smoked', 'Unknown'])
    dietary = st.sidebar.selectbox("Dietary Habits", ['All', 'Vegetarian', 'Non-Vegetarian', 'Mixed'])
    alcohol = st.sidebar.selectbox("Alcohol Consumption", ['All', '0', '1'])
    stress = st.sidebar.selectbox("Chronic Stress", ['All', '0', '1'])
    sleep = st.sidebar.slider("Sleep Hours", 0.0, 12.0, (6.0, 8.0))
    family_history = st.sidebar.selectbox("Family History of Stroke", ['All', '0', '1'])
    education = st.sidebar.selectbox("Education Level", ['All', 'Tertiary', 'Secondary', 'Primary', 'No education'])
    income = st.sidebar.selectbox("Income Level", ['All', 'Low', 'Medium', 'High'])
    region = st.sidebar.selectbox("Region", ['All', 'East', 'West', 'North', 'South'])
    filtered_results = get_filtered_data(data, age_range, glucose_range, hypertension, smoking, dietary, alcohol, stress, sleep, family_history, education, income, region)
    st.write(f"Showing {len(filtered_results)} results")
    st.dataframe(filtered_results)
    if st.button("Save Results to CSV"):
        with open("filtered_results.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(filtered_results)
        st.success("Results saved as filtered_results.csv")

