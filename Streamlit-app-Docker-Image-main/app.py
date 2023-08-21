import streamlit as st
import json
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
from s3fs import S3FileSystem

st.header('Welcome to Barco!')
# st.markdown(
#         """
#         <style>

#         </style>

#         """
#         ,
#         unsafe_allow_html=True,
# )

# business_columns = ["business_id", "name", "address", "city", "state", "postal_code", "latitude", "longitude", "stars", "review_count", "is_open"]
# review_columns = ["review_id", "user_id", "business_id", "stars", "useful", "funny", "cool", "text", "date"]
# user_columns = ["user_id", "name", "review_count", "yelping_since", "useful", "funny", "cool", "elite", "friends", "fans", "average_stars", "compliment_hot", "compliment_more", "compliment_profile", "compliment_cute", "compliment_list", "compliment_note", "compliment_plain", "compliment_cool", "compliment_funny", "compliment_writer", "compliment_photos"]
# tip_columns = ["text", "date", "likes", "business_id", "user_id"]
# checkin_columns = ["business_id", "date"] 
user_login_columns = ["user_id", "password"]


# Create a producer object
producer = KafkaProducer(bootstrap_servers='43.207.149.192:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Create a consumer object
consumer = KafkaConsumer("yelp_test", bootstrap_servers='43.207.149.192:9092',
value_deserializer=lambda x:
json.loads(x.decode('utf-8')))

# Create a s3 object
s3 = S3FileSystem()

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

                producer.send('yelp_test', value=data)
                producer.flush()

                consumer.poll()

                for message in consumer:
                        print(message.value)

                        with s3.open("s3://yelp-etl-project/kafka_test/user_login_{}_{}.json".format(user_id, login_date), "w") as f:
                                json.dump(message, f)

