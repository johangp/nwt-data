FROM apache/airflow:2.10.4

USER root
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

USER airflow

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY nwt_dbt .
