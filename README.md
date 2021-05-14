# chia_notifier
Uses email to notify you of chia plots completed and any chia you have farmed. 

This program will email you when your plots increase or you win Chia. It has been writen to use Gmail but can be modified for any email service that will accept Less Secure Apps. My recommnedation is you setup an email address you do not care about to as a notifier email. In google you must enable the Less Secure Apps option for this program to work: 

https://support.google.com/accounts/answer/6010255?hl=en 

https://support.google.com/a/answer/6260879?hl=en

Finally, for this to work you must first start the Chia virtual environment in the CLI/Terminal/Commandline etc. This python program requires python3 and the following dependancies which can be install with pip3 if they are not already installed:

time,
os,
re,
smtplib,
getpass
