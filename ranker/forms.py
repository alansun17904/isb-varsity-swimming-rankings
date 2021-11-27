import re
from django import forms
from ranker.models import Entry, Hyperparameters, Profile

events = (('FR50m','FR50m'), ('FR100m','FR100m'), ('FR200m','FR200m'), ('FR400m','FR400m'),
        ('BR50m','BR50m'), ('BR100m','BR100m'), ('BA50m','BA50m'), ('BA100m','BA100m'),
        ('FLY50m','FLY50m'), ('FLY100m','FLY100m'), ('IM100m','IM100m'), ('IM200m','IM200m'))

weightfuncs = (('linear', 'linear'), ('polynomial', 'polynomial'), ('uniform', 'uniform'),
                ('exponential', 'exponential'), ('sigmoidal', 'sigmoidal'),
                ('none', 'none'))

class HyperparameterForm(forms.ModelForm):
    weight_type = forms.ChoiceField(choices=weightfuncs, widget=forms.Select)


    class Meta:
        model = Hyperparameters
        fields = '__all__'

class EntryForm(forms.ModelForm):
    event = forms.ChoiceField(choices=events, widget=forms.Select)
    time = forms.CharField(max_length=8)

    def clean(self):
        super().clean()
        time = self.cleaned_data['time']
        if not re.match("^\d{2}\.\d{2}$", time) and not re.match("^\d{1,2}:\d{2}.\d{2}", time):
            raise forms.ValidationError("The time entered is not in the correct \
                format. Please conform to either xx:xx.xx or xx.xx")
        self.cleaned_data['time'] = EntryForm.convert_lts(self.cleaned_data['time'])

    @staticmethod
    def convert_lts(time):
        # time is only seconds, thus we simply convert to float.
        if ':' not in time:
            print(float(time))
            return float(time)
        # there exists minutes in the given string representation of time
        else:
            s = time.split(':')
            return int(s[0]) * 60 + float(s[1])

    class Meta:
        model = Entry
        exclude = ('swimmer', 'rank', 'approved')

class EntryFormAdmin(forms.ModelForm):
    event = forms.ChoiceField(choices=events, widget=forms.Select)
    time = forms.CharField(max_length=8)

    def clean(self):
        super().clean()
        self.cleaned_data['time'] = EntryForm.convert_lts(self.cleaned_data['time'])

    class Meta:
        model = Entry
        exclude = ('rank',)

class ProfileFormAdmin(forms.ModelForm):
    sex = forms.ChoiceField(choices=(('MALE', 'Boy'), ('FEMALE', 'Girl')),
            widget=forms.Select)
    class Meta:
        model = Profile
        fields = '__all__'

