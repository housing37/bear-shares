
## NEW webdrive --headless browser testing ##
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from lxml import html
from datetime import datetime
import sys
import threading, time

# from xvfbwrapper import Xvfb # pip install xvfbwrapper



def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

# Define a function to print dots while waiting for the response
response_received = False
def print_dots():
    global response_received
    while not response_received:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)  # Adjust sleep duration as needed

def test_gen_image_openAI():
    global response_received
    print(f'ENTER - test_gen_image_openAI _ {get_time_now()}')
    from openai import OpenAI
    # client = OpenAI()
    print('init openAI cliet w/ key...')
    client = OpenAI(api_key="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")

    inp_descr = input('\n  Enter description\n  > ')
    print(f'  inp_descr: {inp_descr}')

    ans = input('\n  Enter quality...\n  0 = standard\n  1 = HD\n  > ')
    inp_quality = 'hd' if ans == '1' else 'standard'
    print(f'  inp_quality: {inp_quality}')

    response_received = False
    print(f'\nsending images.generate request... _ {get_time_now()}')
    
    # Start the thread for printing dots
    dot_thread = threading.Thread(target=print_dots)
    dot_thread.start()
    response = client.images.generate(
        model="dall-e-3",
        prompt=inp_descr,
        size="1024x1024",
        quality=inp_quality,
        n=1,
    )

    # Once the response is received, stop the thread
    response_received = True
    dot_thread.join()

    print(f'\nresponse recieved, printing data... _ {get_time_now()}')
    # print(response.data)
    revised_prompt = response.data[0].revised_prompt
    image_url = response.data[0].url
    print(f'\n\nrevised_prompt...\n {revised_prompt}')
    print(f'\nimage_url...\n {image_url}')

    print(f'\nEXIT - test_gen_image_openAI _ {get_time_now()}')

class BingImgGenerator():

    def __init__(self, _email, _pw):
        self.email = _email
        self.password = _pw
        self.driver = None

    def init_webdriver(self, _headless):
        options = Options()
        # options = webdriver.ChromeOptions()
        if _headless:
            options.add_argument("--headless")  # Run Chrome in headless mode
            # options.add_argument("--window-size=1920,1080")

            # LEFT OFF HERE ... possible fix for failing w/ --headless 
            #   try testing headless w/ these 2 additional options
            #   seems to work in req_handler.py for trinity_bot
            options.add_argument("--enable-javascript")  # Run Chrome in headless mode
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")
                
        return webdriver.Chrome(options=options) # Create driver & get html_content
        # return webdriver.Firefox(options=options)

    def perform_login(self, _driver):
        INP_EMAIL = (By.ID, "i0116")
        BTN_NEXT = (By.ID, "idSIButton9")
        INP_PW = (By.ID, "i0118")
        BTN_SIGNIN = (By.ID, "idSIButton9")
        BTN_ACCEPT= (By.ID, "acceptButton") # stay signed in
        # BTN_DECLINE = (By.ID, "declineButton") # stay signed in (decline)
        # BTN_CONTINUE = (By.ID, "id__0") # Misc
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_EMAIL)).send_keys(self.email) # wait for and enter email
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_NEXT)).click() # click next
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_PW)).send_keys(self.password) # wait for and enter pw
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_SIGNIN)).click() # click signin 
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_ACCEPT)).click() # click accept (stay logged in) ... should we?

    # def read_reward_pts(self, _hc):
    #     ans = input("\n  Read reward points? [y/n]\n  > ") 
    #     if ans == 'y' or ans == '1':
    #         # track and read reward points in top right
    #         pts = _hc.xpath("//div[@id='id_h']//a[@id='id_rh']//span[@id='id_rc']")[0].text_content()
    #         print(f'current reward points: {pts}')
    #         return pts
    #     return ''

    def input_descr(self, descr, use_cli, _driver):
        if use_cli: descr = input('\n  Input description...\n  > ') # cli input description
        INP_IMG_DESCR = (By.ID, "sb_form_q")
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_IMG_DESCR)).send_keys(descr) # wait for input & enter description 
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable((By.ID, "create_btn_i"))).click() # click join/create
        return descr

    def get_create_page(self, _driver: webdriver):
        url = 'https://bing.com/images/create'
        print(f'navigating to {url}')
        _driver.get(url) # go to create page

    def execute_gen_image(self, str_promt, use_cli, headless=False):

        # vdisplay = Xvfb()
        # vdisplay.start()

        # launch stuff inside
        # virtual display here.


        print(f'\ninitializing... {get_time_now()}')
        print(f' use_cli: {use_cli} _ headless: {headless}')
        self.driver = self.init_webdriver(headless)

        print(f'\nnav to create page... {get_time_now()}')
        self.get_create_page(self.driver) # nav to bing.com/images/create
        descr = self.input_descr(str_promt, use_cli, self.driver) # True = use_cli

        print(f'\nperform login... {get_time_now()}')
        self.perform_login(self.driver) # nav to 'login.live.com' (then back to bing.com/images/create)

        # wait for images to load (for btn 'Creating ...' turns to 'Create')
        print(f'\nGenerating image for descr ... {get_time_now()}\n "{descr}"')
        xpath_ = "//div[@id='giscope']//form[@id='sb_form']//a[@id='create_btn_c']//span[@id='create_btn']"
        WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, xpath_), 'Create')) 
        # import time
        # time.sleep(40)

        # scrape page source for img urls
        hc = html.fromstring(self.driver.page_source)
        img_urls = hc.xpath("//div[@class='imgpt']//a[@class='iusc']//div[@class='img_cont hoff']//img[@class='mimg']/@src")
        img_urls = [url.split('?')[0] for url in img_urls]
        print(f'\nprinting img urls ... {get_time_now()}', *img_urls, sep='\n ')

        # scrape page source for reward points count
        # pts = hc.xpath("//div[@id='id_h']//a[@id='id_rh']//span[@id='id_rc']")[0].text_content()
        # print(f'\ncurrent reward points ... {get_time_now()}\n {pts}')

        return img_urls
        # test img url received
        sel_img_url = img_urls[0]
        input(f'\nPress Enter to navigate to src url: {sel_img_url}')
        driver.get(sel_img_url)

        input("\nPress Enter to close the driver...")
        # Close the browser
        driver.quit()

        # vdisplay.stop()


if __name__ == "__main__":
    test_gen_image_openAI()

    # email_ = 'bear37.001@hotmail.com'    # ** WARNING ** DO NOT COMMIT!
    # password_ = 'bear102938'     # ** WARNING ** DO NOT COMMIT!
    # big = BingImgGenerator(email_, password_)
    # str_prompt = 'a dog and cat watching tv'
    # imgs = big.execute_gen_image(str_prompt, True) # True = use cli prompt

## LEGACY NAIVE ENDPOINT TESTING FOR bing.com/images/create ## 
# # capilot: temp37373737@gmail.com
# # label: bearsharestest
# # key: ed1f098241ed483f883bb44723b4cc8c.8cc4347ea14aa1c8

# # ref: https://github.com/acheong08/BingImageCreator/blob/main/README.md
# '''
# HOW-TO get required coockie
# login to bing.com/image/creator
#   open inspector (F12)
#   generate an image on the webpage
#   then go back to the opened inspector 
#    then go to 'network' tab
#    then use console cmd: cookieStore.get("_U")
#    then search output for 'value' and copy it (thats the cookie)
#     OR use cmd: cookieStore.get("_U").then(result => console.log(result.value))
# '''

# # LOGGED EXCEPTIONS...
# '''
#  raise Exception("Bad images")
# Exception: Bad images

#  raise Exception(error_redirect)
# Exception: Redirect failed
# '''
# import os
# import webbrowser
# # cook = "1CIx4heldQFrBstIQ-KL7d7ix-Rif8Di0yW_vsuk-Gsfb9lGzgTWTQ20KJ5oJR_Y7bmVNNKrKS_MVEN4v-OjGPVVsQ2a-h9zZkMC90Fj74frtXRSfKPzzJ5p8hdX27bfvEgUQlVJAzC92Mo_dFLTYvr_SgpQrFp-eUbdI-cByE9F57vWbER9z287be7cdsw6TP1_BYzzC9G1jkpYMgi-vYw"
# cook = "1pReBO98zSn9RZN9bQ9Zlr5dUBErYnqzis7_svvLnnlNksC2ic9-zBWiWFIoN0rutuF09dfJX47pCzrLN_21kkSfqEKBkjvHHGjKY-V6rmhnbWPFFpBbFir_4EgviUO6qUHO-MXfr014zz8Y-10ICeIE23NT-DOZn1tmTQKWLMuwl6545t8HT5Ql-u0PwXdlZgvj2VYLPS-YAYGjKpdx_FQ"
# os.environ["BING_COOKIES"] = cook

# # import os
# # import shutil

# # from src.BingImageCreator import ImageGen
# # from BingImageCreator import ImageGen
# from BingImageCreatorHouse import ImageGen
# import requests
# from bs4 import BeautifulSoup
# from requests_html import HTMLSession
# import json
# 
# def is_visible(element):
#     styles = element.get('style', '').lower()
#     if 'display: none' in styles or 'visibility: hidden' in styles:
#         return False
#     return True

# def test_gen_image_4():
#     url = "https://chat.openai.com/backend-api/conversation?offset=0&l‌​imit=20"

#     payload = {
#         "action": "next",
#         "messages": [
#             {
#             "id": "aaa241f8-e8a3-4a3d-a624-9b982cb28cbb",
#             "author": {
#                 "role": "user"
#             },
#             "content": {
#                 "content_type": "text",
#                 "parts": ["hello world lets go"]
#             },
#             "metadata": {}
#             }
#         ],
#         "conversation_id": "31bcf3d7-6185-4a90-8bab-b459352546e0",
#         "parent_message_id": "a786e1a9-157e-4197-b21b-746419ad2d38",
#         "model": "text-davinci-002-render-sha",
#         "timezone_offset_min": 300,
#         "suggestions": [],
#         "history_and_training_disabled": False,
#         "arkose_token": None,
#         "conversation_mode": {
#             "kind": "primary_assistant"
#         },
#         "force_paragen": False,
#         "force_rate_limit": False
#     }

#     headers = {
#         "accept": "text/event-stream",
#         "content-type": "application/json",
#         "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ0ZW1wMzczNzM3MzdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsicG9pZCI6Im9yZy1RM3liQUwxM2pFVVBTb1p6SUJKVWxKOXAiLCJ1c2VyX2lkIjoidXNlci1vQlZ3UVlNcEVYNEwxbTJwUDFWQlBtQ0MifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDY0MmUxNDc2MmZhM2FhY2FkYjUxNjgzYiIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MDgwNjYxOTgsImV4cCI6MTcwODkzMDE5OCwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.NEYpGqQi7SXlogwrtMhuIwGrsRCeaDgrXcrFN9E96kUQ5sINm_SK1H17EDv-UU6dSjzKfj2iobdCzG7rMRFYlMNiEmpS-pmRtIVzpfmdeJptK-BoemtbSTcBpLnyjvJVyF79gIBhz8NtK6JU6JIVx-5sqr4UDv3qXiGpOjAkfbPop9zogjeuPacz3Hqb-36WW_VJj6xHVL-QNiPXR6emZ6tOjDt7SI1WlgArqb1WmUm6uflpacAdPoGmRWi16BVTVdIAZQX44ASeJmCkk-fZI0kgSoHcPbgJiZmV7AVOZZDMg_CdXfwyIZ6X4qQQ_jf_6m7jeH2lP04B2zK5tqU7rQ",
#         "cookie": "__Host-next-auth.csrf-token=7f1673daf106a239defbe217b2d695a4a91791b4d997e7dc16289d71cae60410%7C3532fa90cb69b55ace4f8c17ec1847eb60649f1b6f97c25c96025f5ebf0b9b10; _account=; _cfuvid=CR0mIVLgmXTDeK3iedvGLnIC0Kbv_8MyGSzZucch1CI-1708066173608-0.0-604800000; oai-did=3a2acb36-0439-407b-8a35-f69b5a31c3c8; cf_clearance=yoOskyft1HgGGfqHs_22fiG69pfDBGvO8U9sj.8c53o-1708066180-1.0-Ac/UNe/4q2POeXR5CdZYYMpbyoiNsfsJs+IiubNWT77fvnSkRvmTSZ3xaj1pZLckJVGft1AvWlFr+krX6pHCmWA=; ajs_anonymous_id=a2a5cec9-00b6-478b-a50f-91a52301926e; intercom-device-id-dgkjq2bp=9892a95e-23b3-4678-a7c9-8b554c82c1a7; __Secure-next-auth.callback-url=https%3A%2F%2Fchat.openai.com; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..ygRC18AjPmtsmj5P.F0L6Gzmge_HzVACGEYBoyZXVRv6ly_cRAA8piqSRD06uZINEdZtqki1xUfn0j9eJoENK0WmtD2QyWBCAu6_7Aq1Aubw97xgyRttLRBpsXD6y21w6N0saUYq0S0wq5WVVhGVsI3q8rCpxiU6vxKVZBjrtui1NbyeYezFS9KAGdBlEH8KoFuoGLJ0388RrkV_OGZoGeFqPV8J-nbLVVRA_WstVVNHsTanwMYakK2ONtBm9yShOTAuJIhZLf09wa0mcH6Q3ohUGrTpyRPDuOOxn5OksHzXIINm1cnywdI_bTXUtvc71pAE6rg162HVuC114jBDbMA-dPZWHbF5tnQ92BfTElLrNMNJzSEEa7xJFjuINvbmGjeuviYvOdWznpaNoYQVvpFP3ZCyHl369ymTuSUECaFAh4HdFhi0Bg6hkji1bKLLsBWzoGx1ry2dTp5tkJLtstnmWUZCc1q43F7H_G_WBFwfQIzDDeThBLT8CeMe6VPiXSMZLfZM-rpjOpipe4JUpu5cGxaiQ6_y5Nw3u0kTX6uI26In7nTqbl4Kz05b_zOzYw2EA-Ymeff3Kr0QpE4M-EHX9IOfCccxXlxTzGNzAn2HRnZI4JdBmfQ_59_IhLPY7EidB5TItjvi683z5In7nKvxnDiSe3gLZiG91pVnqcs1KCSqCjbTwokh_0C5H-XoTRQPM6VEXuyqAQnnfbGHC2PTwGm1zD1i2pl9fJAwKkQAA6cXVpdlsfRpOe7nLEXwuyHOHfjlupJORhEN_aWc55tZvlL-u5Np2pnIclbQL1FKx7ulAD5I1K9J_59tfhPJ7y5u3nskZh2u3VyE7TON353V6YAnXfLxddnNjeJrr9nfUoki_1mFr_c_Gmx1DYIKIVVRIfRBczIFOOq4OBBMsieZK2k8cfbKVc7Pa8qgF9NpZvkkgB2DhmvotkogmnGFg4J7-fh62aPWQUjJdPb-8cX1cFIL23ecW1UhNXPBxR8vEmSizLE9AtOSLxbXgDb0w-Qs2EupaEY3gPskwDxlnJarvFYpZt-Ys0XMw1HvCooH0c74-gL7ZSpht7dKGttJ1P_R3FHKKyqyzetl7I147KWZ_qYSHz-aqCFd6UvwyLQK-JwOuWFPvXV7w-RMiBS0qYq4nhaqgGxg4sV4hq6BnR_s0TJVZ9U-voZZlSS-uhwIa4WD4oMxx5zvXCmRDGAf6pxbjAUU6ar-qcBizsLCoIPtILQVeyVMvf3bdhln-TUDb4tMoZwwU2YfWcBOimqPAQ9ahyt2laSXogfWMMptU-eEcfKvVu7tNirb1CpL7TCUjHY7nzYRmWWrMsOUcpV9qC-WZr8ol_9iT2lZLiJ_dfAdD_rQ-Xr1LLsPFYmmCfMf410AhmB1FK2Wb81jDQEN3u5tJOwinBOjpHjWojTbBc_LeXMlTndqMYDd2lRG8NS15gYStKf0Wu29jUnFAxLmmZTTEvpOGZ2-OFWZii-aslU1DwzDuVFPeWqw8I8UlxlA9T6vjmaMYC3L-FuhWszccITSGNlTN6Y3uddJzVqxaLVaeZuOi6xhj_hdLuDJWfHI-02araLVERE_mlRaq_4c3BrIdDMSKidtoH6OTN5WBd5zMXhPLkD6QJ-9ncb70xU_JFjEm3gS7qs65ON9EXX6E-ecHBkQiOnLcZRClBF1Sv8r0R9aIVFbKA1cIUl2XNLyH6FMVtdLITs7CmwtInqwDgdjaJ-0E76XZ9EAygRx0ufjePjnoV9B8RScHdC7ze7obXEhsqzT5MsO6HzKIqhK-Ympv8R7y1i4VnATupZO4xtIIs1n2PHNyR9X2Fl0hMflWwvlIPAA-QsmD_Cls54Woc3ztpOVH0UQ-s__PhpOhpbKGzTKY8ElQM-8hQvwuk3ceYEoAz-Owfmxivd0s3Z6HZNTOE7XB4gvTAQpEfMH8RRKx-neIfhbacsBKGPEuNFnXjG6uPE-57PMV2T0-OsKw8E5icBXEMNL-3Dx2rSmEoxyMthZde1lqfHXgNlZ0PyhXD_pgMLle7ZKPT9t5Y7bsm9ncv3prSxzpxKUeRCti_1LUNWUh5rS22rp_2_rkTQRMxHGlPSwRu03YOVCLh1UTopDHOxbNw2y2qFIDIqi2TwmDSN5TOIT00oQzZ0ms9y1dva1_QrHt5eePwehTu04rbI1Jw-LQyccqfLp99QLhbFsLERiFt791d75JHFDIyoRL8fUuWzeEKEL7MVfJE-_6_CXhKpdAwfe8wJhEghmGoysa9UIRarjekxrzBFuJPcMQrpakXu9his5lMJiqBdCTiN-dm81ph6K2dbTXWyUUWTYrrHbOcp60NfdrQYPcHcQd-P6omm1eVeDagkWP0CNjU7puB_KwabzFzk9JZ04swgFeD4WZ4x2aFpY1ui3YQ74e235txQkk319QB5nx_8mcv2QjIAejwi8AR_sUDR-CQhDJzLhjhE6SaPxY8IdKnu8krf8fae535itXYNbKDwveHaHMujyp0UiWZoWBRm_K52cXnd1TGgE9-h5fW78nUv2GOSmYXQdtVwlVE5NAHH7uRE3yaZR1ab87DUy8dKqI3PDsaLjdMxd0iGy7aIEfDVYJkPYFk91Xt-H4u5TQSQJOO5VNFNQObhcjeNeLyIhLtxWV_Q3aKzJaz7kIYfig0RlCH--Hcq0TCpy4t30_-gp_84sUwAKQZ_R5rxZZYpDWABwg8nOk6C29J4iewB174QCxpJlZmgKYamTuhdC4r6Vz66lM7_GvxIkXCG7bosbx4ev_FAjK7ZNBlPptYCG7LEKtljtuSSVtDaQK2KCQwyALwjb49SP_lIpLZt7ciK4eIS3tqr5lk_jDaZyPcnyS2xeDKEeTrJ-1hdGYdB6sTSJCD4ayzl0e3rVbBqFGkGlEJouY0L6uhZ0QgT-5dFoQp5lWNscIDnHa6VjQ8kyafeL9vF9n2OJ0odI.J2118MsPABRaUjUe8Lcz0A; intercom-session-dgkjq2bp=dGlQNXlqNmR6Tjh1VUlIQlhPcVhnV1NGZmVMWmZMQVRIcUkwNlIwNWhESkd2Sm1vRzJpRVZGR2ppN0NNV2RLVS0tNFREQzJiY3hmRStzVmYvRnlnRTdyUT09--dd3d76035e56cf61516159134801da51baabf36c; __cf_bm=i8dlqkG1v2ghkcK6xcQ3iS1WNhBL9dZ1z3obGFKnLL4-1708070821-1.0-AYks1BBwDKTCbzvqMGTjb2nYoi1uPmIrCV4BZANPG5P9BwqzWkwyi7D9rPhLhi0T/KPS/cNTgqRdNd7VNr2Qoho=; __cflb=0H28vVfF4aAyg2hkHEuhVVUPGkAFmYvk6wzTzzXpnxm; _dd_s=rum=0&expire=1708072316392",
#         "referer": "https://chat.openai.com/c/31bcf3d7-6185-4a90-8bab-b459352546e0",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     }

#     # response = requests.post(url, json=payload, headers=headers)
#     # print(response.text)
#     # soup = BeautifulSoup(response.text, 'html.parser')
#     # plain_text = soup.get_text()
#     # visible_text = [element.get_text() for element in soup.find_all(string=True, recursive=True) if is_visible(element.parent)]
#     # print("\n".join(visible_text))
#     # session: requests.Session = requests.Session()
#     session = HTMLSession()
#     session.headers = headers
#     session.cookies.set("_uasid", "Z0FBQUFBQmx6eG41WUZJQ1pfNE9oSGJqejY2OUdVdUpsanVvOVR3TW52TmlvQnJZWU9DVjJOdVMyN25hUlEtZ3V1ZzBiUDliTFVjSFhVN00ybVFkWGlpaFU5MmF0ZkhibGlweWlKTmxiWUFZN1E2dl92aFhoMF9GWDNBZTdtaERKWW8yb2hfaHhIczdmay1qM25ORlpRVS1icjB0X2RuSVg5cTA4UWs0YjlRT2RlT2tuNXdpZjdBbkxZZFphYWc3c2hqTzNzaWM1SnRqTjZsTUFXTnRXSkR6UVZ2bHRFZkZ2YXcwTWJqSnFPUlNROGZyZUo5X1Y4MnlpVVo2ejNJaHJBenBLS1JiRXNGMmJQT1BhWmVPb2VWV1BqVVRGR2ZCTzg1UXBmWXhZb0RVZ2llVllJMm9Lc1lza0Nja3YwR05aaGgyU1AzUUlrY3N5YTJHTVhwQmFRZ0V0Z2FmNDMzXzBnPT0")
#     session.cookies.set("_umsid", "Z0FBQUFBQmx6eG41QjBRYUkzbFZfalpZd3ZndGdHUEE2el9qbHlFQi1taWJaMzRQX1lwMVB0a0ZWcFJoSm1WekZEN0c4LUkxSVkzTDduWnJUdjl6NW01cmRDcG1xSTlSX19DbkszRS1OeGY1ZmFwQXhtRER0VHJhbVk3LXBsdXJ1c0VhRHBJTXg5U1hkRktBbEZKRUhWSWdHdExNdVE5UlZ0SzVlUVJyblhPSGlTZWVLQ0hSTUhsbVd5NmpoVXhmbTZSeFllVXhKdnMtcmFtSUV0bXpwazBYZ0RLTUhVLWphRGpvM29VampkdFNIQk42Nkp2VnZkdz0")
#     session.cookies.set("cf_clearance", "yoOskyft1HgGGfqHs_22fiG69pfDBGvO8U9sj")
#     json_payload = json.dumps(payload)
#     response = session.post(
#         url,
#         # allow_redirects=False,
#         data=json_payload,
#         timeout=200,
#     )
#     # response.html.render()
#     print(response.text)
#     # Load the JSON data
#     data = json.loads(response.text)

#     # Pretty print the JSON data
#     print(json.dumps(data, indent=4))
#     soup = BeautifulSoup(response.text, 'html.parser')
#     plain_text = soup.get_text()
#     visible_text = [element.get_text() for element in soup.find_all(string=True, recursive=True) if is_visible(element.parent)]
#     # print("\n\n\n\n".join(visible_text))

# # Z0FBQUFBQmx6eHo3aFl2WHBzNVNHOU01M184T01UQk5XRS1ITHRtY1BZb0FnN3d2RDBPZmhBWDlTS1ptdDhIYlRKamxfSlRyaFZkdzkzNU10S2xiOU9lNW1DZW94UUdQcjVHcGoycHhHb2FNRzZGdzVOZWlWOWQzakRSaG5PVkJBTUNVaDl0WEltazZMT0FLWWR5TnltdmsxcVRLbVNBZWlWNnhXSVdhdjA2MTdVZlpMbFFock1pZ21lWlhfWlhyMnk2Q2N0QU9WZnRydlhMOVpqRG9VSzc5b2Myakl0OFlTcGp3cjd6VmZ1Zm5GMlloWWIyV1JHUT0
# # Z0FBQUFBQmx6eG41QjBRYUkzbFZfalpZd3ZndGdHUEE2el9qbHlFQi1taWJaMzRQX1lwMVB0a0ZWcFJoSm1WekZEN0c4LUkxSVkzTDduWnJUdjl6NW01cmRDcG1xSTlSX19DbkszRS1OeGY1ZmFwQXhtRER0VHJhbVk3LXBsdXJ1c0VhRHBJTXg5U1hkRktBbEZKRUhWSWdHdExNdVE5UlZ0SzVlUVJyblhPSGlTZWVLQ0hSTUhsbVd5NmpoVXhmbTZSeFllVXhKdnMtcmFtSUV0bXpwazBYZ0RLTUhVLWphRGpvM29VampkdFNIQk42Nkp2VnZkdz0    
# # Z0FBQUFBQmx6eHo3ZDZ5czdQbEtTZFFmM3dzci1wdkVuT2NWMGt6Y2plQmUzV242bzJOSzMzVHBsc2NnSWhqcE10SE5OOUJjWmpLNllIZ2gyS2thTElmb2RXRDRfbS01eTZRY3d3ei1lVzY3Y3ZNdi14dGwtLUpvR0t0cDFGbTlDek0xZnpiSG9hclhucWZUQUtKemIxT05lSjhWZml3UHFKYU9Lc3FJN29rN1dPSVVjQnZ6QWVzejRTazgyZ2d0eXJia3pSOHFwcXl6SUlFdkVZYzFNcERtYldHMVRjSnVheVZtYkx2YzZIQmg1SE5tbUlNTDRXRjdWX1d2Z1BPcFBtdlM2VG12UFMyUjU5TVR3dU5BQkhreXcwYjFrZzZBVzM2WnNOc201V3hlMk9tdjFYekhoRy1tclcxNko2WlBFek1zQ1hhdWxLQ2M4RWhmVVk4ZW5FRVRjZmh6azJzSGRRPT0
# # Z0FBQUFBQmx6eG41WUZJQ1pfNE9oSGJqejY2OUdVdUpsanVvOVR3TW52TmlvQnJZWU9DVjJOdVMyN25hUlEtZ3V1ZzBiUDliTFVjSFhVN00ybVFkWGlpaFU5MmF0ZkhibGlweWlKTmxiWUFZN1E2dl92aFhoMF9GWDNBZTdtaERKWW8yb2hfaHhIczdmay1qM25ORlpRVS1icjB0X2RuSVg5cTA4UWs0YjlRT2RlT2tuNXdpZjdBbkxZZFphYWc3c2hqTzNzaWM1SnRqTjZsTUFXTnRXSkR6UVZ2bHRFZkZ2YXcwTWJqSnFPUlNROGZyZUo5X1Y4MnlpVVo2ejNJaHJBenBLS1JiRXNGMmJQT1BhWmVPb2VWV1BqVVRGR2ZCTzg1UXBmWXhZb0RVZ2llVllJMm9Lc1lza0Nja3YwR05aaGgyU1AzUUlrY3N5YTJHTVhwQmFRZ0V0Z2FmNDMzXzBnPT0


# # Z0FBQUFBQmx6eDdwWUR5QjZMbFBKaG83SE5QRUtQWS1EN3A1c3BXa0Z4TWJrWHRSTTltblJIb1NUTWZHbFc2NXYwR29jZ2JIV0ROa3hyZFVSa3VWWEhNU3FndEhvOUJqQ2hTTjIyYnM5alBaRVg2dkZ6SHZQb0VKNjRiR3VRQUg0MENwTU04ZTdIbjdfXzJFNTh5M2Roa0NQWnNBWXFtSUFBQ1JNOUF4VHRROUlnM0ZsRnQ0NzZKbWVjT2VXTjlTeVZzTGNPTjVISmYzVTdNUE1TRlhSQUVPenExWFltR0ZmY0lVRUVFSU5Zc2dQRGlVUjJVRGhvRW8zemV3aXExX0U2MVBISWE1WTBQRC1HYjRDekxnX3BpTjF6dDJiR2tVbmg2WTJEci1hbWttdTRfZ0g0ODJXSVpKby13Z0Rndkc3TzJKQ3MyWU1FQkFZeFg3ZGtCeE1UaGJhNHhneVVzYzRRPT0
# # Z0FBQUFBQmx6eDdwRTM2RjVxbDZtZnBYdXFHXy0yZjMzREJVQ01aeDVjVUdtbE0ySGIwRWRoRVJnVjEwQTBHTHROV05qRk1kck9IM0hXalQyakNya1hpVEhIOWplQ0FLS3U0VFpBNjJLVlZlQTJJNnNiQzE3V1VMN2QwYTBMaXQzWnp6NENHaEgzVUVyRHdhMUxNal80ZjZ4MHowVUM4VWFNcUR6cWtYWkdodi00VVFiMUVsaFhrVGE2Qlp3SFJWaEtHWFVGRUlMbnprcDg4X1pBeFZYRjlwMDcwVjlWd2tMWTJmM0NTOVpZU0lIT0xrQXpiblpkTT0
# test_gen_image_4()

# def test_gen_image_3():
    

#     url = "https://api.edenai.run/v2/image/generation"

#     payload = {
#         "response_as_dict": True,
#         "attributes_as_list": False,
#         "show_original_response": False,
#         "resolution": "256x256",
#         "num_images": 1
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTVmZDNlY2UtOTgwZC00NGMxLTgxNTctNTRkNDRkNzcwNDIzIiwidHlwZSI6ImFwaV90b2tlbiJ9.sasLb8kWp4DquWzc2qDnqTAJOI6RE8pQgKnrHhF51Fg"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     print(response.text)

# def test_gen_image():
#     # create a temporary output directory for testing purposes
#     test_output_dir = "test_output"
#     # os.mkdir(test_output_dir)
#     # download a test image
#     test_image_url = "https://picsum.photos/200"
#     # gen = ImageGen(auth_cookie="")
#     gen = ImageGen(auth_cookie=cook, auth_cookie_SRCHHPGUSR=cook)
#     str_prompt = input("\n describe the image ...\n > ")
#     # str_prompt = "a bear saying hello"
#     lst_imgs = gen.get_images(str_prompt)
#     print('DONE GETTING IMAGES...')
#     print(*lst_imgs, sep='\n')
#     print('LAUNCHING IMAGES...')

#     for url in lst_imgs:
#         safari = webbrowser.get('safari')  # specify the browser
#         safari.open_new_tab(url)

    

# # test_gen_image()
# # test_gen_image_2()


# def test_save_images():
#     # create a temporary output directory for testing purposes
#     test_output_dir = "test_output"
#     os.mkdir(test_output_dir)
#     # download a test image
#     test_image_url = "https://picsum.photos/200"
#     # gen = ImageGen(auth_cookie="")
#     gen = ImageGen(auth_cookie=cook)
#     str_prompt = "a bear saying hello"
#     lst_imgs = gen.get_images(str_prompt)
#     print(lst_imgs)
    
#     # gen.save_images([test_image_url], test_output_dir)
#     # gen.save_images([test_image_url], test_output_dir, file_name="test_image")
#     # # check if the image was downloaded and saved correctly
#     # assert os.path.exists(os.path.join(test_output_dir, "test_image_0.jpeg"))
#     # assert os.path.exists(os.path.join(test_output_dir, "0.jpeg"))
#     # # remove the temporary output directory
#     # shutil.rmtree(test_output_dir)

# # from openai import OpenAI
# # client = OpenAI(api_key="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")
# # # BearShares key: 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

# # response = client.images.generate(
# #   model="dall-e-3",
# #   prompt="a white siamese cat",
# #   size="1024x1024",
# #   quality="standard",
# #   n=1,
# # )

# # image_url = response.data[0].url