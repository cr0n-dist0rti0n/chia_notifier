"""
This program will email you when your plots increase or you win Chia. It has been writen to use Gmail but can be modified for any email service that will accept Less Secure Apps. My recommnedation is you setup an email address you do not care about to as a notifier email. In google you must enable the Less Secure Apps option for this program to work: 

https://support.google.com/accounts/answer/6010255?hl=en 
https://support.google.com/a/answer/6260879?hl=en

Finally, for this to work you must first start the Chia virtual environment in the CLI/Terminal/Commandline etc. This python program requires python3 and the following dependancies which can be install with pip if they are not already installed:

time
os
re
smtplib
getpass

"""

import time
import os
import re
import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Code for Email
gmail_user = input("Enter your gmail address: ")
gmail_password = getpass.getpass(prompt=f'\n{gmail_user} Password: ', stream=None) 
print("\n")

# Check Passowrd
while True:
    print("\nChecking Password")
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.close()
    except (smtplib.SMTPAuthenticationError):
        print("\nWrong Password\n")
        gmail_password = getpass.getpass(prompt=f'{gmail_user} Password: ', stream=None)
        continue
    break

# Get Initial Chia Data
os.system("chia farm summary > chia_notification.log")
farm_sum =  open('chia_notification.log', 'r')

for line in farm_sum:
    if "Total chia farmed:" in line:
        total_chia = re.findall("\d+\.\d+", line)
    if "Plot count:" in line:
        plot_count = re.findall("\d+", line)
    if "Total size of plots:" in line:
        total_plots = re.findall("\d+\.\d+", line)
    if "Estimated network space:" in line:
        total_network = re.findall("\d+\.\d+", line)
    if "Expected time to win:" in line:
        time_win = line

total_chia = float(total_chia[0])
plot_count = int(plot_count[0])
total_plots = float(total_plots[0])
total_network = float(total_network[0])

total_chia_pre = total_chia
total_plots_pre = total_plots

# Notification Loop
while True:
    os.system("chia farm summary > chia_notification.log")
    farm_sum =  open('chia_notification.log', 'r')
    
    try:    
        for line in farm_sum:
            if "Farming status:" in line:
                farming_status = line
            if "Total chia farmed:" in line:
                total_chia = re.findall("\d+\.\d+", line)
            if "Plot count:" in line:
                plot_count = re.findall("\d+", line)
            if "Total size of plots:" in line:
                total_plots = re.findall("\d+\.\d+", line)
            if "Estimated network space:" in line:
                total_network = re.findall("\d+\.\d+", line)
            if "Expected time to win:" in line:
                time_win = line
        
        farm_sum.close()
        total_chia = float(total_chia[0])
        plot_count = int(plot_count[0])
        total_plots = float(total_plots[0])
        total_network = float(total_network[0])
        
    except:
        farm_sum.close()
        continue
    
    if total_chia != total_chia_pre:
        chia_dif = total_chia - total_chia_pre
        total_chia_pre = total_chia
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Congrats: You Have {total_chia} Chia"
        msg['From'] = gmail_user
        msg['To'] = '[ENTER EMAIL ADDRESSES YOU WANT TO SEND EMAIL TO SEPERATED BY COMMA]'
    
        email_html = f"""\
        <html>
        <head></head>
        <body>
    
        <p><img src="https://s.yimg.com/ny/api/res/1.2/Vu2Ur3t68t1KsKcNL28ZrA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTM3MS4y/https://s.yimg.com/uu/api/res/1.2/2ZGjV0RIRronwewQKZ1UJw--~B/aD0yMzI7dz02MDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/news_direct/ce6147fdd35ccf00e11e44ec8b05fcdb" alt="Chia Logo" width="600" height="232" /></p>
        <p>&nbsp;</p>
        <p><strong>Congratulations!</strong></p>
        <p><strong>You just won {chia_dif} Chia!</strong></p>
        <p><strong>You now have {total_chia} chia!</strong></p>
        <p><span style="color: #ff6600;"><strong>*************************</strong></span></p>
        <p>{farming_status}<br />
        Total chia farmed: {total_chia}<br />
        Plot count: {plot_count}<br />
        Total size of plots: {total_plots} TiB<br />
        Estimated network space: {total_network} PiB<br />
        {time_win}</p>
    
        </body>
        </html>
        """
        msg.attach(MIMEText(email_html, 'html'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, msg['To'], msg.as_string())
        server.close()
    
        
    if total_plots != total_plots_pre:
        plots_dif = (total_plots - total_plots_pre)*1000
        total_plots_pre = total_plots
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Congrats: You Have {total_plots} TiB Plots"
        msg['From'] = gmail_user
        msg['To'] = '[ENTER EMAIL ADDRESSES YOU WANT TO SEND EMAIL TO SEPERATED BY COMMA]'
    
        email_html = f"""\
        <html>
        <head></head>
        <body>
    
        <p><img src="https://s.yimg.com/ny/api/res/1.2/Vu2Ur3t68t1KsKcNL28ZrA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTM3MS4y/https://s.yimg.com/uu/api/res/1.2/2ZGjV0RIRronwewQKZ1UJw--~B/aD0yMzI7dz02MDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/news_direct/ce6147fdd35ccf00e11e44ec8b05fcdb" alt="Chia Logo" width="450" height="174" /></p>
        <p>&nbsp;</p>
        <p><strong>Plotter just finished creating {plots_dif} GiB in plot space!</strong></p>
        <p><strong>You now have created {total_plots} TiB in plots!</strong></p>
        <p><span style="color: #ff6600;"><strong>*************************</strong></span></p>
        <p>{farming_status}<br />
        Total chia farmed: {total_chia}<br />
        Plot count: {plot_count}<br />
        Total size of plots: {total_plots} TiB<br />
        Estimated network space: {total_network} PiB<br />
        {time_win}</p>
    
        </body>
        </html>
        """
        msg.attach(MIMEText(email_html, 'html'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, msg['To'], msg.as_string())
        server.close()
        
    
    # Pause loop for 10 minutes
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print('\n', current_time, '\n')
    print(os.system('chia farm summary'))
    print('\n ************************ \n')
    time.sleep(600)
