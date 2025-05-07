import streamlit as st
import csv

st.set_page_config("Stroke Data Analysis", layout="wide")
st.title("\U0001F9E0 Stroke Data Analysis and Reporting")

# Load CSV
uploaded_file = st.file_uploader("Upload Stroke Dataset (CSV)", type=["csv"])

def read_csv_basic(file):
    lines = file.read().decode('utf-8').splitlines()
    reader = csv.reader(lines)
    headers = next(reader)
    data = [dict(zip(headers, row)) for row in reader]
    return headers, data

def save_csv(name, headers, rows):
    with open(name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def get_column(data, col, condition=lambda x: True):
    return [float(row[col]) for row in data if col in row and row[col] and condition(row)]

def basic_stats(values):
    if not values:
        return {"Average": None, "Median": None, "Mode": None}
    avg = sum(values) / len(values)
    sorted_vals = sorted(values)
    n = len(values)
    median = sorted_vals[n//2] if n % 2 == 1 else (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
    mode = max(set(values), key=values.count)
    return {"Average": avg, "Median": median, "Mode": mode}

if uploaded_file:
    headers, data = read_csv_basic(uploaded_file)
    st.success("Data loaded. Select an analysis from the sidebar.")

    st.sidebar.header("Select Analysis")
    option = st.sidebar.selectbox("Choose function", [
        "i. Smoked + Hypertension + Stroke",
        "ii. Heart Disease + Stroke",
        "iii. Hypertension by Gender",
        "iv. Smoking vs Stroke",
        "v. Urban vs Rural + Stroke",
        "xi. Sleep Hours vs Stroke"
    ])

    if option == "i. Smoked + Hypertension + Stroke":
        vals = get_column(data, "Age", lambda x: x['Hypertension'] == '1' and x['Stroke'] == '1' and x['Smoking Status'].lower() != 'never smoked')
        stats = basic_stats(vals)
        st.write(stats)

    elif option == "ii. Heart Disease + Stroke":
        age_vals = get_column(data, "Age", lambda x: x['Heart Disease'] == '1' and x['Stroke'] == '1')
        glucose_vals = get_column(data, "Average Glucose Level", lambda x: x['Heart Disease'] == '1' and x['Stroke'] == '1')
        st.write("Age Stats:", basic_stats(age_vals))
        st.write("Average Glucose:", sum(glucose_vals) / len(glucose_vals) if glucose_vals else None)

    elif option == "iii. Hypertension by Gender":
        for g in set(row['Gender'] for row in data):
            for h in ['0', '1']:
                vals = get_column(data, "Age", lambda x: x['Gender'] == g and x['Hypertension'] == h and x['Stroke'] == '1')
                st.write(f"Gender: {g}, Hypertension: {h}", basic_stats(vals))

    elif option == "iv. Smoking vs Stroke":
        for s in set(row['Smoking Status'] for row in data):
            for stroke in ['0', '1']:
                vals = get_column(data, "Age", lambda x: x['Smoking Status'] == s and x['Stroke'] == stroke)
                st.write(f"Smoking: {s}, Stroke: {stroke}", basic_stats(vals))

    elif option == "v. Urban vs Rural + Stroke":
        for area in set(row['Residence Type'] for row in data):
            vals = get_column(data, "Age", lambda x: x['Residence Type'] == area and x['Stroke'] == '1')
            st.write(f"Residence: {area}", basic_stats(vals))

    elif option == "xi. Sleep Hours vs Stroke":
        for s in ['0', '1']:
            vals = get_column(data, "Sleep Hours", lambda x: x['Stroke'] == s)
            avg_sleep = sum(vals) / len(vals) if vals else None
            st.write(f"Stroke: {s}, Average Sleep Hours: {avg_sleep}")
else:
    st.warning("Upload a CSV file to start analysis.")
