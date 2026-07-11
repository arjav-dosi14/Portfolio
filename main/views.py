from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, Experience, Education

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please fill out all fields.')
            
    experiences = Experience.objects.all()
    educations = Education.objects.all()
            
    return render(request, 'index.html', {'experiences': experiences, 'educations': educations})
