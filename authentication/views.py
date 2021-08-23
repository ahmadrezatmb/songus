from random import randint
from json.encoder import JSONEncoder
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User 
from web.models import group, songususer
from .models import temperoryaccount
def random_string(num):
    final = ''
    li = 'abcdefghijklmnopqrstuxwzyABCDEFGHIJKLMNOPQRSTUYXZ1234567890'
    for i in range(1,num+1):
        random_index = randint(1,57)
        final += li[random_index]
    return final


def customlogin(request):
    if request.user.is_authenticated:
        messages.success(request, 'already logged in.')
        return redirect('dashboard')
    elif 'username' in request.POST and 'password' in request.POST:
        this_user = authenticate(username=request.POST['username'],
                                 password=request.POST['password'])
        if this_user is None:
            context = {
                'usernameerror' : 'username or password is wrong !',
            }
            return render(request, 'authentication/login.html', context)
        login(request, this_user)
        messages.success(request, 'welcome !')
        return redirect('dashboard')
    else:
        return render(request, 'authentication/login.html')


@login_required
def customlogout(request):
    logout(request)
    return redirect('login')


def customregister(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    context = {
        'usernameerror' : '',
        'passworderror' : '',
        'passwordagainerror' : '',
        'emailerror' : ''
    }
    if ('username' in request.POST and 
        'email' in request.POST and 
        'password' in request.POST and 
        'passwordagain' in request.POST):

        password = request.POST['password']
        password_again = request.POST['passwordagain']
        username = request.POST['username']
        email = request.POST['email']
        has_error = False
        if password != password_again :
            context['passwordagainerror'] = 'passwords are not the same'
            has_error = True
        same_users = songususer.objects.filter(user__username=username)
        if same_users.count() != 0 :
            context['usernameerror'] = 'this username is not unique'
            has_error = True
        same_users_eamil = songususer.objects.filter(user__email=email)
        if same_users_eamil.count() != 0 :
            context['emailerror'] = 'email should be unique'
            has_error = True

        if password == '':
            context['passworderror'] = 'password should not be empty!'
            has_error = True


        if username == '':
            context['usernameerror'] = 'username should not be empty!'
            has_error = True


        if  email == '':
            context['emailerror'] = 'email should not be empty'
            has_error = True


        if has_error:
            return render(request, 'authentication/register.html', context)
        
        code = random_string(50)
        temp_account = temperoryaccount.objects.create(
                                            username=username,
                                            password=make_password(password),
                                            email=email,
                                            code=code)
        temp_account.save()
        subject = 'amber signup'
        message = 'here is the famous link.  {}?code={}'.format(
                                                            request.build_absolute_uri('/accounts/register/'),
                                                            code)
        recepient = email
        send_mail(subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [recepient],
                  fail_silently=False)

        messages.success(request, 'verfication link has been send !')
        return render(request, 'authentication/login.html', context)
    
    elif 'code' in request.GET :
        code = request.GET['code']
        # check if link is true and we sent it
        user_exist = temperoryaccount.objects.filter(code = code)
        if user_exist.count() == 0 :
            messages.warning(request, 'wrong code !')
            return render(request, 'authentication/login.html', context )
        
        password = user_exist[0].password 
        # managing data
        username = user_exist[0].username
        email = user_exist[0].email
        # check if this user is unique or not
        same_usr = songususer.objects.filter(user__username=username,
                                             user__email=email)
        if same_usr.count() != 0 :
            # oops! some asshole wants to use activate their account twice !
            messages.warning(request , 'this account has been activated before !')
            return render(request, 'authentication/login.html', context)

        # creating the activated user here
        new_base_user = User.objects.create(username=username,
                                          password=password,
                                          email=email)
        new_user = songususer.objects.create(user=new_base_user)
        private_group = group.objects.create(name='privategroup',
                                             is_private=True,
                                             description='', 
                                             owner=new_user)
        private_group.save()
        user_exist.isactivenow = True
        new_user.save()
        login(request, new_base_user)
        return redirect('dashboard')
    else:
        return render(request, 'authentication/register.html')
    