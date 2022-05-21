curl --location --request GET 'http://127.0.0.1:5000/execute' \
--header 'Content-Type: application/json' \
--data-raw '{
    "job-name": "workflow-skywalker",
    "python-codes-config": "workflow-skywalker-config.json",
    "python-codes-args": [{"name": "HEY!!!"}, {}]
}'
