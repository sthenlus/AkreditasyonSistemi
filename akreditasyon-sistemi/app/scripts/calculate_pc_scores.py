from app import create_app, db
from app.models import StudentExamScore

def calculate_all_pc_scores():
    app = create_app()
    with app.app_context():
        # Tüm sınav notlarını al
        scores = StudentExamScore.query.all()
        
        # Her not için PÇ puanlarını hesapla ve kaydet
        for score in scores:
            score.calculate_pc_scores()
            print(f"Calculated PC scores for student {score.student_id}, exam {score.exam_id}")
        
        print("All PC scores have been calculated and saved.")

if __name__ == '__main__':
    calculate_all_pc_scores() 