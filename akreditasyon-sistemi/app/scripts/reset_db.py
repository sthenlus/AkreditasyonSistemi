from app import create_app, db

app = create_app()

with app.app_context():
    # Tüm tabloları sil
    db.drop_all()
    
    # Tabloları yeniden oluştur
    db.create_all()
    
print("Veritabanı başarıyla sıfırlandı!") 