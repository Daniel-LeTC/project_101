from time import sleep
from driver import Driver
driver = Driver.get_driver()

def login(username, password):
    driver.get('https://en.52wmb.com/login?redirectUrl=https%3A%2F%2Fen.52wmb.com%2F')
    sleep(1)
    driver.refresh()
    sleep(1)
    user_field = driver.find_element('xpath','/html/body/div[1]/div[2]/dic/ul/li[1]/fieldset/input').send_keys(username)
    pass_field = driver.find_element('xpath','/html/body/div[1]/div[2]/dic/ul/li[2]/fieldset/input').send_keys(password)
    login_field = driver.find_element('xpath','//*[@id="sumbit_login"]').click()
    sleep(1)

def logout():
    driver.get('https://en.52wmb.com/login?redirectUrl=https%3A%2F%2Fen.52wmb.com%2F')
    driver.refresh()
    driver.find_element('xpath','//*[@onclick="logout()"]').click()



# NOTE: Just use this code for login
def try_login(username,password):
    while True:
        try:
            driver.get('https://en.52wmb.com/login?redirectUrl=https%3A%2F%2Fen.52wmb.com%2F')
            sleep(1)
            driver.refresh()
            sleep(1)
            login(username,password)
            sleep(1)
            break
        except:
            logout()
            sleep(4)

                