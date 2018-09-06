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
    ],

    license='LICENSE',
    description='Jeeves Commons.',
    install_requires=[
        'sqlalchemy==1.1.5',
        'celery==4.2.1',
        'pika==0.10.0',
    ]
)
