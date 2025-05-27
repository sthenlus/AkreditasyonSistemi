from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Konfigürasyon
    app.config['SECRET_KEY'] = 'gizli-anahtar-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///akreditasyon.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Foreign key desteğini aktifleştir
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'check_same_thread': False}
    }
    
    # Uzantıları başlat
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Blueprint'leri kaydet
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.admin import bp as admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Veritabanını oluştur
    with app.app_context():
        db.create_all()
    
    return app

# User loader function
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def init_db():
    app = create_app()
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        
        # Admin kullanıcısı var mı kontrol et
        from app.models import User
        if not User.query.filter_by(username='mahsum').first():
            # Yeni admin kullanıcısı oluştur
            admin = User(username='mahsum', email='admin@example.com')
            admin.set_password('123456')  # Şifreyi istediğiniz gibi değiştirin
            
            # Kullanıcıyı veritabanına kaydet
            db.session.add(admin)
            db.session.commit()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

if __name__ == '__main__':
    init_db() 