import os
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isbswim.settings')

import django
django.setup()

from django.contrib.auth.models import User
from ranker.models import Profile, Entry
import random

def convert_lts(time):
    # time is only seconds, thus we simply convert to float.
    if ':' not in time:
        print(float(time))
        return float(time)
    # there exists minutes in the given string representation of time
    else:
        s = time.split(':')
        return int(s[0]) * 60 + float(s[1])

### Get all names from the sample excel 
df = pd.read_excel('../rankings-to-date.xlsx')
names = df['Name'].unique()
users = {}

clean = lambda x: ''.join(x.lower().split(' '))

for name in names:
    try:
        username = clean(name)
        password = '1'
        u = User.objects.create(username=username, password=password)
        p = Profile.objects.create(user=u, sex=random.choice(['MALE', 'FEMALE']))
        p.save()
        u.save()
        users[clean(name)] = p
    except:
        continue

for entry in range(len(df)):
    try:
        u = users[clean(df.iloc[entry]['Name'])]
        event = df.iloc[entry]['Event']
        meet = df.iloc[entry]['Meet']
        time = convert_lts(str(df.iloc[entry]['Time']))
        e = Entry.objects.create(swimmer=u, event=event, time=time, meet=meet)
        e.save()
    except:
        continue


