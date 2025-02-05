from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q 
from gym_app.models import User 

@login_required
def user_list(request):
    if request.user.role != 'gerent':
        return HttpResponseForbidden("No pots accedir a aquesta pàgina.")

    users = User.objects.all()

    # Filtrem per cercador
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Ordenar por el campo seleccionado
    sort_by = request.GET.get('sort', 'username')  
    order = request.GET.get('order', 'asc')  

    # Canviem l'ordre depenent de com sigui
    if order == 'desc':
        users = users.order_by(f'-{sort_by}')  
    else:
        users = users.order_by(sort_by) 

    # Paginación
    # Mostrem 10 usuaris per pàgina
    paginator = Paginator(users, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order
    })