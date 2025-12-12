import requests
import os
import json


def sigenu_check(CI: str):

    username = os.getenv("USERNAME_SIGENU") 
    if not username:
        username =""
    password = os.getenv("PASSWORD_SIGENU")
    if not password:
        password =""
    auth = (username,password)


    response = requests.get(f'https://sigenu.uh.cu/sigenu-rest/student/fileStudent/getStudentAllData/{CI}',
                             auth= auth)

    if response.text:
        data = json.loads(response.text)
        if data and len(data) > 0:
            return True
        else:
            return False