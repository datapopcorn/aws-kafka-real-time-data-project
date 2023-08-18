import streamlit as st
import json
from kafka import KafkaProducer


st.header('Welcome to Yelp!')

# business_columns = ["business_id", "name", "address", "city", "state", "postal_code", "latitude", "longitude", "stars", "review_count", "is_open"]
# review_columns = ["review_id", "user_id", "business_id", "stars", "useful", "funny", "cool", "text", "date"]
# user_columns = ["user_id", "name", "review_count", "yelping_since", "useful", "funny", "cool", "elite", "friends", "fans", "average_stars", "compliment_hot", "compliment_more", "compliment_profile", "compliment_cute", "compliment_list", "compliment_note", "compliment_plain", "compliment_cool", "compliment_funny", "compliment_writer", "compliment_photos"]
# tip_columns = ["text", "date", "likes", "business_id", "user_id"]
checkin_columns = ["business_id", "date"] 

# Create a form to enter checkin data
form = st.form(key='my_form')
business_id = form.text_input(label='Business ID')
date = form.text_input(label='Date')
submit_button = form.form_submit_button(label='Submit')

# Create a producer object
producer = KafkaProducer(bootstrap_servers='52.68.237.80:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Create a dictionary
data = {'business_id': business_id,
        'date': date}

# Send data to the topic
producer.send('yelp_test', value=data)
