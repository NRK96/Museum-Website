/************************************************************************/

 $#$#$#$#Don't forget to delete these$#$#$#$#$#
SuperUser: Woogity
Password: shoreshack

Docent: John_Doe
Password: Never4get

Manager: BigWig
Password: DaBigBoss


/************************************************************************/

This product is a reservation management system meant for the purpose of 
schedualing, logging, managing, viewing statistical reports, generating
confirmation letters and emails, and providing general information about
the Museum of South Texas History. This README is to provide information
about the layout and general use of the site. 

- Produced by Team Woogity!!

/************************************************************************/

File Structure :

teamWoogity - external project folder, holds all of the project folders
	|
	- scheduling: - scheduling app
		|-_pycache_ - python cache storage
		|- migrations  - stores migration history for database (tables, and model info)
		|- static 	- static file storage for templates (images etc.)
		|- templates 
			|
			|- admin - modified admin templates for customization
			|- directlinks - templates for nav bar links
			|- scheduling - templates regarding request model, (creating saving and deletion templates)
		| - tests - unit testing suite files
	|- MOSTScheduling - internal project folder, holds manage.py, settings.py, and base url config
		| -_pycache_ - python cache storage
		|- tests - holds functional test suites

/************************************************************************/

Site structure

'most.org/home'
	Displays a brief description of the MOST museum

'most.org/scheduling'
	Page for requesting a reservation, displays a list of currently requested times

'most.org/contact'
	Displays a list of contact information for the museum

'most.org/admin'
	Area where reservations and made and managed, customer profiles are listed and created 


/************************************************************************/

Site uses: The site is intended as a web application used for scheduling tours, tracking information about
tours over time, tracking customer information, and reviewing an employees assigned tour work.

In order to access the scheduling section of the site, an employee must be assigned a login and password
by the superuser. Once setup, the employee will be able to login through the front of the site and access
the scheduling portion of the page.

SCHEDULING RUNDOWN:
Inside the scheduling section is 3 tabs, Statistics, Reservations, and Customer Profiles.
- The statistics tab is used to generate statistical reports based on the tours that the
museum has hosted over a given period of time
- The reservations tab displays all currently requested times by possible customers as well as
a calendar view of all currently scheduled reservations. To create a new reservation, an employee
must click on the 'Create Reservation' button on the bottom of the page.
- The customer profile tab displays a list of all currently tracked customers. In order to create a
reservation for a customer, a customer profile must exist to link it to. To create a new profile, an
employee must click the 'Create New Profile' button at the bottom of the page.

/************************************************************************/

Testing Suite 

 run python3 manage.py test in console 
 runs through all of unit tests and functional tests in scheduling and MOSTScheduling.

Email Account:
    Username: MuseumOfSouthTexas@gmail.com
    Password: Woogity1

