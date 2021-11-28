import yaml

class DefaultConfig:

    def __init__(self):
        self.__config = self.__read_yaml()  

    def anos_disponiveis(self):
        return self.__config.get("anos")

    def estados_disponiveis(self):
        return self.__config.get("estados")

    def codigos_cid10(self):
        return self.__config.get("codigosCid10")
    
    def relatorios(self) -> list:
      return self.__config.get("relatorios")

    def __read_yaml(self):
        with open('./config.yml', 'r', encoding="utf-8") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return dict()


defaultConfig = DefaultConfig()