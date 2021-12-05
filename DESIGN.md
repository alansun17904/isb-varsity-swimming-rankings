# Web Application for ISB Ranking Application
Here, we describe the design of the web application, the models/data structures,
as well as the general logic of the program. 

## Key Functionalities: Minimum Viable Product
- We need to keep the key data (rankings, times of our swimmers) hidden,
as if other teams had access to such aggregate data, they could use this
to strategize against us in future meets. 
- Coaches/Admins have the ability to update the central dataset:
the dataset that is used to rank all swimmers.
  - They must be provided a portal where they can access this dataset.
  - Coaches must also have access to a portal where they can change the
  hyperparameters of the ranking.
- Differentiation of user groups: swimmers and coaches
- Swimmers must be able to enter their own times to the database. However
before these times are used for ranking, their validity needs to be checked
by either coaches or captains.
- Ranking tab that shows separate tabs for boys and girls: needs to
calculate the score in sorted order, as well as the specific times 
used to achieve these scores.
- Keep track of attendance.


## Additional Features
- Registration of users with keycodes given out by coaches.
- What-if analysis for swimmers. Recalculate rankings for "if" a swimmer has 
swam a particular time. 
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
- User
  - ID
  - Name (first, last)
  - Username (simple concatenation of the first and last name)
- Profile
  - User (One-to-one field with user)
  - Sex (CharField)
  - Attendance (BooleanField): whether or not they have achieved the attendance bonus.
  - Is_coach (BooleanField)
- Entry
  - Rank (IntegerField)
  - Event (CharField): must be one of the event codes outlined in the `README.md`
  - Time (FloatField): the time is stored as seconds
  - Meet (CharField)
  - Approved (BooleanField): if this field is `False` it will not be used for ranking.
- Hyperparameters (This should be a Singelton)
  - h-index (IntegerField)
  - Attendance Bonus (BooleanField): whether or not attendance will be taken into account.
  - Attedance Weight (FloatField): the percentage discount that having perfect attendance will
  provide.
  - Weight Type (CharField): The weighting function.
  - Weight A (FloatField): Hyperparameter of the weighting function, please see the 
  white paper for more about this constant.
  - Bonus Matrix (JSONField)
- Practice 
  - Date (DateField)
  - Swimmers (Many-to-many with profile): keeps track of who was there for practice.


