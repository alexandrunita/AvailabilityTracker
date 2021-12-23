# AvailabilityTracker
## Video Demo : [Availability Tracker Demo](https://youtu.be/ibdxmHY2Z0Y)
## Description
- **Availability** Tracker WebApp offers a team visibility on the availability of their colleagues and allows for distribution of tasks according to employee availability.
- Source code available on Github : [Availability Tracker](https://github.com/alexandrunita/AvailabilityTracker)
### Project Components
- Static Files
 - style.css : CSS file with custom overrides to bootstrap built-in functionality
- Templates Files
  - apology.html : error page
  - availability.html : main index page, provides overview for the entire team availability
  - bookOOF.html : allows booking new vacations while providing a preview of upcoming vacations. Switches to a confirmation view after successfully booking is done.
  - layout.html : basic layout file that is extended by all other templates
  - login.html : login page
  - register.html : registration page
  - removeOOF.html : allows cancelling upcoming vacations and truncating ongoing vacations.
- venv Files
  - special folder created by applying steps from : [Using Python environments in VSCode](https://code.visualstudio.com/docs/python/environments)
  - this contains all dependencies needed to run the WebApp
  - contains activation/deactivation scripts to enter/step out of virtual environment
  - ensures we can just download the project on a new windows machine and run directly without having to install all dependencies
- app.py
  - main file for WebApp
  - contains all routes for WebApp and main logic
  - calls helper functions in helper files to accomplish side tasks
- database.py
  - contains helper functions meant to interact with the availability.db SQLite3 database
- helper.py
  - contains a couple Flask app support functions
  - also contains helper function to generate symbols that are printed to the availability table on the index page
- LICENSE
  - standard MIT opensource license for the project