import unittest
import tempfile

from jeeves_commons.storage.database import init_db
from jeeves_commons.storage.storage import StorageClient

from sqlalchemy import create_engine


class BaseStorageTest(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        _, path = tempfile.mkstemp(prefix='jeeves-db')
        sqlite_engine = create_engine('sqlite:///{}'.format(path),
                                      convert_unicode=True)
        init_db(sqlite_engine)
        cls.storage = StorageClient(engine=sqlite_engine)
        # create the default tenant
        cls.storage.tenants.create('default')
