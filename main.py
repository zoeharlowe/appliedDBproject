import pymysql

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
    print("7 - Exit application")


# 1. View speakers and sessions function
def view_speakers_and_sessions():
    # For each speaker whose name is a partial match, the following details are shown:
    # speaker’s name, title of session, name of room 
    
    # If no speaker matches the search string the following message is shown:
    # 'No speakers found of that name'
    # User returned to main menu
    pass


# 2. View attendees by company function
def view_attendees_by_company():
    # The user is asked to enter a company ID.
    # When a valid (numeric) company ID is entered, the company name is shown, along with:
    # The name of each attendee, date of birth, title of the session attended,
    # name of the speaker, name of the room
    # A valid company ID is any number greater than 0.
    # User is asked to enter a valid company ID until one has been entered
    pass


# 3. Add new attendee function
def add_new_attendee():
    # The user is asked to enter the following details for a new attendee:
    # ID, name, DOB, Gender, ID attendee’s company
    # “Attendee successfully added” should be shown, and the user returned to the main menu
    # Error handling in brief
    pass


# 4. View connected attendees function
def view_connected_attendees():
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
    # When this option is chosen the Room ID, Room name, Capacity of all rooms is shown
    # Any new rooms manually added to the MySQL database, after this option has been chosen
    # for the first time, should not be displayed until the user exits and restarts the application.
    pass


def main():

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

        elif choice == "7":
            print("Exiting application.")
            break

        else:
            print("Invalid choice.")
            display_menu()


if __name__ == "__main__":
    main()
