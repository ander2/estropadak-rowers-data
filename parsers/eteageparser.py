from parsers.arc1ageparser import Arc1AgeParser

class EteAgeParser(Arc1AgeParser):
    url_base = 'http://www.ligaete.com/es/'
    file_path = './pages/ete'

    def __init__(self):
        super()

    def isRower(self, content):
        return True