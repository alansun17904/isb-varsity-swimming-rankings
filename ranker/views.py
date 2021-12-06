from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ranker.models import Entry, Hyperparameters, Profile, Practice
from django.contrib.auth.models import User
from ranker.interpolation import rank
from ranker.forms import EntryForm


class ProfileDetailView(DetailView, LoginRequiredMixin):
    context_object_name = 'profile'
    model = Profile
    template_name = 'ranker/profile.html'
    login_url = 'ranker/login'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['practices'] = Practice.objects.all().order_by('-date')
        context['entries'] = Entry.objects.all()
        return context


class EntryCreateView(CreateView, LoginRequiredMixin):
    model = Entry
    form_class = EntryForm

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'ranker/entry_create.html',
            context={'form': self.form_class()}
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            event = form.cleaned_data.get('event')
            time = form.cleaned_data.get('time')
            meet = form.cleaned_data.get('meet')
            swimmer = request.user.profile
            entry = Entry(
                event=event,
                time=time,
                meet=meet,
                swimmer=swimmer
            )
            entry.save()
        return HttpResponseRedirect(
            reverse_lazy('ranker:profile', args=[request.user.profile.pk])
        )


class EntryUpdateView(UpdateView, LoginRequiredMixin):
    model = Entry
    template_name = 'ranker/entry_update.html'
    form_class = EntryForm

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=kwargs['pk'])
        if entry.swimmer.user != request.user:
            raise PermissionDenied('You do not have permission to edit this user\'s entry')
        else:
            entry.approved = False
            entry.save()
            return super(EntryUpdateView, self).post(request, *args, **kwargs)


class EntryDeleteView(DeleteView, LoginRequiredMixin):
    model = Entry
    template_name = 'ranker/entry_delete_confirm.html'

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=kwargs['pk'])
        if entry.swimmer.user != request.user:
            raise PermissionDenied('You do not have permission to delete this user\'s entry')
        else:
            entry.delete()
            return HttpResponseRedirect(reverse_lazy('ranker:profile', args=[request.user.profile.pk]))


#################################
####### Functional Views ########
#################################


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
    frank = rank('FEMALE')
    mrank = rank('MALE')
    # Convert usernames into user objects
    for row in frank:
        row[2] = User.objects.get(username=row[2])

    for row in mrank:
        row[2] = User.objects.get(username=row[2])

    return render(request, 'ranker/rankings.html',
                  {'MALE': mrank, 'FEMALE': frank})


@login_required
def event_ranks(request, sex, event):
    entries = Entry.objects.filter(swimmer__sex=sex,
                                   event=event, approved=True).order_by('rank')
    context = {'entries': entries}
    return render(request, 'ranker/event_ranks.html', context)
