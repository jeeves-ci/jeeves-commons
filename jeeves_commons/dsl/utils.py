
def create_task_dependency_mapping(workflow):
    deps = []
    for task, task_content in workflow.iteritems():
        deps.append((task, task_content.get('dependencies', set())))
    return deps
