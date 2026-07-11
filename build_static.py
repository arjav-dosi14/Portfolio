import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from main.models import Experience, Education
experiences = Experience.objects.all()
educations = Education.objects.all()

context = {
    'experiences': experiences,
    'educations': educations,
}

factory = RequestFactory()
request = factory.get('/')

# Render the template with the database context
html = render_to_string('index.html', context, request=request)

# Make static paths relative so they work on GitHub Pages regardless of repository name
html = html.replace('"/static/', '"./static/')
html = html.replace("'/static/", "'./static/")

os.makedirs('docs', exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Static HTML successfully generated in docs/index.html")
