# Online CatalogApp

This application is project number 3 (of 5) of Udacity's Full Stack Developer 
Nanodegree program. It builds upon the two previous courses: Full Stack 
Foundations & Authentication/Authorization. The application makes use of
starter code provided by Udacity.

The purpose of this excersice is to develop a RESTful web application using 
the Python framework Flask along with implementing third-party OAuth 
authentication. As a result, students will learn when to properly use the 
various HTTP methods available to a developer and how these methods relate to 
CRUD (create, read, update and delete) operations. The application should 
provide a list of items within a variety of categories as well as provide a 
user registration and authentication system. Registered users should have the
ability to create categories and items for those categories. As well as 
provide means for updating and deleting those categories and items. 
Modification and deletion of categories and items is restricted in the 
following manner:

1. Only registered users may modify categories or items
2. A user may only modify or delete categories or items which she has created.

Additionally, the application must meet the following minimum requirements:

Criteria 	  					|				Description
--------------------------------|----------------------------------------------------------------------------------------------------
API Endpoints 					| Application implements JSON endpoints with all required content.
CRUD: Read 	  					| Application reads category and item information from a database.
CRUD: Create  					| Application includes a form allowing users to add new items and correctly processes submitted forms.
CRUD: Update  					| Application includes a function to edit/update a current record in the database table and correctly
								| proceses submitted forms.
CRUD: Delete  					| Application includes a function to delete a current record.
Authentication & Authorization  | Application implements a third-party authentication and authorization service; and create, delete and
								| update operations do consider authorization status prior to execution. Make sure there is a ‘Login’
								| and ‘Logout’ button/link in the project. The aesthetics of this button/link is open for you to design.
Code Quality  					| Code is ready for personal review and neatly formatted.
Comments 	  					| Comments are present and effectively explain longer code procedures.
Documentation 					| A README file (this document you are reading) is included detailing all steps required to successfully
								| run the application.

## Requirements

The following are required to run the application:

1. Download and install Git (Download here - http://git-scm.com/downloads/)
2. Download and install Vagrant (Download here - https://www.vagrantup.com/)
3. Download and install Virtual Box (Download here - https://www.virtualbox.org/)
4. Download and install Python 2.7.6 (Download here - https://www.python.org/downloads/)
	||-- Flask (0.10.1) - Install from command line by entering command 
							'<pip install Flask>'
5. Your favorite web browser.

## Installation

Once you have downloaded and installed the components above, installation of this application is
a snap. Just follow the steps below:

### Setup Environment

##### 1. Open terminal
	* Windows: Open Git Bash, which installed at the time you installed Git. This will open a Unix-style terminal.
	* Other systems: Use any terminal program of your choosing.
##### 2. Change from your root directory to the directory of your choice
	* Example: cd Desktop/ (this will make your desktop the current directory.)
##### 3. Clone Repository
At the terminal prompt, run the following command:
	'<git clone https://github.com/NeoCodesOracle/CatalogApp.git>'
This will copy the folder containing all application files to your desktop (or whatever you working directory is)
##### 4. Change Directory
After cloning directory, you will need to navigate to it by entering the following command at the prompt:
	'<cd catalogapp>'
You are now in the catalogapp directory.

### Run Application
You are now ready to launch application. Type the following commands at the prompt as they appear below:

##### 1. python catalog_database.py
This command will set up the database for the application to store the categories and items that will be
created during runtime.
##### 2. python populate_database.py (OPTIONAL)
This command will populate your database with dummy categories and items for you to interact with. It is suggested
that you run this command in order to ensure testing deletion and modification of other user's data.
##### 3. python catalogApp.py
This command will launch the server, which will serve our application on port 5000
##### 4. View Application in Browser
Open your favorite web browser and type the following in the address bar: 
http://localhost:5000/
You should see the application along with dummy data (if installed).


## Usage

## Screenshots
![App Splash](.\static\images\Screenshots\Frontpage.png)
![App Login](.\static\images\Screenshots\login.png)
![App Categories](.\static\images\Screenshots\cats.png)

## File Contents


Functions	| Descriptions
------------|-------------


##Credits

Created by NeoCodesOracle
Makes use of Ian Lunn's Hover CSS effects
Contains code provided by Udacity
Built Using bootstrap

## License

Licensed under MIT License (MIT)

Copyright (c) 2015 NeoCodesOracle

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without 
limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORIMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.