from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserEditForm 
from gym_app.models import User  

# Llimstem als usuaris
@login_required
def user_list(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("No pots accedir a aquesta pàgina.")
    
    users = User.objects.exclude(id=request.user.id)  # Excloem l'usuari actual
    return render(request, 'user_list.html', {'users': users})



# Editem la informació de l'usuari
@login_required
def edit_user(request, user_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("No pots accedir a aquesta pàgina.")

    user_to_edit = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Si s'envia un formulari, utilitzem les dades proporcionades per actualitzar l'usuari.
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save() 
            messages.success(request, "Perfil actualitzat amb èxit.")
            return redirect('gym_admin:user_list')
        else:
            messages.warning(request, "Corregeix els errors del formulari.")
    else:
        form = UserEditForm(instance=user_to_edit)

    return render(request, 'edit_user.html', {'form': form, 'user': request.user})

# Eliminem un usuari de la BBDD.
@login_required
def delete_user(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("No pots accedir a aquesta pàgina.")

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            # Provem d'agafar l'usuari i eliminar-lo
            user = User.objects.get(id=user_id)
            user.delete() 
            messages.success(request, f"Usuari {user.username} eliminat amb èxit.")
        except User.DoesNotExist:
            messages.error(request, "Usuari no trobat.")
    
    return redirect('gym_admin:user_list')
