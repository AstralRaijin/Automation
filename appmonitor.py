import datetime
import requests
import time
import pytz
import pymsteams
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app_name = input("App_name (input new EXACT app name if you're changing info): ")
bundle_id = input("bundle_id to monitor: ")
link = 'https://play.google.com/store/apps/details?id='
full_link = link + bundle_id
discord_hook = "https://discord.com/api/webhooks/915894181568851999/95WtOLHmUNE6DEfDJSSHa3flMn74hNwDCnraubUgvmjnuEp1rvafreMZNMqSV2L3DrHW"
team_hook = "https://mediastep.webhook.office.com/webhookb2/029355ca-7144-4c6b-bffb-e56d3b684dfa@8b318df0-a908-4fa0-8c6c-8a521ce935e1/IncomingWebhook/1f2e84b11d6c47718a1a4f405666611d/58868632-f34e-4629-bb02-9ce320e5d8f1"
current_time = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))
current_time_formatted = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                  
def notification_email_online():
    data = {"content": '{} is ONLINE - Uploaded to Play Store on {}. Link: {}'.format(app_name, current_time_formatted, full_link)}
    response = requests.post(discord_hook, json = data)
    print('Discord Notification Sent: {}'.format(response))
    teams_notification = pymsteams.connectorcard(team_hook)
    teams_notification.color('03AAF9')
    teams_notification.title('ONLINE - {} is now on Play Store. Uploaded on: {}'.format(app_name, current_time_formatted))
    teams_notification.text('Link: {}'.format(full_link))
    teams_notification.send()
    
def notification_email_offline():
    data = {"content": '{} is in REVIEW - Uploaded to Play Store on {}. Link: {}'.format(app_name, current_time_formatted, full_link)}
    response = requests.post(discord_hook, json = data)
    print('Discord Notification Sent: {}'.format(response))
    teams_notification = pymsteams.connectorcard(team_hook)
    teams_notification.color('DA420F')
    teams_notification.title('OFFLINE - {} is in REVIEW. Uploaded on: {}'.format(app_name, current_time_formatted))
    teams_notification.text('Link: {}'.format(full_link))
    teams_notification.send()

def appname_reviewing():
    data = {"content": 'APP_NAME REVEWING: Name of {} is in REVIEW .Submitted on {}. Link: {}'.format(app_name, current_time_formatted, full_link)}
    response = requests.post(discord_hook, json=data)
    print('Discord Notification Sent: {}'.format(response))
    teams_notification = pymsteams.connectorcard(team_hook)
    teams_notification.color('DA420F')
    teams_notification.title('APP_NAME REVIEWING: Name of {} is in REVIEW. Submitted on: {}'.format(app_name, current_time_formatted))
    teams_notification.text('Link: {}'.format(full_link))
    teams_notification.send()

def appname_online():
    data = {"content": 'APP_NAME ONLINE: Name of {} had been changed - Submitted on {}. Link: {}'.format(app_name, current_time_formatted, full_link)}
    response = requests.post(discord_hook, json = data)
    print('Discord Notification Sent: {}'.format(response))
    teams_notification = pymsteams.connectorcard(team_hook)
    teams_notification.color('03AAF9')
    teams_notification.title('APP_NAME ONLINE: Name of {} had been changed. Submitted on: {}'.format(app_name, current_time_formatted))
    teams_notification.text('Link: {}'.format(full_link))
    teams_notification.send()
    
def newapp_monitoring():
    while True:
        content = requests.get(full_link)
        result = content.text
        filter = result.find('com.')
        if int(filter) == -1:
            print('App is still in review. Sent notification. Sleeping...')
            notification_email_offline()
            time.sleep(7200)
        else:
            print('App is Online. Sent notification. Adios!')
            notification_email_online()
            break

def appinfo_editing():
    while True:
        app = webdriver.Chrome(ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        app.minimize_window()
        app.get(full_link)
        info = app.find_element(By.XPATH, """//span[contains(text(),'{}')]""".format(app_name))
        if info.text == app_name:
            appname_online()
            print('App Name changed. Sent notification.')
            break
        else:
            appname_reviewing()
            print('App Name still in REVIEW.')
            time.sleep(7200)

try:
    while True:
        tracking_type = input('Input: 1 as new application submit | 2 as editing app_name: ')            
        if int(tracking_type) == 1:
            newapp_monitoring()
            break
        elif int(tracking_type) == 2:
            appinfo_editing()
            break
        else:
            print('CHOOSE THE CORRECT OPTION!')
except KeyboardInterrupt:
    print('ERROR')
