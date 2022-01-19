import datetime
import requests
import time
import pytz
import pymsteams

new_appname = input("Enter new app_name: ")
bundle_id = input("Which bundle_id?: ")
link = 'https://play.google.com/store/apps/details?id='
app_link = link + bundle_id
discord_hook = "https://discord.com/api/webhooks/933276671904198676/iqZ2wVpoztNckBMgN4w4jaJFIxQFzGwX-zM7lF9IdQf-wgGUP33R-OCYhd3SwiJ65T5g"
team_hook = "https://mediastep.webhook.office.com/webhookb2/029355ca-7144-4c6b-bffb-e56d3b684dfa@8b318df0-a908-4fa0-8c6c-8a521ce935e1/IncomingWebhook/1f2e84b11d6c47718a1a4f405666611d/58868632-f34e-4629-bb02-9ce320e5d8f1"
current_time = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))
                  
def notification_email_online():
    data = {"content": '{} is ONLINE - Submitted to Play Store on {}. Link: {}'.format(new_appname, current_time, app_link)}
    response = requests.post(discord_hook, json = data)
    print('Discord Notification Sent: {}'.format(response))
    teams_notification = pymsteams.connectorcard(team_hook)
    teams_notification.color('03AAF9')
    teams_notification.title('ONLINE - {} is now on Play Store. Submitted on: {}'.format(new_appname, current_time))
    teams_notification.text('Link: {}'.format(app_link))
    teams_notification.send()
    
def notification_email_offline():
    data = {"content": '{} is in REVIEW - Submitted to Play Store on {}. Link: {}'.format(new_appname, current_time, app_link)}
    response = requests.post(discord_hook, json = data)
    print('Discord Notification Sent: {}'.format(response))
    teams_notification = pymsteams.connectorcard(team_hook)
    teams_notification.color('DA420F')
    teams_notification.title('OFFLINE - {} is in REVIEW. Submitted on: {}'.format(new_appname, current_time))
    teams_notification.text('Link: {}'.format(app_link))
    teams_notification.send()
    
def newapp_monitoring():
    while True:
        content = requests.get(app_link)
        result = content.text
        filter = result.find('com.')
        if int(filter) == -1:
            print('App is still in Review. Sent notification. Sleeping...')
            notification_email_offline()
            time.sleep(7200)
        else:
            print('App is Online. Sent notification.')
            notification_email_online()
            break
newapp_monitoring()