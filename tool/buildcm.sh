#!/bin/bash
if -f *.zip
then
    rm -fr *.zip
    rm -fr app
fi
basedir="../"
find $basedir/src -type f -name *.pyc -delete
find $basedir/src -type f  -not -name "*.css" -not -name "*.html"| xargs -I{} cp {} app/
cp -fr $basedir/src/chronomaster/static app/
cp -fr $basedir/src/chronomaster/templates app/
cd app
zip -r ../skywalker-codes.zip *
codes=$(base64 ../skywalker-codes.zip | tr -d \\n)
kubectl delete configmap skywalker-codes-configmap
kubectl create configmap skywalker-codes-configmap --from-literal=code=$codes
