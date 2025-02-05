from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from gym_trainer.models import Schedule, Routine
from django.contrib import messages
from .forms import *

# Depenent del rol de l'usuari redirigim a una pàgina o un altre
@login_required
def home(request):
    context = {}
    if request.user.role == 'trainer':
        return redirect('gym_trainer:assign_schedule') 
    
    elif request.user.role == 'user':
        return redirect('gym_workouts:workouts')
    
    elif request.user.role == 'admin':
        return redirect('gym_admin:user_list')
    
    elif request.user.role == 'gerent':
        return redirect('gym_gerent:user_list')
    

    return render(request, 'home.html', context)


# Vista per registrar l'usuari
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Registre exitós.")
                return redirect('login')
            except Exception as e:
                print(f"Hi ha hagut un error: {str(e)}")
        else:
            messages.warning(request, "Hi han errors al formulari.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


# Vista per loguejar un usuari
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciat sessió correctament!')
                return redirect('gym_app:home')
            else:
                messages.warning(request, 'ERROR: Credencials incorrectes.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('gym_app:home')


# Vista per editar el perfil
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'El perfil s\'ha actualitzat correctament.')
            return redirect('gym_app:home')
    else:
        form = UserUpdateForm(instance=request.user)
        
    return render(request, 'profile_edit.html', {'form': form, 'active_tab': "profile"})


