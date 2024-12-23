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
    """
    Loads the JSON file into a normalize pandas dataframe and dump the content
    into the raw_media table in postgresql.
    """
    engine = create_engine("postgresql+psycopg2://dbt:dbt@postgres-dbt:5432/dbt")
    folder_path = "/opt/airflow/data/Media/2024/08/01/"

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
        task_id="load_raw_media_data",
        python_callable=load_data,
        dag=dag,
    )

    load_raw_media_data
