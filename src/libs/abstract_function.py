from logger import LoggerFactory


class AbstractFunction(object):
    def __init__(self):
        self.logger = LoggerFactory().Logger
        pass

    def main(self):
        try:
            return self._proceed()
        except Exception as e:
            self.logger.exception(e)
            raise

    def _proceed(self):
        raise NotImplementedError(
            "This is an abstract which should be implemented in child class and not used directly."
        )
