import json

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate,login,logout

from cryptography.fernet import Fernet

from customer.form import SignInForm, SignUpForm

# Create your views here.
def load_key():
    key = getattr(settings, "PASSWORD_ENCRYPTION_KEY", None)
    if key:
        return key
    else:
        raise ImproperlyConfigured("No configuration  found in your PASSWORD_ENCRYPTION_KEY setting.")

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return(encrypted_message.decode("utf-8"))

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

def index(request):
    return render(request,'index.html')

def sign_up(request):
    response_data = {}
    if request.method == 'POST':
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            #create profile
            user_data = User.objects.create_user(
                    username=email,
                    password=password,
                )
            
            data = form.save(commit=False)
            data.user = user_data
            password = encrypt_message(password)
            data.save()
            return redirect(reverse('customer:index'))
        else:
            print("not valid")
            
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else :
        form = SignUpForm()
        
        context = {
        "form" : form,
        "page_name" : 'Sign Up',
        "url": reverse('customer:sign_up')
    }
    return render(request,'registration/signup.html',context)

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                
                    return redirect(reverse('customer:index'))
                else:
                    
                    return redirect(reverse('customer:index'))
            else:
                response_data = {
                    "status": "false",
                    "message": "Incorrect username or password",
                }
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else:
            print("not  valid")
            return redirect(reverse('customer:signin'))
    else :
        form = SignInForm()
        
        context = {
            'form': form,
            'url': reverse('customer:signin')
        }
    
        return render(request,'registration/login.html',context)

def signout(request):
    logout(request)
    return redirect(reverse('customer:index'))