from image import EnvObject


class TaskObject(dict):

    def __init__(self, task):
        self.update(task)

    @property
    def env(self):
        return EnvObject(self.get('env', {}))

    @property
    def pre_script(self):
        return self.get('pre')

    @property
    def script(self):
        return self.get('script')

    @property
    def dependencies(self):
        return self.get('dependencies')
