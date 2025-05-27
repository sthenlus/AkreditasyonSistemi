from app import db

class ProgramOutcome(db.Model):
    __tablename__ = 'program_outcomes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # Örn: PÇ1, PÇ2
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ProgramOutcome {self.code}>' 