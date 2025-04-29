import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres", # Probably postgres
    password="dante", # Whatever your password is
    host="localhost",
    port="5432"
)

# Create a cursor to execute SQL queries
cur = conn.cursor()

# Set the search_path so we don't have to qualify the schema for each query
cur.execute("SET search_path TO taxi_management;")

# HELPER FUNCTIONS --------------------------------------------------------------
def displayMainCommands():
    print()
    print("Welcome! Please observe the command list below:")
    print()
    print("LOGGING IN:")
    print("\tTo log in as a manager, use: login m")
    print("\tTo log in as a driver, use: login d")
    print("\tTo log in as a client, use: login c")
    print()
    print("REGISTRATION:")
    print("\tTo register as a client, use: reg c")
    print("\tTo register a new manager, please log in to an existing manager account first.")
    print()
    print("EXIT:")
    print("\tTo exit the program, use: exit")
    print()

def managerLoop(manager):
    print("Welcome " + manager + "! Please observe the command list below:")
    print()
    print("REGISTRATION:")
    print("\tTo register a new manager, use: reg m")
    print()
    print("ADDING/REMOVING ENTRIES:")
    print("\tTo add or remove a car, use: add c --OR-- rm c")
    print("\tTo add or remove a model, use: add m --OR-- rm m")
    print("\tTo add or remove a driver, use: add d --OR-- rm d")
    print()
    print("LIST INFO:")
    print("\tTo get a list of top clients, use: list c")
    print("\tTo get a list of models used, use: list m")
    print("\tTo get a list of drivers, use: list d")
    print()
    print("CITY TO CITY:")
    print("\tTo get a list of clients from one city who have booked a rent in another, use: c2c")
    print()
    print("LOGGING OUT:")
    print("\tTo log out and go back to the main menu, use: logout")
    print()
    
    while True:
        cur.execute("SET search_path TO taxi_management;")
        print("Enter command: ", end = "")

        command = input()

        if command == "reg m":
            print("Please provide the manager's full name: ", end = "")
            name = input()

            print("Please provide the manager's SSN (without dashes): ", end = "")
            inSSN = input()

            if not inSSN.isnumeric() or not len(inSSN) == 9:
                print()
                print("Invalid SSN. Please try again.")
                print()
                continue

            print("Please provide the manager's e-mail address: ", end = "")
            email = input()

            try:
                cur.execute("""
                    INSERT INTO MANAGER (NAME, SSN, EMAIL)
                    VALUES (%s, %s, %s);
                """, (name, inSSN, email))

                conn.commit()

                print()
                print("Manager inserted successfully!")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "add c":
            print("Please provide the car ID: ", end = "")
            carID = input()

            print("Please provide the brand: ", end = "")
            brand = input()

            try:
                cur.execute("""
                    INSERT INTO CAR (CAR_ID, BRAND)
                    VALUES (%s, %s);
                """, (carID, brand))

                conn.commit()

                print()
                print("Car inserted successfully!")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "add m":
            print("Please provide the model ID: ", end = "")
            modelID = input()

            print("Please provide the transmission type (Manual or Automatic, case sensitive): ", end = "")
            transmission = input()

            tTypes = ["Manual", "Automatic"]

            if not transmission in tTypes:
                print()
                print("Invalid transmission type. Please try again.")
                print()
                continue

            print("Please provide the year: ", end = "")
            year = input()

            if not year.isnumeric() or not len(year) == 4:
                print()
                print("Invalid year (must be 4 digits). Please try again.")
                print()
                continue

            print("Please provide the color: ", end = "")
            color = input()

            print("Please provide the car ID the model is attached to: ", end = "")
            carID = input()

            try:
                cur.execute("""
                    INSERT INTO MODEL (MODEL_ID, TRANSMISSION, YEAR, COLOR, CAR_ID)
                    VALUES (%s, %s, %s, %s, %s);
                """, (modelID, transmission, year, color, carID))

                conn.commit()

                print()
                print("Model inserted successfully!")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "add d":
            print("Please provide the driver's full name: ", end = "")
            name = input()

            print("Please provide the street name of the driver's address: ", end = "")
            street = input()

            print("Please provide the house/apartment number of the driver's address: ", end = "")
            number = input()

            print("Please provide the city of the driver's address: ", end = "")
            city = input()

            try:
                print()
                print("Checking if address exists in database already...")

                cur.execute("""
                    INSERT INTO ADDRESS (ROAD, NUMBER, CITY)
                    VALUES (%s, %s, %s);
                """, (street, number, city))

                conn.commit()

                print("Address does not exist yet, inserted as new address successfully!")
                print("Attaching new driver entry to it...")
            except psycopg2.Error as e:
                print("Address exists already, attaching new driver entry to it...")

                conn.rollback()
                cur.execute("SET search_path TO taxi_management;")

            try:
                cur.execute("""
                    INSERT INTO DRIVER (NAME, ROAD, NUMBER, CITY)
                    VALUES (%s, %s, %s, %s);
                """, (name, street, number, city))

                conn.commit()

                print()
                print("Driver inserted successfully!")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "rm c":
            print("Please provide the car ID: ", end = "")
            carID = input()

            try:
                # Delete from dependent tables first
                cur.execute("DELETE FROM MODEL WHERE CAR_ID = %s;", (carID,))
                cur.execute("DELETE FROM RENT WHERE CAR_ID = %s;", (carID,))
                cur.execute("DELETE FROM CAN_DRIVE WHERE CAR_ID = %s;", (carID,))

                # Now delete the car
                cur.execute("DELETE FROM CAR WHERE CAR_ID = %s;", (carID,))

                conn.commit()

                print()
                print("Car (and related records) deleted successfully! (If car ID was not in database, this still returns successfully).")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "rm m":
            print("Please provide the model ID: ", end = "")
            modelID = input()

            try:
                # Delete from dependent tables first
                cur.execute("DELETE FROM RENT WHERE MODEL_ID = %s;", (modelID,))
                cur.execute("DELETE FROM CAN_DRIVE WHERE MODEL_ID = %s;", (modelID,))

                # Now delete the car
                cur.execute("DELETE FROM MODEL WHERE MODEL_ID = %s;", (modelID,))

                conn.commit()

                print()
                print("Model (and related records) deleted successfully! (If model ID was not in database, this still returns successfully).")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "rm d":
            print("Please provide the driver's full name: ", end = "")
            name = input()

            try:
                # Delete from dependent tables first
                cur.execute("DELETE FROM REVIEW WHERE NAME = %s;", (name,))
                cur.execute("DELETE FROM RENT WHERE NAME = %s;", (name,))
                cur.execute("DELETE FROM CAN_DRIVE WHERE NAME = %s;", (name,))

                # Now delete the car
                cur.execute("DELETE FROM DRIVER WHERE NAME = %s;", (name,))

                conn.commit()

                print()
                print("Driver (and related records) deleted successfully! (If driver name was not in database, this still returns successfully).")
                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()

                conn.rollback()
        elif command == "list c":
            print("What is the maximum amount of clients you would like to display? (Must be > 0): ", end = "")

            try:
                k = int(input())
            except:
                print()
                print("Invalid number, must be an integer > 0. Try again.")
                print()
                continue

            if not k > 0:
                print()
                print("Invalid number, must be an integer > 0. Try again.")
                print()
                continue
            
            try:
                cur.execute("""
                    SELECT c.NAME, c.EMAIL, COUNT(r.RENT_ID) AS rent_count
                    FROM CLIENT c
                    LEFT JOIN RENT r ON c.EMAIL = r.EMAIL
                    GROUP BY c.NAME, c.EMAIL
                    ORDER BY rent_count DESC
                    LIMIT %s;
                """, (k,))

                top_clients = cur.fetchall()

                print()

                num = 1

                for name, email, count in top_clients:
                    if count == 1:
                        print(str(num) + ". " f"{name} ({email}) - {count} rent")
                    else:
                        print(str(num) + ". " f"{name} ({email}) - {count} rents")

                    num = num + 1

                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()
        elif command == "list m":
            try:
                cur.execute("""
                    SELECT m.MODEL_ID, m.CAR_ID, COUNT(r.RENT_ID) AS rent_count
                    FROM MODEL m
                    LEFT JOIN RENT r ON m.MODEL_ID = r.MODEL_ID AND m.CAR_ID = r.CAR_ID
                    GROUP BY m.MODEL_ID, m.CAR_ID
                    ORDER BY rent_count DESC;
                """)

                results = cur.fetchall()

                print()

                for model_id, car_id, count in results:
                    print(f"Model ID: {model_id} (Car ID: {car_id}) - {count} rents")

                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()
        elif command == "list d":
            try:
                cur.execute("""
                    SELECT d.NAME, COUNT(DISTINCT r.RENT_ID) AS total_rents, ROUND(AVG(rv.RATING)::numeric, 2) AS average_rating
                    FROM DRIVER d
                    LEFT JOIN RENT r ON d.NAME = r.NAME
                    LEFT JOIN REVIEW rv ON d.NAME = rv.NAME
                    GROUP BY d.NAME
                    ORDER BY total_rents DESC;
                """)

                print()

                for name, total_rents, average_rating in cur.fetchall():
                    print(f"{name}: {total_rents} rents, Avg Rating: {average_rating or 'No reviews'}")

                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()
        elif command == "c2c":
            print('Please enter the "from" city: ', end = "")
            c1 = input()

            print('Please enter the "to" city: ', end = "")
            c2 = input()

            try:
                cur.execute("""
                    SELECT DISTINCT c.NAME, c.EMAIL
                    FROM CLIENT c
                    JOIN HasAddress ha ON c.EMAIL = ha.EMAIL
                    JOIN RENT r ON c.EMAIL = r.EMAIL
                    JOIN DRIVER d ON r.NAME = d.NAME
                    WHERE ha.CITY = %s AND d.CITY = %s;
                """, (c1, c2))

                results = cur.fetchall()

                print()

                if not results:
                    print(f"No clients found with address in {c1} and rentals with drivers from {c2}.")
                else:
                    print(f"Clients with address in {c1} and rents with drivers from {c2}:")
                    for name, email in results:
                        print(f"\t{name} - {email}")

                print()
            except psycopg2.Error as e:
                print()
                print("ERROR:", e)
                print("Please try again.")
                print()
        elif command == "logout":
            print()
            print("Successfully logged out " + manager + ".")
            print("Returning to main menu...")
            displayMainCommands()
            break
        else:
            print("Unknown command. Please try again.")
            print()

def driverLoop():
    exit()

def clientLoop():
    exit()
# END OF HELPER FUNCTIONS -------------------------------------------------------

# MAIN LOOP ---------------------------------------------------------------------
displayMainCommands()

while True:
    cur.execute("SET search_path TO taxi_management;")
    print("Enter command: ", end = "")
    command = input()

    if command == "login m":
        print("Please provide your SSN (without the dashes): ", end = "")
        inSSN = input()
        
        try:
            cur.execute("SELECT * FROM MANAGER WHERE SSN = %s;", (inSSN,))
            manager = cur.fetchone()
            
            print()

            if manager:
                managerLoop(manager[0])
            else:
                print("Manager not found, please try again.")
                print()
        except psycopg2.Error as e:
            print()
            print("ERROR: ", e)
            print("Please try again.")
            print()
    elif command == "login d":
        driverLoop()
    elif command == "login c":
        clientLoop()
    elif command == "exit":
        print("Thank you and have a great day! Exiting...")
        break
    else:
        print("Unknown command. Please try again.")
        print()
# END OF MAIN LOOP --------------------------------------------------------------

# Clean up
cur.close()
conn.close()
exit()