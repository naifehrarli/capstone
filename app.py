import os
from urllib.parse import quote
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import random
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "academic-permutation-secret-key"
translations = {
    "en": {
        "app_name": "Academic Permutation System",
        "dashboard": "Dashboard",
        "my_profile": "My Profile",
        "registered_users": "Registered Users",
        "top_matches": "Top Matches",
        "potential_matches": "Potential Matches",
        "logout": "Logout",
        "confirm_logout": "Confirm Logout",
        "logout_question": "Are you sure you want to logout?",
        "cancel": "Cancel",
        "yes_logout": "Yes, Logout",
        "welcome": "Welcome",
        "logged_in_message": "You are logged in with your university email.",
        "top_5_matches": "Top 5 matches for you",
        "top_match_each_user": "Top Match for Each User",
        "strongest_match_message": "Each user is shown with their strongest recommended match.",
        "recommended_pair": "Recommended Pair",
        "score": "Score",
        "match_found": "Match Found",
        "view_more_users": "View More Users",
        "view_more_matches": "View More Matches",
        "no_matches": "No matches found yet.",
        "english": "English",
        "turkish": "Türkçe",
        "rank": "Rank",
        "department": "Department",
        "current_university": "Current University",
        "current_city": "Current City",
        "preferred_university": "Preferred University",
        "preferred_city": "Preferred City",
        "teaching_language": "Teaching Language",
        "teaching_mode": "Teaching Mode",
        "top_match": "Top Match",
        "only_top_matches": "Only the top 5 matches are shown first. Extra matches are hidden to avoid clutter.",
        "edit_profile": "Edit Profile",
        "current_academic_info": "Current Academic Information",
        "preferred_academic_info": "Preferred Academic Information",
        "teaching_preferences": "Teaching Preferences",
        "city": "City",
        "university": "University",
        "faculty": "Faculty",
        "preferred_faculty": "Preferred Faculty",
        "preferred_department": "Preferred Department",
        "back_to_profile": "Back to Profile",
        "name": "Name",
        "academic_rank": "Academic Rank",
        "save_changes": "Save Changes",
        "back_to_dashboard": "Back to Dashboard",
        "profile": "Profile",
                "home": "Home",
        "advanced_matches": "Advanced Matches",
        "starred_matches": "Starred Matches",
        "how_it_works": "How It Works",
        "create_profile": "Create Your Profile",
        "explore_users": "Explore Academic Users",
        "receive_matches": "Receive Smart Matches",
        "about_system": "About the System",
        "why_use_platform": "Why Use This Platform",
        "secure_trusted": "Secure & Trusted",
        "smart_matching": "Smart Matching",
        "academic_collaboration": "Academic Collaboration",
        "preference_based": "Preference Based",
        "find_matches": "Find Matches",
        "clear": "Clear",
        "star_match": "Star Match",
        "starred": "Starred",
        "view_profile": "View Profile",
        "new_city_preference": "New City Preference",
        "new_faculty_preference": "New Faculty Preference",
        "new_department_preference": "New Department Preference",
        "minimum_match_score": "Minimum Match Score",
        "profile_picture": "Profile Picture",
        "change_password": "Change Password",
        "leave_password_blank": "Leave these fields blank to keep your current password.",
        "current_password": "Current Password",
        "new_password": "New Password",
        "confirm_new_password": "Confirm New Password",
        "password_strength": "Password strength",
        "password_strength_weak": "Weak",
        "password_strength_fair": "Fair",
        "password_strength_good": "Good",
        "password_strength_strong": "Strong",
        "password_strength_very_strong": "Very strong",
        "back": "Back",
        "no_advanced_matches_found": "No advanced matches found",
        "starred_match": "Starred Match",
        "remove_star": "Remove Star",
        "remove_star_question": "Are you sure you want to remove this starred match?",
        "remove": "Remove",
        "all_cities": "All Cities",
        "all_faculties": "All Faculties",
        "all_departments": "All Departments",
        "no_starred_matches": "No starred matches yet",
        "saved_matches_message": "These are the matches you saved while exploring Advanced Matches.",
        "go_to_advanced_matches": "Go to Advanced Matches and star any match you want to save for later.",
        "why_this_match": "Why This Match?",
        "matched_user_contact": "Matched User Contact",
        "their_preferences": "Their Preferences",
        "why_this_user_matches_you": "Why This User Matches You",
        "compatibility_score": "Compatibility Score",
        "match_level": "Match Level",
        "close": "Close",
        "home_description": "A smart academic exchange and collaboration platform that helps university staff find compatible academic opportunities based on universities, departments, teaching preferences, and destination interests.",
        "show_all_users": "Show All Users",
        "hide_users": "Hide Users",
        "first_five_users": "The first five registered users are shown first.",
        "advanced_match": "Advanced Match",
        "create_profile_desc": "Register your academic information, university, department, teaching preferences, and preferred exchange destination.",
        "explore_users_desc": "Browse registered university staff and explore possible collaboration and academic exchange opportunities.",
        "receive_matches_desc": "The system compares preferences and recommends the most suitable academic matches.",
        "about_system_desc": "The Academic Permutation System uses preference-based matching and biomimetic-inspired logic to connect university staff with compatible exchange opportunities. It evaluates faculties, departments, academic ranks, teaching styles, universities, and destination preferences to produce meaningful recommendations.",
        "benefit_1": "Find relevant academic exchange opportunities",
        "benefit_2": "Connect with compatible university staff",
        "benefit_3": "Save time with intelligent matching",
        "benefit_4": "Understand why each match is recommended",
        "email": "Email",
        "secure_desc": "Your data is safe and protected.",
        "smart_matching_desc": "Intelligent algorithms find the best matches.",
        "academic_collaboration_desc": "Connect and collaborate with academics.",
        "preference_based_desc": "Matches based on your goals.",
        "potential_matches_desc": "Your top five potential matches are shown below. Click a match to understand why it was recommended.",
        "click_match_explanation": "Click to view match explanation.",
        "advanced_matches_desc": "Choose a new city, faculty, or department preference without changing your saved profile.",
        "good_match": "Good Match",
        "weak_match": "Weak Match",
        "excellent_match": "Excellent Match",
        "exploratory_match": "Exploratory Match",
        "reason_same_department": "You are both in the same department.",
        "reason_pref_department": "This user's department matches your preferred department.",
        "reason_pref_city": "This user is currently located in your preferred city.",
        "reason_same_title": "You both hold the same academic title.",
        "reason_mutual_city": "You both prefer to move to each other's city (mutual match).",
        "reason_partial": "This user has partial academic compatibility with your profile.",
        "reason_advanced": "This user matches your advanced search preferences.",
        "reason_starred": "You saved this match from Advanced Matches.",
        "login": "Login",
        "register_user": "Register User",
        "register_new_user": "Register New User",
        "landing_description": "A decision-support platform for university staff registration and preference-based matching.",
        "login_description": "Enter your registered university email and password.",
        "new_user_register_here": "New user? Register here",
        "university_email": "University Email",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "enter_password": "Enter your password",
        "password_min_placeholder": "At least 8 characters",
        "confirm_password_placeholder": "Re-enter password",
        "show_password": "Show password",
        "hide_password": "Hide password",
        "show_confirmed_password": "Show confirmed password",
        "hide_confirmed_password": "Hide confirmed password",
        "register_description": "Complete each step to create your academic permutation profile.",
        "step_personal_details": "Step 1: Personal Details",
        "step_current_city_university": "Step 2: Current City and University",
        "step_current_faculty_department": "Step 3: Current Faculty and Department",
        "step_preferred_city_university": "Step 4: Preferred City and University",
        "step_preferred_faculty_department": "Step 5: Preferred Faculty and Department",
        "step_teaching_preferences": "Step 6: Teaching Preferences",
        "select_academic_rank": "Select academic rank",
        "select_current_city": "Select current city",
        "select_city_first": "Select city first",
        "select_current_faculty": "Select current faculty",
        "select_faculty_first": "Select faculty first",
        "select_preferred_city": "Select preferred city",
        "select_preferred_faculty": "Select preferred faculty",
        "select_language": "Select language",
        "select_teaching_mode": "Select teaching mode",
        "select_university": "Select university",
        "select_department": "Select department",
        "current_faculty": "Current Faculty",
        "preferred_teaching_language": "Preferred Teaching Language",
        "preferred_teaching_mode": "Preferred Teaching Mode",
        "complete_registration": "Complete Registration",
        "next": "Next",
        "full_name_placeholder": "Enter full name",
        "rank_research_assistant": "Research Assistant",
        "rank_lecturer": "Lecturer",
        "rank_assistant_professor": "Assistant Professor",
        "rank_associate_professor": "Associate Professor",
        "rank_professor": "Professor",
        "faculty_engineering": "Engineering",
        "faculty_medicine": "Medicine",
        "faculty_law": "Law",
        "faculty_education": "Education",
        "faculty_arts_sciences": "Arts and Sciences",
        "faculty_economics_admin": "Economics and Administrative Sciences",
        "language_english": "English",
        "language_turkish": "Turkish",
        "language_turkish_english": "Turkish and English",
        "language_french": "French",
        "language_german": "German",
        "language_arabic": "Arabic",
        "language_italian": "Italian",
        "language_russian": "Russian",
        "language_chinese": "Chinese",
        "language_spanish": "Spanish",
        "mode_face_to_face": "Face-to-face",
        "mode_hybrid": "Hybrid",
        "city_istanbul": "Istanbul",
        "city_ankara": "Ankara",
        "city_izmir": "Izmir",
        "city_bursa": "Bursa",
        "city_antalya": "Antalya",
        "university_detected": "University detected",
        "error_valid_university_email": "Please use a valid university email.",
        "error_password_length": "Password must be at least 8 characters long.",
        "error_passwords_do_not_match": "Passwords do not match.",
        "error_email_registered": "This email is already registered. Please login instead.",
        "error_incorrect_password": "Incorrect password. Please try again.",
        "error_email_not_registered": "This email is not registered yet. Please register first.",


    },
    "tr": {
        "app_name": "Akademik Permütasyon Sistemi",
        "dashboard": "Panel",
        "my_profile": "Profilim",
        "registered_users": "Kayıtlı Kullanıcılar",
        "top_matches": "En İyi Eşleşmeler",
        "potential_matches": "Olası Eşleşmeler",
        "logout": "Çıkış Yap",
        "confirm_logout": "Çıkışı Onayla",
        "logout_question": "Çıkış yapmak istediğinizden emin misiniz?",
        "cancel": "İptal",
        "yes_logout": "Evet, Çıkış Yap",
        "welcome": "Hoş geldiniz",
        "logged_in_message": "Üniversite e-postanız ile giriş yaptınız.",
        "top_5_matches": "Sizin için en iyi 5 eşleşme",
        "top_match_each_user": "Her Kullanıcı İçin En İyi Eşleşme",
        "strongest_match_message": "Her kullanıcı en güçlü önerilen eşleşmesi ile gösterilir.",
        "recommended_pair": "Önerilen Eşleşme",
        "score": "Puan",
        "match_found": "Eşleşme Bulundu",
        "view_more_users": "Daha Fazla Kullanıcı Göster",
        "view_more_matches": "Daha Fazla Eşleşme Göster",
        "no_matches": "Henüz eşleşme bulunamadı.",
        "english": "English",
        "turkish": "Türkçe",
        "rank": "Akademik Ünvan",
        "department": "Bölüm",
        "current_university": "Mevcut Üniversite",
        "current_city": "Mevcut Şehir",
        "preferred_university": "Tercih Edilen Üniversite",
        "preferred_city": "Tercih Edilen Şehir",
        "teaching_language": "Ders Dili",
        "teaching_mode": "Ders Verme Şekli",
        "top_match": "En İyi Eşleşme",
        "only_top_matches": "İlk olarak en iyi 5 eşleşme gösterilir. Ek eşleşmeler kalabalığı önlemek için gizlenir.",
        "edit_profile": "Profili Düzenle",
        "current_academic_info": "Mevcut Akademik Bilgiler",
        "preferred_academic_info": "Tercih Edilen Akademik Bilgiler",
        "teaching_preferences": "Ders Tercihleri",
        "city": "Şehir",
        "university": "Üniversite",
        "faculty": "Fakülte",
        "preferred_faculty": "Tercih Edilen Fakülte",
        "preferred_department": "Tercih Edilen Bölüm",
        "back_to_profile": "Profile Dön",
        "name": "İsim",
        "academic_rank": "Akademik Ünvan",
        "save_changes": "Değişiklikleri Kaydet",
        "back_to_dashboard": "Panele Dön",
        "profile": "Profil",
                "home": "Ana Sayfa",
        "advanced_matches": "Gelişmiş Eşleşmeler",
        "starred_matches": "Kaydedilen Eşleşmeler",
        "how_it_works": "Nasıl Çalışır",
        "create_profile": "Profilinizi Oluşturun",
        "explore_users": "Akademisyenleri Keşfedin",
        "receive_matches": "Akıllı Eşleşmeler Alın",
        "about_system": "Sistem Hakkında",
        "why_use_platform": "Neden Bu Platform?",
        "secure_trusted": "Güvenli ve Güvenilir",
        "smart_matching": "Akıllı Eşleştirme",
        "academic_collaboration": "Akademik İş Birliği",
        "preference_based": "Tercih Tabanlı",
        "find_matches": "Eşleşmeleri Bul",
        "clear": "Temizle",
        "star_match": "Kaydet",
        "starred": "Kaydedildi",
        "view_profile": "Profili Gör",
        "new_city_preference": "Yeni Şehir Tercihi",
        "new_faculty_preference": "Yeni Fakülte Tercihi",
        "new_department_preference": "Yeni Bölüm Tercihi",
        "minimum_match_score": "Minimum Eşleşme Puanı",
        "profile_picture": "Profil Fotoğrafı",
        "change_password": "Şifreyi Değiştir",
        "leave_password_blank": "Mevcut şifrenizi korumak için bu alanları boş bırakın.",
        "current_password": "Mevcut Şifre",
        "new_password": "Yeni Şifre",
        "confirm_new_password": "Yeni Şifreyi Onayla",
        "password_strength": "Şifre gücü",
        "password_strength_weak": "Zayıf",
        "password_strength_fair": "Orta",
        "password_strength_good": "İyi",
        "password_strength_strong": "Güçlü",
        "password_strength_very_strong": "Çok güçlü",
        "back": "Geri",
        "no_advanced_matches_found": "Gelişmiş eşleşme bulunamadı",
        "starred_match": "Kaydedilen Eşleşme",
        "remove_star": "Kaydı Kaldır",
        "remove_star_question": "Bu kaydedilen eşleşmeyi kaldırmak istediğinizden emin misiniz?",
        "remove": "Kaldır",
        "all_cities": "Tüm Şehirler",
        "all_faculties": "Tüm Fakülteler",
        "all_departments": "Tüm Bölümler",
        "no_starred_matches": "Henüz kaydedilmiş eşleşme yok",
        "saved_matches_message": "Gelişmiş Eşleşmeler bölümünde kaydettiğiniz eşleşmeler burada görüntülenir.",
        "go_to_advanced_matches": "Kaydetmek istediğiniz eşleşmeleri Gelişmiş Eşleşmeler bölümünden yıldızlayın.",
        "why_this_match": "Neden Bu Eşleşme?",
        "matched_user_contact": "Eşleşen Kullanıcı Bilgileri",
        "their_preferences": "Tercihleri",
        "why_this_user_matches_you": "Bu Kullanıcı Neden Sizinle Eşleşiyor?",
        "compatibility_score": "Uyumluluk Puanı",
        "match_level": "Eşleşme Seviyesi",
        "close": "Kapat",
        "home_description": "Üniversite personelinin üniversite, bölüm, ders tercihleri ve hedef şehir ilgilerine göre uygun akademik değişim ve iş birliği fırsatları bulmasına yardımcı olan akıllı bir akademik platformdur.",
        "show_all_users": "Tüm Kullanıcıları Göster",
        "hide_users": "Kullanıcıları Gizle",
        "first_five_users": "İlk beş kayıtlı kullanıcı önce gösterilir.",
        "advanced_match": "Gelişmiş Eşleşme",
        "create_profile_desc": "Akademik bilgilerinizi, üniversitenizi, bölümünüzü, öğretim tercihlerinizi ve tercih ettiğiniz değişim hedefini kaydedin.",
        "explore_users_desc": "Kayıtlı üniversite personelini inceleyin ve olası akademik iş birliği ve değişim fırsatlarını keşfedin.",
        "receive_matches_desc": "Sistem tercihleri karşılaştırır ve en uygun akademik eşleşmeleri önerir.",
        "about_system_desc": "Akademik Permütasyon Sistemi, üniversite personelini uygun akademik değişim fırsatlarıyla eşleştirmek için tercih tabanlı eşleştirme ve biyomimetik ilhamlı mantık kullanır. Fakülteleri, bölümleri, akademik unvanları, öğretim stillerini, üniversiteleri ve hedef tercihlerini değerlendirerek anlamlı öneriler oluşturur.",
        "benefit_1": "Uygun akademik değişim fırsatlarını bulun",
        "benefit_2": "Uyumlu üniversite personeliyle bağlantı kurun",
        "benefit_3": "Akıllı eşleştirme ile zaman kazanın",
        "benefit_4": "Her eşleşmenin neden önerildiğini anlayın",
        "email": "E-posta",
        "secure_desc": "Verileriniz güvende ve korunmaktadır.",
        "smart_matching_desc": "Akıllı algoritmalar en iyi eşleşmeleri bulur.",
        "academic_collaboration_desc": "Akademisyenlerle bağlantı kurun ve iş birliği yapın.",
        "preference_based_desc": "Hedeflerinize göre eşleşmeler.",
        "potential_matches_desc": "En iyi beş olası eşleşmeniz aşağıda gösterilmektedir. Neden önerildiğini görmek için bir eşleşmeye tıklayın.",
        "click_match_explanation": "Eşleşme açıklamasını görmek için tıklayın.",
        "advanced_matches_desc": "Kayıtlı profilinizi değiştirmeden yeni bir şehir, fakülte veya bölüm tercihi seçin.",
        "good_match": "İyi Eşleşme",
        "weak_match": "Zayıf Eşleşme",
        "excellent_match": "Mükemmel Eşleşme",
        "exploratory_match": "Keşif Eşleşmesi",
        "reason_same_department": "İkiniz de aynı bölümdesiniz.",
        "reason_pref_department": "Bu kullanıcının bölümü tercih ettiğiniz bölümle eşleşiyor.",
        "reason_pref_city": "Bu kullanıcı şu anda tercih ettiğiniz şehirde bulunuyor.",
        "reason_same_title": "İkiniz de aynı akademik unvana sahipsiniz.",
        "reason_mutual_city": "İkiniz de birbirinizin şehrine taşınmayı tercih ediyorsunuz (karşılıklı eşleşme).",
        "reason_partial": "Bu kullanıcı profilinizle kısmi akademik uyuma sahip.",
        "reason_advanced": "Bu kullanıcı gelişmiş arama tercihlerinizle eşleşiyor.",
        "reason_starred": "Bu eşleşmeyi Gelişmiş Eşleşmeler bölümünden kaydettiniz.",
        "login": "Giriş Yap",
        "register_user": "Kullanıcı Kaydı",
        "register_new_user": "Yeni Kullanıcı Kaydı",
        "landing_description": "Üniversite personeli kaydı ve tercih tabanlı eşleştirme için karar destek platformu.",
        "login_description": "Kayıtlı üniversite e-postanızı ve şifrenizi girin.",
        "new_user_register_here": "Yeni kullanıcı mısınız? Buradan kayıt olun",
        "university_email": "Üniversite E-postası",
        "password": "Şifre",
        "confirm_password": "Şifreyi Onayla",
        "enter_password": "Şifrenizi girin",
        "password_min_placeholder": "En az 8 karakter",
        "confirm_password_placeholder": "Şifreyi tekrar girin",
        "show_password": "Şifreyi göster",
        "hide_password": "Şifreyi gizle",
        "show_confirmed_password": "Onay şifresini göster",
        "hide_confirmed_password": "Onay şifresini gizle",
        "register_description": "Akademik permütasyon profilinizi oluşturmak için her adımı tamamlayın.",
        "step_personal_details": "Adım 1: Kişisel Bilgiler",
        "step_current_city_university": "Adım 2: Mevcut Şehir ve Üniversite",
        "step_current_faculty_department": "Adım 3: Mevcut Fakülte ve Bölüm",
        "step_preferred_city_university": "Adım 4: Tercih Edilen Şehir ve Üniversite",
        "step_preferred_faculty_department": "Adım 5: Tercih Edilen Fakülte ve Bölüm",
        "step_teaching_preferences": "Adım 6: Ders Tercihleri",
        "select_academic_rank": "Akademik ünvan seçin",
        "select_current_city": "Mevcut şehir seçin",
        "select_city_first": "Önce şehir seçin",
        "select_current_faculty": "Mevcut fakülte seçin",
        "select_faculty_first": "Önce fakülte seçin",
        "select_preferred_city": "Tercih edilen şehir seçin",
        "select_preferred_faculty": "Tercih edilen fakülte seçin",
        "select_language": "Dil seçin",
        "select_teaching_mode": "Ders verme şekli seçin",
        "select_university": "Üniversite seçin",
        "select_department": "Bölüm seçin",
        "current_faculty": "Mevcut Fakülte",
        "preferred_teaching_language": "Tercih Edilen Ders Dili",
        "preferred_teaching_mode": "Tercih Edilen Ders Verme Şekli",
        "complete_registration": "Kaydı Tamamla",
        "next": "İleri",
        "full_name_placeholder": "Ad soyad girin",
        "rank_research_assistant": "Araştırma Görevlisi",
        "rank_lecturer": "Öğretim Görevlisi",
        "rank_assistant_professor": "Doktor Öğretim Üyesi",
        "rank_associate_professor": "Doçent",
        "rank_professor": "Profesör",
        "faculty_engineering": "Mühendislik",
        "faculty_medicine": "Tıp",
        "faculty_law": "Hukuk",
        "faculty_education": "Eğitim",
        "faculty_arts_sciences": "Fen-Edebiyat",
        "faculty_economics_admin": "İktisadi ve İdari Bilimler",
        "language_english": "İngilizce",
        "language_turkish": "Türkçe",
        "language_turkish_english": "Türkçe ve İngilizce",
        "language_french": "Fransızca",
        "language_german": "Almanca",
        "language_arabic": "Arapça",
        "language_italian": "İtalyanca",
        "language_russian": "Rusça",
        "language_chinese": "Çince",
        "language_spanish": "İspanyolca",
        "mode_face_to_face": "Yüz yüze",
        "mode_hybrid": "Hibrit",
        "city_istanbul": "İstanbul",
        "city_ankara": "Ankara",
        "city_izmir": "İzmir",
        "city_bursa": "Bursa",
        "city_antalya": "Antalya",
        "university_detected": "Üniversite algılandı",
        "error_valid_university_email": "Lütfen geçerli bir üniversite e-postası kullanın.",
        "error_password_length": "Şifre en az 8 karakter uzunluğunda olmalıdır.",
        "error_passwords_do_not_match": "Şifreler eşleşmiyor.",
        "error_email_registered": "Bu e-posta zaten kayıtlı. Lütfen giriş yapın.",
        "error_incorrect_password": "Şifre hatalı. Lütfen tekrar deneyin.",
        "error_email_not_registered": "Bu e-posta henüz kayıtlı değil. Lütfen önce kayıt olun.",


    }
}
ALLOWED_DOMAINS = [
    "@bau.edu.tr",
    "@istanbul.edu.tr",
    "@itu.edu.tr",
    "@bogazici.edu.tr",
    "@marmara.edu.tr",
    "@yildiz.edu.tr",
    "@koc.edu.tr",
    "@sabanciuniv.edu.tr",
    "@bilgi.edu.tr",
    "@uskudar.edu.tr",
    "@medipol.edu.tr",
    "@ankara.edu.tr",
    "@metu.edu.tr",
    "@hacettepe.edu.tr",
    "@gazi.edu.tr",
    "@bilkent.edu.tr",
    "@deu.edu.tr",
    "@ege.edu.tr",
    "@iyte.edu.tr",
    "@uludag.edu.tr",
    "@akdeniz.edu.tr",
    
]

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password_hash TEXT,
            name TEXT NOT NULL,
            rank TEXT NOT NULL,
            department TEXT NOT NULL,
            current_faculty TEXT,
            current_university TEXT NOT NULL,
            current_city TEXT NOT NULL,
            preferred_faculty TEXT,
            preferred_department TEXT,
            preferred_university TEXT NOT NULL,
            preferred_city TEXT NOT NULL,
            teaching_language TEXT,
            teaching_mode TEXT
        )
    """)
        
    columns = [column[1] for column in cursor.execute("PRAGMA table_info(users)").fetchall()]

    if "email" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")

    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")

    if "current_faculty" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN current_faculty TEXT")

    if "preferred_faculty" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN preferred_faculty TEXT")

    if "preferred_department" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN preferred_department TEXT")

    if "teaching_language" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN teaching_language TEXT")
    
    if "teaching_mode" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN teaching_mode TEXT")

    if "profile_picture" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN profile_picture TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS starred_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            matched_user_id INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def university_email(email):
    return any(email.endswith(domain) for domain in ALLOWED_DOMAINS)

def is_logged_in():
    return "email" in session
def get_language():
    return session.get("language", "en")

def get_translations():
    lang = get_language()
    return translations.get(lang, translations["en"])

def public_template_context():
    return {
        "t": get_translations(),
        "lang": get_language(),
    }

def profile_back_url(user_id):
    back_url = request.args.get("back_url")

    if back_url:
        return back_url

    referrer = request.referrer or ""
    own_profile_path = f"/profile/{user_id}"

    if referrer and "/edit-profile/" not in referrer and own_profile_path not in referrer:
        return referrer

    return "/dashboard"

def calculate_match(u1, u2):
    score = 0

    # 1. Department Alignment (+40) — Hard Constraint.
    # If the departments are not aligned the pairing is not viable,
    # so we return 0 immediately instead of scoring other factors.
    department_aligned = (
        u1["department"] == u2["department"]
        or u1["preferred_department"] == u2["department"]
    )
    if not department_aligned:
        return 0
    score += 40

    # 2. Geographical / City Preference (+30)
    if u1["preferred_city"] == u2["current_city"]:
        score += 30

    # 3. Academic Title Equity (+20)
    if u1["rank"] == u2["rank"]:
        score += 20

    # 4. Mutual Choice Bonus (+10)
    if (
        u1["preferred_city"] == u2["current_city"]
        and u2["preferred_city"] == u1["current_city"]
    ):
        score += 10

    return score

@app.route("/")
def home():
    return render_template("index.html", **public_template_context())

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not university_email(email):
            error = get_translations()["error_valid_university_email"]
            return render_template("login.html", error=error, **public_template_context())

        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            password_hash = user["password_hash"]

            if not password_hash:
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (generate_password_hash(password), user["id"])
                )
                conn.commit()
                session["email"] = email
                conn.close()
                return redirect("/dashboard")

            if check_password_hash(password_hash, password):
                session["email"] = email
                conn.close()
                return redirect("/dashboard")

            error = get_translations()["error_incorrect_password"]
        else:
            error = get_translations()["error_email_not_registered"]

        conn.close()

    return render_template("login.html", error=error, **public_template_context())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        name = request.form["name"]
        rank = request.form["rank"]
        current_city = request.form["current_city"]
        current_university = request.form["current_university"]
        current_faculty = request.form["current_faculty"]
        department = request.form["department"]
        preferred_city = request.form["preferred_city"]
        preferred_university = request.form["preferred_university"]
        preferred_faculty = request.form["preferred_faculty"]
        preferred_department = request.form["preferred_department"]
        teaching_language = request.form["teaching_language"]
        teaching_mode = request.form["teaching_mode"]

        if not university_email(email):
            return render_template(
                "register.html",
                error=get_translations()["error_valid_university_email"],
                **public_template_context()
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                error=get_translations()["error_password_length"],
                **public_template_context()
            )

        if password != confirm_password:
            return render_template(
                "register.html",
                error=get_translations()["error_passwords_do_not_match"],
                **public_template_context()
            )

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template(
                "register.html",
                error=get_translations()["error_email_registered"],
                **public_template_context()
            )

        cursor.execute("""
            INSERT INTO users (
                email, password_hash, name, rank,
                current_city, current_university, current_faculty, department,
                preferred_city, preferred_university, preferred_faculty, preferred_department,
                teaching_language, teaching_mode
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email, generate_password_hash(password), name, rank,
            current_city, current_university, current_faculty, department,
            preferred_city, preferred_university, preferred_faculty, preferred_department,
            teaching_language, teaching_mode
        ))

        conn.commit()
        conn.close()

        session["email"] = email
        return redirect("/dashboard")

    return render_template("register.html", **public_template_context())

@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (session["email"],)
    )
    current_user = cursor.fetchone()

    if current_user is None:
        conn.close()
        session.clear()
        return redirect("/login")

    cursor.execute(
        "SELECT * FROM users WHERE email != ?",
        (session["email"],)
    )
    other_users = cursor.fetchall()

    cursor.execute("""
        SELECT matched_user_id
        FROM starred_matches
        WHERE user_email = ?
    """, (session["email"],))
    starred_rows = cursor.fetchall()

    conn.close()

    current_user_dict = dict(current_user)
    other_users_list = [dict(user) for user in other_users]
    starred_ids = [row["matched_user_id"] for row in starred_rows]

    t = get_translations()

    def match_label(score):
        if score >= 70:
            return t["excellent_match"]
        elif score >= 40:
            return t["good_match"]
        elif score > 0:
            return t["weak_match"]
        else:
            return t["exploratory_match"]

    matches = []

    for other_user in other_users_list:
        score = calculate_match(current_user_dict, other_user)

        if score > 0:
            label = match_label(score)

            reasons = []

            # 1. Department Alignment (+40)
            if current_user_dict["department"] == other_user["department"]:
                reasons.append(t["reason_same_department"])
            elif current_user_dict["preferred_department"] == other_user["department"]:
                reasons.append(t["reason_pref_department"])

            # 2. Geographical / City Preference (+30)
            if current_user_dict["preferred_city"] == other_user["current_city"]:
                reasons.append(t["reason_pref_city"])

            # 3. Academic Title Equity (+20)
            if current_user_dict["rank"] == other_user["rank"]:
                reasons.append(t["reason_same_title"])

            # 4. Mutual Choice Bonus (+10)
            if (
                current_user_dict["preferred_city"] == other_user["current_city"]
                and other_user["preferred_city"] == current_user_dict["current_city"]
            ):
                reasons.append(t["reason_mutual_city"])

            if not reasons:
                reasons.append(t["reason_partial"])

            matches.append({
                "user1": current_user_dict["name"],
                "user2": other_user["name"],
                "score": score,
                "label": label,
                "matched_user": other_user,
                "reasons": reasons
            })

    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    city_filter = request.args.get("city_filter", "")
    faculty_filter = request.args.get("faculty_filter", "")
    department_filter = request.args.get("department_filter", "")
    try:
        min_score_filter = int(request.args.get("min_score_filter", 0))
    except ValueError:
        min_score_filter = 0

    min_score_filter = max(0, min(min_score_filter, 100))
    active_section = request.args.get("section", "home")

    advanced_matches = []

    for other_user in other_users_list:
        city_ok = True
        faculty_ok = True
        department_ok = True

        if city_filter:
            city_ok = other_user["current_city"] == city_filter

        if faculty_filter:
            faculty_ok = (
                other_user["current_faculty"] == faculty_filter
                or other_user["preferred_faculty"] == faculty_filter
            )

        if department_filter:
            department_ok = (
                other_user["department"] == department_filter
                or other_user["preferred_department"] == department_filter
            )

        if city_ok and faculty_ok and department_ok:
            score = calculate_match(current_user_dict, other_user)
            if score < min_score_filter:
                continue

            label = match_label(score)

            advanced_matches.append({
                "user1": current_user_dict["name"],
                "user2": other_user["name"],
                "score": score,
                "label": label,
                "matched_user": other_user,
                "reasons": [t["reason_advanced"]]
            })

    advanced_matches = sorted(advanced_matches, key=lambda x: x["score"], reverse=True)

    starred_matches = []

    for other_user in other_users_list:
        if other_user["id"] in starred_ids:
            score = calculate_match(current_user_dict, other_user)
            label = match_label(score)

            starred_matches.append({
                "user1": current_user_dict["name"],
                "user2": other_user["name"],
                "score": score,
                "label": label,
                "matched_user": other_user,
                "reasons": [t["reason_starred"]]
            })

    top_matches = {}

    if matches:
        top_matches[current_user_dict["name"]] = matches[0]

    return render_template(
        "dashboard.html",
        users=other_users,
        matches=matches,
        advanced_matches=advanced_matches,
        starred_matches=starred_matches,
        starred_ids=starred_ids,
        selected_city=city_filter,
        selected_faculty=faculty_filter,
        selected_department=department_filter,
        selected_min_score=min_score_filter,
        active_section=active_section,
        top_matches=top_matches,
        user=current_user,
        t=t,
        lang=get_language()
    )
@app.route("/star-match/<int:matched_user_id>")
def star_match(matched_user_id):
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM starred_matches
        WHERE user_email = ? AND matched_user_id = ?
    """, (session["email"], matched_user_id))

    existing_star = cursor.fetchone()

    if not existing_star:
        cursor.execute("""
            INSERT INTO starred_matches (user_email, matched_user_id)
            VALUES (?, ?)
        """, (session["email"], matched_user_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer or "/dashboard")


@app.route("/unstar-match/<int:matched_user_id>")
def unstar_match(matched_user_id):
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM starred_matches
        WHERE user_email = ? AND matched_user_id = ?
    """, (session["email"], matched_user_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer or "/dashboard")

@app.route("/profile/<int:user_id>")
def profile(user_id):
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    if user is None:
        return "User not found"

    return render_template(
        "profile.html",
        user=user,
        back_url=profile_back_url(user_id),
        t=get_translations(),
        lang=get_language()
    )

@app.route("/edit-profile/<int:user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        conn.close()
        return "User not found"
    
    if user["email"] != session["email"]:
        conn.close()
        return redirect("/dashboard")

    back_url = profile_back_url(user_id)

    if request.method == "POST":
        back_url = request.form.get("back_url") or back_url
        name = request.form["name"]
        rank = request.form["rank"]
        current_city = request.form["current_city"]
        current_university = request.form["current_university"]
        current_faculty = request.form["current_faculty"]
        department = request.form["department"]
        preferred_city = request.form["preferred_city"]
        preferred_university = request.form["preferred_university"]
        preferred_faculty = request.form["preferred_faculty"]
        preferred_department = request.form["preferred_department"]
        teaching_language = request.form["teaching_language"]
        teaching_mode = request.form["teaching_mode"]
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")
        uploaded_file = request.files.get("profile_picture")

        if new_password or confirm_password:
            if len(new_password) < 8:
                conn.close()
                return render_template(
                    "edit_profile.html",
                    user=user,
                    error="New password must be at least 8 characters long.",
                    back_url=back_url,
                    t=get_translations(),
                    lang=get_language()
                )

            if new_password != confirm_password:
                conn.close()
                return render_template(
                    "edit_profile.html",
                    user=user,
                    error="New passwords do not match.",
                    back_url=back_url,
                    t=get_translations(),
                    lang=get_language()
                )

            if user["password_hash"] and not check_password_hash(user["password_hash"], current_password):
                conn.close()
                return render_template(
                    "edit_profile.html",
                    user=user,
                    error="Current password is incorrect.",
                    back_url=back_url,
                    t=get_translations(),
                    lang=get_language()
                )

        profile_picture = user["profile_picture"]
        if uploaded_file and uploaded_file.filename:
             filename = secure_filename(uploaded_file.filename)

             extension = os.path.splitext(filename)[1]

             new_filename = f"user_{user_id}{extension}"

             save_path = os.path.join(
                 "static",
                 "profile_pics",
                 new_filename
             )

             uploaded_file.save(save_path)

             profile_picture = f"profile_pics/{new_filename}"


        cursor.execute("""
            UPDATE users
            SET name = ?,
                rank = ?,
                current_city = ?,
                current_university = ?,
                current_faculty = ?,
                department = ?,
                preferred_city = ?,
                preferred_university = ?,
                preferred_faculty = ?,
                preferred_department = ?,
                teaching_language = ?,
                teaching_mode = ?,
                profile_picture = ?
            WHERE id = ?
        """, (
            name, rank,
            current_city, current_university, current_faculty, department,
            preferred_city, preferred_university, preferred_faculty, preferred_department,
            teaching_language, teaching_mode, profile_picture, user_id
        ))

        if new_password:
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (generate_password_hash(new_password), user_id)
            )

        conn.commit()
        conn.close()
        return redirect(f"/profile/{user_id}?back_url={quote(back_url, safe='')}")

    conn.close()
    return render_template(
    "edit_profile.html",
    user=user,
    back_url=back_url,
    t=get_translations(),
    lang=get_language()
)

@app.route("/set-language/<language>")
def set_language(language):
    if language in ["en", "tr"]:
        session["language"] = language

    return redirect(request.referrer or "/dashboard")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
