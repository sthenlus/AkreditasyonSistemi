from app import db
from datetime import datetime

class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Sınav notları ile ilişki
    scores = db.relationship('StudentExamScore', backref='exam', lazy=True)
    
    # Sınavın program çıktıları ile ilişkisi
    program_outcomes = db.relationship('ProgramOutcome',
                                     secondary='exam_program_outcomes',
                                     backref=db.backref('exams', lazy=True))

    def __repr__(self):
        return f'<Exam {self.exam_name} for Course {self.course_id}>'

class StudentExamScore(db.Model):
    __tablename__ = 'student_exam_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Score {self.score} for Student {self.student_id} in Exam {self.exam_id}>' 