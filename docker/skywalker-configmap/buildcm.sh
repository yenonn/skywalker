#!/bin/bash
rm -fr *.zip
rm -fr app/*
find ../../src -type f | xargs -I{} cp {} app/
cd app
zip ../skywalker-codes.zip *
codes=$(base64 ../skywalker-codes.zip | tr -d \\n)
kubectl delete configmap skywalker-codes-configmap
kubectl create configmap skywalker-codes-configmap --from-literal=code=$codes
