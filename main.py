import streamlit as st
from prediction_helper import predict

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Health Insurance Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLES ---
# You can inject custom CSS for more advanced styling if needed
# For example, to make metric labels bolder
st.markdown("""
<style>
    [data-testid="stMetricLabel"] {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# --- CATEGORICAL OPTIONS ---
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', 'Unemployed'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}


# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.header("About this App")
    st.info(
        """
        This app predicts annual health insurance premiums using a machine learning model. 
        Fill in your details on the main page to get your personalized cost estimate.
        """
    )
    st.markdown("**Built with:**")
    st.markdown("- Python")
    st.markdown("- Streamlit")
    st.markdown("- Scikit-learn")


# --- MAIN PAGE CONTENT ---
st.title('🩺 Health Insurance Cost Predictor')
st.caption('Enter your details below to get an estimated annual insurance premium.')

# Using st.form to group inputs and the button
with st.form("prediction_form"):
    # Two-column layout for the form
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("##### 👤 Personal Information")
            age = st.slider('Age', min_value=18, max_value=100, value=30, help="Your current age in years.")
            gender = st.selectbox('Gender', categorical_options['Gender'])
            marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
            number_of_dependants = st.slider('Number of Dependants', min_value=0, max_value=20, value=0)

        with st.container(border=True):
            st.markdown("##### ❤️ Health Profile")
            bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])
            smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
            medical_history = st.selectbox('Medical History', categorical_options['Medical History'])
            genetical_risk = st.slider('Genetical Risk', min_value=0, max_value=5, value=0, help="A score representing hereditary health risks.")


    with col2:
        with st.container(border=True):
            st.markdown("##### 💼 Financial & Employment")
            income_lakhs = st.slider('Annual Income (₹ in Lakhs)', min_value=0.0, max_value=200.0, value=10.0, step=0.5)
            employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])
            insurance_plan = st.selectbox('Current Insurance Plan', categorical_options['Insurance Plan'])
            region = st.selectbox('Region', categorical_options['Region'])

    # The submit button for the form
    st.markdown("") # Spacer
    predict_button = st.form_submit_button(
        'Predict My Premium',
        type="primary",
        use_container_width=True
    )


# --- PREDICTION DISPLAY LOGIC ---
if predict_button:
    # Create the dictionary for the model
    input_dict = {
        'Age': age,
        'Number of Dependants': number_of_dependants,
        'Income in Lakhs': income_lakhs,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Marital Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking Status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }

    with st.spinner('🧠 Analyzing your details...'):
        prediction = predict(input_dict)

    st.divider()
    st.success("Here is your estimated annual premium:")

    # Display the result in a metric card within a column for centering
    _, col_metric, _ = st.columns([1, 2, 1])
    with col_metric:
        st.metric(
            label="Predicted Cost",
            value=str(prediction),
            help="This is an estimate. Actual premiums may vary."
        )

    st.warning(
        "**Disclaimer:** This is an estimated cost. Actual premiums may vary based on the insurer and a more detailed assessment.",
        icon="⚠️"
    )

else:
    st.info("Please fill out the form and click 'Predict My Premium' to see your result.", icon="👈")