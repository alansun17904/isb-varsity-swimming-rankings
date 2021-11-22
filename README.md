# ISB Varsity Swim Team Ranking Program 
Herein contains the program for the ISB (International School of Beijing) varsity
swim team selection algorithm. This program compiles the data collated in the
excel sheets in the repository, calculates each person's ranking based on the 
selection criteria, and then outputs this in pretty form in a specified file. 

For more information about the algorithm itself, please see the white paper that
is attached in the repository.

## Prerequisites
We note that the notation of events is incredibly important. Each event is 
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

## Installation

## Usage
Usage comes in three stages: data entry, hyperparameter determination, and ranking.
Here we describe each of these stages in full. 

### Data Entry
The data for the ranking progarm is stored in two main Excel sheets: `rankings-to-date.xlsx`
and `attendance.xlsx`. The former contains the times of each person for each event, and
the latter contains attendance inforamtion for bonus points determination. 

We proceed by discussing the former first. The `rankings-to-date.xlsx` Excel sheet is 
divided into 6 columns: `Ranking`, `Time`, `Name`, `Event`, `Sex`, `Meet`. 

The first field is an automatically calculated field that updates based on the time field. 
Here, the user **does not** need to modify anything, as the formula for determining this
rank stays constant. 

The second field represents the time that the given swimmer has swam
for this particular event. We note that if the time is less than a minute, it can be
represented in short form:
- `ss.mm`
such that the first two digits represent the time in seconds, and the second two
digits represent milisecond time. 
On the other hand, if the time is longer than a minute, it must be represented in 
long form:
- `mm:ss.ii`
such that the first two digits represent the time in minutes; the second two
represents the time in seconds, and the last two digits represents the time in miliseconds.

The third field is the name of the swimmer. The name and its format must be consistent
for the swimmer throughout the sheet.

The fourth field `Event` represents the event code in which the swimmer has achieved 
this time. Please see the table in the previous subsection for a reference on the 
relationship between the event names and the codes.

The fifth field represents the `sex` of the swimmer. Since boys are girls are ranked
separately, this is necessary, and must be entered for every row. Note that this field
must be encoded in all caps: either `MALE` or `FEMALE` is accepted.

The sixth field is option and represents the meet where this swimmer has achieved this time.

We note that each row in the Excel sheet represents the swimmer's fastest time in each event.
Thus, if a swimmer achieves a faster time than is previously recorded in the Excel sheet, the
corresponding row needs to be updated *rather than adding a new row*.

We also note that any change in the structure of the sheet, for example, changing the name
of the columns may result in undefined behavior from the ranker.

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

The values for these hyperparameters must be entered on separate lines in the 
`hyperparameters.settings` file. Each line will begin with the name of the hyperparameter
and its corresponding value. An example of this is given below:
```
h-index 10
attendance-bonus true 0.02
weighting-function uniform 1
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
The user can run the application through the folloing steps:
0. Downloading this entire folder. 
1. Open the Terminal application (assuming Mac)
2. Type in the command `cd` in Terminal, then drag the icon of the downloaded
folder and drop the icon into the Terminal window. 
3. Press <Enter>
4. Type in the command `./rank.sh` then press <Enter>
5. The program will then start and prompt the user.

