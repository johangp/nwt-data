from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

DBT_DIR = "/opt/airflow/"

with DAG(
    "dbt_bashoperator_example",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    # Define dbt run command
    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f"cd {DBT_DIR} && dbt debug",
    )

    # Define dbt run command
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run",
    )

    dbt_debug >> dbt_run
