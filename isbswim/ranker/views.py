from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ranker.models import Entry, Hyperparameters
from django.contrib.auth.models import User
from ranker.interpolation import calculate_entry_ranks, rank

# Create your views here.
def index(request):
    return render(request, 'ranker/index.html')

def about(request):
    hyp = Hyperparameters.objects.all()[0]
    return render(request, 'ranker/about.html',
            {'hyperparameters': hyp})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'ranker/login.html',
                        {'message': 'User has been deactivated by staff.'})
        else:
            return render(request, 'ranker/login.html',
                {'message': 'Invalid email or password. Please try again.'})
    return render(request, 'ranker/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def rankings(request):
    ## We recalculate the ranks everytime that it is requested.
    entries = Entry.objects.all()
    calculate_entry_ranks()
    frank = rank('FEMALE')
    mrank = rank('MALE')
    return render(request, 'ranker/rankings.html',
            {'MALE': mrank, 'FEMALE': frank})

