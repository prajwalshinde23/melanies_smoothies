# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# --- Main App Title ---
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the Fruits You Want in Your Custom Smoothie!"""
)

# --- Smoothie Order Form ---
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the smoothie will be:", name_on_order)

# Get the session and fruit options from Snowflake
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Create the multi-select widget for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# This block only runs if the user has selected at least one ingredient
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    # The "Submit Order" button and its logic are now INSIDE this block
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Check if both name and ingredients are provided
        if name_on_order and ingredients_string:
            my_insert_stmt = f"""
                INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                VALUES ('{ingredients_string}', '{name_on_order}')
            """
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        else:
            st.warning("Please enter a name for the order.")

# --- New Section: Fruityvice Fruit Advice! ---
st.write("---")
st.header("Fruityvice Fruit Advice!")

# Let the user enter a fruit to look up
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')

if st.button('Get Fruit Info'):
    if fruit_choice:
        # Make the API call with the user's choice
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        
        # Check if the request was successful before parsing JSON
        if fruityvice_response.status_code == 200:
            fruityvice_data = fruityvice_response.json()
            # Display the data in a clean table
            st.dataframe(data=fruityvice_data, use_container_width=True)
        else:
            st.error(f"Sorry, we couldn't find information for '{fruit_choice}'.")
    else:
        st.warning("Please enter a fruit to look up.")

