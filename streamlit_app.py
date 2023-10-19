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

#let's call Fruityvice API from Our Streamlit App!
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# if you don't add json fn at the end, it'll return rq status = "200"
streamlit.text(fruityvice_response.json())


