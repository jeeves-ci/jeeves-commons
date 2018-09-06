import os
import json

from celery import Celery
from celery.app.control import Control
from kombu import Exchange, Queue

from jeeves_commons.storage.storage import get_storage_client
from jeeves_commons.constants import (RABBITMQ_HOST_IP_ENV,
                                      RABBITMQ_HOST_PORT_ENV,
                                      RABBITMQ_USERNAME_ENV,
                                      RABBITMQ_PASSWORD_ENV,
                                      POSTGRES_HOST_IP_ENV,
                                      POSTGRES_HOST_PORT_ENV,
                                      POSTGRES_USERNAME_ENV,
                                      POSTGRES_PASSWORD_ENV,
                                      DEFAULT_BROKER_PORT,
                                      DEFAULT_POSTGRES_PORT,
                                      POSTGRES_RESULTS_DB,
                                      MINION_TASKS_QUEUE)
# Get message broker details
MESSAGE_BROKER_HOST_IP = os.getenv(RABBITMQ_HOST_IP_ENV, '172.17.0.3')
MESSAGE_BROKER_HOST_PORT = os.getenv(RABBITMQ_HOST_PORT_ENV,
                                     DEFAULT_BROKER_PORT)
MESSAGE_BROKER_USERNAME = os.getenv(RABBITMQ_USERNAME_ENV, 'guest')
MESSAGE_BROKER_PASSWORD = os.getenv(RABBITMQ_PASSWORD_ENV, 'guest')

# Get the result handler details
RESULTS_BACKEND_HOST_IP = os.getenv(POSTGRES_HOST_IP_ENV, '172.17.0.2')
RESULTS_BACKEND_HOST_PORT = os.getenv(POSTGRES_HOST_PORT_ENV,
                                      DEFAULT_POSTGRES_PORT)
RESULTS_BACKEND_USERNAME = os.getenv(POSTGRES_USERNAME_ENV, 'postgres')
RESULTS_BACKEND_PASSWORD = os.getenv(POSTGRES_PASSWORD_ENV, 'postgres')


broker_url = 'amqp://{0}:{1}@{2}:{3}//'.format(MESSAGE_BROKER_USERNAME,
                                               MESSAGE_BROKER_PASSWORD,
                                               MESSAGE_BROKER_HOST_IP,
                                               MESSAGE_BROKER_HOST_PORT)
backend_url = 'db+postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    RESULTS_BACKEND_USERNAME,
    RESULTS_BACKEND_PASSWORD,
    RESULTS_BACKEND_HOST_IP,
    RESULTS_BACKEND_HOST_PORT,
    POSTGRES_RESULTS_DB)

app = Celery(broker=broker_url,
             backend=backend_url)
remote_control = Control(app=app)

tasks_queue = Queue(name=MINION_TASKS_QUEUE,
                    exchange=Exchange(''),
                    routing_key=MINION_TASKS_QUEUE,
                    no_declare=True)


def send_task_message(message,
                      producer=None):
    with app.producer_or_acquire(producer) as producer:
        producer.publish(
            message,
            serializer='json',
            exchange=tasks_queue.exchange,
            routing_key=tasks_queue.routing_key,
            declare=[tasks_queue],
            retry=True,
        )


def put_task_in_queue():
    pass


def put_workflow_in_queue(workflow):
    pass


# Revoke all tasks dependent on the failed task + all their dependencies
def revoke_task_tree(head, terminate=True):
    workflow_tasks = get_storage_client().tasks.list(
                                            workflow_id=head.workflow_id)
    for task in workflow_tasks:
        dependencies = json.loads(task.task_dependencies)
        if head.task_id in dependencies:
            remote_control.revoke(task_id=task.task_id, terminate=terminate)
            revoke_task_tree(head=task)


def revoke_workflow_manually(workflow, terminate=True):
    for task in workflow.tasks:
        if task.status not in ['SUCCESS', 'REVOKED']:
            remote_control.revoke(task_id=task.task_id,
                                  terminate=terminate)
            get_storage_client().tasks.update(task.task_id,
                                              status='REVOKED_MANUALLY')
    get_storage_client().workflows.update(workflow.workflow_id,
                                          status='REVOKED')
    get_storage_client().commit()


def shutdown_minion(minion_ip):
    remote_control.shutdown(minion_ip)
# revoke_tasks(['87048a04-0b21-43bd-ac7b-6dd0b4e72293'])
