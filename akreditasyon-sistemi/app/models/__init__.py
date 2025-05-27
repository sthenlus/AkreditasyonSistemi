from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
from collections import defaultdict

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    exam_scores = db.relationship('StudentExamScore', backref='student', lazy=True)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_pc_scores(self):
        """Öğrencinin program çıktıları başarı düzeylerini hesaplar"""
        pc_scores = {}
        
        # Öğrencinin tüm sınav notlarını al
        exam_scores = self.exam_scores
        
        for score in exam_scores:
            # Her sınav için program çıktısı puanlarını hesapla
            score_pc_scores = score.calculate_pc_scores()
            
            # Her program çıktısı için puanları topla
            for pc_code, pc_score in score_pc_scores.items():
                if pc_code not in pc_scores:
                    pc_scores[pc_code] = []
                pc_scores[pc_code].append(pc_score)
        
        # Her program çıktısı için ortalama hesapla
        avg_scores = {}
        for pc_code, scores in pc_scores.items():
            avg_scores[pc_code] = sum(scores) / len(scores) if scores else 0
            
        return avg_scores

    def get_pc_scores_by_semester(self):
        """Her dönem ve genel için program çıktısı ortalamalarını döndürür."""
        # {semester_id: {pc_code: [puanlar]}}
        semester_pc_scores = defaultdict(lambda: defaultdict(list))
        all_pc_scores = defaultdict(list)
        for score in self.exam_scores:
            semester_id = getattr(score, 'semester_id', None)
            score_pc_scores = score.calculate_pc_scores()
            for pc_code, pc_score in score_pc_scores.items():
                if semester_id:
                    semester_pc_scores[semester_id][pc_code].append(pc_score)
                all_pc_scores[pc_code].append(pc_score)
        # Ortalamaları hesapla
        semester_pc_averages = {}
        for semester_id, pcs in semester_pc_scores.items():
            semester_pc_averages[semester_id] = {pc: sum(vals)/len(vals) if vals else 0 for pc, vals in pcs.items()}
        all_pc_averages = {pc: sum(vals)/len(vals) if vals else 0 for pc, vals in all_pc_scores.items()}
        return {
            'by_semester': semester_pc_averages,
            'overall': all_pc_averages
        }

    def __repr__(self):
        return f'<Student {self.student_number}: {self.first_name} {self.last_name}>'

class Semester(db.Model):
    __tablename__ = 'semesters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Dönemin dersleri ile ilişkisi
    courses = db.relationship('Course', backref='semester', lazy=True)

    def __repr__(self):
        return f'<Semester {self.name}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    instructor_name = db.Column(db.String(100), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    exams = db.relationship('Exam', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.course_code}: {self.course_name}>'

class ProgramOutcome(db.Model):
    __tablename__ = 'program_outcomes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # İlişkileri burada tanımlayalım
    related_courses = db.relationship('Course',
                                    secondary='course_program_outcomes',
                                    backref=db.backref('program_outcomes', lazy='dynamic'),
                                    lazy='dynamic')
    
    related_exams = db.relationship('Exam',
                                  secondary='exam_program_outcomes',
                                  backref=db.backref('program_outcomes', lazy='dynamic'),
                                  lazy='dynamic')

    def __repr__(self):
        return f'<ProgramOutcome {self.code}>'

class CourseProgramOutcome(db.Model):
    __tablename__ = 'course_program_outcomes'
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    program_outcome_id = db.Column(db.Integer, db.ForeignKey('program_outcomes.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Sınavın ağırlığı (yüzde)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student_scores = db.relationship('StudentExamScore', backref='exam', lazy=True)

    def __repr__(self):
        return f'<Exam {self.exam_name} for Course {self.course_id}>'

class ExamProgramOutcome(db.Model):
    __tablename__ = 'exam_program_outcomes'
    
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), primary_key=True)
    program_outcome_id = db.Column(db.Integer, db.ForeignKey('program_outcomes.id'), primary_key=True)
    weight = db.Column(db.Float, nullable=False, default=1.0)  # PÇ ağırlığı (0-1 arası)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudentExamScore(db.Model):
    __tablename__ = 'student_exam_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # 0-100 arası not
    letter_grade = db.Column(db.String(2))
    outcome_scores = db.Column(db.JSON)  # Program çıktısı puanlarını JSON olarak sakla
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_letter_grade(self):
        """Notu harf notuna çevirir"""
        if self.score >= 90:
            return 'AA'
        elif self.score >= 85:
            return 'BA'
        elif self.score >= 80:
            return 'BB'
        elif self.score >= 75:
            return 'CB'
        elif self.score >= 70:
            return 'CC'
        elif self.score >= 65:
            return 'DC'
        elif self.score >= 60:
            return 'DD'
        elif self.score >= 50:
            return 'FD'
        else:
            return 'FF'
    
    def calculate_pc_scores(self):
        """Sınav notunu PÇ puanlarına dönüştürür ve kaydeder"""
        pc_scores = {}
        
        try:
            # Sınavın program çıktılarını al
            exam_outcomes = self.exam.program_outcomes
            
            for outcome in exam_outcomes:
                try:
                    # İlgili program çıktısının ağırlığını bul
                    exam_outcome = ExamProgramOutcome.query.filter_by(
                        exam_id=self.exam_id,
                        program_outcome_id=outcome.id
                    ).first()
                    
                    if exam_outcome:
                        # PÇ puanı = (Sınav notu / 100) * 100 * PÇ ağırlığı
                        pc_scores[outcome.code] = round((self.score / 100) * 100 * exam_outcome.weight, 2)
                    else:
                        # Eğer ağırlık tanımlanmamışsa varsayılan olarak 1.0 kullan
                        pc_scores[outcome.code] = round(self.score, 2)
                except Exception as e:
                    print(f"Error calculating score for outcome {outcome.code}: {str(e)}")
                    pc_scores[outcome.code] = round(self.score, 2)
            
            # PÇ puanlarını JSON olarak kaydet
            self.outcome_scores = pc_scores
            db.session.commit()
            
        except Exception as e:
            print(f"Error in calculate_pc_scores: {str(e)}")
        
        return pc_scores

    def __repr__(self):
        return f'<StudentExamScore {self.student_id} - {self.exam_id}>'

# Modelleri dışa aktar
__all__ = ['User', 'Student', 'Course', 'ProgramOutcome', 'Exam', 'StudentExamScore']