from time import sleep

from seleniumwire import webdriver
class Driver:
    _driver = None
    def __init__(self):
        pass

    @staticmethod
    def get_driver():
        if Driver._driver is None:
            Driver._driver = webdriver.Chrome()
        return Driver._driver
    @staticmethod
    def reset_driver():
        Driver._driver.quit()
        Driver._driver = None
        Driver._driver = webdriver.Chrome()
        return Driver._driver
    @staticmethod
    def header_gets(url):
        _driver = Driver.get_driver()
        _driver.get(url)
        for request in _driver.requests:
            pass
        return request.headers

if __name__ == '__main__':
    driver =Driver.get_driver()
    driver.get('https://en.52wmb.com/customs-data/vietnam')
    sleep(1)
    Driver.reset_driver()
    driver.get('https://en.52wmb.com/customs-data/vietnam')