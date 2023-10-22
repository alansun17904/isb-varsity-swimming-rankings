# ISB Varsity Swim Team Ranking Program 
Herein lies the source code for the [ISB Varsity Swimming](https://isbswim.herokuapp.com/)
ranking website. This site implements the ranking algorithm described by Alan Sun and
Emory Sun, which can be found [here](https://github.com/alansun17904/isb-varsity-swimming-rankings/blob/main/static/ranker/an-algorithm-for-varsity-swim-team-selection.pdf).
## Installation
1. Clone the repository `git clone https://github.com/alansun17904/isb-varsity-swimming-rankings.git`
2. Install the dependencies; here, we note that Python 3.7.0 is being used. `pip install requirements.txt`
3. Start the server by running `python manage.py runserver` in the top-level directory.

## Prerequisites
We note that the notation of events is incredibly important, as knowledge of this 
notation is assumed throughout the interface of the website. Each event is 
assigned a unique code that is consistent throughout the input/output of the
program. It is crucial that the user is conscious of correspondance between
the value of these codes and its events. A table of this is shown below:

| Event | Code |
|:-----:|:----:|
|50m Freestyle|FR50m|
|100m Freestyle|FR100m|
|200m Freestyle|FR200m|
|400m Freestyle|FR400m|
|50m Fly|FLY50m|
|100m Fly|FLY100m|
|50m Backstroke|BA50m|
|100m Backstroke|BA100m|
|50m Breaststroke|BR50m|
|100m Breaststroke|BR100m|
|100m IM| IM100m|
|200m IM| IM200m|

Please note that the casing of the codes is also significant.

## Contributing
To start, please see the issues page for any outstanding features/problems with the website.
Those interested in contributing can learn about the structure of the project and its implementation
quickly through the [design specifications](https://github.com/alansun17904/isb-varsity-swimming-rankings/blob/main/DESIGN.md)
and the [implementation specifications]().

## Usage
Usage comes in three stages: data entry, hyperparameter determination, and ranking.
Here we describe each of these stages in full. 

We note that since the website is to only be accessed by swimmers of the International
School of Beijing and its coaches, coaches (superusers) must pre-make accounts for incoming 
swimmers. This can be done by accessing the [staff page](https://isbswim.herokuapp.com/admin/).

Once accounts for each swimmer is made, they can log in and start data entry.

### Data Entry
Each swimmer is responsible for entering their own times. The validitiy of these times are then 
checked by coaches/captains/staff managing the website. 

Times must be entered in the long-format and the adherence to this format will be checked. 
We note that if the time is less than a minute, it can be represented in short form:
- `ss.mm`
such that the first two digits represent the time in seconds, and the second two
digits represent milisecond time.

On the other hand, if the time is longer than a minute, it must be represented in 
long form:
- `mm:ss.ii`
such that the first two digits represent the time in minutes; the second two
represents the time in seconds, and the last two digits represents the time in miliseconds.

Once swimmers enter their times, these entries will be pending approval. If these entries are
approved, they will be actively used in the ranking. 

### Hyperparameter Determination
Hyperparameters are crucial to the functionality of the program. They determine how many 
events each swimmer will be judged on, the weighting function being used, and whether
attendance will be factored into the ranking. 

Currently, only three hyperparamters are supported:
- `h-index`: the number of events each swimming will be judged on. This number ranges
from 1 to 12. The higher this number is the more versatile each swimmer must be.
- `attendance-bonus`: whether or not swimmers will be given a bonus if they
attend all practices.
- `weighting-function`: the weighting function that is used to determine the score. 
The possible values for this parameter are detailed in the white paper.
- `event-bonus`: the bonuses assigned to each rank in each event. *This field must be
entered in JSON format on the admin page*.

An example of these fields is shown below:
```
h-index 10
attendance-bonus true 0.02
weighting-function uniform 1
event-bonus {
    "FR50m": [0.1, 0.08, 0.06, 0.04],
    "FR100m": [0.1, 0.08, 0.06, 0.04],
    ...
}
```

the first line corresponds to the `h-index` and the number that follows it is the
number of events each swimmer will be judged by. The second line corresponds to the
`attendance-bonus` hyperparameter, if the word that comes after this is `true` then
attendence will be considered. Otherwise, the user can simply input `false` after this
hyperparameter and continue. However, if `true` is given the user must also provide the
bonus value attached to perfect attendance. The last line corresponds to the weighting
function. The default weighting function is a quadratic weighting function. Possible 
functions include:
- `uniform`
- `linear`
- `polynomial`
- `sigmoidal`
- `exponential`
More about this is presented in the white paper itself.

### Ranking
Here, ranking is handled by the website itself. Thus, the user needs only to make sure that 
each user has entered the correct times and that the hyperparameters being used are desirable. 
