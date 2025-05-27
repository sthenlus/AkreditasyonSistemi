from app import create_app, db
from app.models import ProgramOutcome

app = create_app()

program_outcomes = [
    {
        'code': 'PÇ1',
        'title': 'Mühendislik Bilgisi',
        'description': 'Matematik, fen bilimleri, temel mühendislik, bilgisayarla hesaplama ve ilgili mühendislik disiplinine özgü konularda bilgi; bu bilgileri, karmaşık mühendislik problemlerinin çözümünde kullanabilme becerisi.'
    },
    {
        'code': 'PÇ2',
        'title': 'Problem Analizi',
        'description': 'Karmaşık mühendislik problemlerini, temel bilim, matematik ve mühendislik bilgilerini kullanarak ve ele alınan problemle ilgili BM Sürdürülebilir Kalkınma Amaçlarını* gözeterek tanımlama, formüle etme ve analiz becerisi.'
    },
    {
        'code': 'PÇ3',
        'title': 'Mühendislik Tasarımı',
        'description': 'Karmaşık mühendislik problemlerine yaratıcı çözümler tasarlama becerisi; karmaşık sistemleri, süreçleri, cihazları veya ürünleri gerçekçi kısıtları ve koşulları* gözeterek, mevcut ve gelecekteki gereksinimleri karşılayacak biçimde tasarlama becerisi.'
    },
    {
        'code': 'PÇ4',
        'title': 'Teknik ve Araçların Kullanımı',
        'description': 'Karmaşık mühendislik problemlerinin analizi ve çözümüne yönelik, tahmin ve modelleme de dahil olmak üzere, uygun teknikleri, kaynakları ve modern mühendislik ve bilişim araçlarını, sınırlamalarının da farkında olarak seçme ve kullanma becerisi.'
    },
    {
        'code': 'PÇ5',
        'title': 'Araştırma ve İnceleme',
        'description': 'Karmaşık mühendislik problemlerinin incelenmesi için literatür araştırması, deney tasarlama, deney yapma, veri toplama, sonuçları analiz etme ve yorumlama dahil, araştırma yöntemlerini kullanma becerisi.'
    },
    {
        'code': 'PÇ6',
        'title': 'Mühendislik Uygulamalarının Küresel Etkisi',
        'description': 'Mühendislik uygulamalarının BM Sürdürülebilir Kalkınma Amaçları kapsamında, topluma, sağlık ve güvenliğe, ekonomiye, sürdürülebilirlik ve çevreye etkileri hakkında bilgi; mühendislik çözümlerinin hukuksal sonuçları konusunda farkındalık.'
    },
    {
        'code': 'PÇ7',
        'title': 'Etik Davranış',
        'description': 'Mühendislik meslek ilkelerine uygun davranma, etik sorumluluk hakkında bilgi; hiçbir konuda ayrımcılık yapmadan, tarafsız davranma ve çeşitliliği kapsayıcı olma konularında farkındalık.'
    },
    {
        'code': 'PÇ8',
        'title': 'Bireysel ve Takım Çalışması',
        'description': 'Bireysel olarak ve disiplin içi ve çok disiplinli takımlarda (yüz yüze, uzaktan veya karma) takım üyesi veya lideri olarak etkin biçimde çalışabilme becerisi.'
    },
    {
        'code': 'PÇ9',
        'title': 'Sözlü ve Yazılı İletişim',
        'description': 'Hedef kitlenin çeşitli farklılıklarını (eğitim, dil, meslek gibi) dikkate alarak, teknik konularda sözlü, yazılı etkin iletişim kurma becerisi.'
    },
    {
        'code': 'PÇ10',
        'title': 'Proje Yönetimi',
        'description': 'Proje yönetimi ve ekonomik yapılabilirlik analizi gibi iş hayatındaki uygulamalar hakkında bilgi; girişimcilik ve yenilikçilik hakkında farkındalık.'
    },
    {
        'code': 'PÇ11',
        'title': 'Yaşam Boyu Öğrenme',
        'description': 'Bağımsız ve sürekli öğrenebilme, yeni ve gelişmekte olan teknolojilere uyum sağlayabilme ve teknolojik değişimlerle ilgili sorgulayıcı düşünebilmeyi kapsayan yaşam boyu öğrenme becerisi.'
    }
]

with app.app_context():
    # Önce mevcut program çıktılarını temizle
    ProgramOutcome.query.delete()
    
    # Yeni program çıktılarını ekle
    for outcome in program_outcomes:
        new_outcome = ProgramOutcome(
            code=outcome['code'],
            title=outcome['title'],
            description=outcome['description']
        )
        db.session.add(new_outcome)
    
    # Değişiklikleri kaydet
    db.session.commit()
    
print("Program çıktıları başarıyla eklendi!") 