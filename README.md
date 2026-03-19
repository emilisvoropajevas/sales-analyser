#DB
Databse structure in sqlite using SQL Model, data imported in as csv and parsed before being written

#Stage 1
First API Endpoint : User uploads file
This works when the user does the following:

2 api calls:
-Upload File (Clean and parse)
-Save File

User Clicks button -> New -> Drags and drops or selects file (file limit = 1) -> sent to api backend, parsed and cleaned, sent back to user to see .head()
-> User sees -> names the file, clicks save and it's sent to the backend to save in local database. Save confirmed -> User clicks open -> New page 

when new page loads api call to load report id{} etc and data ia automatically sent to front end for plots to instantly enter, javascript object on front end that is edited with the user inputs to render plots

Next API Endpoint
Name the report and save it to the database 
    -include database crud tests and crud endpoint