# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """ Choose fruits you want to customize
    """
)
from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

options = st.multiselect(
    "Choose upto 5 ingredient",
   my_dataframe
)
if options:
    intergration_string = ''
    for fruit_chosen in options:
        intergration_string+= fruit_chosen + ' '
    #st.write(intergration_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + intergration_string + """')"""
    #st.write(my_insert_stmt)
    if intergration_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
