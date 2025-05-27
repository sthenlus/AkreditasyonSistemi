from app import create_app, db
from app.models import ProgramOutcome

def add_program_outcomes():
    app = create_app()
    with app.app_context():
        # Önce mevcut program çıktılarını temizle
        ProgramOutcome.query.delete()
        
        # Program çıktılarını ekle
        outcomes = [
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
            ('PÇ11', 'Yaşam Boyu Öğrenme: Bağımsız ve sürekli öğrenebilme, yeni ve gelişmekte olan teknolojilere uyum sağlayabilme ve teknolojik değişimlerle ilgili sorgulayıcı düşünebilmeyi kapsayan yaşam boyu öğrenme becerisi.')
        ]
        
        for code, description in outcomes:
            outcome = ProgramOutcome(code=code, description=description)
            db.session.add(outcome)
        
        db.session.commit()
        print("Program çıktıları başarıyla eklendi!")

if __name__ == '__main__':
    add_program_outcomes() 