import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
print(config.sections()[0])