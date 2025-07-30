# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the Fruits You Want in Your Custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on smoothie will be:", name_on_order)

# Connect to Snowflake and get fruit options
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'),col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()

# Create the multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections= 5
)

# This block only runs if the user has selected at least one ingredient
if ingredients_list:
    ingredients_string = ''

    # This loop displays nutrition info for each selected fruit
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        try:
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
            st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        except requests.exceptions.RequestException:
            st.error(f"Could not retrieve data for {fruit_chosen}.")

    # --- Order Submission Logic ---
    # This logic is now correctly placed inside the if-block
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                           VALUES ('{ingredients_string.strip()}', '{name_on_order}')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if name_on_order and ingredients_string:
            session.sql( my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        else:
            st.warning("Please enter a name for the order.")
