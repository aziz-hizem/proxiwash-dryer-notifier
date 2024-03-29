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
        duration=0  # Make the notification persistent (don't touch it)
    )

    
# Function to open a pop-up window when the washing cycle is finished
def show_completion_popup(root):
    messagebox.showinfo("Washing Completed !", "Go Take your Clothes !")

# Function to check washing machine status
def check_washing_machine_status(root, machine_number):
    # Set up Edge options
    edge_options = Options()
    edge_options.use_chromium = True

    # Path to your Edge driver executable
    edge_driver_path = r'C:\Users\PCS\Documents\edgedriver_win64\msedgedriver.exe'

    # Start the WebDriver and open the website
    driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)
    driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE")  # Replace with the URL of your website

    time.sleep(2) 
    
    try:
        # Click on a certain button (identified by XPath) before entering the while loop
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[2]"))  
        )
        button.click()
        print("Button clicked")
        
    except Exception as e:
        print("Error:", e)
        
    print("checking machine n°",machine_number,"...")
    send_notification("Checking is on !")
    
    
    # machine 2 : //*[@id="app"]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h3[1]
    # machine 3 : //*[@id="app"]/main[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/h3[1]

    # Find the element containing the status of your washing machine based on the machine number
    try:
        if machine_number==2 :
            machine_status_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h3[1]"))
            )
        elif machine_number==3 :
            machine_status_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/main[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/h3[1]"))
            )
            
        machine_status = machine_status_element.text
        print("Machine ",machine_number," status:", machine_status)
        
        # Check if the machine status indicates it's available
        if machine_status.lower() == "available":
            print("Your washing cycle is finished! Python Terminal")
            send_notification("Your washing cycle is finished!")
            # Schedule the show_completion_popup function to run after a delay
            root.after(1000, show_completion_popup)  # 1000 milliseconds (1 second) delay
        else:
            print("Your washing machine is still busy.")
        
    except Exception as e:
        print("Error:", e)
    

# Function to create GUI for selecting machine number
def select_machine():
    def handle_selection(machine_number):
        root.destroy()  # Close the selection window
        print(machine_number)
        check_washing_machine_status(root, machine_number)  # Pass root as an argument        
    
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
     
    # Button for machine 2
    btn_machine_2 = tk.Button(root, text="2", font=custom_font, width=20, padx=20, pady=10, command=lambda: handle_selection(2), bd=2, relief="solid", highlightbackground="red")
    btn_machine_2.pack(pady=10)
    btn_machine_2.bind("<Enter>", lambda event, btn=btn_machine_2: on_enter(btn))
    btn_machine_2.bind("<Leave>", lambda event, btn=btn_machine_2: on_leave(btn))
    
    
    # Button for machine 3
    btn_machine_3 = tk.Button(root, text="3", font=custom_font, width=20, padx=20, pady=10, command=lambda: handle_selection(3), bd=2, relief="solid", highlightbackground="red")
    btn_machine_3.pack(pady=10)
    btn_machine_3.bind("<Enter>", lambda event, btn=btn_machine_3: on_enter(btn))
    btn_machine_3.bind("<Leave>", lambda event, btn=btn_machine_3: on_leave(btn))
       
    root.mainloop()

# Call the function to select machine and check its status
select_machine()
