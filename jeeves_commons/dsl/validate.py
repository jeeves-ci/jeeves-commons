from jeeves_commons.dsl import utils


# TODO: REPLACE ASAP!
def _topology_iter(source):
    """perform topo sort on elements.

    :arg source: list of ``(name, [list of dependancies])`` pairs
    :returns: list of names, with dependancies listed first
    """
    pending = [(name, set(deps)) for name, deps in source]
    emitted = []
    while pending:
        next_pending = []
        next_emitted = []
        for entry in pending:
            name, deps = entry
            # remove deps we emitted last pass
            deps.difference_update(emitted)
            # still has deps? recheck during next pass
            if deps:
                next_pending.append(entry)
            else:
                # no more deps? time to emit
                yield name
                emitted.append(name)
                next_emitted.append(name)
        if not next_emitted:
            raise ValidationError('cyclic or missing dependency detected: {}'
                                  .format(next_pending))
        pending = next_pending
        emitted = next_emitted


def _validate_topology(workflow):
    dep_mapping = utils.create_task_dependency_mapping(workflow)
    validator = _topology_iter(source=dep_mapping)
    try:
        while validator.next():
            pass
    except StopIteration:
        pass


def _validate_env(task_name, task_content):
    if not task_content.get('env', {}).get('image'):
        raise ValidationError(
            'Task \'{0}\' does not contain an image. under '
            '<task_name>:<env>:<image>, add a base image to '
            'define the environment of your execution.'.format(task_name))


def _validate_script(task_name, task_content):
    if not task_content.get('script'):
        raise ValidationError(
            'Task \'{0}\' does not contain an script section. under '
            '<task_name>:<script>, add a the script to be executed by the '
            'minion.'.format(task_name))


def validate_workflow(workflow):
    _validate_topology(workflow=workflow)
    for task_name, task_content in workflow.iteritems():
        _validate_env(task_name=task_name, task_content=task_content)
        _validate_script(task_name=task_name, task_content=task_content)


class ValidationError(Exception):
    pass


# import os
# import yaml
# with open(os.path.join('/home/adaml/dev/jeeves-minion/resources/examples/'
#                        'jeeves_task.yaml'),
#           'r') as task_stream:
#     workflow = yaml.load(task_stream)
#
# validate_topology(workflow)
