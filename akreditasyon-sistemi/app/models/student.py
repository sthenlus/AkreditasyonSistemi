from app import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Öğrencinin sınav notları ile ilişki
    exam_scores = db.relationship(
        'StudentExamScore',
        backref='student',
        lazy=True,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Student {self.student_number}: {self.first_name} {self.last_name}>'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

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