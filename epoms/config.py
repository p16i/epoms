import yaml

class EPOMSConfig:
    def __init__(self):
        stream = open("config.yaml", "r")
        config = yaml.load(stream)

        self.config = config

    def get( self, key ):
        return self.config[key]
