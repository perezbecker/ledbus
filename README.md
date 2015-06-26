# ledbus

crondisplay - Displays bus and bart data onto two 16x32 led matrices. Set to run every two minutes in cron. The script checks if the program is already running, in which case it does nothing, otherwise it will display the bustimes and bartimes files on the displays.

crongetbus - Gets bus data. Set to run every two minutes in cron. The script checks if the program is already running, in which case it does nothing, otherwise it will run the nextbus-led.py program. 

nextbus-led.py - Continuosly gets bus data. If it cannot update data for a minute it closes (and waits to be restarted by cron via crongetbus).

nextbart-led.py - Run on cron every 30s. It gets bart data, updates barttimes file and exits. (does not run continuosly).