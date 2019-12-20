from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth


# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name'] 
        username= request.POST['username'] 
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
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                    last_name=last_name)
                    messages.success(request, 'Sucesfully created new account')
                    context = {
                        'current_user': user
                    }
                    return render(request, 'accounts/login.html', context)
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        messages.debug(request, 'This is GET')
        return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')
    
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
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
        messages.debug(request, 'This is GET')
        return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


def logout(request):
    # if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def admindashboard(request):
    return render(request, 'accounts/admindashboard.html')
