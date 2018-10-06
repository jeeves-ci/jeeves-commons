import unittest
import tempfile

from jeeves_commons.storage import database
from jeeves_commons.storage.storage import StorageClient


class BaseStorageTest(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        _, path = tempfile.mkstemp(prefix='jeeves-db')
        database.db_url = 'sqlite:///{}'.format(path)
        database.init_db()

        # create storage client to be used by all tests.
        cls.storage = StorageClient()
        # create the default tenant
        cls.storage.tenants.create('default')
