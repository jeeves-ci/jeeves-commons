import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from jeeves_commons.constants import (POSTGRES_HOST_IP_ENV,
                                      POSTGRES_HOST_PORT_ENV,
                                      POSTGRES_USERNAME_ENV,
                                      POSTGRES_PASSWORD_ENV,
                                      POSTGRES_RESULTS_DB,
                                      DEFAULT_POSTGRES_PORT)

RESULTS_BACKEND_HOST_IP = os.getenv(POSTGRES_HOST_IP_ENV, '172.17.0.2')
RESULTS_BACKEND_HOST_PORT = os.getenv(POSTGRES_HOST_PORT_ENV,
                                      DEFAULT_POSTGRES_PORT)
RESULTS_BACKEND_USERNAME = os.getenv(POSTGRES_USERNAME_ENV, 'postgres')
RESULTS_BACKEND_PASSWORD = os.getenv(POSTGRES_PASSWORD_ENV, 'postgres')

Base = declarative_base()
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'
                       .format(RESULTS_BACKEND_USERNAME,
                               RESULTS_BACKEND_PASSWORD,
                               RESULTS_BACKEND_HOST_IP,
                               RESULTS_BACKEND_HOST_PORT,
                               POSTGRES_RESULTS_DB),
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_db_session():
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine)), engine
