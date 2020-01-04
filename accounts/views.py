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
import datetime
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.views import View


# Create your views here.
def register(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            first_name = request.POST['first_name'] 
            last_name = request.POST['last_name'] 
            username= request.POST['username'].lower() 
            password = request.POST['password'] 
            password2 = request.POST['password2'] 
            email = request.POST['email'] 
            
            # Validate passwords
            if password == password2 and password:
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
                if password == '':
                    messages.error(request, 'Password field cannot be empty')
                else:
                    messages.error(request, 'Passwords do not match')
                return redirect('register')
        else:
            return render(request, 'accounts/register.html')

    else:
            messages.error(request, 'You already have an account')
            return redirect('dashboard')

    
def login(request):

    # If user is not logged in, you can only then acces this page
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print('login passed')
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

        # The signal that alerts on social user creation by allauth module doesn't work, so -->
        # -- > this condiftion checks if user is new or 10 secs have passed since he used the social register
        if SocialAccount.objects.filter(user=request.user,
            date_joined__gte=datetime.datetime.now()- datetime.timedelta(seconds=5 * 2)).exists():
            request.session['new_socialuser'] = True
            return redirect('profile/username/' + str(request.user.id))


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

# Test this out (make social_auth redirect to this page instead!!)
def change_username(request, user_id):

    # prefarable to add token on this site so not everyone can log in
    if request.user.id == user_id:  
        user = User.objects.get(id=request.user.id)

        # Check the session
        if request.POST.get('refresh_session', '') == 'refresh':
            del request.session['new_socialuser']
            first_time_social_login = True
            if request.POST['username'] == '':
                return redirect('dashboard')

        if user is not None:
            # Check is username exists
            if 'username' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password', False)
                password2 = request.POST.get('password2', False)
                if User.objects.filter(username=username).exists() or username == '':
                    if username == '':
                        messages.warning(request, 'Username cannot be empty!')
                    else:
                        messages.warning(request, 'Username is already taken! Try again')

                    # If it's first time loging in, but there are errors return the needed template with arg. new_socialuser
                    if request.session.get('new_socialuser', False) or first_time_social_login:
                        request.session['new_socialuser'] = True 
                        return render(request, 'accounts/change_username.html', {'new_socialuser': True})
                    elif SocialAccount.objects.filter(user=request.user).exists():
                        return render(request, 'accounts/change_username.html', {'from_social': True})
                    else:
                        return render(request, 'accounts/change_username.html', {'from_social': False})
                else:
                    # if there's password in the form check if passwords are valid(this is for normal user)
                    if password and password==password2 or first_time_social_login:
                        if first_time_social_login:
                            user.username = username
                            user.save()
                            messages.success(request, f'Username changed to {user.username}')
                            return redirect('dashboard')
                        else:
                            if user.check_password(password):
                                user.username = username
                                user.save()
                                messages.success(request, f'Username changed to {user.username}')
                                return redirect('dashboard')
                            else:
                                messages.error(request, 'Password does not match existing password')
                                return render(request, 'accounts/change_username.html', {'from_social': False})
                                
                    else:
                        # if passwords don't match
                        messages.error(request, 'Invalid password!')
                        if request.session.get('new_socialuser', False):
                            return render(request, 'accounts/change_username.html', {'new_socialuser': True})
                        elif SocialAccount.objects.filter(user=request.user).exists():
                            return render(request, 'accounts/change_username.html', {'from_social': True})
                        else:
                            return render(request, 'accounts/change_username.html', {'from_social': False})
                    
            else:
                # If the form is not submitted, just return the template with appropriate form
                if request.session.get('new_socialuser', False):
                        return render(request, 'accounts/change_username.html', {'new_socialuser': True})
                elif SocialAccount.objects.filter(user=user).exists():
                    return render(request, 'accounts/change_username.html', {'from_social': True})
                else:
                    return render(request, 'accounts/change_username.html', {'from_social': False})
    else:
        # return absolute url here so you stay where u are TODO
        previous_url = request.META.get('HTTP_REFERER')
        return redirect('index')

# Make situations to check if old_pass is same with new_one!!!!
def change_password(request, user_id):

    if request.user.id == user_id:  
        if request.method == 'POST':
            old_password = request.POST.get('old_password', False)
            password = request.POST.get('password', False)
            password2 = request.POST.get('password2', False)
            if old_password and password and password2:
                if password == password2:
                    user = User.objects.get(id=request.user.id)
                    if user.has_usable_password():
                        if user.check_password(old_password):
                            if user.check_password(password):
                                # if the current password is same with the new password
                                messages.error(request, "Password can't be same as current password")
                                return render(request, 'accounts/change_password.html')
                            messages.success(request, 'Password has been changed successfully')
                            user.set_password(password)
                            user.save()
                            auth.update_session_auth_hash(request, user)
                            return redirect('dashboard')
                        else:
                            messages.error(request, 'Password does not match existing password')
                            return render(request, 'accounts/change_password.html')
                    else:
                        user.set_password(password)
                        user.save()
                        auth.update_session_auth_hash(request, user)
                        messages.success(request, 'Password has been successfully added')
                        return redirect('dashboard')             
                else:
                    messages.error(request, 'Passwords do not match')
                    return render(request, 'accounts/change_password.html')    
            else:
                messages.error(request, 'Invalid password')
                return render(request, 'accounts/change_password.html')
        else:
            # return the page 
            return render(request, 'accounts/change_password.html')
    else:
        # previous_url = request.META.get('HTTP_REFERER')
        return redirect('index')
