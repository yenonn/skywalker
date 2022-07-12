minikube start
kubectx minikube
#kubectl patch cm config -n metallb-system -p '{"data": {"config": "address-pools:\n- name: default\n  protocol: layer2\n  addresses:\n  - 192.168.39.240-192.168.39.245\n"}}'

## install skywalker
# proxy
kubectl apply -f ../build/k8s/skywalker-proxy/skywalker-proxy-service.yaml
kubectl apply -f ../build/k8s/skywalker-proxy/skywalker-proxy.yaml
# executor
kubectl apply -f ../build/k8s/skywalker-executor/skywalker-executor.yaml
# chronomaster
kubectl apply -f ../build/k8s/skywalker-chronomaster/skywalker-chronomaster-service.yaml
kubectl apply -f ../build/k8s/skywalker-chronomaster/skywalker-chronomaster.yaml

