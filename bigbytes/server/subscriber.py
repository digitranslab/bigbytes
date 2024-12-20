from datetime import datetime
from bigbytes.server.active_kernel import get_active_kernel_client
from bigbytes.server.logger import Logger

logger = Logger().new_server_logger(__name__)


def get_messages(callback=None):
    now = datetime.utcnow()

    while True:
        try:
            client = get_active_kernel_client()
            message = client.get_iopub_msg(timeout=1)

            if message.get('content'):
                if callback:
                    callback(message)
                else:
                    logger.warn(f'[{now}] No callback for message: {message}')
        except Exception as e:
            if str(e):
                logger.error(f'[{now}] Error: {e}', )
            pass
