# NWT Data

This project loads the JSON data stored in an S3 bucket from different sources (Media, Youtube, etc) into a DWH.
Once the data is loaded into a database it can be transformed using DBT creating useful models to explore.

## How to run this project

The current architecture is composed of an Airflow instance to orchestrate the workflows and a DBT project to run the
SQL models into the DwH. For the sake of reproducibility, I've used PostgreSQL instead of a real DWH.

After you clone this project, you can reproduce it by running docker compose up (be sure you have it previously installed).
You'll have an Airflow server running on your localhost:8080. Have in mind that it will ask for the credentials, in this case
is airflow for the user and password.

You'll see there are a couple of DAG, one to load the raw_data into the database. This DAG runs every 30 minutes.
The other DAG is one that is meant to be run manually as the DBT scheduler is not ready yet. 

![image](https://github.com/user-attachments/assets/42ec4464-312c-46df-9e98-d1ed371063a5)

After you run both models, first loading the data and then the dbt one, you'll end up with the following tables
in the postgre database:

![image](https://github.com/user-attachments/assets/aa8a9aad-13f6-46c3-bf7b-6a34e613862c)

You can take a look at the docker-compose.yml to see the host and the credentials to connect to the dbt database. 

DAGs are defined in the airflow/dags folder and the dbt models are defined in the nwt_dbt/models folder.

Also, have in mind that the data must be downloaded into a folder called bucket in the root of this repo as the connector to S3 is not ready yet.

## Future approach

This repo is nothing more than a proof of concept to illustrate how a solid, resilient and reliable data platform could work for this kind of 
ingestion. The pipelines are idempotent and an ELT approach was decided to take advantage of a powerful tool such as DBT. 

Here I illustrate the architecture that I'll create for this project




