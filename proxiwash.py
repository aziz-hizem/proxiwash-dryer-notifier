import os
import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from win10toast import ToastNotifier  # Import ToastNotifier from win10toast

# Function to send notification
def send_notification(message):
    # Create a ToastNotifier object
    toaster = ToastNotifier()
    
    # Display the notification
    toaster.show_toast(
        "Washing Machine Status",  # Title of the notification
        message,  # Message content
        icon_path="icon.ico",  # Path to the icon file
        duration=0  # Make the notification persistent
    )

# Function to open a pop-up window when the washing cycle is finished
def show_completion_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Show pop-up window
    messagebox.showinfo("Drying is finished !", "You can take your Clothes !")

# Function to check washing machine status
def check_washing_machine_status(machine_number):
    # Set up Edge options
    edge_options = Options()
    edge_options.use_chromium = True

    # Path to your Edge driver executable
    edge_driver_path = r'C:\Users\PCS\Documents\edgedriver_win64\msedgedriver.exe'

    # Start the WebDriver and open the website
    driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)
    driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE")  # Replace with the URL of your website
    time.sleep(2)  

    # Find the element containing the status of your washing machine based on the machine number
    machine_xpath = f"//*[@id='app']/main[1]/div[1]/div[4]/div[1]/div[1]/div[{machine_number}]/div[1]/h3[1]"
    try:
        machine_status_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, machine_xpath))
        )
        machine_status = machine_status_element.text
        print(f"Machine {machine_number} status:", machine_status.lower())
        
        # Check if the machine status indicates it's available
        if machine_status.lower() == "available":
            print("Your washing cycle is finished! Python Terminal")
            send_notification("Your washing cycle is finished!")
            show_completion_popup()
        else:
            print("Your washing machine is still busy.")
        
    except Exception as e:
        print("Error:", e)

# Function to create GUI for selecting machine number
def select_machine():
    def handle_selection(machine_number):
        root.destroy()  # Close the selection window
        check_washing_machine_status(machine_number)
    
    root = tk.Tk()
    root.title("Choose Your Machine !")
    root.geometry("300x250")  # Set window size
    
    # Define custom font
    custom_font = ("Segoe UI", 12)
    
    label = tk.Label(root, text="Choose Your Machine !", font=("Segoe UI", 20))
    label.pack(pady=20)
    
    # Function to handle button hover
    def on_enter(btn):
        btn.config(bg="turquoise")
    
    # Function to handle button hover exit
    def on_leave(btn):
        btn.config(bg="grey")
    
    # Define fixed button width
    button_width = 60
    
    # Button for machine 2
    btn_machine_2 = tk.Button(root, text="2", font=custom_font, width=button_width, padx=20, pady=10, command=lambda: handle_selection(2), bd=2, relief="solid", highlightbackground="red")
    btn_machine_2.pack(pady=10)
    btn_machine_2.bind("<Enter>", lambda event, btn=btn_machine_2: on_enter(btn))
    btn_machine_2.bind("<Leave>", lambda event, btn=btn_machine_2: on_leave(btn))
    
    # Button for machine 3
    btn_machine_3 = tk.Button(root, text="3", font=custom_font, width=button_width, padx=20, pady=10, command=lambda: handle_selection(3), bd=2, relief="solid", highlightbackground="red")
    btn_machine_3.pack(pady=10)
    btn_machine_3.bind("<Enter>", lambda event, btn=btn_machine_3: on_enter(btn))
    btn_machine_3.bind("<Leave>", lambda event, btn=btn_machine_3: on_leave(btn))
    
    root.mainloop()

# Call the function to select machine
select_machine()
