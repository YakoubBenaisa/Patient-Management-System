from .database import Database
from ..patient import Patient

class PatientService:
    def __init__(self):
        self.db = Database()
        
    def add_patient(self, patient):
        query = '''INSERT INTO patients 
                   (full_name, phone, gender, birth_date, comments)
                   VALUES (?, ?, ?, ?, ?)'''
        params = (patient.full_name, patient.phone, 
                 patient.gender, patient.birth_date, patient.comments)
        patient_id = self.db.execute_query(query, params)
        return patient_id
    
    def delete_patient(self, patient_id):
        query = "DELETE FROM patients WHERE id = ?"
        self.db.execute_query(query, (patient_id,))
    
    def get_all_patients(self):
        query = "SELECT * FROM patients ORDER BY created_at DESC"
        return [Patient.from_row(row) for row in self.db.fetch_all(query)]
    
    def search_patients(self, search_term):
        query = '''SELECT * FROM patients 
                   WHERE full_name LIKE ? OR phone LIKE ?'''
        params = (f"%{search_term}%", f"%{search_term}%")
        return [Patient.from_row(row) for row in self.db.fetch_all(query, params)]