from pprint import pprint
from time import sleep
from seleniumwire import webdriver
from seleniumwire.webdriver import ChromeOptions
# from seleniumwire.webdriver.chrome.options import Options

def get_auth_token():
    auth_value = ''

    # Create a new instance of the Chrome driver
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    options.add_argument('--no-sandbox')  # Last I checked this was necessary.

    driver = webdriver.Chrome(chrome_options=options)

    driver.get('https://xe.com')

    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            if request.url == 'https://www.xe.com/api/protected/midmarket-converter/':
                for header, value in request.headers.items():
                    if header == 'authorization':
                        auth_value = f'{value}'

                
    print(auth_value)
    return auth_value
