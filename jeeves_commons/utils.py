import os
import time
import socket
import logging
from contextlib import contextmanager

import pika


@contextmanager
def open_channel(rabbit_host_ip,
                 rabbit_port=5672,
                 rabbit_username='guest',
                 rabbit_password='guest'):
    creds = pika.credentials.PlainCredentials(username=rabbit_username,
                                              password=rabbit_password)
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host_ip,
                                      port=rabbit_port,
                                      credentials=creds))
        channel = connection.channel()
        yield channel
    except Exception as e:
        print 'Error connecting to queue: {message}' \
            .format(message=e.message)
    finally:
        channel.close()


def wait_for_port(host, port, duration=60, interval=3):

    end = time.time() + duration
    while time.time() < end:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        opened = sock.connect_ex((host, port)) == 0
        if opened:
            print 'Connected successfully.'
            return True
        else:
            print 'Failed connecting on {0}:{1}. Retrying in {2} seconds...' \
                .format(host, port, interval)
            time.sleep(interval)
    return False


def create_logger(name, path=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    if path:
        logger.addHandler(_create_file_handler(path))
    logger.addHandler(logging.StreamHandler())
    logger.level = level
    return logger



def _create_file_handler(path):
    _make_dir(path)
    return logging.FileHandler(path)


def get_or_create_file_logger(name, path):
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        logger.addHandler(_create_file_handler(path))
    return logger


def _make_dir(path):
    path_dir = os.path.dirname(path)
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)


def which(executable):
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, executable)):
            return os.path.join(path, executable)

    return None

# create_logger('aa')
# create_logger('aa')
# pass
