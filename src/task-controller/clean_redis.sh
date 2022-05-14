 redis-cli -h 192.168.39.240 --pass "CvmvLA9aBT" --scan --pattern 'celery*' | xargs redis-cli -h 192.168.39.240 --pass "CvmvLA9aBT" DEL
