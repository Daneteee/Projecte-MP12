from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from gym_trainer.models import Routine, Schedule
from .forms import RoutineForm
from django.contrib import messages

# Comprovem que l'usuari es trainer
def is_trainer(user):
    return user.role == 'trainer'

# En cas que no sigui trainer redirigim a la home
def trainer_required(view_func):
    return user_passes_test(
        is_trainer,
        login_url='home'
    )(view_func)


# Vista per crear una rutina utilitzant el formulari RoutineForm
@login_required
@trainer_required
def create_routine(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.trainer = request.user
            routine.save()
            messages.success(request, 'Rutina creada amb èxit!')
            return redirect('home')
    else:
        form = RoutineForm()
    return render(request, 'create_routine.html', {'form': form, 'active_tab': 'create_routine'})


# Vista on passem les dades per crear el calendari amb les rutines
@login_required
@trainer_required
def assign_schedule(request):
    
    # Agafem totes les rutines i inicialitzem variables
    routines = Routine.objects.all()
    days_of_week = ['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres']
    hours = ['16', '17', '18', '19', '20', '21']
    schedule_data = {}

    # Comprovem si hi han rutines assignades a aquell dia 
    for day in days_of_week:
        for hour in hours:
            schedule_entry = Schedule.objects.filter(day=day, time=f"{hour}:00").first()
            schedule_data[f"{day}_{hour}"] = schedule_entry.routine.id if schedule_entry else None
    
    # Assignem la rutina a un horari        
    if request.method == 'POST':
        for key in schedule_data.keys():
            routine_id = request.POST.get(key)
            if routine_id:
                day, hour = key.split('_')
                Schedule.objects.update_or_create(
                    day=day,
                    time=f"{hour}:00",
                    defaults={'routine_id': routine_id}
                )

        messages.success(request, 'Les rutines han sigut assignades correctament.')

        return redirect('gym_trainer:assign_schedule')

    return render(request, 'schedule.html', {
        'routines': routines,
        'days_of_week': days_of_week,
        'hours': hours,
        'schedule_data': schedule_data,
    })

# Bista per editar la rutina
@login_required
@trainer_required
def edit_routine(request, routine_id):
    # Si trobem la rutina l'editem amb el formulari RoutineForm
    routine = get_object_or_404(Routine, id=routine_id)
    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rutina actualitzada amb èxit.')
            return redirect('gym_trainer:assign_schedule')
    else:
        form = RoutineForm(instance=routine)
    return render(request, 'edit_routine.html', {'form': form, 'routine': routine})

# Vista per eliminar l'assignació duna rutina a l'horari
@login_required
@trainer_required
def delete_schedule(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        time = request.POST.get('time')

        Schedule.objects.filter(day=day, time=time).delete()

        messages.success(request, 'La rutina ha sido eliminada del horario.')
    return redirect('gym_trainer:assign_schedule')


# Vista per eliminar una rutina 
@login_required
@trainer_required
def delete_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)
    if request.method == 'POST':
        routine.delete()
        messages.success(request, 'Rutina eliminada con éxito.')
        return redirect('gym_trainer:assign_schedule')
    return redirect('home')