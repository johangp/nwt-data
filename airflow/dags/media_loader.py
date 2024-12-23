import json
import os
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import create_engine

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "start_date": datetime(2024, 8, 1),
    "retries": 1,
}


def get_execution_timestamp(execution_date: datetime) -> str:
    rounded_time = execution_date.replace(second=0, microsecond=0)
    if rounded_time.minute % 30 != 0:
        rounded_time = rounded_time + timedelta(minutes=(30 - rounded_time.minute % 30))

    timestamp = rounded_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return timestamp


def load_data(**kwargs):
    """
    Loads the JSON file into a normalize pandas dataframe and dump the content
    into the raw_media table in postgresql.
    """
    execution_date = kwargs["execution_date"]
    timestamp = get_execution_timestamp(execution_date)
    formatted_date = execution_date.strftime("%Y/%m/%d")
    folder_path = f"/opt/airflow/data/Media/{formatted_date}"

    engine = create_engine("postgresql+psycopg2://dbt:dbt@postgres-dbt:5432/dbt")

    for filename in os.listdir(folder_path):
        # Process the corresponding JSON file aligned with the execution time.
        if timestamp in filename:
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
    schedule_interval="*/30 * * * *",
    catchup=True,
) as dag:
    load_raw_media_data = PythonOperator(
        task_id="load_raw_media_data",
        python_callable=load_data,
        provide_context=True,
        dag=dag,
    )

    load_raw_media_data
