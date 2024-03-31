import os
import sys
import time
import tkinter as tk
import winsound
import keyboard
import threading
from pynput import keyboard
from PIL import Image, ImageTk 
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from win10toast import ToastNotifier  
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to send notification
def send_notification(message):
    # Create a ToastNotifier object
    toaster = ToastNotifier()
    
    # Display the notification
    toaster.show_toast(
        "Drying Machine Status",  # Title of the notification
        message,  # Message content
        icon_path=resource_path(r"C:\Users\PCS\Downloads\ProxiWash-Automation\icon1.ico"),  # Path to the icon file
        # Make the notification persistent (don't touch it)
    )
    print("Notification sent.")

    
# Function to check washing machine status
def check_washing_machine_status(machine_number, root):
   
    # Set up Edge options
    edge_options = Options()
    edge_options.use_chromium = True

    # Path to your Edge driver executable
    edge_driver_path = resource_path(r'C:\Users\PCS\Downloads\ProxiWash-Automation\edgedriver_win64\msedgedriver.exe')

    # Start the WebDriver and open the website
    driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)
    driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE")  # Replace with the URL of your website

    time.sleep(2) 
    
    try:
        # Click on a certain button (identified by XPath) before entering the while loop
        button = driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[2]")
        driver.execute_script("arguments[0].click();", button)
        print("Button clicked")
        #send_notification("Checking is on !")
        
    except Exception as e:
        print("Error:", e)
        
        
    washing_machine_button=driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[1]")
   
    print("checking machine n°",machine_number,"...")
    
    def on_key_press(key):
        try:
            # Check if the pressed key is Escape
            if key == keyboard.Key.f3:
                print("Exit Key : F3 pressed")
                driver.quit()
                quit()
                os._exit(0)
        except AttributeError:
            pass
    
   # Start a separate thread to listen for keyboard events
    keyboard_listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press).start())
    keyboard_listener_thread.daemon = True
    keyboard_listener_thread.start()
        
    
    # machine 2 : //*[@id="app"]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h3[1]
    # machine 3 : //*[@id="app"]/main[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/h3[1]      
    
    # Find the element containing the status of your washing machine based on the machine number
    g56=1
    c=1 
    while c==1 :
        try:
            if machine_number==2 :
                time.sleep(2)
                machine_status_element = driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/h3[1]")
            elif machine_number==3 :
                time.sleep(2)
                machine_status_element = driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/h3[1]")

            if machine_status_element.text:
                machine_status_text = machine_status_element.text
                g56=1
                print(machine_status_text)
            else :
                g56=0 
            

        
            # Check if the machine status indicates it's busy
            if g56==1 :
                if machine_status_text.lower() in ["busy", "buzy", "finished"]:
                    time.sleep(10)
                    driver.execute_script("arguments[0].click();", washing_machine_button)
                    time.sleep(5)
                    driver.execute_script("arguments[0].click();", button)
                    if machine_status_text.lower() in ["busy", "buzy", "finished"]:
                        print("Your drying cycle is finished!")
                        c=0 
                        show_drying_complete_window(driver)
                        driver.quit()
                        os._exit(0)
                    
                    else:
                        c=1
                        print("The drying machine is either busy or not being used.")
                        time.sleep(20)
                        try :
                            driver.execute_script("arguments[0].click();", washing_machine_button)
                            time.sleep(2)
                            driver.execute_script("arguments[0].click();", button)
                        except Exception as e:
                            driver.refresh()
                            driver.execute_script("arguments[0].click();", button)
                        print("Rechecking")
                else:
                        c=1
                        print("The drying machine is either busy or not being used.")
                        time.sleep(20)
                        try :
                            driver.execute_script("arguments[0].click();", washing_machine_button)
                            time.sleep(2)
                            button.click()
                        except Exception as e :
                             driver.refresh()
                        print("Rechecking")
            elif g56==0 :
                c=1
                print("The drying machine is either busy or not being used.")
                time.sleep(20)
                try :
                    driver.execute_script("arguments[0].click();", washing_machine_button)
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", button)
                except Exception as e:
                    driver.refresh()
                    driver.execute_script("arguments[0].click();", button)     
        except StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Scrolling back to the top of the page...")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
            continue
 

# Function to create GUI for selecting machine number
def select_machine():
    def handle_selection(machine_number):
        root.destroy()  # Close the selection window
        print(machine_number)
        check_washing_machine_status(machine_number, root)  
    
    root = tk.Tk()
    root.title("Choose Your Machine !")
    
    #placement
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates for the window to be placed in the middle
    x_coordinate = int((screen_width - root.winfo_reqwidth()) / 2)
    y_coordinate = int((screen_height - root.winfo_reqheight()) / 2)

    # Set the geometry of the window to place it in the middle
    root.geometry("+{}-{}".format(x_coordinate, y_coordinate))

    
    # Define custom font
    custom_font = ("Segoe UI", 12)
    
    # Load the image
    original_image = Image.open(resource_path(r"C:\Users\PCS\Downloads\ProxiWash-Automation\icon1.ico"))
    
    # Resize the image
    width, height = 50, 50  # Set the desired width and height
    resized_image = original_image.resize((width, height))
    
    # Convert the resized image to PhotoImage
    image = ImageTk.PhotoImage(resized_image)
    
    # Display the image
    label_image = tk.Label(root, image=image)
    label_image.pack(pady=10)
    
    
    label = tk.Label(root, text="Choose Your Machine !", font=("Segoe UI", 20))
    label.pack(pady=20)
    
    # Function to handle button hover
    def on_enter(btn):
        btn.config(bg="cyan")
    
    # Function to handle button hover exit
    def on_leave(btn):
        btn.config(bg="turquoise")
     
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
    
    label2=tk.Label(root, text="By Aziz Hizem.", font=("Segoe UI", 9), fg="grey", padx=10, pady=10)
    label2.pack()
       
    root.mainloop()

def play_sound():
    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
    
  
#This function is not being used, still in dev phase    
def quit():
       
    # Function to exit the program
    def exit_program():
        #window.destroy()
        os._exit(0)
        
    window = tk.Tk()
    window.title("Program Terminated.")
    window.geometry("500x250")
    
    # Load the image
    original_image2 = Image.open(resource_path(r"C:\Users\PCS\Downloads\ProxiWash-Automation\bubbles.ico"))
    
    # Resize the image
    width, height = 50, 50  # Set the desired width and height
    resized_image2 = original_image2.resize((width, height))
    
    # Convert the resized image to PhotoImage
    image2 = ImageTk.PhotoImage(resized_image2)
    
    # Display the image
    label_image2 = tk.Label(window, image=image2)
    label_image2.pack(pady=10)
    
    # Create a label with the message
    label2 = tk.Label(window, text="Abort Mission !", font=("Segoe UI", 20), padx=10, pady=10)
    label2.pack()
    
    # Define custom font
    custom_font2 = ("Segoe UI", 12)
    
    # Function to handle button hover
    def on_enter(btn2):
        btn2.config(bg="cyan")
    
    # Function to handle button hover exit
    def on_leave(btn2):
        btn2.config(bg="turquoise")
     
    # Button for machine 2
    btn_done2 = tk.Button(window, background="turquoise", text="Quit", font=custom_font2, width=20, padx=20, pady=10, command=lambda: exit_program(), bd=2, relief="solid", highlightbackground="red")
    btn_done2.pack(pady=10)
    btn_done2.bind("<Enter>", lambda event, btn=btn_done2: on_enter(btn))
    btn_done2.bind("<Leave>", lambda event, btn=btn_done2: on_leave(btn))
    
    play_sound()
       
    # Run the tkinter event loop
    window.mainloop()
    

def show_drying_complete_window(driver):
    def over_and_out () :
        print("Over and Out.")
        window.destroy()  
        time.sleep(2)
        send_notification("Your drying cycle is finished. Arrivederci !")
        driver.quit()
        os._exit(0)
        
    
    # Create a new tkinter window
    window = tk.Tk()
    window.title("Drying Complete !")
    
    
    #placement
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates for the window to be placed in the middle
    x_coordinate = int((screen_width - window.winfo_reqwidth()) / 2)
    y_coordinate = int((screen_height - window.winfo_reqheight()) / 2)

    # Set the geometry of the window to place it in the middle
    window.geometry("+{}-{}".format(x_coordinate, y_coordinate))
    
    # Load the image
    original_image = Image.open(resource_path(r"C:\Users\PCS\Downloads\ProxiWash-Automation\icon2.ico"))
    
    # Resize the image
    width, height = 50, 50  # Set the desired width and height
    resized_image = original_image.resize((width, height))
    
    # Convert the resized image to PhotoImage
    image = ImageTk.PhotoImage(resized_image)
    
    # Display the image
    label_image = tk.Label(window, image=image)
    label_image.pack(pady=10)
    
    # Create a label with the message
    label = tk.Label(window, text="Drying is Complete!\nYou can get your clothes now!", font=("Segoe UI", 20), padx=10, pady=10)
    label.pack()
    
    
    # Define custom font
    custom_font = ("Segoe UI", 12)
    
    # Function to handle button hover
    def on_enter(btn):
        btn.config(bg="cyan")
    
    # Function to handle button hover exit
    def on_leave(btn):
        btn.config(bg="turquoise")
     
    # Button for machine 2
    btn_done = tk.Button(window, text="Okay !", font=custom_font, width=20, padx=20, pady=10, command=lambda: over_and_out(), bd=2, relief="solid", highlightbackground="red")
    btn_done.pack(pady=10)
    btn_done.bind("<Enter>", lambda event, btn=btn_done: on_enter(btn))
    btn_done.bind("<Leave>", lambda event, btn=btn_done: on_leave(btn))
    
    label2=tk.Label(window, text="By Aziz Hizem.", font=("Segoe UI", 9), fg="grey", padx=10, pady=10)
    label2.pack()
    
    play_sound()       
    # Run the tkinter event loop
    window.mainloop()
    
    
def close_window(window):
    """Function to close a specific Tkinter window."""
    window.destroy()
    


# Call the function to select machine and check its status
select_machine()
