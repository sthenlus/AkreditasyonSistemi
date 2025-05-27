from app import create_app, db
from app.models import ProgramOutcome

def init_program_outcomes():
    app = create_app()
    with app.app_context():
        # Program çıktılarını tanımla
        outcomes = [
            {
                'code': 'PÇ1',
                'description': 'Matematik, fen bilimleri ve kendi alanlarındaki kuramsal ve uygulamalı bilgileri mühendislik çözümleri için kullanabilme becerisi'
            },
            {
                'code': 'PÇ2',
                'description': 'Karmaşık mühendislik problemlerini saptama, tanımlama, formüle etme ve çözme becerisi'
            },
            {
                'code': 'PÇ3',
                'description': 'Karmaşık bir sistemi, süreci, cihazı veya ürünü gerçekçi kısıtlar ve koşullar altında, belirli gereksinimleri karşılayacak şekilde tasarlama becerisi'
            },
            {
                'code': 'PÇ4',
                'description': 'Mühendislik uygulamalarında karşılaşılan karmaşık problemlerin analizi ve çözümü için gerekli olan modern teknik ve araçları geliştirme, seçme ve kullanma becerisi'
            },
            {
                'code': 'PÇ5',
                'description': 'Karmaşık mühendislik problemlerinin veya disipline özgü araştırma konularının incelenmesi için deney tasarlama, deney yapma, veri toplama, sonuçları analiz etme ve yorumlama becerisi'
            }
        ]
        
        # Veritabanına ekle
        for outcome in outcomes:
            if not ProgramOutcome.query.filter_by(code=outcome['code']).first():
                pc = ProgramOutcome(
                    code=outcome['code'],
                    description=outcome['description']
                )
                db.session.add(pc)
                print(f"Eklenen PÇ: {outcome['code']}")
        
        try:
            db.session.commit()
            print("Program çıktıları başarıyla eklendi!")
        except Exception as e:
            db.session.rollback()
            print(f"Hata oluştu: {str(e)}")

if __name__ == '__main__':
    init_program_outcomes() 