from time import sleep
from util import Driver
driver = Driver.get_driver()
import  os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

_username = os.getenv("USER_NAME")
_password = os.getenv("PASSWORD")
def login():
    try:
        driver.get('https://en.52wmb.com/login?redirectUrl=https%3A%2F%2Fen.52wmb.com%2F')
        sleep(1)
        driver.refresh()
        sleep(3)
        user_field = driver.find_element('xpath','/html/body/div[1]/div[2]/dic/ul/li[1]/fieldset/input').send_keys(_username)
        pass_field = driver.find_element('xpath','/html/body/div[1]/div[2]/dic/ul/li[2]/fieldset/input').send_keys(_password)
        login_field = driver.find_element('xpath','//*[@id="sumbit_login"]').click()
        sleep(1)
    except:

def logout():
    driver.get('https://en.52wmb.com/login?redirectUrl=https%3A%2F%2Fen.52wmb.com%2F')
    driver.refresh()
    driver.find_element('xpath','//*[@onclick="logout()"]').click()



def logout_then_login():
    driver.get('https://en.52wmb.com/login?redirectUrl=https%3A%2F%2Fen.52wmb.com%2F')
    logout()
    sleep(1)
    login()

