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
RESULTS_BACKEND_HOST_PORT = int(os.getenv(POSTGRES_HOST_PORT_ENV,
                                          DEFAULT_POSTGRES_PORT))
RESULTS_BACKEND_USERNAME = os.getenv(POSTGRES_USERNAME_ENV, 'postgres')
RESULTS_BACKEND_PASSWORD = os.getenv(POSTGRES_PASSWORD_ENV, 'postgres')

Base = declarative_base()

db_url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(RESULTS_BACKEND_USERNAME,
                                                   RESULTS_BACKEND_PASSWORD,
                                                   RESULTS_BACKEND_HOST_IP,
                                                   RESULTS_BACKEND_HOST_PORT,
                                                   POSTGRES_RESULTS_DB)


def init_db():
    pq_engine = create_engine(db_url, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=True,
                                             bind=pq_engine))
    Base.query = db_session.query_property()
    # Base.metadata.drop_all(bind=pq_engine)
    Base.metadata.create_all(bind=pq_engine)


def get_db_session():
    engine = create_engine(db_url, convert_unicode=True)
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=True,
                                       bind=engine)), engine
