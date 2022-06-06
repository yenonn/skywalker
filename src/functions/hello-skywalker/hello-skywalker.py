from fake_elasticsearch import FakeElasticsearch
from abstract_function import AbstractFunction


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


class HelloSkywalker(AbstractFunction):
    def __init__(self, **kwargs):
        AbstractFunction.__init__(self)
        self.kwargs = kwargs

    def _proceed(self):
        self.logger.info("hello world skywalker")
        for var, val in self.kwargs.items():
            self.logger.info(f"{var}: {val}")
        pi = calculate_pi()
        self.logger.info(f"pi: {pi}")
        es = FakeElasticsearch()
        es.fake_task()
        self.logger.info("testing testing")


# main entrypoint for function
def main(**kwargs):
    HelloSkywalker(**kwargs).main()


if __name__ == "__main__":
    kwargs = {"name": "Hey!"}
    HelloSkywalker(**kwargs).main()
