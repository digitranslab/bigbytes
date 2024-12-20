from typing import Dict, List

from bigbytes.streaming.sinks.base import BaseSink


class BasePythonSink(BaseSink):
    def __init__(self, **kwargs):
        """
        Not require config in the python sink
        """
        super().__init__(None, **kwargs)

    def init_client(self):
        """
        Initialize the client for the sink.
        """

    def batch_write(self, messages: List[Dict]):
        """
        Batch write the messages to the sink.

        For each message, the message format could be one of the following ones:
        1. message is the whole data to be wirtten into the sink
        2. message contains the data and metadata with the foramt {"data": {...}, "metadata": {...}}
            The data value is the data to be written into the sink. The metadata is used to store
            extra information that can be used in the write method (e.g. timestamp, index, etc.).
        """
