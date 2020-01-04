# from django.dispatch import receiver
# from allauth.socialaccount.signals import social_account_added, social_account_updated
# from django.shortcuts import render, redirect
# from django.contrib import messages


# # Signal not working 
# @receiver(social_account_added)
# def user_signed_up_(request, sociallogin, **kwargs):
#     print('im here')
#     return render(request, 'accounts/social_login.html')

# @receiver(social_account_updated)
# def user_signed_up_(request, sociallogin, **kwargs):
#     messages.success(request, 'Ma shtaaa')
#     print(sociallogin)
#     return redirect('dashboard')
    