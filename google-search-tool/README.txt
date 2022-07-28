SET UP PYTHON:
1) https://www.python.org/downloads/ or use the windows app store.
2) install the modules listed in requirements.txt

HOW TO USE:
1) Open .env using notepad.
2) Make the necessary edits to .env. Please keep everything in lowercase and in the formats provided. Save .env
3) Ensure that ".env", "author_script.py", "html_extractor.py", "RUN_ME.py" and "website_data.csv" are all in the same folder.
4) Double click on RUN_ME.py. The script should execute and output a .csv file with a name of your choosing.
5) You can then upload the .csv to google sheets where it should work automatically.
6) When you are ready to generate emails, save the google sheet as .csv, rename it to input, and save it in the same folder as the email-maker.py. Run email-maker.py to generate potential 
email combinations.


A lot of the time, the script will try to pull the page html for author without knowing exactly how the webpage stores the author data. This results in a lot of errors or blank entries.
You can input websites and the appropriate data into the website_data.csv file to ensure the author is accurately pulled from that website every time.
To do this, go to an article and view the source code. Search for the author's surname, and locate a section where there is unique html before the name (i.e., it doesn't appear anywhere else
in the source code. Copy and paste the html before and immediately after the authors name, as well as any non-space separators, into the .csv.
E.g., for :[{"@type":"Person","name":"Phillip-Inman",
unique html before author 	= "Person","name":"
html after author 		= "
html separator			= -


	main website address,	unique html before author,	html after author,	email format/email domain,	html character as separator between first and last name, 	location
