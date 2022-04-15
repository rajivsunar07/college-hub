from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Planner
from .forms import PlannerForm
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from group.models import Group
# Create your views here.

@login_required
def plan(request):
    ''' To view the plans of the user '''
    plans = Planner.objects.filter(user=request.user)
    dates = Planner.objects.values_list('date', flat=True).filter(user=request.user)
    date_list = []
    for date in dates:
        if date not in date_list:
            date_list.append(date)
    form = PlannerForm()
    context = {
        'plans': plans,
        'dates': date_list,
        'time': timezone.now(),
        'form': form,
        'title': 'Plans',
        'groups': Group.objects.filter(user=request.user)
    }
    return render(request, 'planner/plan.html', context)

@login_required
@require_POST 
def plan_create(request):
    ''' To create a plan '''
    form = PlannerForm(request.POST)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('plan')
    
@login_required
def plan_update(request, id):
    ''' To update a plan '''
    plan = Planner.objects.get(id=id)
    if request.user == plan.user:
        form = PlannerForm(instance=plan)
        if request.method == "POST":
            form = PlannerForm(request.POST, instance=plan)
            if form.is_valid():
                form.save()
                return redirect('plan')
        context = {
            'form': form,
            'title': 'Update Plan',
            'time': timezone.now(),
            'groups': Group.objects.filter(user=request.user),
            'id': id
        }
        return render(request, 'planner/plan_update.html', context)
    return redirect('plan')

@login_required
def plan_delete(request, id):
    ''' To delete a plan '''
    plan = Planner.objects.get(id=id)
    if plan.user == request.user:
        plan.delete()

        return redirect('plan')
    return redirect('plan')

@login_required
def plan_complete(request, id):
    ''' To change the completed status of a plan to True '''
    plan = Planner.objects.get(id=id)
    if plan.user == request.user:
        plan.completed = True
        plan.save()

        return redirect('plan')
    return redirect('plan')
    
@login_required
def delete_completed(request):
    ''' To delete all the completed plans of a user '''
    plans = Planner.objects.filter(user=request.user)
    for plan in plans:
        if plan.completed == True:
            plan.delete()
    
    return redirect('plan')

@login_required
def delete_old(request):
    ''' To delete all the plans of a user that are before current day's date '''
    plans = Planner.objects.filter(user=request.user)
    date = timezone.now()
    for plan in plans:
        if plan.date < date.date():
            plan.delete()
    
    return redirect('plan')