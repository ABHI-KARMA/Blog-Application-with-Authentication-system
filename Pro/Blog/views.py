from .models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import message, send_mail
from django.contrib.auth import login,authenticate,logout
from .forms import SearchForm,ContactForm
from .models import BlogPost,Contact
from django.http import Http404
from django.contrib.auth.decorators import login_required

# HOME PAGE VIEW
@login_required
def home(request):
    dataset = BlogPost.objects.all()[:4]
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            try:
                blog = BlogPost.objects.get(title=title)
            except BlogPost.DoesNotExist:
                raise Http404("Data Does Not Exist")
                pk = blog.pk
                return redirect('post',pk=pk)
    else:
        form = SearchForm()
        context = {
            'dataset':dataset,
            'form':form,
            }
    return render(request,'index.html',context)

@login_required
def post(request,pk): 
    data = BlogPost.objects.get(pk=pk)
    return render(request,'post.html',{'data':data})

# ABOUT VIEW
@login_required
def about(request):
    return render(request,'about.html')

# CONTACT VIEW
@login_required
def contact(request):
    if request.method == 'POST':
        n = request.POST.get('name')
        e = request.POST.get('email')
        num = request.POST.get('number')
        msg = request.POST.get('desc')
        contact = Contact.objects.create(name=n,email=e,number=num,message=msg)
        return redirect('contact')
    else:
        form = ContactForm()
    return render(request,'contact.html')


# LOGIN VIEW
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.info(request,'User Not Found')
            return redirect('LOGIN')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.info(request,'Your account is not verified')
            return redirect('LOGIN')

        user = authenticate(username=username,password=password)
        if user is None:
            messages.info(request,'Wrong username and password')
            return redirect('LOGIN')
        else:
            messages.success(request,'Logged In')
            login(request,user)
            return redirect('home')

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('LOGIN')


# REGISTER VIEW
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            if User.objects.filter(username=username).first():
                messages.info(request,'User Name is already Exist!')
                return redirect('REGISTER')
        
            if User.objects.filter(email=email).first():
                messages.info(request,'Email addres is already Exist!')
                return redirect('REGISTER')

            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            sendMail(email,auth_token)
            return redirect('TOKENSEND')
        except Exception as e:
    return render(request,'register.html')

def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'tokensend.html')

# HELPER FUNCTION FOR SEND VERIFICATION EMAIL
def sendMail(email,token):
    subject = 'Verification Mail'
    message = f"Hello, Please paste the link to verify your account http://127.0.0.1:8000/verify/{token} "
    email_from = settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject,message,email_from,recipient)


# VERIFICATION EMAIL VIEW
def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your Account is already Verified')
                return redirect('LOGIN')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your Account has been verified')
            return redirect('LOGIN')
        else:
            return redirect('ERROR')
    except Exception as e:

def error_page(request):
    return render(request,'error.html')


# HELPER FUNCTION FOR SAND MAIL
def send_forget_pass_mail(email,token):
    subject = 'Forget Password Mail'
    message = f"Hello, Click the link to reset your password http://127.0.0.1:8000/recreate-password/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject,message,email_from,recipient)
    return True


# FORGOT PASSWORD VIEW
def forgotPass(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            user_obj = User.objects.filter(username=username)

            if user_obj is None:
                messages.info(request,'User Name Is not Valid')
                return redirect('FORGOTPASS')

            user_obj = User.objects.get(username=username)
            email = user_obj.email
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_pass_token = token
            profile_obj.save()

            send_forget_pass_mail(email,token)
            return redirect('TOKENSEND')

    except Exception as e:
        
    
    return render(request,'forgot-pass.html')


# RECREATE PASSWORD VIEW
def recreatePass(request,token):
    context = {}
    try:
        profile_obj = Profile.objects.get(forgot_pass_token=token)
        context = {
            'user_id':profile_obj.user_id
        }
        if request.method == 'POST':
            new_pass = request.POST['new-pass']
            re_pass = request.POST['new-re-pass']
            user_id = request.POST['user_id']

            if user_id is None:
                messages.info(request,'User not found')
                return redirect(f'/recreate-password/{token}')

            if new_pass != re_pass:
                messages.info(request,'Both password are not same')
                return redirect(f'/recreate-password/{token}')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(re_pass)
            user_obj.save()
            return redirect('LOGIN')

    except Exception as e:
    return render(request,'recreate-pass.html',context)
