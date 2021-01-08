import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook

def discord_webhook_success(link, resort, day, month):
    webhook = DiscordWebhook(url=link, content='Your Reservations on\n' + month + ' ' + str(day) + '\n@' + resort + '\nHas been successful')
    webhook.execute()

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
    print('Initiating Sign In')
    time.sleep(1)
    driver.find_element_by_name('email').send_keys(email)
    print(f'Inputting Email: {email}')
    time.sleep(1)
    driver.find_element_by_name('password').send_keys(password)
    print(f'Inputting Password: ', end = ' ')
    print(len(password)*'*')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="scrolling-body"]/section/div/div/div/div[1]/div/div/div[1]/div/form/button').click()
    print('Successfully Signed In')
    avaliable = False
    time.sleep(5)
    driver.get('https://account.ikonpass.com/en/myaccount/add-reservations/')
    time.sleep(2)
    print('Finding Resort')
    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/input').send_keys(resort) #selecting resort
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div/ul/li').click()#selecting resort
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[2]/button').click()#selecting resort
    print(f'Resort Found: {resort}')
    time.sleep(1)
    print('Going to Month')
    for i in range(month):
        time.sleep(.25)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/button[2]').click()
    i=0
    j=0
    while avaliable == False:
        if j == 15:
            print(f'[{time.strftime("%H:%M:%S")}] Resetting')
            driver.quit()
            return(False)
        if i == 3:
            i = 0
            time.sleep(15)
            driver.refresh()
            print(f'[{time.strftime("%H:%M:%S")}] Refresh')
            time.sleep(3)
            try:
                print('Finding Resort')
                driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/input').send_keys(resort) #selecting resort
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div/ul/li').click()#selecting resort
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[2]/div[2]/button').click()#selecting resort
                print('Resort Found')
                time.sleep(1)
                print('Going to Month')
                for i in range(month):
                    time.sleep(.25)
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/button[2]').click()            
                j+=1

            except:
                print(f'[{time.strftime("%H:%M:%S")}] resetting')
                driver.quit()
                return(False)


        time.sleep(1)
        print('Finding Day')
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
    
        i+=1
    if avaliable == True:
        try:
            print('Attempting To Reserve')
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[2]/button').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[4]/div/div[4]/label/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[4]/div/div[5]/button').click()
            print('Reservation Successful')
            return(True)
        except:
            print(f'[{time.strftime("%H:%M:%S")}] Resetting')
            driver.quit()
            return(False)
def run():
    months = {
        'december': 0,
        'january':0,
        'february':1,
        'march':2,
        'april':3
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
    discord_input = input('Would You Like a Discord Notification Upon Success?> ')
    discord_bool = False

    if 'y' in discord_input:
        discord_link = input('Enter Discord Webhook> ')
        discord_bool = True

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
    
    if discord_bool == True and end == True:
        discord_webhook_success(discord_link, resort, date, month_travel)
    
run()