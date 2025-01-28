import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # type: ignore
from PIL import Image, ImageTk
from ...utils.validators import validate_phone

class PatientForm(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self.create_widgets()
        
    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        
        # Header
        ttk.Label(self, text="New Patient Registration", 
                 style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        
        # Form Fields
        self.create_form_field("Full Name:", 1, "full_name")
        self.create_phone_field("Phone:", 2)
        self.create_date_field("Birth Date:", 3)
        self.create_gender_field("Gender:", 4)
        self.create_comments_field("Comments:", 5)
        
        # Avatar Preview
        self.avatar_label = ttk.Label(self)
        self.avatar_label.grid(row=1, column=2, rowspan=4, padx=20)
        self.update_avatar()
        
    def create_form_field(self, label_text, row, field_name):
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="w", padx=10)
        entry = ttk.Entry(self, width=30)
        entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        setattr(self, f"{field_name}_entry", entry)
        
    def create_phone_field(self, label_text, row):
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="w", padx=10)
        self.phone_entry = ttk.Entry(self, width=30, validate="key")
        self.phone_entry['validatecommand'] = (self.register(validate_phone), '%P')
        self.phone_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        
    def create_date_field(self, label_text, row):
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="w", padx=10)
        self.birth_date_entry = DateEntry(
            self, 
            date_pattern="yyyy-mm-dd",
            background="white",
            foreground="black"
        )
        self.birth_date_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        
    def create_gender_field(self, label_text, row):
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="w", padx=10)
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(
            self, 
            textvariable=self.gender_var,
            values=["Male", "Female", "Other"],
            state="readonly"
        )
        self.gender_combobox.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        
    def create_comments_field(self, label_text, row):
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky="nw", padx=10)
        self.comments_text = tk.Text(self, width=30, height=4)
        self.comments_text.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        
    def update_avatar(self):
        gender = self.gender_var.get().lower()
        avatar_path = f"app/assets/images/{gender}_avatar.png" if gender else "default_avatar.png"
#        img = Image.open(avatar_path).resize((120, 120))
#        self.avatar_img = ImageTk.PhotoImage(img)
        self.avatar_label.config()#image=self.avatar_img)
        
    def get_form_data(self):
        return {
            "full_name": self.full_name_entry.get(),
            "phone": self.phone_entry.get(),
            "gender": self.gender_var.get(),
            "birth_date": self.birth_date_entry.get_date().isoformat(),
            "comments": self.comments_text.get("1.0", tk.END).strip()
        }