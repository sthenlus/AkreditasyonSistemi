from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin(username, password):
    app = create_app()
    with app.app_context():
        if User.query.filter_by(username=username).first():
            print(f"Kullanıcı adı '{username}' zaten mevcut!")
            return
        admin = User(
            username=username,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Yeni admin oluşturuldu: {username}")

if __name__ == "__main__":
    create_admin("halil", "123456") 