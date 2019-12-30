from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from trainingprograms.models import Program_User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings




# Create your views here.
def register(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST':
            first_name = request.POST['first_name'] 
            last_name = request.POST['last_name'] 
            username= request.POST['username'].lower() 
            password = request.POST['password'] 
            password = request.POST['password'] 
            password2 = request.POST['password2'] 
            email = request.POST['email'] 
            
            # Validate passwords
            if password == password2:
                #Checking username
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is already taken')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "There's an account already registered with this mail")
                        return redirect('register')
                    else:
                        #Validation good
                        user = User.objects.create_user(username=username, email=email, password=password, 
                        first_name=first_name, last_name=last_name, is_active=False)
                        # Get current site
                        subject = 'Activate your Account'
                        current_site = get_current_site(request)
                        # create Message
                        # message = render_to_string('accounts/account_activation_email.txt', {      #Normal string(message) in the  mail
                        #     'user': user,
                        #     'domain': current_site.domain,
                        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                        #     'token': account_activation_token.make_token(user),
                        # })
                        domain = current_site.domain
                        message = render_to_string('accounts/account_activation_email.html', {
                            'user': user,
                            'domain': domain[:-1],
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        # send activation link to the user
                        user.email_user(subject=subject, message=message)

                        messages.success(request, 'Mail has been sent')

                        context = {
                            'current_user': user
                        }
                        return render(request, 'accounts/login.html', context)
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
        else:
            return render(request, 'accounts/register.html')

    else:
            messages.error(request, 'You already have an account')
            return redirect('dashboard')

    
def login(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, f'Welcome {username.capitalize()}, you have been successfully logged in!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid login! Try again')
                return redirect('login')        
        else:
            return render(request, 'accounts/login.html')
    else:
        messages.error(request, 'You are already logged in!')
        return redirect('dashboard')
    

def logout(request):
    # if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

def dashboard(request):
    
    if not request.user.is_authenticated:
        messages.error(request, 'Login required')
        messages.debug(request, "You can't use dashboard if not logged in!")
        return redirect('login')
    else:
        user_liked_programs = Program_User.objects.order_by('-program__list_date').filter(user=request.user.id, is_liked=True, program__is_published=True)

        paginator = Paginator(user_liked_programs, 6)

        page = request.GET.get('page')
        user_liked_programs_paginated = paginator.get_page(page)

        context = {
            'programs': user_liked_programs_paginated
        }
        return render(request, 'accounts/dashboard.html', context)




def admindashboard(request):
    return render(request, 'accounts/admindashboard.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email conformation is valid! You can log in')
        return redirect('login')
    else:
        messages.error(request, 'Invalid email conformation, please try again!')
        return render(request, 'accounts/account_activation_invalid.html')