from app import create_app, db
from app.models import ProgramOutcome

app = create_app()

with app.app_context():
    outcomes = ProgramOutcome.query.all()
    print(f"Toplam {len(outcomes)} program çıktısı bulundu:")
    for outcome in outcomes:
        print(f"\n{outcome.code} - {outcome.title}")
        print(f"Açıklama: {outcome.description}") 