import sqlite3
import random
import unicodedata

random.seed(42)

universities_by_city = {
    "Istanbul": [
        "Istanbul University", "Istanbul Technical University", "Boğaziçi University",
        "Marmara University", "Yıldız Technical University", "Koç University",
        "Sabancı University", "Bahçeşehir University", "Üsküdar University",
        "Istanbul Medipol University", "Istanbul Bilgi University", "Istanbul Aydın University",
        "Istanbul Kültür University", "Galatasaray University", "Mimar Sinan Fine Arts University",
    ],
    "Ankara": [
        "Ankara University", "Middle East Technical University", "Hacettepe University",
        "Gazi University", "Bilkent University", "TOBB University of Economics and Technology",
        "Başkent University", "Çankaya University", "Atılım University", "TED University",
    ],
    "Izmir": [
        "Ege University", "Dokuz Eylül University", "Izmir Institute of Technology",
        "Izmir University of Economics", "Yaşar University",
    ],
    "Bursa": ["Bursa Uludağ University", "Bursa Technical University"],
    "Antalya": ["Akdeniz University", "Antalya Bilim University"],
}

departments_by_faculty = {
    "Engineering": [
        "Computer Engineering", "Software Engineering", "Electrical and Electronics Engineering",
        "Mechanical Engineering", "Civil Engineering", "Industrial Engineering",
        "Chemical Engineering", "Environmental Engineering", "Mechatronics Engineering",
        "Biomedical Engineering",
    ],
    "Medicine": [
        "Medicine", "Surgery", "Internal Medicine", "Pediatrics",
        "Public Health", "Anatomy", "Cardiology", "Neurology",
    ],
    "Law": [
        "Public Law", "Private Law", "International Law",
        "Criminal Law", "Commercial Law", "Constitutional Law",
    ],
    "Education": [
        "Primary Education", "Mathematics Education", "Science Education",
        "English Language Teaching", "Guidance and Psychological Counseling", "Preschool Education",
    ],
    "Arts and Sciences": [
        "Psychology", "Sociology", "Mathematics", "Physics", "Chemistry",
        "History", "Turkish Language and Literature", "Molecular Biology and Genetics",
    ],
    "Economics and Administrative Sciences": [
        "Business Administration", "Economics", "International Relations",
        "Political Science and Public Administration", "Finance",
        "Management Information Systems", "International Trade",
    ],
}

ranks = ["Research Assistant", "Lecturer", "Assistant Professor", "Associate Professor", "Professor"]
cities = list(universities_by_city.keys())
faculties = list(departments_by_faculty.keys())
languages = ["English", "Turkish", "English and Turkish"]
modes = ["Face-to-face", "Hybrid"]

allowed_domains = [
    "bau.edu.tr", "istanbul.edu.tr", "itu.edu.tr", "bogazici.edu.tr", "marmara.edu.tr",
    "yildiz.edu.tr", "koc.edu.tr", "sabanciuniv.edu.tr", "bilgi.edu.tr", "uskudar.edu.tr",
    "medipol.edu.tr", "ankara.edu.tr", "metu.edu.tr", "hacettepe.edu.tr", "gazi.edu.tr",
    "bilkent.edu.tr", "deu.edu.tr", "ege.edu.tr", "iyte.edu.tr", "uludag.edu.tr", "akdeniz.edu.tr",
]

first_names = [
    "Ahmet", "Mehmet", "Mustafa", "Ali", "Hüseyin", "Hasan", "İbrahim", "Osman", "Yusuf", "Murat",
    "Emre", "Burak", "Can", "Kerem", "Onur", "Serkan", "Tolga", "Volkan", "Cem", "Barış",
    "Ayşe", "Fatma", "Emine", "Hatice", "Zeynep", "Elif", "Merve", "Büşra", "Esra", "Sevgi",
    "Selin", "Deniz", "Ece", "Gizem", "İrem", "Aslı", "Pınar", "Dilek", "Gül", "Ebru",
    "Furkan", "Yasin", "Okan", "Sinan", "Ufuk", "Gökhan", "Berk", "Kaan", "Hakan", "Levent",
]

last_names = [
    "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
    "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
    "Polat", "Korkmaz", "Çakır", "Erdoğan", "Güneş", "Aksoy", "Bulut", "Karahan", "Avcı", "Taş",
    "Şen", "Acar", "Toprak", "Yalçın", "Bozkurt", "Turan", "Güler", "Tekin", "Ünal", "Aydoğan",
]


def slugify(text):
    text = text.replace("ı", "i").replace("İ", "i").replace("ş", "s").replace("Ş", "s")
    text = text.replace("ğ", "g").replace("Ğ", "g").replace("ü", "u").replace("Ü", "u")
    text = text.replace("ö", "o").replace("Ö", "o").replace("ç", "c").replace("Ç", "c")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text.lower()


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

existing_emails = {row[0] for row in cursor.execute("SELECT email FROM users").fetchall()}

inserted = 0
attempts = 0
while inserted < 50 and attempts < 5000:
    attempts += 1
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"

    domain = random.choice(allowed_domains)
    base = f"{slugify(first)}.{slugify(last)}"
    email = f"{base}@{domain}"
    suffix = 1
    while email in existing_emails:
        suffix += 1
        email = f"{base}{suffix}@{domain}"
    existing_emails.add(email)

    rank = random.choice(ranks)

    current_city = random.choice(cities)
    current_university = random.choice(universities_by_city[current_city])
    current_faculty = random.choice(faculties)
    department = random.choice(departments_by_faculty[current_faculty])

    preferred_city = random.choice([c for c in cities if c != current_city])
    preferred_university = random.choice(universities_by_city[preferred_city])
    preferred_faculty = random.choice(faculties)
    preferred_department = random.choice(departments_by_faculty[preferred_faculty])

    teaching_language = random.choice(languages)
    teaching_mode = random.choice(modes)

    cursor.execute("""
        INSERT INTO users (
            email, name, rank,
            current_city, current_university, current_faculty, department,
            preferred_city, preferred_university, preferred_faculty, preferred_department,
            teaching_language, teaching_mode
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email, name, rank,
        current_city, current_university, current_faculty, department,
        preferred_city, preferred_university, preferred_faculty, preferred_department,
        teaching_language, teaching_mode,
    ))
    inserted += 1

conn.commit()
print(f"Inserted {inserted} users. Total now: {cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]}")
conn.close()
