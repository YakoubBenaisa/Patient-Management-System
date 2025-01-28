import tkinter as tk
from tkinter import ttk
from .components.sidebar import Sidebar
from .components.patient_form import PatientForm
from ..models.services.patient_service import PatientService

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clinic Management System")
        self.configure_styles()
        self.patient_service = PatientService()
        self.create_widgets()
        self.center_window()
        self.refresh_table()
        
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Custom Styles
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#2c3e50")
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), foreground="#34495e")
        style.configure("Treeview", rowheight=30, font=("Helvetica", 10))
        style.map("Treeview", background=[("selected", "#3498db")])
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        # Main Container
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sidebar
        self.sidebar = Sidebar(main_container, self)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        
        # Content Area
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Patient Form
        self.patient_form = PatientForm(content_frame, self)
        self.patient_form.pack(fill="x", pady=(0, 10))
        
        # Table
        self.create_patient_table(content_frame)
        
        # Action Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Add Patient", 
                  command=self.add_patient, style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_patient).pack(side="left", padx=5)
        
    def create_patient_table(self, parent):
        self.table = ttk.Treeview(parent, columns=("ID", "Name", "Phone", "Gender", "Birth Date"), show="headings")
        
        # Configure columns
        columns = [
            ("ID", 80),
            ("Name", 200),
            ("Phone", 150),
            ("Gender", 100),
            ("Birth Date", 120)
        ]
        
        for col, width in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=width, anchor="center")
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)
        
    def add_patient(self):
        data = self.patient_form.get_form_data()
        if not data["full_name"] or not data["phone"]:
            self.show_error("Name and Phone are required fields")
            return
            
        self.patient_service.add_patient(data)
        self.refresh_table()
        self.patient_form.clear_form()
        
    def delete_patient(self):
        selected_item = self.table.selection()
        if not selected_item:
            return
            
        patient_id = self.table.item(selected_item[0])["values"][0]
        self.patient_service.delete_patient(patient_id)
        self.refresh_table()
        
    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
            
        patients = self.patient_service.get_all_patients()
        for patient in patients:
            self.table.insert("", "end", values=(
                patient.id,
                patient.full_name,
                patient.phone,
                patient.gender,
                patient.birth_date
            ))
            
    def show_error(self, message):
        error_label = ttk.Label(self.patient_form, text=message, 
                               foreground="red", style="Error.TLabel")
        error_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.after(3000, error_label.destroy)
    
    