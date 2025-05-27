-- Kullanıcılar tablosu
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Öğrenciler tablosu
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Dersler tablosu
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL,
    instructor_name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Program çıktıları tablosu
CREATE TABLE program_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Ders-Program çıktıları ilişki tablosu
CREATE TABLE course_program_outcomes (
    course_id INTEGER NOT NULL,
    program_outcome_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (course_id, program_outcome_id),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (program_outcome_id) REFERENCES program_outcomes(id) ON DELETE CASCADE
);

-- Sınavlar tablosu
CREATE TABLE exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    exam_name VARCHAR(100) NOT NULL,
    exam_date DATE NOT NULL,
    weight FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Sınav-Program çıktıları ilişki tablosu
CREATE TABLE exam_program_outcomes (
    exam_id INTEGER NOT NULL,
    program_outcome_id INTEGER NOT NULL,
    weight FLOAT NOT NULL DEFAULT 1.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (exam_id, program_outcome_id),
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    FOREIGN KEY (program_outcome_id) REFERENCES program_outcomes(id) ON DELETE CASCADE
);

-- Öğrenci sınav notları tablosu
CREATE TABLE student_exam_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    exam_id INTEGER NOT NULL,
    score FLOAT NOT NULL,
    outcome_scores JSON,
    semester VARCHAR(20) NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
);

-- İndeksler
CREATE INDEX idx_student_exam_scores_student ON student_exam_scores(student_id);
CREATE INDEX idx_student_exam_scores_exam ON student_exam_scores(exam_id);
CREATE INDEX idx_student_exam_scores_semester ON student_exam_scores(semester, academic_year);
CREATE INDEX idx_exams_course ON exams(course_id);
CREATE INDEX idx_course_program_outcomes_course ON course_program_outcomes(course_id);
CREATE INDEX idx_exam_program_outcomes_exam ON exam_program_outcomes(exam_id);

-- Program çıktıları
INSERT INTO program_outcomes (code, description) VALUES
('PÇ1', 'Mühendislik Bilgisi: Matematik, fen bilimleri, temel mühendislik, bilgisayarla hesaplama ve ilgili mühendislik disiplinine özgü konularda bilgi; bu bilgileri, karmaşık mühendislik problemlerinin çözümünde kullanabilme becerisi.'),
('PÇ2', 'Problem Analizi: Karmaşık mühendislik problemlerini, temel bilim, matematik ve mühendislik bilgilerini kullanarak ve ele alınan problemle ilgili BM Sürdürülebilir Kalkınma Amaçlarını gözeterek tanımlama, formüle etme ve analiz becerisi.'),
('PÇ3', 'Mühendislik Tasarımı: Karmaşık mühendislik problemlerine yaratıcı çözümler tasarlama becerisi; karmaşık sistemleri, süreçleri, cihazları veya ürünleri gerçekçi kısıtları ve koşulları gözeterek, mevcut ve gelecekteki gereksinimleri karşılayacak biçimde tasarlama becerisi.'),
('PÇ4', 'Teknik ve Araçların Kullanımı: Karmaşık mühendislik problemlerinin analizi ve çözümüne yönelik, tahmin ve modelleme de dahil olmak üzere, uygun teknikleri, kaynakları ve modern mühendislik ve bilişim araçlarını, sınırlamalarının da farkında olarak seçme ve kullanma becerisi.'),
('PÇ5', 'Araştırma ve İnceleme: Karmaşık mühendislik problemlerinin incelenmesi için literatür araştırması, deney tasarlama, deney yapma, veri toplama, sonuçları analiz etme ve yorumlama dahil, araştırma yöntemlerini kullanma becerisi.'),
('PÇ6', 'Mühendislik Uygulamalarının Küresel Etkisi: Mühendislik uygulamalarının BM Sürdürülebilir Kalkınma Amaçları kapsamında, topluma, sağlık ve güvenliğe, ekonomiye, sürdürülebilirlik ve çevreye etkileri hakkında bilgi; mühendislik çözümlerinin hukuksal sonuçları konusunda farkındalık.'),
('PÇ7', 'Etik Davranış: Mühendislik meslek ilkelerine uygun davranma, etik sorumluluk hakkında bilgi; hiçbir konuda ayrımcılık yapmadan, tarafsız davranma ve çeşitliliği kapsayıcı olma konularında farkındalık.'),
('PÇ8', 'Bireysel ve Takım Çalışması: Bireysel olarak ve disiplin içi ve çok disiplinli takımlarda (yüz yüze, uzaktan veya karma) takım üyesi veya lideri olarak etkin biçimde çalışabilme becerisi.'),
('PÇ9', 'Sözlü ve Yazılı İletişim: Hedef kitlenin çeşitli farklılıklarını (eğitim, dil, meslek gibi) dikkate alarak, teknik konularda sözlü, yazılı etkin iletişim kurma becerisi.'),
('PÇ10', 'Proje Yönetimi: Proje yönetimi ve ekonomik yapılabilirlik analizi gibi iş hayatındaki uygulamalar hakkında bilgi; girişimcilik ve yenilikçilik hakkında farkındalık.'),
('PÇ11', 'Yaşam Boyu Öğrenme: Bağımsız ve sürekli öğrenebilme, yeni ve gelişmekte olan teknolojilere uyum sağlayabilme ve teknolojik değişimlerle ilgili sorgulayıcı düşünebilmeyi kapsayan yaşam boyu öğrenme becerisi.');

-- Örnek admin kullanıcısı (şifre: admin123)
INSERT INTO users (username, email, password_hash, is_admin) VALUES
('admin', 'admin@example.com', 'pbkdf2:sha256:260000$7tGrwEgL$a3f4f4b7f4e9f4b3f4e9f4b3f4e9f4b3f4e9f4b3f4e9f4b3f4e9f4b3', 1); 