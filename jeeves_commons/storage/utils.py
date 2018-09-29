import json
import uuid
from collections import namedtuple

from jeeves_commons.dsl.utils import create_task_dependency_mapping
from jeeves_commons.dsl.topology import topological_sort

from sqlalchemy.ext.declarative import DeclarativeMeta


def create_workflow(storage_client,
                    name,
                    content,
                    workflow_id,
                    tenant_id,
                    env={},
                    commit=True):
    workflow = storage_client.workflows.create(
        name=name,
        wf_id=workflow_id,
        tenant_id=tenant_id,
        content=json.dumps(content),
        env=json.dumps(env))
    tasks = _create_workflow_tasks(storage_client,
                                   content,
                                   workflow_id)
    if commit:
        storage_client.commit()
    else:
        storage_client.flush()
    return workflow, tasks


def _create_workflow_tasks(storage_client, workflow, workflow_id):
    deps = create_task_dependency_mapping(workflow)
    topology = topological_sort(deps)
    tasks = _create_task_id_dependencies(topology)

    result = []
    for task in tasks:
        task_res = storage_client.tasks.create(
                        workflow_id=workflow_id,
                        task_id=task.id,
                        task_dependencies=json.dumps(list(task.dep_ids)),
                        task_name=task.name,
                        content=json.dumps(workflow.get(task.name)))
        result.append(task_res)
    return result


def _create_task_id_dependencies(graph_sorted):
    Task = namedtuple('Task', 'name id dep_names dep_ids')
    tasks_name_mapping = {}
    tasks = []
    for task in graph_sorted:
        task_id = str(uuid.uuid4())
        task_deps = []
        for task_dep in task[1]:
            task_deps.append(tasks_name_mapping[task_dep])
        tasks_name_mapping[task[0]] = task_id
        task = Task(task[0], task_id, task[1], task_deps)
        tasks.append(task)

    return tasks


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if
                          not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # raise error on field failure
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
