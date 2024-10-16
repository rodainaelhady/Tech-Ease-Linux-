import subprocess
import customtkinter as ctk
from PIL import Image
import os

class NetworkCheck(ctk.CTkFrame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)

        back_icon = ctk.CTkImage(Image.open("images/home.png"), size=(20, 20))
        back_button = ctk.CTkButton(self, text="Home", font=("Comic Sans MS", 20), height=35, image=back_icon, compound="left",
                                     command=lambda: show_frame(None))
        back_button.pack(side=ctk.TOP, anchor=ctk.W, padx=(10, 0), pady=(10, 0))

        # عنوان الصفحة في المنتصف
        network_image = ctk.CTkImage(Image.open("images/network2.png"), size=(50, 50))        
        label = ctk.CTkLabel(self, text="Network Check ", font=("Comic Sans MS", 60), image=network_image, compound='right')
        label.pack(pady=(20, 20))

        self.result_textbox = ctk.CTkTextbox(self, 
                                              width=600, 
                                              height=300, 
                                              corner_radius=10, 
                                              fg_color="#2B2B2B",  
                                              text_color="white",   
                                              font=("Comic Sans MS", 15))   
        self.result_textbox.pack(pady=20)

        reset_image = ctk.CTkImage(Image.open("images/reset.png"), size=(30, 30))
        reset_button = ctk.CTkButton(self, text="Reset Network", font=("Comic Sans MS", 30), command=self.show_password_window, image=reset_image, compound="right")
        reset_button.pack(pady=20)

    def show_password_window(self):
        self.password_window = ctk.CTkToplevel(self)
        self.password_window.title("Enter Password")
        self.password_window.geometry("300x200")

        label = ctk.CTkLabel(self.password_window, text="Please enter your password:", font=("Comic Sans MS", 20))
        label.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.password_window, show="*", width=200)
        self.password_entry.pack(pady=10)

        submit_button = ctk.CTkButton(self.password_window, text="Submit", command=self.reset_network)
        submit_button.pack(pady=10)

    def reset_network(self):
        password = self.password_entry.get()  
        self.password_window.destroy()  

        self.result_textbox.delete('1.0', ctk.END)  
        try:
            self.result_textbox.insert(ctk.END, "Releasing IP address...\n")
            command_down = f'echo {password} | sudo -S ifconfig eth0 down'
            subprocess.run(command_down, shell=True, check=True)

            self.result_textbox.insert(ctk.END, "Renewing IP address...\n")
            command_renew = f'echo {password} | sudo -S dhclient eth0'
            subprocess.run(command_renew, shell=True, check=True)

            self.result_textbox.insert(ctk.END, "Network settings reset successfully.\n")
        except subprocess.CalledProcessError as e:
            self.result_textbox.insert(ctk.END, f"An error occurred while resetting network settings: {e}\n")

def main():
    app = ctk.CTk()
    app.title("Network Reset Tool")
    app.geometry("800x600")

    network_check_frame = NetworkCheck(app, show_frame=lambda x: None)
    network_check_frame.pack(expand=True, fill="both")

    app.mainloop()

if __name__ == "__main__":
    main()
