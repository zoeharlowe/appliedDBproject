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
Go to http://localhost.7474// on your browser (or whichever port number is output by the command prompt).
Click on the Databases icon on the top left and run the Neo4j Schema in **appdbprojNeo4j.txt** to create all required nodes and relationships.
5. Launch the program main.py locally or in VSCode:
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


