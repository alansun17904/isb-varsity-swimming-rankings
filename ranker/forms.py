from django import forms
from ranker.models import Entry

class EntryForm(forms.ModelForm):
    event = forms.ChoiceField(choices=(
        ('FR50m','FR50m'), ('FR100m','FR100m'), ('FR200m','FR200m'), ('FR400m','FR400m'),
        ('BR50m','BR50m'), ('BR100m','BR100m'), ('BA50m','BA50m'), ('BA100m','BA100m'),
        ('FLY50m','FLY50m'), ('FLY100m','FLY100m'), ('IM100m','IM100m'), ('IM200m','IM200m'),
    ), widget=forms.Select)
    time = forms.CharField(max_length=8)
    def clean(self):
        super().clean()
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

