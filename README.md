# SI206_FinalProject
The Ticket Sellers

Final_Project.py runs the spotify program and stores data into database
Main_Project.py runs the ticketmaster program, based on input from spotify database, and stores data into ticketmaster database

model.py is a revised file that should replace an existing model.py file in your ticketpy folder
  the old model.py that came with the library was buggy

coordinates.py determines your coordinates from ip address
  IMPORTANT 
  1. You must pip install selenium
  2. You must download chromedriver from this link https://sites.google.com/a/chromium.org/chromedriver/downloads according to your chrome version
  3. You must download the chromedriver folder into the same folder as this python file, extract the contents of folder, and move chromedriver.exe into the same folder as this python file

calculations.py calculates the nearest concert from ticketmaster database based on user location
visuals.py makes visualzations based on data from the spotify and ticktmaster database

RUNTHIS.py executes all of the programs above
