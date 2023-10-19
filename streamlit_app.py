import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("Das Ristorante")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
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


#create a repeatable code block
def get_fruityvice_data(this_fruit_choice):
    #let's call Fruityvice API from Our Streamlit App!
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
    # if you don't add json fn at the end, it'll return rq status = "200"
    # asssign json to a param 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # push param'd json to streamlit table and remove the pure json response afew lines above.
    return fruityvice_normalized  


streamlit.header("Fruityvice Fruit Advice!")

try:
    # now I parameterized the user input and put the parameter to the api call
    fruit_choice = streamlit.text_input('What fruit would you like information about?')

    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()


#don't run anything past here
streamlit.stop()


streamlit.header("Fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()


#add a button to load the fruit
if streamlit.button('Get Fruit Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)



def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit +"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

