import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Sidebar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Sidebar.TFrame")
        self.controller = controller
        self.selected_button = None
        self.buttons = []
        self.create_widgets()
        
    def create_widgets(self):
        # Sidebar Header
        self.header_frame = ttk.Frame(self, style="SidebarHeader.TFrame")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        logo_img = Image.open("app/assets/images/clinic_logo.png").resize((40, 40))
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        ttk.Label(self.header_frame, image=self.logo_photo, background="#2c3e50").pack(side="left", padx=10)
        ttk.Label(self.header_frame, text="My Clinic", style="SidebarTitle.TLabel").pack(side="left")
        
        # Navigation Buttons
        nav_items = [
            ("dashboard", "Dashboard", self.show_dashboard),
            ("patients", "Patients", self.show_patients),
            ("emergency", "Emergency", self.show_emergency),
            ("medications", "Medications", self.show_medications),
            ("reports", "Reports", self.show_reports),
            ("settings", "Settings", self.show_settings)
        ]
        
        for icon, text, command in nav_items:
            btn = self.create_nav_button(icon, text, command)
            self.buttons.append(btn)
            
        # System Info
        self.info_frame = ttk.Frame(self, style="SidebarInfo.TFrame")
        self.info_frame.pack(side="bottom", fill="x", pady=10)
        
        ttk.Label(self.info_frame, text="v1.0.0", style="SidebarInfo.TLabel").pack()
        ttk.Label(self.info_frame, text="© 2018 My Clinic", style="SidebarInfo.TLabel").pack()
        
    def create_nav_button(self, icon_name, text, command):
        frame = ttk.Frame(self, style="NavButton.TFrame")
        frame.pack(fill="x", padx=5, pady=2)
        
        # Load icon
#        icon_img = Image.open(f"app/assets/icons/{icon_name}.png").resize((24, 24))
 #       icon_photo = ImageTk.PhotoImage(icon_img)
        
        btn = ttk.Button(
            frame,
 #           image=icon_photo,
            text=f"  {text}",
            compound="left",
            style="NavButton.TButton",
            command=lambda: self.handle_button_click(frame, command)
        )
 #       btn.image = icon_photo  # Keep reference
        btn.pack(fill="x", ipady=5)
        
        # Hover effects
        btn.bind("<Enter>", lambda e, f=frame: f.configure(style="NavButtonHover.TFrame"))
        btn.bind("<Leave>", lambda e, f=frame: (
            f.configure(style="NavButton.TFrame") if f != self.selected_button else None
        ))
        
        return frame
        
    def handle_button_click(self, frame, command):
        # Update visual selection
        if self.selected_button:
            self.selected_button.configure(style="NavButton.TFrame")
        self.selected_button = frame
        self.selected_button.configure(style="NavButtonActive.TFrame")
        
        # Execute associated command
        command()
        
    def show_dashboard(self):
        self.controller.show_frame("Dashboard")
        
    def show_patients(self):
        self.controller.show_frame("Patients")
        
    def show_emergency(self):
        self.controller.show_frame("Emergency")
        
    def show_medications(self):
        self.controller.show_frame("Medications")
        
    def show_reports(self):
        self.controller.show_frame("Reports")
        
    def show_settings(self):
        self.controller.show_frame("Settings")