from app import db

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    instructor_name = db.Column(db.String(100), nullable=False)

    # Dersin sınavları ile ilişki
    exams = db.relationship('Exam', backref='course', lazy=True)
    
    # Dersin program çıktıları ile ilişkisi
    program_outcomes = db.relationship('ProgramOutcome', 
                                     secondary='course_program_outcomes',
                                     backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f'<Course {self.course_code}: {self.course_name}>' 