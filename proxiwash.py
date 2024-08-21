import os
import time
import customtkinter
import winsound
import threading
from pynput import keyboard
from PIL import Image 
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from plyer import notification


def send_notification(message):
    notification.app_name = "ProxiWash 1.7 By Aziz Hizem"
    notification.notify(
        title="Drying Machine Status",
        message=message,
        app_icon=("icons\\icon1.ico"),
        timeout=1
    )
  
    
def check_washing_machine_status(machine_number):
   
    # Set up Edge options
    edge_options = Options()
    edge_options.use_chromium = True

    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)
    driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE") 
    #send_notification("Checking is on !")
    time.sleep(2) 
    
    try:
        button = driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[2]")
        driver.execute_script("arguments[0].click();", button)
        print("Button clicked")
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
                    time.sleep(3)
                    driver.get("https://www.google.com")                     
                    time.sleep(2)
                    driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE")  
                    button = driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[2]")
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
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
            driver.get("https://www.proxiwash.com/laverie?code=82fc94&fbclid=IwAR04XPVHi0cGsI1CtQS-qWPLHjVAbsHtah8lm_ull0bNhLxpvbUtu5OwdqE")  
            button = driver.find_element(By.XPATH, "//*[@id='app']/main[1]/div[1]/div[2]/button[2]")
            driver.execute_script("arguments[0].click();", button)
            continue
 

def quit():
       
    # Function to exit the program
    def exit_program():
        #window.destroy()
        os._exit(0)
        
    window = customtkinter.CTk()
    window.title("Program Terminated.")
    window.geometry("450x210")
    
    window.iconbitmap("icons\\icon2.ico")
    
    custom_font = ("Roboto", 24)
    
    # Load the image
    image = customtkinter.CTkImage(light_image=Image.open("icons\\icon2.ico"),
	dark_image=Image.open("icons\\icon2.ico"),
	size=(50,50)) # WidthxHeight
       
    my_label = customtkinter.CTkLabel(window, text="", image=image)
    my_label.pack(pady=10)
    
    
    # Create a label with the message 
    label = customtkinter.CTkLabel(master=window, text="Abort Mission !", font=(custom_font, 20))
    label.pack(pady=10)
    
 
    btn_done = customtkinter.CTkButton(master=window,
                                text="Quit",
                                font=(custom_font,30),
                                text_color=("white","dark slate gray"),
                                width=270,
                                height=40,
                                border_width=2,
                                border_color=("white","black"),
                                corner_radius=20,
                                command=lambda:exit_program(), 
                                fg_color=("cyan","lightgray"),
                                hover_color=("#4ee89b","cyan")  
                                )
    btn_done.pack(pady=4)
    

    label = customtkinter.CTkLabel(master=window, text="By Aziz Hizem.",text_color="gray", font=(custom_font, 9),
                               width=120,
                               height=25,
                               corner_radius=20)
    label.pack(pady=3)
    
    play_sound()
       
    # Run the tkinter event loop
    window.mainloop()
    

def show_drying_complete_window(driver):
    def over_and_out () :
        print("Over and Out.")
        window.destroy()  
        time.sleep(2)
        driver.quit()
        os._exit(0)
        
    
    # Create a new tkinter window
    window = customtkinter.CTk()
    window.title("Drying Complete !")
    window.iconbitmap("icons\\bubbles.ico")
    window.geometry("400x220")
    
    custom_font = ("Roboto", 24)

    # Set the geometry of the window to place it in the middle
    #window.geometry("+{}+{}".format(x_coordinate, y_coordinate))
    
    # Load the image
    image = customtkinter.CTkImage(light_image=Image.open("icons\\bubbles.ico"),
	dark_image=Image.open("icons\\bubbles.ico"),
	size=(50,50)) # WidthxHeight
       
    my_label = customtkinter.CTkLabel(window, text="", image=image)
    my_label.pack(pady=10)
    
    
    # Create a label with the message 
    label = customtkinter.CTkLabel(master=window, text="Drying is Complete!\nYou can get your clothes now!", font=(custom_font, 20))
    label.pack(pady=10)
    
 
    # Okay Button
    #btn_done = tk.Button(window, text="Okay !", font=custom_font, width=20, padx=20, pady=10, command=lambda: over_and_out(), bd=2, relief="solid", highlightbackground="red")
    
    btn_done = customtkinter.CTkButton(master=window,
                                text="Okay !",
                                font=(custom_font,20),
                                text_color=("white","dark slate gray"),
                                width=270,
                                height=40,
                                border_width=3,
                                border_color=("white","black"),
                                corner_radius=20,
                                command=lambda:over_and_out(), 
                                fg_color=("cyan","lightgray"),
                                hover_color=("#4ee89b","cyan")       
                                )
    btn_done.pack(pady=4)
    

    label = customtkinter.CTkLabel(master=window, text="By Aziz Hizem.",text_color="gray", font=(custom_font, 9),
                               width=120,
                               height=25,
                               corner_radius=20)
    label.pack(pady=3)
      
    play_sound()       
    # Run the tkinter event loop
    window.mainloop()
   
    
def select_machine():
    def handle_selection(machine_number):
        root.destroy()  # Close the selection window
        print(machine_number)
        check_washing_machine_status(machine_number)  
    
    root = customtkinter.CTk()
    root.title("Choose Your Machine !")
    root.iconbitmap("icon.ico")
    
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates for the window to be placed in the middle
    x_coordinate = int((screen_width - root.winfo_reqwidth()) / 2)
    y_coordinate = int((screen_height - root.winfo_reqheight()) / 2)

    # Set the geometry of the window to place it in the middle
    #root.geometry("+{}+{}".format(x_coordinate, y_coordinate))
    root.geometry("300x360")
  
    
    # Define custom font
    custom_font = ("Roboto", 24)
    
    #image 
    my_image = customtkinter.CTkImage(light_image=Image.open("icons\\icon1.ico"),
	dark_image=Image.open("icons\\icon1.ico"),
	size=(50,50)) # WidthxHeight

    my_label = customtkinter.CTkLabel(root, text="", image=my_image)
    my_label.pack(pady=10)
    

    label = customtkinter.CTkLabel(master=root, text="Choose Your Machine !", font=(custom_font, 20))
    label.pack(pady=10)
    #label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    #must be n, ne, e, se, s, sw, w, nw, or center
    

    label = customtkinter.CTkLabel(master=root, text="(Use F3 to close the program later)",fg_color="light gray", font=(custom_font, 9),
                               text_color=("white","dark slate gray"),
                               width=120,
                               height=25,
                               corner_radius=20)
    label.pack(pady=10)
     
    # Button for machine 2
    btn_machine_2 = customtkinter.CTkButton(master=root,
                                text="2",
                                font=custom_font,
                                text_color=("white","dark slate gray"),
                                width=270,
                                height=32,
                                border_width=2,
                                border_color=("white","black"),
                                corner_radius=20,
                                command=lambda:handle_selection(2), 
                                fg_color=("cyan","lightgray"),
                                hover_color=("#4ee89b","cyan")    
                                )
    btn_machine_2.pack(pady=10)
    
    # Button for machine 3
    btn_machine_3= customtkinter.CTkButton(master=root,
                                text="3",
                                font=custom_font,
                                text_color=("white","dark slate gray"),
                                width=270,
                                height=32,
                                border_width=2,
                                border_color=("white","black"),
                                corner_radius=20,
                                command=lambda:handle_selection(3), 
                                fg_color=("cyan","lightgray"),
                                hover_color=("#4ee89b","cyan")        
                                )
    btn_machine_3.pack(pady=10)

    
    #aziz
    def aziz_click():
        s=customtkinter.get_appearance_mode()
        if s=="Light":
            customtkinter.set_appearance_mode("Dark")
        elif s=="Dark":
            customtkinter.set_appearance_mode("Light")
        pass
    
    
    aziz= customtkinter.CTkButton(master=root,
                                text="By Aziz Hizem.",
                                font=("Roboto", 9),
                                text_color="dark slate gray",
                                
                                width=120,
                                height=25,
                                
                                corner_radius=20,
                                command=lambda:aziz_click(), 
                                fg_color=("lavender", "lavender"),
                                hover_color="turquoise"       
                                )
    aziz.pack(pady=2)
   

    label = customtkinter.CTkLabel(master=root, text="Click my name...",text_color="dark gray", font=("Roboto", 9),
                               )
    label.pack()
    
      
    root.mainloop()


def play_sound():
    winsound.PlaySound("SystemExclamation",0)


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

# Call the function to select machine and check its status : Main program
select_machine()

