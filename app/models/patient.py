from datetime import datetime

class Patient:
    def __init__(self, id=None, full_name="", phone="", gender="", birth_date=None, comments=""):
        self.id = id
        self.full_name = full_name
        self.phone = phone
        self.gender = gender
        self.birth_date = birth_date or datetime.now().date().isoformat()
        self.comments = comments
        self.created_at = datetime.now().isoformat()
    
    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0],
            full_name=row[1],
            phone=row[2],
            gender=row[3],
            birth_date=row[4],
            comments=row[5]
        )