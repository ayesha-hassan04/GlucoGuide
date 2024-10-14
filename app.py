import streamlit as st
import anthropic

api_key = st.secrets["anthropic_api_key"]

# Function to get meal plan from Claude AI
def get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare the user message
    user_message = f"""
    Given the following sugar levels:
    - Fasting Sugar Level: {fasting_sugar} mg/dL
    - Pre-meal Sugar Level: {pre_meal_sugar} mg/dL
    - Post-meal Sugar Level: {post_meal_sugar} mg/dL
    
    Dietary Preference: {dietary_preferences}
    
    Please provide a personalized meal plan that helps manage these sugar levels.
    """

    # Sending request to Claude AI
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.5,  # Adjust temperature for creativity
        messages=[{"role": "user", "content": user_message}]
    )

    # Extract and return the required text from the response
    return response.content.strip()

# Title and description
st.title("Glucuguide")
st.write("""
    Welcome to Glucuguide! This app is designed to help diabetic patients manage their blood sugar levels by providing personalized meal plans based on your sugar level inputs and dietary preferences.
""")

# Sidebar inputs
st.sidebar.header("Enter Details:")

# API key input

# Fasting, pre-meal, and post-meal sugar levels
fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0, max_value=500, value=100)
pre_meal_sugar = st.sidebar.number_input("Pre-meal Sugar Level (mg/dL)", min_value=0, max_value=500, value=100)
post_meal_sugar = st.sidebar.number_input("Post-meal Sugar Level (mg/dL)", min_value=0, max_value=500, value=120)

# Dietary preferences
dietary_preferences = st.sidebar.selectbox(
    "Select Your Dietary Preferences",
    options=["Vegetarian", "Vegan", "Non-Vegetarian", "Gluten-Free", "Low-Carb"]
)

# Button to generate meal plan
if st.sidebar.button("Get Meal Plan"):
    if not api_key:
        st.error("Please enter your API key.")
    else:
        st.write("### Personalized Meal Plan")
        
        # Get meal plan from AI
        meal_plan = get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
        
        st.write(meal_plan)

# Footer
st.write("---")
st.write("Please consult with a healthcare professional before making any dietary changes.")
