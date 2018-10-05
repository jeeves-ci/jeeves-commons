

class TaskDoesNotExistError(Exception):
    pass


class TaskAlreadyExistsError(Exception):
    pass


class WorkflowAlreadyExistsError(Exception):
    pass


class WorkflowDoesNotExistError(Exception):
    pass


class MinionAlreadyExistsError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class TenantAlreadyExistsError(Exception):
    pass


class MinionDoesNotExistError(Exception):
    pass
