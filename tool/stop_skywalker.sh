## Uninstall skywalker
# proxy
kubectl delete -f ../build/k8s/skywalker-proxy/skywalker-proxy-service.yaml
kubectl delete -f ../build/k8s/skywalker-proxy/skywalker-proxy.yaml
# executor
kubectl delete -f ../build/k8s/skywalker-executor/skywalker-executor.yaml
# chronomaster
kubectl delete -f ../build/k8s/skywalker-chronomaster/skywalker-chronomaster-service.yaml
kubectl delete -f ../build/k8s/skywalker-chronomaster/skywalker-chronomaster.yaml

sleep 20
minikube stop
