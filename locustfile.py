from locust import HttpUser, TaskSet, task, constant, FastHttpUser, constant_pacing, SequentialTaskSet
from locust import LoadTestShape
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
# from selenium.webdriver.common.action_chains import ActionChains
from locust import TaskSet, task
from selenium.webdriver.support.ui import WebDriverWait
# chrome web service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
# import openpyxl as xl
import time
import requests
from faker import Faker
import random
from random import randint
# CHROMEDRIVER = '/opt/chrome/chromedriver'
HOST = "http://localhost"
# options = Options()
# options.add_argument('--headless')  
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# chrome_service = fs.Service(executable_path=CHROMEDRIVER) 
# driver = webdriver.Chrome(service=chrome_service, options=options)
# driver.get(URL)

def initialize(l):
    l.client.get(HOST + "/")

def ticket_site(l):
    l.client.get(HOST + "/ticket")

def cart_ticket(l):
    l.client.get(HOST + "/products")

def products_list(l):
    l.client.get(HOST + "/products/チケット一覧")
    # with Browser('phantomjs') as browser:
    #     ticket_id = [214, 215, 216, 213]
    #     url = WebsiteUser.host + "shop/?add-to-cart=" + random.choice(ticket_id)
    #     browser.visit(url) 
def add_ticket_cart(l):
    ticket_id = [214, 215, 216, 213]
    url = HOST +  "/shop/?add-to-cart=" + str(random.choice(ticket_id))
    # print(url)
    l.client.get(url)
def select_calendar(l):
    l.client.get(HOST + "/products/カレンダー選択")

def cart(l):
    l.client.get(HOST + "/cart")


def checkout(l):
    # driver = webdriver.Chrome()
    # driver.get(HOST + "/checkout")
    l.client.get(HOST + "/checkout")
    fake = Faker('jp-JP')
    name_split = fake.name().split(" ")
    print(name_split)
    company = fake.company()
    print(company)
    prof = fake.profile()
    city = fake.city()
    print(f"city: {city}")
    chome = fake.chome()
    print(f"chome: {chome}")
    print(prof)
    phone_n = fake.phone_number()
    postcode = fake.postcode()
    security_code = fake.credit_card_security_code()
    credit_full = fake.credit_card_full()
    print(f"creditfull: {credit_full}")
    time_credit = fake.credit_card_expire(start='now', end='+10y', date_format='%m %y')
    print(time_credit)


    # l.get(ticket_url + "/shop/?add-to-cart=" + str(random.choice(ticket_id)))
    # //*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input
    # driver.client.get(HOST + "/checkout")
    element = l.client.locust_find_element(By.NAME, "billing_first_name")
    element.send_keys(name_split[1])
    l.client.find_element(By.NAME, "billing_last_name").send_keys(name_split[0])
    l.client.find_element(By.NAME, "billing_company").send_keys(company)

    l.client.find_element(By.NAME, "billing_postcode").send_keys(postcode)
    l.client.find_element(By.NAME, "billing_city").send_keys(prof['address'])
    l.client.find_element(By.NAME, "billing_address_1").send_keys(chome)
    l.client.find_element(By.NAME, "billing_phone").send_keys(phone_n)
    l.client.find_element(By.NAME, "billing_email").send_keys(prof['mail'])

    l.client.switch_to.frame(frame_reference=l.find_element(By.XPATH, '//*[@id="stripe-card-element"]/div/iframe'))
    l.client.find_element(By.NAME, "cardnumber").send_keys(4242424242424242)
    l.client.switch_to.default_content()
    l.client.switch_to.frame(frame_reference=l.find_element(By.XPATH, '//*[@id="stripe-exp-element"]/div/iframe'))
    l.client.find_element(By.NAME, "exp-date").send_keys(str(time_credit))
    l.client.switch_to.default_content()
    l.client.switch_to.frame(frame_reference=l.find_element(By.XPATH, '//*[@id="stripe-cvc-element"]/div/iframe'))
    l.client.find_element(By.NAME, "cvc").send_keys(security_code)
    l.client.switch_to.default_content()
    l.client.find_element(By.NAME, "woocommerce_checkout_place_order").click()
        # self.client.post("/orders", data)

    # l.client.post(HOST + "/checkout", )

class ScenarioTask(SequentialTaskSet):
    # ()内の数値＝実行順番
    @task
    def initialize(self):
        initialize(self)

    @task
    def ticket_site(self):
        ticket_site(self)

    @task
    def cart_ticket(self):
        cart_ticket(self)

    @task
    def products_list(self):
        products_list(self)

    @task
    def select_calendar(self):
        select_calendar(self)

    @task
    def add_ticket_cart(self):
        add_ticket_cart(self)

    @task
    def cart(self):
        cart(self)

    @task
    def checkout(self): 
        checkout(self)

class WebsiteUser(FastHttpUser):
    wait_time = constant_pacing(1)
    tasks = [ScenarioTask]

class StagesShape(LoadTestShape):
    stages = [{'duration': 60, 'users': 24, 'spawn_rate': 24} ,
{'duration': 120, 'users': 28, 'spawn_rate': 28} ,
{'duration': 180, 'users': 14, 'spawn_rate': 14} ,
{'duration': 240, 'users': 11, 'spawn_rate': 11} ,
{'duration': 300, 'users': 8, 'spawn_rate': 8} ,
{'duration': 360, 'users': 9, 'spawn_rate': 9} ,
{'duration': 420, 'users': 9, 'spawn_rate': 9} ,
{'duration': 480, 'users': 16, 'spawn_rate': 16} ,
{'duration': 540, 'users': 31, 'spawn_rate': 31} ,
{'duration': 600, 'users': 65, 'spawn_rate': 65} ,
{'duration': 660, 'users': 58, 'spawn_rate': 58} ,
{'duration': 720, 'users': 65, 'spawn_rate': 65} ,
{'duration': 780, 'users': 71, 'spawn_rate': 71} ,
{'duration': 840, 'users': 67, 'spawn_rate': 67} ,
{'duration': 900, 'users': 88, 'spawn_rate': 88} ,
{'duration': 960, 'users': 76, 'spawn_rate': 76} ,
{'duration': 1020, 'users': 57, 'spawn_rate': 57} ,
{'duration': 1080, 'users': 59, 'spawn_rate': 59} ,
{'duration': 1140, 'users': 43, 'spawn_rate': 43} ,
{'duration': 1200, 'users': 39, 'spawn_rate': 39} ,
{'duration': 1260, 'users': 36, 'spawn_rate': 36} ,
{'duration': 1320, 'users': 49, 'spawn_rate': 49} ,
{'duration': 1380, 'users': 40, 'spawn_rate': 40} ,
{'duration': 1440, 'users': 38, 'spawn_rate': 38} ]
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
        #13:08~13:32
