from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ranker.models import Entry, Hyperparameters, Profile
from django.contrib.auth.models import User
from ranker.interpolation import rank
from ranker.forms import EntryForm

# Create your views here.
def index(request):
    form = EntryForm()
    profile = None

    if request.user.is_authenticated:
        profile = Profile.objects.all().get(user=request.user)
        if profile.is_coach:
            profile = None
    context = {'entries': Entry.objects.all(),
            'profile': profile,
            'updateForm': form}
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = Entry(event=form.cleaned_data['event'],
                    time=form.cleaned_data['time'],
                    meet=form.cleaned_data['meet'],
                    swimmer=profile)
            entry.save()
            return HttpResponseRedirect(reverse('index'))
        return HttpResponse("The data submitted was invalid. Please check your \
                formatting and try again (especially for the time field)")
    return render(request, 'ranker/index.html', context)

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
    frank = rank('FEMALE')
    mrank = rank('MALE')
    return render(request, 'ranker/rankings.html',
            {'MALE': mrank, 'FEMALE': frank})

@login_required
def event_ranks(request, sex, event):
    entries = Entry.objects.filter(swimmer__sex=sex,
            event=event).order_by('rank')
    context = {'entries': entries}
    return render(request, 'ranker/event_ranks.html', context)
