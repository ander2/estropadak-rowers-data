import config
from parsers.arc1ageparser import Arc1AgeParser


class EteAgeParser(Arc1AgeParser):
    url_base = 'http://www.ligaete.com/es/'
    file_path = config.ETE_FILES_PATH

    def __init__(self):
        super()

    def isRower(self, content):
        return True
