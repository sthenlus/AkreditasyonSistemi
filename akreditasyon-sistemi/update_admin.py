from app import app, db
from app.models import User

def update_admin_status(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"{username} kullanıcısına admin yetkisi verildi.")
        else:
            print(f"{username} kullanıcısı bulunamadı.")

if __name__ == '__main__':
    username = input("Admin yetkisi verilecek kullanıcı adını girin: ")
    update_admin_status(username) 