#!/bin/bash
rm -fr *.zip
cd app
zip ../skywalker-codes.zip *
codes=$(base64 ../skywalker-codes.zip | tr -d \\n)
sed -e "s/CODES/${codes}/g" ../configmap.yaml.template
