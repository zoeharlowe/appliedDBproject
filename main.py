import datetime
from neo4j import GraphDatabase
import pymysql
import time

neo4j_driver = None

def connect_neo4j():
    uri = "neo4j://localhost:7687"
    return GraphDatabase.driver(uri, auth=("neo4j", "neo4jneo4j"))

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='appdbproj',
    cursorclass=pymysql.cursors.DictCursor
)

# ANSI color codes for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

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

def loading():
    print("Loading", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="")
    print("\n")

# 1. View speakers and sessions function
def view_speakers_and_sessions():
    name = input("\nEnter speaker name : ")

    cursor = conn.cursor()

    # Check speaker exists
    check_sql = "SELECT speakerName FROM session WHERE speakerName LIKE %s"
    cursor.execute(check_sql, ('%' + name + '%',))
    speaker_exists = cursor.fetchone()

    if not speaker_exists:
        print(RED + "\nSessions details for " + name + ":" + RESET)
        print("-------------------------------------")
        print(RED + "\nNo speakers found of that name." + RESET)
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

    print(GREEN + "\nSessions details for " + name + ":" + RESET)
    print("-------------------------------------")
    for s in sessions:
        print(s['speakerName'], '|', s['sessionTitle'], '|', s['roomName'])


# 2. View attendees by company function
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
            print(RED + f"*** ERROR *** Company with ID {company_id} doesn't exist" + RESET)
            continue 

        company_name = row['companyName']

        # Check if company has attendees
        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, r.roomName, s.sessionDate
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
            print(RED + f"No attendees found for {company_name}" + RESET)
            return

        # VALID company with attendees → print results
        print(GREEN + f"\n{company_name} Attendees" + RESET)
        for s in sessions:
            print(
                s['attendeeName'], '|',
                s['attendeeDOB'], '|',
                s['sessionTitle'], '|',
                s['speakerName'], '|',
                s['sessionDate'], '|',
                s['roomName']
            )
        return

# 3. Add new attendee function
def add_new_attendee():
    cursor = conn.cursor()

    # Attendee ID
    attendee_id = input("Attendee ID : ")

    # Check if attendee ID exists
    check_attendee_sql = "SELECT * FROM attendee WHERE attendeeID = %s"
    cursor.execute(check_attendee_sql, (attendee_id,))
    if cursor.fetchone():
        print(RED + f"*** ERROR *** Attendee ID: {attendee_id} already exists." + RESET)
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
        print(RED + "*** ERROR *** Gender must be Male/Female" + RESET)
        return

    # Company ID
    company_id = input("Company ID : ")

    # Check if company exists 
    check_company_sql = "SELECT * FROM company WHERE companyID = %s"
    cursor.execute(check_company_sql, (company_id,))
    if not cursor.fetchone():
        print(RED + f"*** ERROR *** Company ID: {company_id} does not exist" + RESET)
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
            print(RED + "No attendee added." + RESET)
        else:
            print(GREEN + "Attendee successfully added." + RESET)

    except pymysql.MySQLError as e:
        print(RED + f"*** ERROR *** {e.args}" + RESET)

# 4. View connected attendees function
def view_connected_attendees():
    global neo4j_driver
    cursor = conn.cursor()

    # Ask for attendee ID
    attendee_id = input("Enter Attendee ID: ")

    if not attendee_id.isdigit():
        print(RED + "*** ERROR *** Invalid Attendee ID" + RESET)
        return

    # Check attendee exists in MySQL
    sql = "SELECT attendeeName FROM attendee WHERE attendeeID = %s"
    cursor.execute(sql, (attendee_id,))
    row = cursor.fetchone()

    # If attendee does not exist in MySQL → automatic error
    if not row:
        print(RED + "*** ERROR *** Attendee ID does not exist." + RESET)
        return
    
    if row: 
        print(f"Attendee Name: {row['attendeeName']}")

    # Only safe to access after the check
    attendee_name = row["attendeeName"]

    # Check Neo4j for connections (IDs only)
    loading()
    cypher = """
        MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
        RETURN b.AttendeeID AS id
        ORDER BY b.AttendeeID
    """

    with neo4j_driver.session() as session:
        results = list(session.run(cypher, {"id": int(attendee_id)}))

    # If attendee exists in MySQL but not in Neo4j
    if not results:
        print(RED + "No connections" + RESET)
        return

    # If attendee exists in both → show connected attendees
    if results:
        print("---------------------\n" + GREEN + "These attendees are connected:" + RESET)
    for r in results:
        connected_id = r["id"]

        # Look up name in MySQL
        cursor.execute(
            "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
            (connected_id,)
        )
        name_row = cursor.fetchone()
        connected_name = name_row["attendeeName"] if name_row else "Unknown"

        print(f"{connected_id} | {connected_name}")

# 5. Add attendee connection function
def add_attendee_connection():
    global neo4j_driver
    cursor = conn.cursor()

    # Input two Attendee IDs
    a1 = input("Enter Attendee 1 ID : ").strip()
    a2 = input("Enter Attendee 2 ID : ").strip()

    # Validate numeric
    if not a1.isdigit() or not a2.isdigit():
        print(RED + "*** ERROR *** Attendee IDs must be numbers" + RESET)
        return

    # Validate not equal
    if a1 == a2:
        print(RED + "*** ERROR *** An attendee cannot connect to him/herself" + RESET)
        return
    
     # Validate both attendees together
    check_sql = "SELECT attendeeID, attendeeName FROM attendee WHERE attendeeID IN (%s, %s)"
    cursor.execute(check_sql, (a1, a2))
    rows = cursor.fetchall()

    if len(rows) != 2:
        print(RED + "*** ERROR *** One or both attendee IDs do not exist." + RESET)
        return
    
    # Extract names
    name1 = None
    name2 = None
    for row in rows:
        if str(row["attendeeID"]) == a1:
            name1 = row["attendeeName"]
        else:
            name2 = row["attendeeName"]

    # Check if relationship already exists in Neo4j
    loading()
    check_rel = """
        MATCH (a:Attendee {AttendeeID: $a1})-[:CONNECTED_TO]-(b:Attendee {AttendeeID: $a2})
        RETURN a
    """

    with neo4j_driver.session() as session:
        rel_exists = session.run(check_rel, {"a1": int(a1), "a2": int(a2)}).single()
        if rel_exists:
            print(RED + f"*** ERROR *** These attendees are already connected." + RESET)
            return

    # Create nodes if needed
    create_nodes = """
        MERGE (a:Attendee {AttendeeID: $a1})
        MERGE (b:Attendee {AttendeeID: $a2})
    """

    # Create relationship
    create_rel = """
        MATCH (a:Attendee {AttendeeID: $a1})
        MATCH (b:Attendee {AttendeeID: $a2})
        MERGE (a)-[:CONNECTED_TO]-(b)
    """

    with neo4j_driver.session() as session:
        session.run(create_nodes, {"a1": int(a1), "a2": int(a2)})
        session.run(create_rel, {"a1": int(a1), "a2": int(a2)})

    print(GREEN + f"Connection created between {name1} (ID {a1}) and {name2} (ID {a2})." + RESET)

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
        print(RED + "\nNo rooms found." + RESET)
        return

    for r in rooms:
        print(r['roomID'], '|', r['roomName'], '|', r['capacity'])

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
