# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()

options = st.multiselect(
    "Choose upto 5 ingredient",
   my_dataframe,
   max_selections=5
)
if options:
    intergration_string = ''
    for fruit_chosen in options:
        intergration_string+= fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json() , use_container_width=True)
    #st.write(intergration_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + intergration_string + """','"""+name_on_orders+"""')"""
    st.write(my_insert_stmt)
    st.stop
    if intergration_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


