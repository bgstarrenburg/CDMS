import re


def correctPassword(password) -> bool:
    # this regex will check if the password is of the correct length
    length = len(password)
    correctLength = 7 < length < 31
    # these regex's will check if the password contains a correct combination
    checkNum = bool(re.search(r"[0-9]", password))
    checkLowerChar = bool(re.search(r"[a-z]", password))
    checkUpperChar = bool(re.search(r"[A-Z]", password))
    CheckSpecialChar = bool(re.search(
        r"[^A-Za-z0-9]", password))
    checks = checkNum and checkLowerChar and checkUpperChar and CheckSpecialChar
    # charachters do not have to be checked since they are all allowed
    if (checks and correctLength):
        return True
    return False


def correctUsername(username) -> bool:
    regex = r"([a-z-A-Z]){1}([a-z]|[0-9]|[-]|[_]|[\']|[\.]){5,20}"
    if (re.fullmatch(regex, username)):
        return True
    return False


def correctZipCode(zipcode) -> bool:
    regex = r"[0-9]{4}[a-z-A-Z]{2}"
    if (re.fullmatch(regex, zipcode)):
        return True
    return False


def correctPhoneNumber(number) -> bool:
    regex = r"[0-9]{8}"
    if (re.fullmatch(regex, number)):
        return True
    return False


def correctEmail(email) -> bool:
    regex = r"[\w\.-]+@[\w\.-]+\.(\w){2,4}"
    if (re.fullmatch(regex, email)):
        return True
    return False
