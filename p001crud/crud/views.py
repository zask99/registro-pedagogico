from django.shortcuts import render,redirect,get_object_or_404
from .models import task
from .forms import TaskForm

def task_list_and_create(request):
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_list')
    else:
        form=TaskForm()
    form = TaskForm()
    #tasks=task.objects.all()
    completed_tasks= task.objects.filter(is_completed=True)
    incomplete_tasks= task.objects.filter(is_completed=False)
    
    return render(request, 'task_list.html',{
        'form':form,
        'completed_tasks':completed_tasks, 
        'incomplete_tasks':incomplete_tasks
    })
    
def update_task(request, task_id):
    if request.method == 'POST':
        tasks = task.objects.get(id=task_id)
        tasks.is_completed = not tasks.is_completed  # CORREGIDO AQUÍ
        tasks.save()
        return redirect('crud:crud_list')
    
from django.shortcuts import render, get_object_or_404, redirect
from .models import task
from .forms import TaskForm

def edit_task(request, task_id):
    tasks = get_object_or_404(task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=tasks)  # <- CORREGIDO
        if form.is_valid():
            form.save()
            return redirect('crud:crud_list')
    else:
        form = TaskForm(instance=tasks)  # <- MÁS LIMPIO
    
    return render(request, 'edit_task.html', {'form': form})

def delete_task(request,task_id):
    if request.method=='POST':
        tasks = task.objects.get(id=task_id)
        tasks.delete()
        return redirect ('crud:crud_list')
