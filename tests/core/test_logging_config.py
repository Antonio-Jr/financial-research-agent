import logging
from unittest.mock import patch
from src.core.logging_config import setup_logging

@patch("logging.config.dictConfig")
def test_setup_logging_called(mock_dict_config):
    setup_logging()
    mock_dict_config.assert_called_once()
