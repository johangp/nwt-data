{{ config(
    materialized='incremental',
    unique_key='date,sentiment'
) }}

select
    date,
    sentiment,
    count(*) as message_count
from {{ ref('stg_raw_media') }}
group by date, sentiment

{% if is_incremental() %}
having date > (select max(date) from {{ this }})
{% endif %}
