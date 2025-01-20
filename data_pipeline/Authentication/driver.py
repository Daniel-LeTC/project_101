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
    def header_gets(url):
        _driver = Driver.get_driver()
        _driver.get(url)
        for request in _driver.requests:
            pass
        return request.headers

