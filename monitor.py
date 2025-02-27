import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from plyer import notification
import time
import pygame

# Your appointment page URL (Replace with the actual link that you got from email with title "Swiss-Visa: appointment xxxxxxxx" after booking an appointment at Swiss consulate website. The website contains your personal token so you can directly access this website by simply copying and pasting to search bar of browser)
APPOINTMENT_URL = "https://www.ch-edoc-reservation.admin.ch/#/session?token=your_token&locale=en-US"

# Email configuration (Replace with your intended email addresses and app password)
SENDER_EMAIL = "sender@gmail.com"  # Replace this with the sender email address
SENDER_PASSWORD = "app_password_of_sender_gmail"  # Replace this with the sender email address's app password (need 2-step verification enabled)
RECEIVER_EMAIL = "receiver@gmail.com"  # Replace this with the receiver email address

DECISION = ""

def send_email(subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server and send the email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_appointment():
    # "--headless" option is not working for some reason, so I have replaced it with driver.minimize_window() to minimize the effect of popping browser window
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    # 1 for booking, 2 for rescheduling
    if DECISION == "1":
        try:
            driver.get(APPOINTMENT_URL)
            wait = WebDriverWait(driver, 10)

            # Wait and click the "Next free appointments" button
            next_free_btn = wait.until(EC.element_to_be_clickable((By.ID, "bookingListBtn")))
            next_free_btn.click()

            time.sleep(3)  # Wait for pop-up to load

            # Check if "No entries found" message exists
            try:
                no_entries_msg = driver.find_element(By.XPATH, "//p[contains(text(), 'No entries found')]")
                print("❌ No appointments available.")

            except:
                print("✅ Appointments might be available!")
                pygame.mixer.init()
                pygame.mixer.music.load('siren.mp3')
                pygame.mixer.music.play()
                # Send desktop notification
                notification.notify(
                    title="Visa Appointment Alert",
                    message="Appointments might be available! Check now.",
                    timeout=10,
                )
                # Edit the email content as needed
                send_email(
                    subject="From your script: You have a free visa appointment!",
                    body="The script has completed the check for appointments. Please check if appointments are available."
                )
        except Exception as e:
            print(f"Error: {e}")

        finally:
            driver.quit()
    else:
        try:
            driver.get(APPOINTMENT_URL)
            wait = WebDriverWait(driver, 10)

            # Wait and click the "Reschedule" button
            reschedule_btn = wait.until(EC.element_to_be_clickable((By.ID, "rebookBtn")))
            reschedule_btn.click()

            # Wait and click the "Next free appointments" button
            next_free_btn = wait.until(EC.element_to_be_clickable((By.ID, "bookingListBtn")))
            next_free_btn.click()

            time.sleep(3)  # Wait for pop-up to load

            # Check if more than 1 appointment is available
            try:
                table_rows = driver.find_elements(By.CSS_SELECTOR, "table.mat-table tbody tr")
                if len(table_rows) > 1:
                    raise Exception("Other appointments available")
                else:
                    print("❌ No other appointments available.")

            except:
                print("✅ Other appointments might be available!")
                pygame.mixer.init()
                pygame.mixer.music.load('siren.mp3')
                pygame.mixer.music.play()
                # Send desktop notification
                notification.notify(
                    title="Visa Appointment Alert",
                    message="Appointments might be available! Check now.",
                    timeout=10,
                )
                # Edit the email content as needed
                send_email(
                    subject="From your script: You have a possible visa appointment for rescheduling!",
                    body="The script has completed the check for appointments. Please check if other appointments are available."
                )
        except Exception as e:
            print(f"Error: {e}")

        finally:
            driver.quit()

def main():
    # Run the script periodically
    DECISION = input("Do you want to find an (1) available appointment or (2) reschedule your appointment? Choose 1 or 2: ")
    if DECISION == "1":
        print("Checking for available appointments for booking every minute...")
    elif DECISION == "2":
        print("Checking for available appointments for rescheduling every minute...")
    else:
        print("Invalid input. Please restart the script and choose 1 or 2.")
        exit()
    while True:
        check_appointment()
        time.sleep(60)  # Wait 1 minute before checking again

if __name__ == "__main__":
    main()