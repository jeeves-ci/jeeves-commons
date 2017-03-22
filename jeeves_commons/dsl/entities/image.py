
class EnvObject(dict):

    def __init__(self, image):
        self.update(image)

    @property
    def image(self):
        return self.get('image')
