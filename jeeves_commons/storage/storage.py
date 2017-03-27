import datetime

from models import Task, Workflow, Minion
from database import get_db_session
from base import BaseStorage
from exceptions import (TaskDoesNotExistError,
                        TaskAlreadyExistsError,
                        WorkflowAlreadyExistsError,
                        WorkflowDoesNotExistError,
                        MinionAlreadyExistsError,
                        MinionDoesNotExistError)


class WorkflowClient(BaseStorage):

    def __init__(self, session):
        super(WorkflowClient, self).__init__(session=session)

    def list(self, status=None, **kwargs):
        return self._list(Workflow, status=status, **kwargs)

    def create(self, wf_id, content, env):
        workflow = Workflow.query.filter_by(workflow_id=wf_id).first()
        if workflow:
            raise WorkflowAlreadyExistsError('Workflow with id {} '
                                             'already exists.'.format(wf_id))
        workflow = self._create_workflow(wf_id, content, env)
        return workflow

    def get(self, workflow_id, **kwargs):
        workflow = self._get(Workflow, workflow_id=workflow_id, **kwargs)
        return workflow

    def update(self, wf_id,
               status=None,
               env_result=None,
               date_done=None,
               started_at=None,):
        workflow = self.get(wf_id)
        # Change to kwargs!!
        workflow = self._update_workflow(workflow,
                                         status,
                                         env_result,
                                         date_done,
                                         started_at)
        # Return the new, updated workflow
        return workflow

    def delete(self, wf_id, **kwargs):
        workflow = self.get(wf_id, **kwargs)
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
                         started_at=None):
        if status:
            workflow.status = status
        if date_done:
            workflow.date_done = date_done
        if started_at and not workflow.started_at:
            workflow.started_at = started_at
        if env_result:
            workflow.env_result = env_result
        self.db_session.commit()
        return workflow

    def _delete_workflow(self, workflow):
        result = workflow.first()
        workflow.delete()
        self.db_session.commit()
        return result

    def _create_workflow(self, wf_id, content, env):
        status = 'CREATED'
        created_at = str(datetime.datetime.now())
        workflow = Workflow(workflow_id=wf_id,
                            content=content,
                            env=env,
                            env_result=env,
                            status=status,
                            created_at=created_at)
        self.db_session.add(workflow)
        self.db_session.commit()
        return workflow


class TaskClient(BaseStorage):

    def list(self, workflow_id=None, status=None, **kwargs):
        return self._list(Task,
                          workflow_id=workflow_id,
                          status=status,
                          **kwargs)

    def get(self, task_id, **kwargs):
        return self._get(Task, task_id=task_id, **kwargs)

    def create(self,
               workflow_id,
               task_id,
               task_dependencies,
               task_name,
               content):
        task = Task.query.filter_by(task_id=task_id).first()
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
        self.db_session.commit()
        return task

    def _create_task(self,
                     workflow_id,
                     task_id,
                     task_dependencies,
                     task_name,
                     content):
        status = 'CREATED'
        created_at = str(datetime.datetime.now())
        task = Task(workflow_id=workflow_id,
                    task_id=task_id,
                    task_name=task_name,
                    content=content,
                    status=status,
                    created_at=created_at,
                    task_dependencies=task_dependencies,)
        self.db_session.add(task)
        self.db_session.commit()
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
        started_at = str(datetime.datetime.now())
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
        self.db_session.commit()
        return minion


class StorageClient(object):
    def __init__(self):
        self.session = get_db_session()
        self.workflows = WorkflowClient(self.session)
        self.tasks = TaskClient(self.session)
        self.minions = MinionClient(self.session)

    def close(self):
        self.session.close()


client = StorageClient()


def get_storage_client():
    return client


def create_storage_client():
    return StorageClient()
