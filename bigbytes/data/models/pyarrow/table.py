import pyarrow as pa

from bigbytes.data.models.pyarrow.shared import Base


class Table(Base):
    def __init__(self, target: pa.Table, **kwargs):
        super().__init__(target, **kwargs)
