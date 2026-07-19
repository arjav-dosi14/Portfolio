from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import logging
from .models import ContactMessage, Experience, Education

logger = logging.getLogger(__name__)

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Determine if the request is an AJAX request from our JS frontend
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json'
        
        if name and email and message:
            try:
                # Save to database
                ContactMessage.objects.create(name=name, email=email, message=message)
                
                # Send email to admin
                subject = f"New Portfolio Contact | {name}"
                body = f"------------------------------------\nName: {name}\n\nEmail: {email}\n\nSubject: {subject}\n\nMessage:\n{message}\n------------------------------------"
                admin_email = settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else 'arjav.dosi0107@gmail.com'
                
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=False,
                )
                
                # Send automatic confirmation email to the visitor
                visitor_subject = "Thanks for contacting me!"
                visitor_body = f"Hello {name},\n\nThank you for contacting me through my portfolio.\n\nI have received your message and will get back to you as soon as possible.\n\nRegards,\nArjav Dosi"
                send_mail(
                    visitor_subject,
                    visitor_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True, # Don't fail if the visitor's email is invalid
                )
                
                if is_ajax:
                    return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent successfully.'})
                
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('home')
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                if is_ajax:
                    return JsonResponse({'status': 'error', 'message': 'Unable to send your message. Please try again later.'}, status=500)
                
                messages.error(request, 'Unable to send your message. Please try again later.')
                return redirect('home')
        else:
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': 'Please fill out all fields.'}, status=400)
                
            messages.error(request, 'Please fill out all fields.')
            
    experiences = Experience.objects.all()
    educations = Education.objects.all()
            
    return render(request, 'index.html', {'experiences': experiences, 'educations': educations})
