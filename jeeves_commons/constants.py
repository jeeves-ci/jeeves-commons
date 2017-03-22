# Environment vars that will be injected to the clients
RABBITMQ_HOST_IP_ENV = 'RABBITMQ_HOST_IP_ENV'
RABBITMQ_HOST_PORT_ENV = 'RABBITMQ_HOST_PORT_ENV'
RABBITMQ_USERNAME_ENV = 'RABBITMQ_HOST_USERNAME_ENV'
RABBITMQ_PASSWORD_ENV = 'RABBITMQ_HOST_PASSWORD_ENV'

POSTGRES_HOST_IP_ENV = 'POSTGRES_HOST_IP_ENV'
POSTGRES_HOST_PORT_ENV = 'POSTGRES_HOST_PORT_ENV'
POSTGRES_USERNAME_ENV = 'POSTGRES_HOST_USERNAME_ENV'
POSTGRES_PASSWORD_ENV = 'POSTGRES_HOST_PASSWORD_ENV'

MASTER_HOST_PORT_ENV = 'MASTER_HOST_PORT_ENV'

NUMBER_OF_MINIONS_ENV = 'NUMBER_OF_MINIONS_ENV'
NUM_MINION_WORKERS_ENV = 'NUM_MINION_WORKERS_ENV'


# Messaging queue used to pass time json messages
CLIENT_MESSAGING_QUEUE = 'client_messaging_queue'
CLIENT_FANOUT_EXCHANGE = 'client_fanout_exchange'

# Bootstrap defaults
DEFAULT_REST_PORT = 8080
DEFAULT_NUM_OF_MINIONS = 4
DEFAULT_NUM_MINION_WORKERS = '4'
DEFAULT_BROKER_PORT = 5672
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_RESULT_SOCKET_PORT = 7777
POSTGRES_RESULTS_DB = 'postgres'
MINION_TASKS_QUEUE = 'minion_tasks_queue'


# Logging constants
