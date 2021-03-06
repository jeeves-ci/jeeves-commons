import datetime
import hashlib
import uuid

from models import Task, Workflow, Minion, User, Tenant
from database import get_db_session
from base import BaseStorage
from storage_exceptions import (TaskDoesNotExistError,
                                TaskAlreadyExistsError,
                                WorkflowAlreadyExistsError,
                                WorkflowDoesNotExistError,
                                MinionAlreadyExistsError,
                                TenantAlreadyExistsError,
                                UserAlreadyExistsError,
                                MinionDoesNotExistError)


class WorkflowClient(BaseStorage):

    def __init__(self, session):
        super(WorkflowClient, self).__init__(session=session)

    def list(self,
             tenant_id,
             status=None,
             page=0,
             size=10,
             order_by=None,
             pattern=None,
             **kwargs):
        return self._list(Workflow,
                          tenant_id=tenant_id,
                          status=status,
                          order_by=order_by,
                          pattern=pattern,
                          page=page,
                          size=size,
                          **kwargs)

    def create(self, name, tenant_id, content, env):
        workflow = self._get(Workflow, name=name)
        if workflow:
            raise WorkflowAlreadyExistsError('Workflow with name {} '
                                             'already exists.'.format(name))
        workflow = self._create_workflow(name, tenant_id, content, env)
        return workflow

    def get(self, **kwargs):
        workflow = self._get(Workflow, **kwargs)
        return workflow

    def update(self,
               wf_id,
               status=None,
               env_result=None,
               date_done=None,
               started_at=None,
               ended_at=None):
        workflow = self.get(workflow_id=wf_id)
        # Change to kwargs!!
        workflow = self._update_workflow(workflow,
                                         status,
                                         env_result,
                                         date_done,
                                         started_at,
                                         ended_at)
        # Return the new, updated workflow
        return workflow

    def delete(self, wf_id, **kwargs):
        workflow = self.get(workflow_id=wf_id, **kwargs)
        # Todo: remove all associated tasks.
        # self._delete_all_tasks(workflow.id)
        if not workflow:
            raise WorkflowDoesNotExistError('Workflow with id {} not found.'
                                            .format(workflow))
        workflow = self._delete_workflow(workflow)
        return workflow

    def _update_workflow(self,
                         workflow,
                         status=None,
                         env_result=None,
                         date_done=None,
                         started_at=None,
                         ended_at=None):
        if status:
            workflow.status = status
        if date_done:
            workflow.date_done = date_done
        if started_at and not workflow.started_at:
            workflow.started_at = started_at
        if ended_at and not workflow.ended_at:
            workflow.ended_at = ended_at
        if env_result:
            workflow.env_result = env_result
        return workflow

    def _delete_workflow(self, workflow):
        result = workflow.first()
        workflow.delete()
        return result

    def _create_workflow(self, name, tenant_id, content, env):
        status = 'CREATED'
        created_at = datetime.datetime.now().replace(microsecond=0)
        workflow = Workflow(name=name,
                            tenant_id=tenant_id,
                            content=content,
                            env=env,
                            env_result=env,
                            status=status,
                            created_at=created_at)
        self.db_session.add(workflow)
        return workflow


class TaskClient(BaseStorage):

    def list(self,
             workflow_id=None,
             status=None,
             order_by=None,
             page=0,
             size=100,
             **kwargs):
        return self._list(Task,
                          workflow_id=workflow_id,
                          status=status,
                          order_by=order_by,
                          page=page,
                          size=size,
                          **kwargs)

    def get(self, task_id, **kwargs):
        return self._get(Task, task_id=task_id, **kwargs)

    def create(self,
               workflow_id,
               task_id,
               task_dependencies,
               task_name,
               content):
        task = self._get(Task, task_id=task_id)
        if task:
            raise TaskAlreadyExistsError('Task with id {} '
                                         'already exists.'.format(task_id))
        task = self._create_task(workflow_id,
                                 task_id,
                                 task_dependencies,
                                 task_name,
                                 content)
        return task

    def update(self,
               task_id,
               status=None,
               result=None,
               started_at=None,
               minion_ip=None):
        task = self.get(task_id)
        if not task:
            raise TaskDoesNotExistError('Task with id {} not found.'
                                        .format(task_id))

        task = self._update_task(task, status, result, started_at, minion_ip)
        return task

    def _update_task(self, task, status, result, started_at, minion_ip):
        if status:
            task.status = status
        if result:
            task.result = result
        if started_at:
            task.started_at = started_at
        if minion_ip:
            task.minion_ip = minion_ip
        return task

    def _create_task(self,
                     workflow_id,
                     task_id,
                     task_dependencies,
                     task_name,
                     content):
        status = 'CREATED'
        created_at = datetime.datetime.now()
        task = Task(workflow_id=workflow_id,
                    task_id=task_id,
                    task_name=task_name,
                    content=content,
                    status=status,
                    created_at=created_at,
                    task_dependencies=task_dependencies,)
        self.db_session.add(task)
        return task


class MinionClient(BaseStorage):

    def get(self, minion_ip, **kwargs):
        return self._get(Minion, minion_ip=minion_ip, **kwargs)

    def list(self, **kwargs):
        return self._list(Minion, **kwargs)

    def create(self, minion_ip, **kwargs):
        minion = self._get(Minion, minion_ip=minion_ip)
        if minion:
            raise MinionAlreadyExistsError('Minion with ip {} '
                                           'already exists.'.format(minion_ip))
        started_at = datetime.datetime.now()
        return self._create(Minion,
                            minion_ip=minion_ip,
                            started_at=started_at,
                            **kwargs)

    def update(self, minion_ip, status=None, **kwargs):
        minion = self.get(minion_ip)
        if not minion:
            raise MinionDoesNotExistError('Minion with ID {0} does not exist.')
        if status:
            minion.status = status
        return minion


class UserClient(BaseStorage):

    def get(self, email, **kwargs):
        return self._get(User,
                         email=email,
                         **kwargs)

    def list(self, **kwargs):
        return self._list(User, **kwargs)

    def create(self, email, password, role, tenant_id, **kwargs):
        user = self._get(User, email=email)
        if user:
            raise UserAlreadyExistsError('User with email {} '
                                         'already exists.'.format(email))
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        return self._create(User,
                            password=hashed_password,
                            email=email,
                            salt=salt,
                            role=role,
                            tenant_id=tenant_id,
                            **kwargs)


class TenantClient(BaseStorage):

    def get(self, name, **kwargs):
        return self._get(Tenant, name=name, **kwargs)

    def list(self, **kwargs):
        return self._list(Tenant, **kwargs)

    def create(self, name):
        tenant = self._get(Tenant, name=name)
        if tenant:
            raise TenantAlreadyExistsError('Tenant with name {} '
                                           'already exists.'.format(name))
        return self._create(Tenant, name=name)


class StorageClient(object):
    def __init__(self):
        self.session, self.engine = get_db_session()
        self.workflows = WorkflowClient(self.session)
        self.tasks = TaskClient(self.session)
        self.minions = MinionClient(self.session)
        self.users = UserClient(self.session)
        self.tenants = TenantClient(self.session)

    def close(self):
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def flush(self):
        self.session.flush()

    def dispose(self):
        self.engine.dispose()


client = StorageClient()


def get_storage_client():
    return client


def create_storage_client():
    return StorageClient()
