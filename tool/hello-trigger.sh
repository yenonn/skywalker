curl --location --request POST 'http://127.0.0.1:5000/execute' \
--header 'Content-Type: application/json' \
--data-raw '{
    "job-name": "hello-skywalker",
    "python-codes-config": "hello-skywalker-config.json"
}'
