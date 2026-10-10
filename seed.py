"""Seed demo designers. Run: python seed.py"""
from app.database import Base, SessionLocal, engine
from app.models import Designer

Base.metadata.create_all(bind=engine)
DEMO = [
    ("Studio Verve Interiors", "Pune", "Modern Minimalist & Compact Homes", 4.8, 132, 18.5204, 73.8567),
    ("Bluestone Design Co.", "Pune", "Luxury Residences", 4.9, 87, 18.5314, 73.8446),
    ("GreenLeaf Spatial Studio", "Pune", "Scandinavian & Eco-friendly", 4.7, 64, 18.5074, 73.8077),
    ("Foundry & Form", "Mumbai", "Industrial Loft Interiors", 4.6, 151, 19.0760, 72.8777),
    ("Nordic Nest Studio", "Bengaluru", "Scandinavian Interiors", 4.7, 98, 12.9716, 77.5946),
]
db = SessionLocal()
for n, c, s, r, rv, la, lo in DEMO:
    db.add(Designer(name=n, city=c, specialty=s, rating=r, reviews=rv, latitude=la, longitude=lo))
db.commit()
print("Seeded", len(DEMO), "designers")
