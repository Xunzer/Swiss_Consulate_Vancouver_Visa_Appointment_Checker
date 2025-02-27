# Swiss_Consulate_Vancouver_Visa_Appointment_Checker
A Python script to check for available visa appointments at the Swiss Consulate General in Vancouver.

## Install required modules
Run the following command:
```shell
pip install selenium webdriver-manager plyer pygame
```

## Modify appointment URL and emails
```python
# Your appointment page URL (Replace with the actual link that you got from email with title "Swiss-Visa: appointment xxxxxxxx" after booking an appointment at Swiss consulate website. The website contains your personal token so you can directly access this website by simply copying and pasting to search bar of browser)
APPOINTMENT_URL = "https://www.ch-edoc-reservation.admin.ch/#/session?token=your_token&locale=en-US"

# Email configuration (Replace with your intended email addresses and app password)
SENDER_EMAIL = "sender@gmail.com"  # Replace this with the sender email address
SENDER_PASSWORD = "app_password_of_sender_gmail"  # Replace this with the sender email address's app password (need 2-step verification enabled)
RECEIVER_EMAIL = "receiver@gmail.com"  # Replace this with the receiver email address
```

## Run the Python script
```shell
python3 monitor.py
```

## Enter your decision to either find a free appointment or reschedule an existing one
```shell
Do you want to find an (1) available appointment or (2) reschedule your appointment? Choose 1 or 2: [enter 1 or 2]
```

## Completion
Congratulations! You've successfully set up the appointment checker script.
