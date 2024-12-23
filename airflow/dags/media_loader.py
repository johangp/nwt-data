import json
import os
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}


def load_data():
    engine = create_engine("postgresql+psycopg2://dbt:dbt@localhost:5433/dbt")
    folder_path = "bucket/Media/2024/08/01/"

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            data = json.load(file)

        df = pd.json_normalize(data)
        df["categories"] = df["categories"].apply(json.dumps)
        df = df.rename(
            columns={
                "msgId": "msg_id",
                "feed.id": "feed_id",
                "feed.name": "feed_name",
                "source.title": "source_title",
            }
        )

        df.to_sql("raw_media", engine, if_exists="append", index=False)


with DAG(
    "raw_media_loader",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    load_raw_media_data = PythonOperator(
        task_id="load_raw_media_data",  # Task ID
        python_callable=load_data_to_postgres,  # Function to call
        dag=dag,
    )

    load_raw_media_data
