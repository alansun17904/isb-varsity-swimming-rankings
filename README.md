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

## Usage

