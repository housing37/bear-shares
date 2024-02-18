from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from lxml import html

def init_webdriver():
    ## Selenium: init webdrive ##
    print(f'\nInitializing Selenium webdriver...')

    # Configure Selenium options
    options = Options()
    # options.add_argument("--headless")  # Run Chrome in headless mode

    # Create a new Selenium driver & get html_content
    return webdriver.Chrome(options=options)

# login.live.com workflow
INP_EMAIL = (By.ID, "i0116")
BTN_NEXT = (By.ID, "idSIButton9")
INP_PW = (By.ID, "i0118")
BTN_SIGNIN = (By.ID, "idSIButton9")

#   Stay signed in?
BTN_DECLINE = (By.ID, "declineButton")
BTN_ACCEPT= (By.ID, "acceptButton")

#   Misc
BTN_CONTINUE = (By.ID, "id__0")

# bing.com/images/create
INFO_REWARD_PTS = (By.ID, "id_rc")
INP_IMG_DESCR = (By.ID, "sb_form_q")




# browser = webdriver.Firefox()
driver = init_webdriver()
# driver.get('https://login.live.com')

email = 'myst37.014@hotmail.com'    # ** WARNING ** DO NOT COMMIT!
password = 'myst2012mayan13206hotmail'     # ** WARNING ** DO NOT COMMIT!

def perform_login():
    # driver.get('https://login.live.com')
    # wait for email field and enter email
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(INP_EMAIL)).send_keys(email)

    # Click Next
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_NEXT)).click()

    # wait for password field and enter password
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(INP_PW)).send_keys(password)

    # Click Login - same id?
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_SIGNIN)).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_ACCEPT)).click()

def read_reward_pts():
    ans = input("\n  Read reward points? [y/n]\n  > ") 
    if ans == 'y' or ans == '1':
        # span_element = driver.find_element_by_id('id_rc')  # Replace 'your_span_id' with the ID of your <span> element
        # Find the <span> element by its ID
        # span_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, INFO_REWARD_PTS)))
        # span_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, INFO_REWARD_PTS)))
        pts = hc.xpath("//div[@id='id_h']//a[@id='id_rh']//span[@id='id_rc']")[0].text_content()
        
        # Get the text content of the <span> element
        # span_text = span_element.text
        # print(f'current reward points: {span_text}')
        print(f'current reward points: {pts}')
        return pts
        

# input("Press Enter to navigate to bing.com/images/create...")
url_create = 'https://bing.com/images/create'
print(f'navigating to {url_create}')
driver.get(url_create)

# WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_ACCEPT)).click()


# input("Press Enter get cookies...")
# # Get the cookies
# cookies = driver.get_cookies()

# # Extract the '_U' cookie
# u_cookie = None
# for cookie in cookies:
#     if cookie['name'] == '_U':
#         u_cookie = cookie['value']
#         break

# if u_cookie:
#     print('found cookie successful!')
#     print("U Cookie:", u_cookie)
# else:
#     print('found cookie failed.')

inp_descr = input('\n  Input description...\n  > ')
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(INP_IMG_DESCR)).send_keys(inp_descr)


# click 'create'
# BTN_CREATE = (By.ID, "create_btn_c")
# BTN_CREATE = (By.ID, "create_btn_e") # fails
BTN_CREATE = (By.ID, "create_btn_i") # success
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_CREATE)).click()

perform_login()

hc = html.fromstring(driver.page_source)

# # xpath_expr = hc.xpath("//div[@id='giscope']//form[@id='sb_form']//a[@id='create_btn_c']//span[@id='create_btn' and contains(text(), 'Create')]")
# # xpath_expr = hc.xpath("//div[@id='giscope']//form[@id='sb_form']//a[@id='create_btn_c']//span[@id='create_btn']/text()")
# xpath_expr = hc.xpath("//div[@id='giscope']//form[@id='sb_form']//a[@id='create_btn_c']//span[@id='create_btn']")
# BTN_CREATE_1 = (By.XPATH, xpath_expr) # success
# WebDriverWait(driver, 40).until(EC.text_to_be_present_in_element(BTN_CREATE_1, 'Create'))
# print("found 'create' button... images done loading... ")
input('Press Enter to get img url (after BING finishes generating image) ...')

# Define the alt attribute value
# alt_attr_value_tail_0 = "Image " # from "Image 1 of 4"
# alt_attr_value_tail_1 = " of 4" # from "Image 1 of 4"
# inp_descr = 'a doga and cat playing pool in a pool'
# Define the XPath to locate the <img> tag with the specified alt attribute value
# xpath_expression = f'//img[@alt="{alt_attribute_value}"]'
# xpath_expression = f'//img[contains(@alt, "{inp_descr}")]'
# xpath_expression = f'//img[contains(@src, ".svg")]'
# xpath_expression = '//img[contains(@src, ".svg") and @width="37"]'
# xpath_expression = '//img[contains(@src, ".svg") and contains(@class, "mimg")]'
# xpath_expression = '//img[contains(@src, ".svg") and @class="mimg"]'
# xpath_expression = '//img[contains(@src, ".svg") and @width="270"]'
# # xpath_expression = '//img[contains(@src, ".svg") and @width="270" and contains(@class, "mimg")]'

# # Wait for all <img> elements with src attribute ending in '.svg' to be present
# img_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))

# # Extract src values of all matching <img> elements
# svg_src_values = [img.get_attribute('src') for img in img_elements]

# LEFT OFF HERE ... getting image urls was indeed working, but now its not
# hc = html.fromstring(driver.page_source)
# auth_url = hc.xpath("//span[@class='featured-article-publish']//a/@href")[0]
img_urls = hc.xpath("//div[@class='imgpt']//a[@class='iusc']//div[@class='img_cont hoff']//img[@class='mimg']/@src")
print('printing img urls (pre-split)...', *img_urls, sep='\n')
img_urls = [url.split('?')[0] for url in img_urls]
print('printing img urls...', *img_urls, sep='\n')

# img_elements = driver.find_elements_by_xpath('//img[contains(@src, ".svg")]')
# Define the XPath to locate the <img> tag with the alt attribute value ending with the partial match
# xpath_expression = f'//img[substring(@alt, string-length(@alt) - {len(partial_match)} + 1) = "{partial_match}"]'

# Wait for the <img> element with the specified alt attribute value
# img_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))

# Get the value of the src attribute of the <img> element
# src_value = img_element.get_attribute('src')

pts_cnt = read_reward_pts()

sel_img_url = img_urls[0]
input(f'Press Enter to navigate to src url: {sel_img_url}')
driver.get(sel_img_url)

input("Press Enter to close the driver...")
# Close the browser
driver.quit()




#===================================================#
#===================================================#
    
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# import time

# def init_webdriver():
#     ## Selenium: init webdrive ##
#     print(f'\nInitializing Selenium webdriver...')

#     # Configure Selenium options
#     options = Options()
#     options.add_argument("--headless")  # Run Chrome in headless mode

#     # Create a new Selenium driver & get html_content
#     return webdriver.Chrome(options=options)

# # Your Hotmail or Microsoft Live credentials
# email = 'myst37.014@hotmail.com'    # ** WARNING ** DO NOT COMMIT!
# password = 'myst2012mayan13206hotmail'     # ** WARNING ** DO NOT COMMIT!

# # Path to your webdriver. For example, if using Chrome, make sure chromedriver is installed.
# # And specify its path.
# # webdriver_path = '/path/to/your/chromedriver'

# # Create a webdriver instance
# # driver = webdriver.Chrome(executable_path=webdriver_path)
# driver = init_webdriver()

# # Open the login page
# driver.get('https://login.live.com/')

# # Wait for the page to load
# time.sleep(2)

# # Find the email input field and enter email
# email_input = driver.find_element_by_name('loginfmt')
# email_input.send_keys(email)

# # Click Next
# email_input.send_keys(Keys.RETURN)

# # Wait for the page to load
# time.sleep(2)

# # Find the password input field and enter password
# password_input = driver.find_element_by_name('passwd')
# password_input.send_keys(password)

# # Click Sign in
# password_input.send_keys(Keys.RETURN)

# # Wait for the page to load
# time.sleep(5)

# # Get the cookies
# cookies = driver.get_cookies()

# # Extract the '_U' cookie
# u_cookie = None
# for cookie in cookies:
#     if cookie['name'] == '_U':
#         u_cookie = cookie['value']
#         break

# if u_cookie:
#     print('Login successful!')
#     print("U Cookie:", u_cookie)
# else:
#     print('Login failed.')

# # Close the browser
# driver.quit()



#===================================================#
#===================================================#

# import requests

# # Your Hotmail or Microsoft Live credentials
# email = 'myst37.014@hotmail.com'    # ** WARNING ** DO NOT COMMIT!
# password = 'myst2012mayan13206hotmail'     # ** WARNING ** DO NOT COMMIT!

# # Define the login URL
# login_url = 'https://login.live.com/'

# # Create a session object
# session = requests.Session()

# # Perform a GET request to the login page to retrieve cookies
# response = session.get(login_url)

# # Extract the '_U' cookie from the response
# u_cookie = session.cookies.get('_U')

# print("Initial Cookies:", session.cookies)

# # Data to be sent for login
# login_data = {
#     'loginfmt': email,
#     'passwd': password,
#     'LoginOptions': '3',
#     'type': '28',
# }

# # POST request to login
# response = session.post(login_url, data=login_data)

# # Check if login was successful
# if 'Logged in' in response.text:
#     print('Login successful!')
#     print("Cookies after login:", session.cookies)
#     print("U Cookie:", u_cookie)
# else:
#     print('Login failed.')

