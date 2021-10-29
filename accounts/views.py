from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from accounts.forms import UserUpdate

# Create your views here.

@login_required(login_url='login') 
def home(request):
    if request.user.is_superuser:
        return redirect('admin-dash')
    else:
        return render(request, 'home.html')


def login(request):
    
    
    if request.user.is_authenticated:

        return redirect('home')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        
            if not user.is_active:
                messages.info(request,'Access Denied')
                return redirect('login')
        except:
            pass

        user = auth.authenticate(username=username,password=password)
        
        if user is not None:

            if user.is_superuser:
                messages.info(request,'Invalid Credentials')
                return redirect('login')

            auth.login(request, user)

            return redirect('home')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html')
        


def register(request):

    if request.user.is_authenticated:

        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')

        else:
            messages.info(request,'Password not matching')
            print('Password not matching')
            return redirect('register')
        
    else:
        return render(request,'register.html')


def logout(request):

    auth.logout(request)
    return redirect('home')
    




def admin(request):
    

    if request.user.is_authenticated:
        return redirect('admin-dash')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            

            if user.is_superuser:
                auth.login(request, user)
                
                return redirect('admin-dash')
            else:
                messages.info(request, 'You are not admin')
                return redirect('admin-login')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('admin-login')

    else:
        return render(request,'admin-login.html')
        

@login_required(login_url='admin-login') 
def admindash(request):
    

    users = User.objects.all()

    context = {
        'users' : users
    }

    return render(request, 'admin-panel.html',context)


def delete(request,pk):
    

    
    User.objects.get(id=pk).delete()
    return redirect('admin-dash')

   



def update(request,pk):

    user = User.objects.get(id=pk)

    form = UserUpdate(instance=user)

    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin-dash')

    context = {'form':form}

    return render(request, 'update.html', context)



def adminlogout(request):
    auth.logout(request)
    return redirect('admin-login')


def blockuser(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    return redirect('admin-dash')

def unblockuser(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save()
    return redirect('admin-dash')
    


def adduser(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('adduser')
                
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('adduser')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('admin-dash')

        else:
            messages.info(request,'Password not matching')
            print('Password not matching')
            return redirect('adduser')
        
    else:
        return render(request,'adduser.html')