# Web Application for ISB Ranking Application
This is the design document for the ISB swim team ranking algorithm.

## Key Functionalities: MVP
- Need to key data hidden to the public, only current team members 
and coaches have the ability to access the site.
- Coaches/Admins have the ability to update the central dataset:
the dataset that is used to rank all swimmers.
  - They must be provided a portal where they can access this dataset.
  - Coaches must also have access to a portal where they can change the
  hyperparameters of the ranking.
- Differentiation of user groups: swimmers and coaches
- Ranking tab that shows separate tabs for boys and girls: needs to
calculate the score in sorted order, as well as the specific times 
used to achieve these scores.

## Additional Features
- What-if analysis for swimmers.
- PBlocks integration, optimization for post-selection/pre-championship
season.
- Data showing historical APAC data and trends.
- Goal settings / journaling.

## Pages
- Homepage
  - Login, choose swimmer or coach
- If swimmer direct them to the ranking page
  - Have a portal where they can see their own times, upcoming meets etc.
- If coach direct them to the hyperparameter/data page and also show
them the ranking page.

## Models
- User model
  - ID
  - Name (first, last)
  - Type
  - Points
  - Rank
  - Times (foreign key)

- Entries
  - Event
  - Time
  - Meet


