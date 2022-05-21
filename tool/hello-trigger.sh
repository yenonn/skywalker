curl --location --request GET 'http://127.0.0.1:5000/execute' \
--header 'Content-Type: application/json' \
--data-raw '{
    "job-name": "hello-skywalker",
    "python-codes-config": "hello-skywalker-config.json",
    "python-codes-args": {"name": "HEY!!!"}
}'
