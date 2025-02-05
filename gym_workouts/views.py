from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from gym_trainer.models import Schedule, Routine
from .forms import SubscriptionForm, EnrollForm
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import Subscription
from datetime import timedelta

# Mostrem les rutines a les que l'usuari podría inscriure-se'n
@login_required
def workouts(request):
    routines = Routine.objects.all()
    hours = ['16', '17', '18', '19', '20', '21']
    schedule_data = {}

    # Data d'avui
    today = timezone.now().date()
    
    # Obtenim el dia de la setmana (0 = Dilluns, ..., 6 = Diumenge)
    current_weekday = today.weekday()

    # Definim els noms dels dies
    days_of_week = ['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres']

    week_dates = []
    for i, day_name in enumerate(days_of_week):
        if i < 2:  # Dilluns i Dimarts han de ser de la setmana següent
            next_week_day = today + timedelta(days=(7 - current_weekday + i))
            week_dates.append(next_week_day.strftime("%d/%m"))
        else:  # Dimecres, Dijous i Divendres són de la setmana actual
            this_week_day = today - timedelta(days=current_weekday - i)
            week_dates.append(this_week_day.strftime("%d/%m"))

    # Combinem els dies de la setmana amb els dies numèrics
    days_with_dates = list(zip(days_of_week, week_dates))

    # Agafem les rutines programades
    for day, date in days_with_dates:
        for hour in hours:
            schedule_entry = Schedule.objects.filter(day=day, time=f"{hour}:00").first()
            if schedule_entry:
                schedule_data[f"{day}_{hour}"] = {
                    'schedule': schedule_entry,
                    'is_enrolled': request.user in schedule_entry.enrollments.all()
                }
            else:
                schedule_data[f"{day}_{hour}"] = None  

    return render(request, 'workouts.html', {
        'routines': routines,
        'days_with_dates': days_with_dates, 
        'hours': hours,
        'schedule_data': schedule_data,
        'user': request.user,
        'today': today.strftime("%d/%m"),  
    })



# Vista per seleccionar la subscripcio
@login_required
def select_subscription(request):
    subscriptions = Subscription.objects.all() 
    form = SubscriptionForm() 

    # Obtenim la subscripció actual si es que hi ha
    current_subscription = getattr(request.user, 'subscription', None) 

    # Guardem l'estat de la subscripció
    if current_subscription is not None:
        subscription_status = current_subscription.get_name_display()  
    else:
        subscription_status = "Cap"  

    # Utilitzem el formulari SuscriptionForm per canviar la subscripció
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)  
        if form.is_valid():
            selected_subscription = form.cleaned_data['subscription']
            request.user.subscription = selected_subscription
            request.user.save()
            messages.success(request, f"Subscripció '{selected_subscription.get_name_display()}' assignada correctament!")
            return redirect('gym_workouts:home') 
        else:
            print(form.errors) 
            
    return render(request, 'select_subscription.html', {
        'form': form,
        'subscriptions': subscriptions,
        'subscription_status': subscription_status,  
    })


@login_required
def enroll_user(request):
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            schedule_id = form.cleaned_data['id']
            schedule = get_object_or_404(Schedule, id=schedule_id)

            # Verifiquem que l'usuari tingui subscripció
            if not request.user.subscription:
                messages.warning(request, "Has de tenir una subscripció per inscriure't a rutines.")
                return redirect('gym_workouts:workouts')

            # Obtenim el màxim de rutines segons la subscripció de l'usuari
            max_routines = request.user.subscription.max_routines if request.user.subscription else 0

            # Si la subscripció és il·limitada
            if request.user.subscription and request.user.subscription.name == 'unlimited':
                max_routines = float('inf')  # Il·limitat

            # Comprovem que l'usuari es pot inscriure
            if schedule.count_enrolled() < 10 and request.user.enrolled_schedules.count() < max_routines:
                schedule.enrollments.add(request.user)
                messages.success(request, "T'has inscrit a la rutina correctament!")
            else:
                messages.warning(request, 'Ja no et pots inscriure!.')
        else:
            print(form.errors)  
            messages.warning(request, 'Hi ha hagut un error inesperat.')

    return redirect('gym_workouts:workouts')


    
# Vista per sortir d'una rutina
def leave_routine(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)
        
        if request.user in schedule.enrollments.all():
            schedule.enrollments.remove(request.user) 
            messages.success(request, "Has sortit de la rutina amb éxit.")
        else:
            messages.warning(request, "No estàs inscrit a aquesta rutina.")

    return redirect('gym_workouts:workouts')