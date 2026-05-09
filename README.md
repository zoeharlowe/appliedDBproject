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
- Neo4j (via `neo4j` Python driver)
- Standard libraries: `datetime`, `time`

## MySQL Connection Instructions
1. Start MySQL Server on the VM.
2. Open MySQL Workbench or the MySQL shell.
3. Create the database:

CREATE DATABASE appdbproj;

4. Select the database:

USE appdbproj;

5. Run the SQL schema below to create all required tables.

### SQL Schema

CREATE TABLE company (
    companyID INT PRIMARY KEY,
    companyName VARCHAR(100)
);

CREATE TABLE room (
    roomID INT PRIMARY KEY,
    roomName VARCHAR(100),
    capacity INT
);

CREATE TABLE session (
    sessionID INT PRIMARY KEY,
    sessionTitle VARCHAR(200),
    speakerName VARCHAR(100),
    sessionDate DATE,
    roomID INT,
    FOREIGN KEY (roomID) REFERENCES room(roomID)
);

CREATE TABLE attendee (
    attendeeID INT PRIMARY KEY,
    attendeeName VARCHAR(100),
    attendeeDOB DATE,
    attendeeGender VARCHAR(10),
    attendeeCompanyID INT,
    FOREIGN KEY (attendeeCompanyID) REFERENCES company(companyID)
);

CREATE TABLE registration (
    attendeeID INT,
    sessionID INT,
    PRIMARY KEY (attendeeID, sessionID),
    FOREIGN KEY (attendeeID) REFERENCES attendee(attendeeID),
    FOREIGN KEY (sessionID) REFERENCES session(sessionID)
);

## Neo4j Connection Instructions
The application uses the official Neo4j Python driver.  

Connection string used:
neo4j://localhost:7687

Before running the application, create and start a Neo4j database with:
Username: neo4j  
Password: neo4jneo4j

No Cypher setup is required. The application automatically creates Attendee nodes and CONNECTED_TO relationships using MERGE.

## Installation
Install required Python packages:
`pip install -r requirements.txt`

## Running the Application
1. Ensure MySQL is running and the database/tables are created.
2. Ensure Neo4j Desktop or Neo4j Community Edition is running.
3. Start the Neo4j database that contains the `Attendee` nodes.
4. Run the application:
`python main.py`

## File Structure
/project-root
main.py
innovation.doc
GitLink.txt
requirements.txt

## GitHub Repository
The GitHub link is included in **GitLink.txt** in the project root.


