import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def main(login_info):
    # dictionary containing email, username, password
    load_dotenv()
    login_info['execution'] = os.getenv("EXECUTION")
    login_info['_eventId'] = "submit"

    # general cas login - login info will be save for login
    request_url = "https://webauth.claremont.edu/cas/login"

    # request session to keep login cookies
    with requests.Session() as s:

        # login POST request TODO: if response is not 200, do smth about it
        cas = s.post(request_url, data=login_info)
        return s.cookies.get_dict()
