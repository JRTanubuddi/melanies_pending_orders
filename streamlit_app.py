# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """*Orders That need to filled.*
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_df:
    df_edit = st.data_editor(my_df)
    submitted = st.button('Submit')
    if submitted:
      og_dataset = session.table("smoothies.public.orders")
      edited_dataset = session.create_dataframe(df_edit)
      try:
          og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
          st.success("Order(s) updated!.",icon ='👍')
      except:
          st.write('Something went wrong.')

else:
    st.success("No Pending Orders right now!.",icon ='👍')
