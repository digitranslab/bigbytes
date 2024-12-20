from bigbytes_integrations.sources.paystack.streams.base import BasePaystackStream


class CustomersStream(BasePaystackStream):
    TABLE = 'customers'
    ENTITY = 'customer'
    REPLICATION_METHOD = 'INCREMENTAL'
    REPLICATION_KEY = 'createdAt'
    KEY_PROPERTIES = ['id']
    BOOKMARK_PROPERTIES = ['createdAt']
    SELECTED_BY_DEFAULT = True
    VALID_REPLICATION_KEYS = ['createdAt']
    INCLUSION = 'available'
    API_METHOD = 'GET'
    SCHEMA = 'customers'

    def get_url(self):
        return 'https://api.paystack.co/customer'
