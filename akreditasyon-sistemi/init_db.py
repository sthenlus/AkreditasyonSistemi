from app import create_app, db
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        
        # Admin kullanıcısı var mı kontrol et
        if not User.query.filter_by(username='mahsum').first():
            # Yeni admin kullanıcısı oluştur
            admin = User(username='mahsum', email='admin@example.com', is_admin=True)
            admin.set_password('123456')
            
            # Kullanıcıyı veritabanına kaydet
            db.session.add(admin)
            db.session.commit()
            print("Admin hesabı oluşturuldu!")
        else:
            print("Admin hesabı zaten mevcut.")

if __name__ == '__main__':
    init_db() 