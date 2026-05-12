# Applied Databases Project
by Zoe McNamara Harlowe

### Welcome to my project submission for the Applied Databases module. This module is provided by ATU (Atlantic Technological University) as part of the HDip in Computing in Data Analytics.
In this project, I have created a conference management system in Python for managing conference attendees, speakers, rooms, and attendee network connections using both MySQL and Neo4j databases.

## Overview
This application allows users to:
- View speakers and sessions
- View attendees by company
- Add new attendees
- View connected attendees 
- Add attendee-to-attendee connections
- View rooms

The system uses:
- MySQL for structured attendee and conference data
- Neo4j for graph-based attendee connection data

## Prerequisites

- Python 3.12
- Required packages (listed in `requirements.txt`):  
  ```bash
  neo4j
  pymysql
  ```

## Libraries & Packages
- PyMySQL: https://pypi.org/project/PyMySQL/
- Neo4j Python Driver: https://neo4j.com/docs/api/python-driver/current/
- datetime: https://docs.python.org/3/library/datetime.html
- time: https://docs.python.org/3/library/time.html

## Setup
**Clone the repository onto your local/virtual machine:**
1. In Commander, clone the repo and change directory:
```bash 
git clone <https://github.com/zoeharlowe/applieddbproject>
cd <applieddbproject>
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Start MySQL Server by opening MySQL Workbench or the MySQL Command Line Client.
Log into MySQL using username 'root' and password 'root' (not to be used for production environments).
Run the SQL Schema in **appdbproj.sql** to create the database and tables.
4. Start Neo4j by changing directory to the \bin\ folder of neo4j-community-edition in Command Prompt.
Enter the command:
```bash
neo4j.bat console
```

5. Go to http://localhost.7474// on your browser (or whichever port number is output by the command prompt).
Click on the Databases icon on the top left and run the Neo4j Schema in **appdbprojNeo4j.txt** to create all required nodes and relationships.

6. Launch the program main.py locally or in VSCode:
```bash
python main.py
```

## File Structure
### **applieddbproject:**
- main.py
- innovation.doc
- GitLink.txt
- requirements.txt
- appdbproj.sql
- appdbprojNeo4j.txt
- README.md

## GitHub Repository
The GitHub link is included in **GitLink.txt** in the project root.

## Bibliography
- I used Microsoft Copilot to help me get this program working on a Virtual Machine. See conversation relating to PATH issues: https://copilot.microsoft.com/shares/hYZyhfH3RA9cTiNEuvnF7
- Tutorial on ANSI colours: https://codehs.com/tutorial/andy/ansi-colors
- DataCamp: Setting up Neo4j: https://www.datacamp.com/tutorial/neo4j-tutorial?utm_cid=23340058065&utm_aid=192632748929&utm_campaign=230119_1-ps-dscia~dsa-tofu~python_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=9040158-&utm_mtd=-c&utm_kw=&utm_source=google&utm_medium=paid_search&utm_content=ps-dscia~emea-en~dsa~tofu~tutorial~python&gad_source=1&gad_campaignid=23340058065&gbraid=0AAAAADQ9WsGzbvcZCQrP5xHzGuOX46QB1&gclid=CjwKCAjwn4vQBhBsEiwAq3hhNzj0veh6MhgzLtNpC238-GwyKa_Pe7c5_qCtzv_ApUDkZbr9hCoIsxoCCy0QAvD_BwE
- Lecture videos from the Applied Databases module (Lecturer: Gerard Harrison) to write the SQL and Neo4j commands in the code
- Copilot and DataCamp to insert a 'Loading...' animation while waiting for Neo4j requests: https://www.datacamp.com/tutorial/progress-bars-in-python

## Author
Zoe McNamara Harlowe
G00473469
HDip in Computing in Data Analytics
Atlantic Technological University (ATU)

