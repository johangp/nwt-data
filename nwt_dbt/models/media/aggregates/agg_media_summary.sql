{{ config(
    materialized='incremental',
    unique_key='feed_name,source_title,sentiment'
) }}

select
    feed_name,
    source_title,
    sentiment,
    count(*) as message_count
from {{ ref('stg_raw_media') }}
group by feed_name, source_title, sentiment

{% if is_incremental() %}
having max(date) > (select max(date) from {{ this }})
{% endif %}
