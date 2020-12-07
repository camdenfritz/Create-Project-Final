import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


def monitor(email, password, headless, resort, month, day, row):
    options = Options()
    options.headless = True
    options.add_argument('log-level=3')
    if 'y' in headless.lower():
        driver = webdriver.Chrome(chrome_options=options)
    else:
        driver = webdriver.Chrome()

    time.sleep(3)
    driver.get('https://account.ikonpass.com/en/login')
    time.sleep(1)
    driver.find_element_by_name('email').send_keys(email)
    time.sleep(1)
    driver.find_element_by_name('password').send_keys(password)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="scrolling-body"]/section/div/div/div/div[1]/div/div/div[1]/div/form/button').click()
    avaliable = False
    time.sleep(5)
    driver.get('https://account.ikonpass.com/en/myaccount/add-reservations/')
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/input').send_keys(resort) #selecting resort
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div/ul/li').click()#selecting resort
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[2]/button').click()#selecting resort
    time.sleep(1)
    for i in range(month):
        time.sleep(.25)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/button[2]').click()
    i=0
    j=0
    while avaliable == False:
        if j == 15:
            print(f'[{time.strftime("%H:%M:%S")}] resetting')
            driver.quit()
            return(False)
        if i == 3:
            i = 0
            time.sleep(15)
            driver.refresh()
            print(f'[{time.strftime("%H:%M:%S")}] Refresh')
            time.sleep(3)
            try:
                driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/input').send_keys(resort) #selecting resort
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div/ul/li').click()#selecting resort
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[2]/button').click()#selecting resort
                time.sleep(2)
                for i in range(month):
                    time.sleep(.25)
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/button[2]').click()            
                j+=1

            except:
                print(f'[{time.strftime("%H:%M:%S")}] resetting')
                driver.quit()
                return(False)


        time.sleep(1)
        driver.find_element_by_xpath(f'/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div[2]/div[{str(row)}]/div[{str(day)}]').click() #the day I want to reserve
        time.sleep(5)
        try:
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[2]/div/div[4]/button[1]').click()
            print(f'[{time.strftime("%H:%M:%S")}] Avaliable!!')
            avaliable = True
        except:
            driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[3]/button').click()
            print('Unavaliable')
            time.sleep(2)
        else:
            print(f'[{time.strftime("%H:%M:%S")}] resetting')
            driver.quit()
            return(False)
    
        i+=1
    if avaliable == True:
        try:
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[2]/button').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[4]/div/div[4]/label/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[4]/div/div[5]/button').click()
            print('Complete')
            return(True)
        except:
            print(f'[{time.strftime("%H:%M:%S")}] resetting')
            driver.quit()
            return(False)
def run():
    months = {
        'december': 0,
        'january':1,
        'february':2,
        'march':3,
        'april':4
    }
    days_of_week = {
        'sunday':1,
        'monday':2,
        'tuesday':3,
        'wednesday':4,
        'thursday':5,
        'friday':6,
        'saturday':7
    }

    month_constants = [3,6,2,2,5]


    end = False
    headless = input('Do You Want This Process Headless?> ')
    emaii = input('Ikon Email> ')
    password = input('Ikon Password> ')
    resort = input('What Resort are you Traveling To?> ')
    month_travel = input('What Month is your Travel?> ')
    date = int(input('What is the date (number)> '))
    day_of_week = input('What is the day of week(monday, tuesday, ect)?> ')

    click_through = months[month_travel.lower()]

    row = int((month_constants[click_through]+date)/7+1)

    day_of_week = days_of_week[day_of_week.lower()]

    while end == False:
        end = monitor(emaii, password, headless, resort, click_through, day_of_week, row)
    
run()