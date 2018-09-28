from sqlalchemy.orm import relationship
from sqlalchemy import (Column,
                        Integer,
                        String,
                        LargeBinary,
                        DateTime,
                        ForeignKey)

from database import Base


class Task(Base):
    __tablename__ = 'celery_taskmeta'
    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True)
    task_dependencies = Column(String)
    task_name = Column(String, unique=False)
    workflow_id = Column(String,
                         ForeignKey('jeeves_workflows.workflow_id'))
    minion_ip = Column(String,
                       ForeignKey('jeeves_minions.minion_ip'))
    status = Column(String, unique=False)
    result = Column(LargeBinary, unique=False)
    date_done = Column(DateTime(timezone=False), unique=False)
    traceback = Column(String, unique=False)
    started_at = Column(DateTime(timezone=False), unique=False)
    created_at = Column(DateTime(timezone=False), unique=False)
    content = Column(String, unique=False)

    workflow = relationship("Workflow", back_populates="tasks")

    # Minion id foreign key
    minion = relationship('Minion', back_populates='tasks')

    def __init__(self,
                 task_id=None,
                 task_dependencies=None,
                 task_name=None,
                 status=None,
                 result=None,
                 date_done=None,
                 traceback=None,
                 workflow_id=None,
                 created_at=None,
                 started_at=None,
                 content=None):
        self.task_id = task_id
        self.task_dependencies = task_dependencies
        self.task_name = task_name
        self.status = status
        self.result = result
        self.date_done = date_done
        self.traceback = traceback
        self.workflow_id = workflow_id
        self.started_at = started_at
        self.created_at = created_at
        self.content = content

    def __repr__(self):
        return '<task {}>'.format(self.task_id)


class Workflow(Base):
    __tablename__ = 'jeeves_workflows'
    name = Column(String, unique=False)
    workflow_id = Column(String, primary_key=True, unique=True)
    env = Column(String, unique=False)
    env_result = Column(String, unique=False)
    status = Column(String, unique=False)
    content = Column(String, unique=False)
    created_at = Column(DateTime(timezone=False), unique=False)
    started_at = Column(DateTime(timezone=False), unique=False)
    ended_at = Column(DateTime(timezone=False), unique=False)

    # Set one to many relationship
    tasks = relationship('Task', back_populates='workflow')

    def __init__(self,
                 name=None,
                 workflow_id=None,
                 content=None,
                 status=None,
                 env=None,
                 env_result=None,
                 created_at=None,
                 started_at=None,
                 ended_at=None):
        self.name = name
        self.workflow_id = workflow_id
        self.content = content
        self.status = status
        self.env = env
        self.env_result = env_result
        self.created_at = created_at
        self.started_at = started_at
        self.ended_at = ended_at

    def __repr__(self):
        return '<workflow {}>'.format(self.workflow_id)


class Minion(Base):
    __tablename__ = 'jeeves_minions'
    minion_ip = Column(String, unique=True, primary_key=True)
    status = Column(String, unique=False)
    started_at = Column(DateTime(timezone=False), unique=False)

    # define a one to many relationship
    tasks = relationship('Task', back_populates='minion')

    def __init__(self,
                 minion_ip=None,
                 status=None,
                 started_at=None):
        self.minion_ip = minion_ip
        self.status = status
        self.started_at = started_at

    def __repr__(self):
        return '<minion {}>'.format(self.ip)


class User(Base):
    __tablename__ = 'jeeves_users'
    id = Column(Integer, unique=True, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, unique=True)
    role = Column(String, unique=False)
    salt = Column(String, unique=False)
    tenant_id = Column(ForeignKey('jeeves_tenants.id'), nullable=False)

    def __init__(self,
                 password=None,
                 tenant_id=None,
                 role=None,
                 email=None,
                 salt=None):
        self.password = password
        self.tenant_id = tenant_id
        self.role = role
        self.email = email
        self.salt = salt

    def __repr__(self):
        return '<user {}>'.format(self.ip)


class Tenant(Base):
    __tablename__ = 'jeeves_tenants'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self,
                 name=None):
        self.name = name

    def __repr__(self):
        return '<tenant {}>'.format(self.ip)
