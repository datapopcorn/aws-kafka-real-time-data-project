import json
import yaml
from kafka import KafkaProducer


# Create a producer object
producer = KafkaProducer(bootstrap_servers='43.207.149.192:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# read /yelp_raw_data_sample/business_data_sample.json and produce message line by line to kafka topic "business"

with open(f"yelp_raw_data_sample/business_data_sample.json", 'r', encoding="utf-8") as f:
    for line_number, line in enumerate(f):
        obj = json.loads(line)

        producer.send('yelp_business_topic', value=obj)
        producer.flush()
        print(f"Sent business data message {line_number}")

# read /yelp_raw_data_sample/user_data_sample.json and produce message line by line to kafka topic "user"

with open(f"yelp_raw_data_sample/user_data_sample.json", 'r', encoding="utf-8") as f:
    for line_number, line in enumerate(f):
        obj = json.loads(line)

        producer.send('yelp_user_topic', value=obj)
        producer.flush()
        print(f"Sent user data message {line_number}")

# read /yelp_raw_data_sample/review_data_sample.json and produce message line by line to kafka topic "review"

with open(f"yelp_raw_data_sample/review_data_sample.json", 'r', encoding="utf-8") as f:
    for line_number, line in enumerate(f):
        obj = json.loads(line)

        producer.send('yelp_review_topic', value=obj)
        producer.flush()
        print(f"Sent review data message {line_number}")

