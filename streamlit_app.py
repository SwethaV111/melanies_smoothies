# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """ Choose fruits you want to customize
    """
)



name_on_orders = st.text_input("Order the smoothie")
st.write("The name on your smoothie will be", name_on_orders)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

options = st.multiselect(
    "Choose upto 5 ingredient",
   my_dataframe,
   max_selections=5
)
if options:
    intergration_string = ''
    for fruit_chosen in options:
        intergration_string+= fruit_chosen + ' '
    #st.write(intergration_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + intergration_string + """','"""+name_on_orders+"""')"""
    st.write(my_insert_stmt)
    st.stop
    if intergration_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
