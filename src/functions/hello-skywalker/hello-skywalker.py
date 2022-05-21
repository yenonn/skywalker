from fake_elasticsearch import FakeElasticsearch
from logger import LoggerFactory


def main(**kwargs):
    logger = LoggerFactory().Logger
    logger.info("hello world skywalker")
    for var, val in kwargs.items():
        logger.info(f"{var}: {val}")
    pi = calculate_pi()
    logger.info(f"pi: {pi}")
    es = FakeElasticsearch()
    es.fake_task()
    logger.info("testing testing")


def calculate_pi():
    # Initialize denominator
    k = 1
    # Initialize sum
    s = 0
    for i in range(1000000):
        # even index elements are positive
        if i % 2 == 0:
            s += 4 / k
        else:
            # odd index elements are negative
            s -= 4 / k
        # denominator is odd
        k += 2
    return s
