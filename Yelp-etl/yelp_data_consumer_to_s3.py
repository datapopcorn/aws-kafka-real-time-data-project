import json
from kafka import KafkaConsumer
from s3fs import S3FileSystem
from datetime import datetime

# Create an S3FileSystem object
s3 = S3FileSystem()

# Create a consumer object for the business, user, review topic
consumer = KafkaConsumer("yelp_business_topic", "yelp_user_topic", "yelp_review_topic",
                          bootstrap_servers='43.207.149.192:9092',
value_deserializer=lambda x:
json.loads(x.decode('utf-8')))

batch_size = 100
business_current_batch = []
user_current_batch = []
review_current_batch = []


for message in consumer:
        consumer.poll()
        if message.topic == "yelp_business_topic":
                business_current_batch.append(message.value)
                if len(business_current_batch) >= batch_size:
                        now = datetime.now()
                        with s3.open("s3://yelp-etl-project/raw_data/to_process/business_{}.json".format(now), "w") as f:
                                json.dump(business_current_batch, f)
                        business_current_batch = []
                        print("Wrote business_{} to S3".format(now))
        elif message.topic == "yelp_user_topic":
                user_current_batch.append(message.value)
                if len(user_current_batch) >= batch_size:
                        now = datetime.now()
                        with s3.open("s3://yelp-etl-project/raw_data/to_process/user_{}.json".format(now), "w") as f:
                                json.dump(user_current_batch, f)
                        user_current_batch = []
                        print("Wrote user_{} to S3".format(now))
        elif message.topic == "yelp_review_topic":
                review_current_batch.append(message.value)
                if len(review_current_batch) >= batch_size:
                        now = datetime.now()
                        with s3.open("s3://yelp-etl-project/raw_data/to_process/review_{}.json".format(now), "w") as f:
                                json.dump(review_current_batch, f)
                        review_current_batch = []
                        print("Wrote review_{} to S3".format(now))


