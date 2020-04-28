import re

class Validator:
    
    @staticmethod
    def validate_username(string):
        requirement = re.compile(r'^[A-Za-z\d]{4,}$')
        #minimum 4 char
        return bool(requirement.match(string))

    @staticmethod
    def validate_fullname(string):
        requirement = re.compile(r'^([A-Za-z])+ ([A-Za-z])+$')
        #format <firstname> <lastname>
        return bool(requirement.match(string))

    @staticmethod
    def validate_password(string):
        requirement = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')
        #minimum 6 char, with at least 1 letter and 1 number
        return bool(requirement.match(string))
