import datetime
from neo4j import GraphDatabase
import pymysql

neo4j_driver = None

def connect_neo4j():
    uri = "bolt://localhost:7687"
    return GraphDatabase.driver(uri, auth=("neo4j", "neo4jneo4j"))


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='appdbproj',
    cursorclass=pymysql.cursors.DictCursor
)

# Display menu function
def display_menu():
    print("")
    print("Conference Management")
    print("-" * 23)
    print("\nMENU")
    print("=" * 4)
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendee")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit application")


# 1. View speakers and sessions function
def view_speakers_and_sessions():
    name = input("Enter speaker name : ")

    cursor = conn.cursor()

    # Check speaker exists
    check_sql = "SELECT speakerName FROM session WHERE speakerName LIKE %s"
    cursor.execute(check_sql, ('%' + name + '%',))
    speaker_exists = cursor.fetchone()

    if not speaker_exists:
        print("\nNo speakers found of that name.")
        return

    # Full query for sessions + rooms
    query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
    """

    cursor.execute(query, ('%' + name + '%',))
    sessions = cursor.fetchall()

    print("\nSessions found:")
    for s in sessions:
        print(s['speakerName'], '|', s['sessionTitle'], '|', s['roomName'])


#2. View attendees by company function
def view_attendees_by_company():
    cursor = conn.cursor()

    while True:
        company_id = input("Enter company ID : ")

        # Must be numeric and > 0
        if not company_id.isdigit():
            continue

        if int(company_id) <= 0:
            continue

        # Check if company exists
        company_name_query = "SELECT companyName FROM company WHERE companyID = %s"
        cursor.execute(company_name_query, (company_id,))
        row = cursor.fetchone()

        if not row:
            continue   # company doesn't exist → reprompt

        company_name = row['companyName']

        # Check if company has attendees
        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, r.roomName
            FROM attendee a
            JOIN company c ON a.attendeeCompanyID = c.companyID
            JOIN registration reg ON a.attendeeID = reg.attendeeID
            JOIN session s ON reg.sessionID = s.sessionID
            JOIN room r ON s.roomID = r.roomID
            WHERE c.companyID = %s
        """

        cursor.execute(query, (company_id,))
        sessions = cursor.fetchall()

        # Company exists but has no attendees → print message and return
        if not sessions:
            print(f"{company_name} Attendees")
            print(f"No attendees found for {company_name}")
            return

        # VALID company with attendees → print results
        print(f"\n{company_name} Attendees")
        for s in sessions:
            print(
                s['attendeeName'], '|',
                s['attendeeDOB'], '|',
                s['sessionTitle'], '|',
                s['speakerName'], '|',
                s['roomName']
            )
        return


    # The user is asked to enter a company ID.
    # When a valid (numeric) company ID is entered, the company name is shown, along with:
    # The name of each attendee, date of birth, title of the session attended,
    # name of the speaker, name of the room
    # A valid company ID is any number greater than 0.
    # User is asked to enter a valid company ID until one has been entered
    pass

# 3. Add new attendee function
import datetime
import pymysql

def add_new_attendee():
    cursor = conn.cursor()

    # Attendee ID
    attendee_id = input("Attendee ID : ")

    # Check if attendee ID exists
    check_attendee_sql = "SELECT * FROM attendee WHERE attendeeID = %s"
    cursor.execute(check_attendee_sql, (attendee_id,))
    if cursor.fetchone():
        print(f"*** ERROR *** Attendee ID: {attendee_id} already exists.")
        return

    # 2. Name
    attendee_name = input("Name : ")

    # 3. DOB
    dob = input("DOB : ")

    # 4. Gender
    gender = input("Gender : ")
    gender = gender.strip().lower()
    if gender in ['m', 'male']:
        gender_value = 'Male'
    elif gender in ['f', 'female']:
        gender_value = 'Female'
    else:
        print("*** ERROR *** Gender must be Male/Female")
        return

    # Company ID
    company_id = input("Company ID : ")

    # Check if company exists 
    check_company_sql = "SELECT * FROM company WHERE companyID = %s"
    cursor.execute(check_company_sql, (company_id,))
    if not cursor.fetchone():
        print(f"*** ERROR *** Company ID: {company_id} does not exist.")
        return

    # Insert attendee
    insert_sql = """
        INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        rowsAffected = cursor.execute(insert_sql, (attendee_id, attendee_name, dob, gender_value, company_id))
        conn.commit()

        if rowsAffected == 0:
            print("No attendee added.")
        else:
            print("Attendee successfully added.")

    except pymysql.MySQLError as e:
        print(f"*** ERROR *** {e.args}")


# 4. View connected attendees function
def view_connected_attendees():
    global neo4j_driver
    cursor = conn.cursor()

    # 1. Ask for attendee ID
    attendee_id = input("Enter attendee ID: ")

    # Must be numeric
    if not attendee_id.isdigit():
        print("*** ERROR *** Attendee ID must be numeric.")
        return

    # 2. Check attendee exists in MySQL
    check_sql = "SELECT attendeeName FROM attendee WHERE attendeeID = %s"
    cursor.execute(check_sql, (attendee_id,))
    row = cursor.fetchone()

    if not row:
        print(f"*** ERROR *** Attendee ID {attendee_id} does not exist.")
        return

    attendee_name = row["attendeeName"]

    # 3. Query Neo4j for connected attendees
    cypher = """
        MATCH (a:Attendee {id: $id})-[:CONNECTED_TO]-(other)
        RETURN other.id AS id, other.name AS name
        ORDER BY other.name
    """

    with neo4j_driver.session() as session:
        results = list(session.run(cypher, {"id": attendee_id}))

    # 4. Print results
    print(f"\nConnections for {attendee_name} (ID {attendee_id}):")
    for result in results:
        print(f"  - {result['name']} (ID: {result['id']})")

    # The user is asked to enter an attendee ID.
    # The name of the attendee as well as the ID and name of all other attendees
    # that have a CONNECTED_TO relationship (in either direction) to this attendee are shown
    # Error handling in brief
    pass


# 5. Add attendee connection function
def add_attendee_connection():
    # The user is asked to enter 2 Attendee IDs.
    # If these attendee IDs exist in the MySQL database, and neither actor has a CONNECTED_TO
    # relationship in the Neo4j database, then a CONNECTED_TO relationship should be created
    # between both nodes
    # LOTS of error handling here - check brief
    pass


# 6. View rooms function
def view_rooms():
    query = """
        SELECT roomID, roomName, capacity
        FROM room
        """

    cursor = conn.cursor()
    cursor.execute(query)
    rooms = cursor.fetchall()

    if not rooms:
        print("\nNo rooms found.")
        return

    for r in rooms:
        print(r['roomID'], '|', r['roomName'], '|', r['capacity'])
    # When this option is chosen the Room ID, Room name, Capacity of all rooms is shown
    # Any new rooms manually added to the MySQL database, after this option has been chosen
    # for the first time, should not be displayed until the user exits and restarts the application.
    pass


def main():
    global neo4j_driver
    neo4j_driver = connect_neo4j()

    # Show display menu
    display_menu()

    # Loop until user exits
    while True:
        choice = input("Choice: ")

        if choice == "1":
            view_speakers_and_sessions()
            display_menu()

        elif choice == "2":
            view_attendees_by_company()
            display_menu()

        elif choice == "3":
            add_new_attendee()
            display_menu()

        elif choice == "4":
            view_connected_attendees()
            display_menu()

        elif choice == "5":
            add_attendee_connection()
            display_menu()

        elif choice == "6":
            view_rooms()
            display_menu()

        elif choice == "x" or choice == "X":
            print("Exiting application.")
            break

        else:
            print("Invalid choice.")
            display_menu()

    neo4j_driver.close()


if __name__ == "__main__":
    main()
