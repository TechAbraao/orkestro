from pytest import mark
import logging

@mark.api
class TestApiTokensEndpoints:
    @classmethod
    def setup_class(cls):
        logging.disable(logging.CRITICAL)