from dataclasses import dataclass
from typing import Dict

from bigbytes.cache.constants import CacheItemType
from bigbytes.data_preparation.models.block import Block
from bigbytes.shared.models import BaseDataClass


@dataclass
class CacheItem(BaseDataClass):
    block: Block = None
    item: Dict = None
    item_type: CacheItemType = None
    uuid: str = None

    def __post_init__(self):
        self.serialize_attribute_enums('item_type', CacheItemType)
