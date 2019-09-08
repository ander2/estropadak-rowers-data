class Rower:

    def __init__(self, name, birthplace, birthday, age, historial):
        self.name = name
        self.birthplace = birthplace
        self.birthday = birthday
        self.historial = historial
        self.age = age

    def __eq__(self, rower):
        return (self.name == rower.name and 
                self.birthday == rower.birthday and 
                self.birthplace == rower.birthplace)

