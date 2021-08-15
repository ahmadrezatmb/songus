from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login ,logout
from json.encoder import JSONEncoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from web.models import group, songususer
from random import randint
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import temperoryaccount
from django.contrib.auth.models import User 

def random_string(num):
    final = ''
    li = 'abcdefghijklmnopqrstuxwzyABCDEFGHIJKLMNOPQRSTUYXZ1234567890'
    for i in range(1,num+1):
        random_index = randint(1,57)
        final += li[random_index]
    return final


def customlogin(request):
    if request.user.is_authenticated:
        messages.success(request , 'already logged in.')
        return redirect('dashboard')
    elif 'username' in request.POST and 'password' in request.POST :
        thisuser = authenticate(username=request.POST['username'], password=request.POST['password'])
        if thisuser is None :
            context = {
                'usernameerror' : 'username or password is wrong !',
            }
            return render(request , 'authentication/login.html' , context)
        login(request ,thisuser)
        messages.success(request , 'welcome !')
        return redirect('dashboard')
    else:
        return render(request , 'authentication/login.html')


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
    if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST and 'passwordagain' in request.POST:
        password = request.POST['password']
        passwordagain = request.POST['passwordagain']
        username = request.POST['username']
        email = request.POST['email']
        haserror = False
        if password != passwordagain :
            context['passwordagainerror'] = 'passwords are not the same'
            haserror = True
        sameusers = songususer.objects.filter(user__username = username).count()
        if sameusers != 0 :
            context['usernameerror'] = 'this username is not unique'
            haserror = True
        sameuserseamil = songususer.objects.filter(user__email = email).count()
        if sameuserseamil != 0 :
            context['emailerror'] = 'email should be unique'
            haserror = True

        if password == '':
            context['passworderror'] = 'password should not be empty!'
            haserror = True


        if username == '':
            context['usernameerror'] = 'username should not be empty!'
            haserror = True


        if  email == '':
            context['emailerror'] = 'email should not be empty'
            haserror = True


        if haserror:
            return render(request , 'authentication/register.html' , context)
        
        code = random_string(50)
        temp_account = temperoryaccount.objects.create(username = username , password = password , email = email , code = code)
        temp_account.save()

        subject = 'amber signup'
        message = 'here is the famous link.  {}?code={}'.format(request.build_absolute_uri('/accounts/register/'), code)
        recepient = email
        send_mail(subject, 
        message, settings.EMAIL_HOST_USER, [recepient], fail_silently = False)
        # context = {
        #     'header' : 'activation link just sent !',
        #     'body' : 'activate your account with open it :|'
        # }
        messages.success(request , 'verfication link has been send !' )
        return render(request , 'authentication/login.html' , context)
    elif 'code' in request.GET :
        code = request.GET['code']
        # check if link is true and we sent it
        user_exist = temperoryaccount.objects.filter(code = code)
        if user_exist.count() == 0 :
            # context = {
            #     'header' : 'wrong code !',
            #     'body' : 'the code is wrong !'
            # }
            messages.warning(request , 'wrong code !')
            return render(request , 'authentication/login.html' , context ) 
        
        this_user = user_exist.get()
        password = user_exist[0].password 

        # managing data
        username = user_exist[0].username
        email = user_exist[0].email

        # check if this user is unique or not
        sameusr = songususer.objects.filter( user__username = username , user__email = email)
        if sameusr.count() != 0 :
            # oops! some asshole wants to use activate their account twice !123
            # context = {
            #         'header' : 'this account has been activated before !',
            #         'body' : 'this account has been activated before !'
            #     }
            messages.warning(request , 'this account has been activated before !')
            return render(request , 'authentication/login.html' , context ) 

        # creating the activated user here
        newbaseuser = User.objects.create(username = username , password= make_password(password) , email = email )
        newuser = songususer.objects.create(user = newbaseuser )
        privategroup = group.objects.create(name = 'privategroup' , isprivate=True , description='' ,owner = newuser)
        privategroup.save()
        user_exist.isactivenow = True
        newuser.save()
        login(request , newbaseuser)
        return redirect('dashboard')
    else:
        return render(request , 'authentication/register.html')
    