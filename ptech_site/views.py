from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm, UpdateProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import send_mail
from django.template import loader
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.conf import settings

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        print("post reques is coming ", request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("form is valid", form)
            user = form.save(commit=False)
            # user.refresh_from_db()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account'
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.FROM_EMAIL, [to_email], fail_silently=False) ##TODO change email from settings
            return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
        else:
            return HttpResponse('username is already taken or password didnt match')
    else:
        form = RegisterForm()
        print("no post request", form)
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # if user is not None and account_activation_token.check_token(user, token): #TODO uncomment this for token validation
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        template = loader.get_template('index.html')
        context = {
                'some_variable': '',
            }
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

def Login(request): 
    if request.method == 'POST': 
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            print("login - username", username, "pass", password)
            user = authenticate(request, username = username, password = password) 
            if user is not None:
                if user.is_active:
                    print("user", user)
                    form = login(request, user) 
                    # messages.success(request, f' wecome {username} !!') 
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("Your account was inactive.")
            else: 
                return HttpResponse("Invalid login details given")
    form = AuthenticationForm() 
    return render(request, 'login.html', {'form':form})

def profile(request):
    if request.method == 'POST':
        print("request.POST",request.user, request.POST)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            print(' success full y upated password                                 ')
            return redirect('/')
        else:
            print(form.errors)
            # return HttpResponse("Your account was inactive.")
            return render(request, 'profile.html',{'form':form} )
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile.html',{'form':form} )

def index(request):
    return render(request, 'index.html')

# def profile(request):
#     return render(request, 'profile.html')

def students(request):
    return render(request, 'students.html')

def billing(request):
    return render(request, 'billing.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def recoverpw(request):
    return render(request, 'recoverpw.html')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your account was inactive.")
#         else:
#             print("Someone tried to login and failed.")
#             print("They used username: {} and password: {}".format(username,password))
#             return HttpResponse("Invalid login details given")
#     else:
#         return render(request, 'login.html', {})