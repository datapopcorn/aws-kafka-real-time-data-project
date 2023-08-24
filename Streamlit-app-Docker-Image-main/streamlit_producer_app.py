import streamlit as st
import json
from kafka import KafkaProducer
from datetime import datetime


st.header('Welcome to Yelp!')
# st.markdown(
#         """
#         <style>

#         </style>

#         """
#         ,
#         unsafe_allow_html=True,
# )


user_login_columns = ["user_id", "password"]


# Create a producer object
producer = KafkaProducer(bootstrap_servers='43.207.149.192:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Create a form to enter checkin data
with st.form(key='my_form'):
        user_id = st.text_input(label='User ID')
        password = st.text_input(label='Password', type='password')
        submitted = st.form_submit_button(label='Submit')
        login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if submitted:
                login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Create a dictionary
                data = {'user_id': user_id,
                'password': password,
                'login_time': login_date}

                producer.send('user_login', value=data)
                producer.flush()
                st.success('Data successfully submitted!!')

        else:
                st.write('Please enter the data and click submit button!!')

