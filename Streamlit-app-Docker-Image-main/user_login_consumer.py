import json
from kafka import KafkaConsumer
from s3fs import S3FileSystem


# Create a consumer object
consumer = KafkaConsumer("user_login", bootstrap_servers='43.207.149.192:9092',
value_deserializer=lambda x:
json.loads(x.decode('utf-8')))


s3 = S3FileSystem()

for message in consumer:
        with s3.open("s3://streamlit-data-project/user_login/{}_{}.json".format(message.value["user_id"], message.value["login_time"]), "w") as f:
                json.dump(message.value, f)
        print(message.value)
