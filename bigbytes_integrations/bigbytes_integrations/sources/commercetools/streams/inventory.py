from bigbytes_integrations.sources.commercetools.streams.base import BaseStream


class InventoryStream(BaseStream):
    KEY_PROPERTIES = ['id']

    URL_PATH = '/inventory'
