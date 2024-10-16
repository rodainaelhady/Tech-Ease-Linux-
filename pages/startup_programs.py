import customtkinter as ctk
import os
import subprocess
import tkinter.messagebox as messagebox
from PIL import Image

class StartupPrograms(ctk.CTkFrame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)

        arrow_image = ctk.CTkImage(Image.open("images/home.png"), size=(24, 24))
        back_button = ctk.CTkButton(self, text="Home", image=arrow_image, font=("Comic Sans MS", 20), height=35,
                                     compound="left", command=lambda: show_frame(None))
        back_button.pack(pady=10, padx=10, anchor="nw")  

        startup_image = ctk.CTkImage(Image.open("images/startup.png"), size=(50, 50))
        label = ctk.CTkLabel(self, text="Startup Programs", image=startup_image, compound="right", font=("Comic Sans MS", 60))
        label.pack(pady=10)

        self.programs_frame = ctk.CTkFrame(self)
        self.programs_frame.pack(pady=10, fill="both", expand=True)

        self.current_page = 0
        self.items_per_page = 5  

        self.prev_button = ctk.CTkButton(self, text="Previous", font=("Comic Sans MS", 20), command=self.show_previous_page)
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.next_button = ctk.CTkButton(self, text="Next", font=("Comic Sans MS", 20), command=self.show_next_page)
        self.next_button.pack(side="right", padx=10, pady=10)

        self.programs = self.list_startup_programs()
        self.load_startup_programs()

    def load_startup_programs(self):
        for widget in self.programs_frame.winfo_children():
            widget.destroy()

        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page

        for name, status in self.programs[start_index:end_index]:
            program_frame = ctk.CTkFrame(self.programs_frame)
            program_frame.pack(pady=5, padx=10, fill="x")

            label = ctk.CTkLabel(program_frame, text=f"{name} ({status})", width=400, height=50, font=("Comic Sans MS", 20))
            label.pack(side="left", padx=(0, 10))

            disable_image = ctk.CTkImage(Image.open("images/disaple.png"))
            disable_button = ctk.CTkButton(program_frame, text="Disable", font=("Comic Sans MS", 20), image=disable_image, compound="right", command=lambda name=name: self.disable_startup_program(name))
            disable_button.pack(side="right")

        self.update_navigation_buttons()

    def list_startup_programs(self):
        result = subprocess.run(["systemctl", "list-unit-files", "--type=service", "--state=enabled"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")

        startup_programs = []

        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                service_name = parts[0]
                service_status = parts[1]
                startup_programs.append((service_name, service_status))

        return startup_programs

    def disable_startup_program(self, service_name):
        try:
            subprocess.run(["sudo", "systemctl", "disable", service_name], check=True)
            messagebox.showinfo("Success", f"Disabled service: {service_name}")
            self.programs = self.list_startup_programs()  
            self.load_startup_programs()  
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Failed to disable service: {service_name}")

    def show_next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.programs):
            self.current_page += 1
            self.load_startup_programs()

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_startup_programs()

    def update_navigation_buttons(self):
        if self.current_page == 0:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")

        if (self.current_page + 1) * self.items_per_page >= len(self.programs):
            self.next_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")

def main():
    app = ctk.CTk()
    app.title("Startup Programs Management")
    app.geometry("600x400")

    startup_programs_frame = StartupPrograms(app, show_frame=lambda x: None)
    startup_programs_frame.pack(expand=True, fill="both")

    app.mainloop()

if __name__ == "__main__":
    main()
