from setuptools import setup


setup(
    zip_safe=True,
    name='jeeves-commons',
    version='0.1',
    author='adaml',
    author_email='adam.lavie@gmail.com',
    packages=[
        'jeeves_commons',
        'jeeves_commons.dsl',
        'jeeves_commons.dsl.entities',
        'jeeves_commons.queue',
        'jeeves_commons.storage',
        'jeeves_commons.tests',
        'jeeves_commons.tests.unit',
        'jeeves_commons.tests.resources',
    ],

    license='LICENSE',
    description='Jeeves Commons.',
    install_requires=[
        'sqlalchemy==1.2.12',
        'psycopg2==2.7.1',
        'celery==4.2.1',
        'pika==0.10.0',
    ],
    package_data={
        'jeeves_commons': ['tests/resources/*.yaml'],
    },

)
