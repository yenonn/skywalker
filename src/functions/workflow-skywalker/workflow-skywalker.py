from abstract_function import AbstractFunction


class WorkflowSkywalker(AbstractFunction):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def _proceed(self):
        self.logger.info("workflow skywalker")


def main(**kwargs):
    WorkflowSkywalker(**kwargs).main()


if __name__ == "__name__":
    kwargs = {}
    WorkflowSkywalker(**kwargs).main()
