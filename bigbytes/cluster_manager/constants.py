from bigbytes.shared.enum import StrEnum

# ECS environment variables
ECS_CLUSTER_NAME = 'ECS_CLUSTER_NAME'
ECS_TASK_DEFINITION = 'ECS_TASK_DEFINITION'
ECS_CONTAINER_NAME = 'ECS_CONTAINER_NAME'

# GCP environment variables
GCP_PROJECT_ID = 'GCP_PROJECT_ID'
GCP_PATH_TO_KEYFILE = 'path_to_keyfile'
GCP_REGION = 'GCP_REGION'
# this should be the name of the current cloud run service that is running Bigbytes
GCP_SERVICE_NAME = 'GCP_SERVICE_NAME'

# K8s environment variables
KUBE_NAMESPACE = 'KUBE_NAMESPACE'
KUBE_SERVICE_TYPE = 'KUBE_SERVICE_TYPE'
KUBE_SERVICE_GCP_BACKEND_CONFIG = 'KUBE_SERVICE_GCP_BACKEND_CONFIG'
KUBE_STORAGE_CLASS_NAME = 'KUBE_STORAGE_CLASS_NAME'
KUBE_SERVICE_ACCOUNT_NAME = 'KUBE_SERVICE_ACCOUNT_NAME'
CLOUD_SQL_CONNECTION_NAME = 'CLOUD_SQL_CONNECTION_NAME'
CONNECTION_URL_SECRETS_NAME = 'CONNECTION_URL_SECRETS_NAME'
DB_SECRETS_NAME = 'DB_SECRETS_NAME'
SERVICE_ACCOUNT_SECRETS_NAME = 'SERVICE_ACCOUNT_SECRETS_NAME'
SERVICE_ACCOUNT_CREDENTIAL_FILE_PATH = 'SERVICE_ACCOUNT_CREDENTIAL_FILE_PATH'

# K8s constants
GCP_BACKEND_CONFIG_ANNOTATION = 'cloud.google.com/backend-config'
NODE_PORT_SERVICE_TYPE = 'NodePort'


class ClusterType(StrEnum):
    EMR = 'emr'
    ECS = 'ecs'
    CLOUD_RUN = 'cloud_run'
    K8S = 'k8s'