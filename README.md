# Conference Management System
A Python-based console application for managing conference attendees, speakers, rooms, and attendee network connections using both MySQL and Neo4j databases.

## Overview
This application allows users to:
- View speakers and sessions
- View attendees by company
- Add new attendees
- View connected attendees (MySQL + Neo4j integration)
- Add attendee-to-attendee connections (Neo4j graph)
- View rooms

The system uses:
- MySQL for structured attendee and conference data
- Neo4j for graph-based attendee connection data

## Technologies Used
- Python 3.12.12
- MySQL (via `pymysql`)
- Neo4j-community-edition (via `neo4j` Python driver)
- Standard libraries: `datetime`, `time`

## Installation
Install required Python packages:
`pip install -r requirements.txt`

## MySQL Connection Instructions
1. Start MySQL Server on the VM.
2. Open MySQL Workbench or the MySQL shell.
3. Log into MySQL using username 'root' and password 'root'.
4. Run the SQL schema in **appdbproj.sql** to create all required tables.

## Neo4j Connection Instructions
1. Open Command Prompt.
2. Change directory to the \bin\ folder of neo4j-community-edition.
3. Enter the command 'neo4j.bat console'.
4. Go to http://localhost.7474// on your browser (or whichever port number is output by the command prompt).
5. Click on the Databases icon on the top left and run the Neo4j Schema in **appdbprojNeo4j.txt** to create all required nodes and relationships.

## Running the Application
1. Ensure MySQL is running and the database/tables are created.
2. Ensure Neo4j Community Edition is running.
3. Start the Neo4j database that contains the Attendee nodes.
4. Run the application:
`python main.py`

## File Structure
/applieddbproject
main.py
innovation.doc
GitLink.txt
requirements.txt
appdbproj.sql
appdbprojNeo4j.txt
README.md

## GitHub Repository
The GitHub link is included in **GitLink.txt** in the project root.


