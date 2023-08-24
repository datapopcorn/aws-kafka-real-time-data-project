import json
import polars as pl
import boto3
from io import StringIO
from datetime import datetime

def business_data_transform(data):

    business_list = []

    business_columns_list = ["business_id", "name", "address", "city", "state", "postal_code", "latitude", "longitude", "stars", "review_count", "is_open"]

    for obj in data:
        temp_dict = {}
        for column in business_columns_list:
            temp_dict[column] = obj[column]
        business_list.append(temp_dict)


    df = pl.DataFrame(business_list)
    return df


def checkin_data_transform(data):

    checkin_list = []

    checkin_columns_list = ["business_id", "date"]


    for obj in data:
        temp_dict = {}
        for column in checkin_columns_list:
            if column == "date":
                temp_dict[column] = obj[column].split(", ")
            else:
                temp_dict[column] = obj[column]
        checkin_list.append(temp_dict)


    df = pl.DataFrame(checkin_list)
    df = df.explode("date")
    df = df.with_columns(
    pl.col("date").str.to_datetime("%Y-%m-%d %H:%M:%S")
    )

    return df

def review_data_transform(data):

    review_list = []
    review_columns_list = ["review_id", "user_id", "business_id", "stars", "date", "text", "useful", "funny", "cool"]


    for obj in data:
        temp_dict = {}
        for column in review_columns_list:
            temp_dict[column] = obj[column]
        review_list.append(temp_dict)


    df = pl.DataFrame(review_list)
    df = df.with_columns(
    pl.col("date").str.to_datetime("%Y-%m-%d %H:%M:%S")
    )

    return df

def tip_data_transform(data):

    tip_list = []
    tip_columns_list = ["text", "date", "compliment_count", "business_id", "user_id"]

    for obj in data:

        temp_dict = {}
        for column in tip_columns_list:
            temp_dict[column] = obj[column]
        tip_list.append(temp_dict)


    df = pl.DataFrame(tip_list)
    df = df.with_columns(
    pl.col("date").str.to_datetime("%Y-%m-%d %H:%M:%S")
    )

    return df

def user_data_transform(data):

    user_list = []
    user_columns_list = ["user_id", "name", "review_count", "yelping_since", "fans", "average_stars"]


    for obj in data:

        temp_dict = {}
        for column in user_columns_list:
            temp_dict[column] = obj[column]
        user_list.append(temp_dict)


    df = pl.DataFrame(user_list)
    df = df.with_columns(
    pl.col("yelping_since").str.to_datetime("%Y-%m-%d %H:%M:%S")
    )

    return df

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    Bucket = "yelp-etl-project"
    Key = "raw_data/to_process/"

    yelp_data = []
    yelp_keys = []
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)["Contents"]:
        file_key = file["Key"]
        print(file_key)
        if file_key.split(".")[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=file_key)
            content = response["Body"]
            jsonObject = json.loads(content.read())
            yelp_data.append(jsonObject)
            yelp_keys.append(file_key)

            if "business" in file_key:
                df = business_data_transform(jsonObject)
                key = "transformed_data/business_data/business_transformed_" + str(datetime.now()) + ".csv"

            elif "checkin" in file_key:
                df = checkin_data_transform(jsonObject)
                key = "transformed_data/checkin_data/checkin_transformed_" + str(datetime.now()) + ".csv"

            elif "review" in file_key:
                df = review_data_transform(jsonObject)
                key = "transformed_data/review_data/review_transformed_" + str(datetime.now()) + ".csv"

            elif "tip" in file_key:
                df = tip_data_transform(jsonObject)
                key = "transformed_data/tip_data/tip_transformed_" + str(datetime.now()) + ".csv"

            elif "user" in file_key:
                df = user_data_transform(jsonObject)
                key = "transformed_data/user_data/user_transformed_" + str(datetime.now()) + ".csv"

            csv_content = df.write_csv()
            s3.put_object(Bucket=Bucket, Key=key, Body=csv_content)

    s3_resource = boto3.resource("s3")
    for key in yelp_keys:
        copy_source = {
            "Bucket" : Bucket,
            "Key" : key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, "raw_data/processed/" + key.split("/")[-1])
        s3_resource.Object(Bucket, key).delete()
