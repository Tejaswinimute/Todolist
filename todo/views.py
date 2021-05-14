from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForms
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

def singupuser(request):
    if request.method == 'GET':
        return render(request,'singupuser.html',{'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'singupuser.html',{'form': UserCreationForm(), 'error': 'That Username has already been taken. Please choose a new username.'})
        else:
            return render(request,'singupuser.html',{'form': UserCreationForm(),'error': 'Passwords Did Not Match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'loginuser.html',{'form':AuthenticationForm()})
    else:
        user= authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(),'error':'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodos(request):
    if request.method == 'GET':
        return render(request, 'createtodos.html', {'form':TodoForms()})
    else:
        try:
            form = TodoForms(request.POST)
            newtodo= form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodos.html', {'form': TodoForms(),'error':'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'currenttodos.html',{'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'completedtodos.html',{'todos':todos})

@login_required
def viewtodos(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET' :
        form=TodoForms(instance=todo)
        return render(request,'viewtodos.html',{'todos':todo,'form':form})
    else:
        try:
            form = TodoForms(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'viewtodos.html', {'todo': todo, 'form': form,'error': 'Bad Info.'})

@login_required
def completetodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST' :
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST' :
        todo.delete()
        return redirect('currenttodos')
