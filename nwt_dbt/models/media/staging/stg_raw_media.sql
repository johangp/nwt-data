{{ config(
    materialized='incremental',
    unique_key='id'
) }}

with raw as (
    select
        id,
        sentiment,
        jsonb_array_elements_text(categories) as category,
        feed_id,
        feed_name,
        date,
        msg_id,
        type,
        title,
        summary,
        text,
        source_title,
        link
    from {{ source('raw_data', 'raw_media') }}
)

select
    id,
    sentiment,
    category,
    feed_id,
    feed_name,
    date,
    msg_id,
    type,
    title,
    summary,
    text,
    source_title,
    link
from raw

{% if is_incremental() %}
where date > (select max(date) from {{ this }})
{% endif %}

