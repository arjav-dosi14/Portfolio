import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from main.models import Experience, Education

# Clear existing
Experience.objects.all().delete()
Education.objects.all().delete()

# Education entries
Education.objects.create(
    degree="Bachelor of Technology (B.Tech) in Computer Science & Engineering",
    institution_name="Medi-Caps University, Indore",
    board_or_university="(First Year Completed)",
    start_year="2025",
    end_year="Present",
    percentage_or_cgpa="",
    description="",
    display_order=1
)

Education.objects.create(
    degree="Higher Secondary School Certificate (Class XII)",
    institution_name="Gyan Sagar Vidya Niketan, Indore",
    board_or_university="MPBSE",
    start_year="2024",  # assuming based on graduation 2025? No, the resume says 2025. Wait, 2025 for 12th? Wait, it says "2025-Present" for University, and "2025" for 12th. Let's use start_year="-" end_year="2025". Or just start_year="2024" end_year="2025".
    end_year="2025",
    percentage_or_cgpa="Aggregate: 88%",
    description="Selected as 'MEDHAVI CHHATRA' by the MP state government",
    display_order=2
)

Education.objects.create(
    degree="Secondary School Examination (Class X)",
    institution_name="Lokmanya Vidya Niketan, Indore",
    board_or_university="CBSE",
    start_year="-",
    end_year="2023",
    percentage_or_cgpa="Aggregate: 80%",
    description="",
    display_order=3
)

print("Database populated successfully.")
