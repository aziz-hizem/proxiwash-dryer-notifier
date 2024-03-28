from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from plyer import notification

# Function to send notification
def send_notification(message):
    notification.notify(
        title='Washing Machine Status',
        message=message,
        app_name='Washing Machine Notification',
        app_icon=r'C:\Users\PCS\Downloads\ProxiWash Automation\icon.ico',   
        timeout=None # Adjust the timeout as needed
       
    )

# Function to check washing machine status
def check_washing_machine_status():
    # Set up Edge options
    edge_options = Options()
    edge_options.use_chromium = True

    # Path to your Edge driver executable
    edge_driver_path = r'C:\Users\PCS\Documents\edgedriver_win64\msedgedriver.exe'

    # Start the WebDriver and open the website
    driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)
    driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE")  # Replace with the URL of your website

    # Find the element containing the status of your washing machine
    try:
        # Click on a certain button (identified by XPath) before entering the while loop
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[2]"))  
        )
        button.click()
        print("Button clicked")
        
    except Exception as e:
        print("Error clicking button:", e)
    
    print("Notification icon path:", r'C:\Users\PCS\Downloads\ProxiWash Automation\icon.ico')
    send_notification("Checking is on !")

    while True:
        try:
            machine_status_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h3[1]"))
            )
            machine_status = machine_status_element.text     
            print(machine_status.lower())
            state = machine_status.lower() 
        except Exception as e2:
            print("Error getting machine status:", e2)
        
        # Check if the machine status indicates it's available
        if state == "available":
            print("Your washing cycle is finished! Python Terminal")
            send_notification("Your washing cycle is finished!")
            break
        else:
            time.sleep(60)
            
    # Close the browser
    driver.quit()

# Call the function
check_washing_machine_status()
