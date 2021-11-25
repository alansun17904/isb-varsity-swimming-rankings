from ranker.models import User, Entry


event_codes = ['FLY50m', 'FR50m', 'BA50m', 'BR50m', 'FLY100m', 'FR100m',
        'BA100m', 'BR100m', 'FR200m', 'FR400m', 'IM100m', 'IM200m']

def calculate_entry_ranks():
    # calculate ranks for each event
    # thus, we need to filter by event codes first
    for event in event_codes:
        event_entries = Entry.objects.filter(event=event)
        sorted(event_entries, key=convert_lts)
        print(event_entries)
        for rank, entry in enumerate(event_entries):
            entry.rank = rank + 1
            entry.save()

def convert_lts(entry):
    # time is only seconds, thus we simply convert to float.
    print(entry.swimmer.username, entry.event, entry.time)
    if ':' not in entry.time:
        print(float(entry.time))
        return float(entry.time)
    # there exists minutes in the given string representation of time
    else:
        s = entry.time.split(':')
        print(int(s[0]) * 60 + float(s[1]))
        return int(s[0]) * 60 + float(s[1])
