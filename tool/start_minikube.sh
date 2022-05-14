minikube start
kubectx minikube
kubectl patch cm config -n metallb-system -p '{"data": {"config": "address-pools:\n- name: default\n  protocol: layer2\n  addresses:\n  - 192.168.39.240-192.168.39.245\n"}}'

