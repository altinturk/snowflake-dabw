import streamlit

streamlit.title("Das Ristorante")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Banana'])
# alternative code: 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.Fruit))

# show only selected fruits
fruits_to_show = my_fruit_list.loc[fruits_selected]
#reference for loc - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

# now I parameterized the user input and put the parameter to the api call
# so this way i can show only what the user needed 
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


#let's call Fruityvice API from Our Streamlit App!
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
# if you don't add json fn at the end, it'll return rq status = "200"
##streamlit.text(fruityvice_response.json())

# asssign json to a param 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# push param'd json to streamlit table and remove the pure json response afew lines above.
streamlit.dataframe(fruityvice_normalized)


import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)