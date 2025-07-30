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
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

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
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

if smoothiefroot_response.status_code == 200:
    # If successful, parse the JSON and display it in a nice table
    fruityvice_data = smoothiefroot_response.json()
    st.dataframe(data=fruityvice_data, use_container_width=True)
else:
    # If not successful, show a helpful error message instead of crashing
    st.error("Could not retrieve data from the API.")
    st.write("Status Code:", smoothiefroot_response.status_code)
    st.write("Response Body:", smoothiefroot_response.text) # This shows what the server actually sent back
    

