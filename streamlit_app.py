# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the Fruits You Want in Your Custom Smoothie!
    """
)



name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections= 5
)
if ingredients_list:
    

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)


    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string.strip()}', '{name_on_order}')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    # Moved the button and its logic inside the if block to prevent errors
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql( my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
# --- SmoothieFroot Fruit Advice! ---
st.write("---")
st.header("SmoothieFroot Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.write("Please select a fruit to get information.")
    else:
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choice)
        # Check the status code before trying to parse the JSON
        if smoothiefroot_response.status_code == 200:
             # Use st.dataframe to display the JSON in a structured table
             smoothiefroot_data = smoothiefroot_response.json()
             st.dataframe(data=smoothiefroot_data, use_container_width=True)
        else:
             st.error(f"Could not retrieve data for '{fruit_choice}'. Please check the spelling.")

except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while trying to contact the API: {e}")

