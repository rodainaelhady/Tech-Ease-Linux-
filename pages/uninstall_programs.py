import os
import subprocess
import threading
import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image

class UninstallPrograms(ctk.CTkFrame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)

        arrow_image = ctk.CTkImage(Image.open("images/home.png"), size=(24, 24))
        self.back_button = ctk.CTkButton(self, text="Home", image=arrow_image, font=("Comic Sans MS", 20), height=35,
                                         compound="left", command=lambda: show_frame(None))
        self.back_button.pack(side="top", anchor="nw", padx=10, pady=(10, 0))

        clean_image = ctk.CTkImage(Image.open("images/clean2.png"), size=(50, 50))
        label = ctk.CTkLabel(self, text="Uninstall Programs", font=("Comic Sans MS", 60), image=clean_image, compound="right")
        label.pack(pady=(10, 20))

        self.programs_frame = ctk.CTkScrollableFrame(self)
        self.programs_frame.pack(expand=True, fill="both", pady=20)

        show_image = ctk.CTkImage(Image.open("images/show.png"), size=(30, 30))
        self.show_button = ctk.CTkButton(self, text="Show Installed Programs", image=show_image, compound="right",
                                         font=("Comic Sans MS", 30), command=self.list_installed_programs_thread)
        self.show_button.pack(pady=10)

    def list_installed_programs_thread(self):
        threading.Thread(target=self.list_installed_programs).start()

    def list_installed_programs(self):
        self.show_button.pack_forget()

        for widget in self.programs_frame.winfo_children():
            widget.destroy()

        command = 'dpkg --get-selections | grep -v deinstall'
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
            programs = result.stdout.splitlines()
            
            self.programs = [p.split()[0] for p in programs]  
            
            if not self.programs:
                messagebox.showinfo("Info", "No installed programs found.")
                return

            for idx, program in enumerate(self.programs, 1):  
                program_label = ctk.CTkLabel(self.programs_frame, text=program, font=("Comic Sans MS", 20))
                program_label.pack(side="top", anchor="w", padx=10)

                uninstall_image = ctk.CTkImage(Image.open("images/uninstall2.png"))
                uninstall_button = ctk.CTkButton(self.programs_frame, text="Uninstall", image=uninstall_image,
                                                 compound="right", font=("Comic Sans MS", 20),
                                                 command=lambda p=program: self.perform_uninstall_thread(p))
                uninstall_button.pack(side="top", anchor="e", padx=10)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while listing the installed programs: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def perform_uninstall_thread(self, program_name):
        threading.Thread(target=lambda: self.perform_uninstall(program_name)).start()

    def perform_uninstall(self, program_name):
        command = f'sudo apt remove -y {program_name}'
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"{program_name} uninstalled successfully!")
                self.list_installed_programs()  
            else:
                messagebox.showwarning("Warning", f"Failed to uninstall {program_name}. It might require manual removal.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while trying to uninstall {program_name}: {e}")

def main():
    app = ctk.CTk()
    app.title("Program Uninstaller")
    app.geometry("600x400")

    uninstall_frame = UninstallPrograms(app, show_frame=lambda x: None)
    uninstall_frame.pack(expand=True, fill="both")

    app.mainloop()

if __name__ == "__main__":
    main()
