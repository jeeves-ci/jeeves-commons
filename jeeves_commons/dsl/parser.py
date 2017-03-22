from validate import validate_workflow
from entities.task import TaskObject


def get_tasks(workflow, validate=True):
    if validate:
        validate_workflow(workflow)

    tasks = []
    for task_name, task_content in workflow.iteritems():
        task_content['task_name'] = task_name
        task = TaskObject(task_content)
        tasks.append(task)
    return tasks


def get_task(content):
    return TaskObject(content)


# import os
# import yaml
# with open(os.path.join('/home/adaml/dev/jeeves-minion/resources/examples/'
#                        'jeeves_workflow.yaml'),
#           'r') as task_stream:
#     workflow = yaml.load(task_stream)
#
# tasks = get_tasks(workflow)
#
