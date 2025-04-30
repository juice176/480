import psycopg2

# Connect to your PostgreSQL database
# make sure the tables have a increment for rent_id and review_id fro rent and review
conn = psycopg2.connect(database="postgres",
                    host="localhost",
                    user="andreais_745",
                    password="localhost",
                    port=5432)

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

def driverLoop(driver_name):
    while True:
        print("What would you like to do?")
        print("\t1. Change address")
        print("\t2. View car models")
        print("\t3. Declare car models you can drive")
        print("\t4. Logout")
        print()
        print("Enter the number of your choices: ",end="")
        choice = input().strip()
        if choice == "1":
            changeAddress(driver_name)
        if choice == "2":
            viewCarModels()
        elif choice == "3":
            declareCars(driver_name)
        elif choice == "4":
            print()
            print("Successfully logged out " + driver_name + ".")
            print("Returning to main menu...")
            break
        else:
            print("Unknown command. Please try again.")
            print()
def changeAddress(driver_name):
    print("Please provide your new street name: ", end="")
    street = input().strip()

    print("Please provide your new house/apt number:", end="")
    number = input().strip()

    print("Please provide your new city: ",end="")
    city=input().strip()
    try: 
        cur.execute("""
            SELECT * FROM ADDRESS WHERE ROAD = %s AND NUMBER = %s AND CITY = %s;
        """, (street, number, city))
        address = cur.fetchone()
        if address:
            print("Address already exists in the database.")
        else:
            print("Address does not exist in the database, inserting...")
            cur.execute("""
                INSERT INTO ADDRESS (ROAD, NUMBER, CITY)
                VALUES (%s, %s, %s);
            """, (street, number, city))
            conn.commit()
            print("Address inserted successfully!")
        cur.execute("""
                    UPDATE DRIVER
                    SET ROAD =%s,NUMBER=%s,CITY=%s
                    WHERE NAME = %s;
        """,(street,number,city,driver_name))
        conn.commit()
        print("Your address has been updated successfully!")
    except psycopg2.Error as e:
        print("ERROR:",e)
        print("Failed to update address.")
    return

def viewCarModels():
    try:
        cur.execute("""
            SELECT MODEL_ID,TRANSMISSION,YEAR,COLOR,CAR_ID
            FROM MODEL;
        """)
        models = cur.fetchall()
        print("\nAvailable Car Models:")
        for model in models:
            model_id,transmission,year,color,car_id = model
            print(f"Model ID: {model_id}, Transmission:{transmission}, Year: {year}, Color:{color},Car_ID:{car_id}")
    except psycopg2.Error as e:
        print("ERROR:",e)
        print("Failed to retrive car models.")
def declareCars(driver_name):
    print("Please enter the model_id and car_id for the car(s) you can drive")
    print("You can enter 'done' when you are finished")

    while True:
        print("Enter model ID: ", end="")
        model_id = input().strip()
        if model_id.lower() == 'done':
            break
        print("Enter car_id: ",end="")
        car_id = input().strip()
        try:
            cur.execute("""
                INSERT INTO CAN_DRIVE (DRIVER_NAME,MODEL_ID,CAR_ID)
                VALUES(%s,%s,%s);
            """,(driver_name,model_id,car_id))
            conn.commit()
            print(f"Model {model_id} and Car{car_id} successfully declared.")
        except psycopg2.Error() as e:
            print("ERROR: ",e)
            print(f"Failed to declare Model{model_id} and Car{car_id}.")
    return




def clientLoop(client_email):
    while True:
        print("Welcome to the Client Menu!")
        print("\t1. View available cars on a specific date")
        print("\t2. Book a car")
        print("\t3. View your rents")
        print("\t4. Leave a review for a driver")
        print("\t5. Logout")
        print()
        print("Enter the number of your choice: ", end="")
        choice = input().strip()

        if choice == "1":
            viewAvailableCars()
        elif choice == "2":
            bookCar(client_email)
        elif choice == "3":
            viewRents(client_email)
        elif choice == "4":
            leaveReview(client_email)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

def viewAvailableCars():
    print("Please provide the date you want to check for available cars (YYYY-MM-DD): ", end="")
    rent_date = input().strip()

    try:
        cur.execute("""
            SELECT m.MODEL_ID, m.CAR_ID
            FROM MODEL m
            LEFT JOIN RENT r ON m.MODEL_ID = r.MODEL_ID AND m.CAR_ID = r.CAR_ID AND r.RENT_DATE = %s
            WHERE r.RENT_ID IS NULL;
        """, (rent_date,))

        available_cars = cur.fetchall()

        if available_cars:
            print("Available Cars:")
            for model_id, car_id in available_cars:
                print(f"Model ID: {model_id}, Car ID: {car_id}")
        else:
            print("No cars are available on that date.")
    except psycopg2.Error as e:
        print("ERROR:", e)
    return

def bookCar(client_email):
    print("Please provide the date you want to book the car (YYYY-MM-DD): ", end="")
    rent_date = input().strip()

    print("Please provide the car model ID: ", end="")
    model_id = input().strip()

    try:
        cur.execute("""
            SELECT m.MODEL_ID, m.CAR_ID
            FROM MODEL m
            LEFT JOIN RENT r ON m.MODEL_ID = r.MODEL_ID AND m.CAR_ID = r.CAR_ID AND r.RENT_DATE = %s
            WHERE m.MODEL_ID = %s AND r.RENT_ID IS NULL;
        """, (rent_date, model_id))

        available_cars = cur.fetchall()

        if available_cars:
            print("Available cars:")
            for model_id, car_id in available_cars:
                print(f"Model ID: {model_id}, Car ID: {car_id}")

            car_id = available_cars[0][1]

            cur.execute("""
                SELECT d.NAME
                FROM DRIVER d
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM RENT r
                    WHERE r.NAME = d.NAME AND r.RENT_DATE = %s
                )
                AND EXISTS (
                    SELECT 1
                    FROM CAN_DRIVE cd
                    WHERE cd.DRIVER_NAME = d.NAME AND cd.MODEL_ID = %s AND cd.CAR_ID = %s
                )
                LIMIT 1;
            """, (rent_date, model_id, car_id))

            available_driver = cur.fetchone()

            if available_driver:
                driver_name = available_driver[0]
                print(f"Booking successful! Driver: {driver_name}")

                cur.execute("""
                    INSERT INTO RENT (RENT_DATE, EMAIL, NAME, MODEL_ID, CAR_ID)
                    VALUES (%s, %s, %s, %s, %s);
                """, (rent_date, client_email, driver_name, model_id, car_id))

                conn.commit()

                print("Car booked successfully!")
            else:
                print("No available driver for the selected car on that date.")
        else:
            print("No available cars for the selected model on that date.")
    except psycopg2.Error as e:
        print("ERROR:", e)
        conn.rollback()
    return

def viewRents(client_email):
    try:
        cur.execute("""
            SELECT r.RENT_DATE, m.MODEL_ID, m.CAR_ID, d.NAME
            FROM RENT r
            JOIN MODEL m ON r.MODEL_ID = m.MODEL_ID AND r.CAR_ID = m.CAR_ID
            JOIN DRIVER d ON r.NAME = d.NAME
            WHERE r.EMAIL = %s;
        """, (client_email,))

        rents = cur.fetchall()

        if rents:
            for rent_date, model_id, car_id, driver_name in rents:
                print(f"Date: {rent_date}, Model ID: {model_id}, Car ID: {car_id}, Driver: {driver_name}")
        else:
            print("You have no rents booked.")
    except psycopg2.Error as e:
        print("ERROR:", e)
        conn.rollback()
    return

def leaveReview(client_email):
    print("Please provide the driver's name: ", end="")
    driver_name = input().strip()
    #leaves review, this is where the increment counter for rent_id is needed
    try:
        cur.execute("""
            SELECT r.RENT_ID
            FROM RENT r
            WHERE r.NAME = %s AND r.EMAIL = %s;
        """, (driver_name, client_email))

        if cur.fetchone():
            print("Please provide your rating (1-5): ", end="")
            rating = int(input().strip())

            print("Please provide your review message: ", end="")
            message = input().strip()

            cur.execute("""
                    SELECT * FROM REVIEW WHERE NAME = %s AND EMAIL = %s;
                    """, (driver_name, client_email))
            existing_review = cur.fetchone()

            if existing_review:
                print("You have already reviewed this driver.")
            else:
                try: 
                    cur.execute("""
                        INSERT INTO REVIEW (RATING, MESSAGE, NAME, EMAIL)
                        VALUES (%s, %s, %s, %s);
                    """, (rating, message, driver_name, client_email))
                    conn.commit()
                    print("Review submitted successfully!")
                except psycopg2.Error as e:
                    conn.rollback()
        else:
            print("You cannot review this driver as they were not assigned to any of your rentals.")
    except psycopg2.Error as e:
        print("ERROR:", e)
        conn.rollback()
    return
# END OF HELPER FUNCTIONS -------------------------------------------------------

# MAIN LOOP ---------------------------------------------------------------------
displayMainCommands()

while True:
    cur.execute("SET search_path TO taxi_management;")
    print("Enter command: ", end = "")
    command = input()
    if command == "reg c":
        print("Please provide the client's full name: ", end="")
        name = input().strip()

        print("Please provide the client's email: ", end="")
        email = input().strip()

        cur.execute("SET search_path TO taxi_management;")
        #inputs client info or checks if they already exist
        try:
            cur.execute("""
                INSERT INTO CLIENT (NAME, EMAIL)
                VALUES (%s, %s);
            """, (name, email))
            conn.commit()
            print("Client inserted successfully!")
        except psycopg2.errors.UniqueViolation:
            print("Client already exists. Continuing to address/credit card entry...")
            conn.rollback()
        except psycopg2.Error as e:
            print("ERROR:", e)
            conn.rollback()
            break

        # --- Address Loop ---
        while True:
            print("Please provide the street name for address: ", end="")
            street = input().strip()

            print("Please provide the house/apartment number: ", end="")
            number = input().strip()

            print("Please provide the city: ", end="")
            city = input().strip()

            cur.execute("SET search_path TO taxi_management;")
            try:
                # checks if address already exists in the address table then inputs into hasaddress
                cur.execute("""
                    SELECT * FROM ADDRESS WHERE ROAD = %s AND NUMBER = %s AND CITY = %s;
                """, (street, number, city))
                existing_address = cur.fetchone()

                if existing_address:
                    print("Address already exists. Linking to client...")
            except psycopg2.Error() as e:
                conn.rollback()
            else:
                try:
                    cur.execute("""
                        INSERT INTO ADDRESS (ROAD, NUMBER, CITY)
                        VALUES (%s, %s, %s);
                    """, (street, number, city))
                    conn.commit()
                    print("Address added successfully!")
                except psycopg2.Error as e:
                    print("Error:", e)
                    conn.rollback()

            try:
                cur.execute("""
                    INSERT INTO HasAddress (EMAIL, ROAD, NUMBER, CITY)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (EMAIL, ROAD, NUMBER, CITY) DO NOTHING;
                """, (email, street, number, city))
                conn.commit()
                print("Address linked to client successfully!")
            except psycopg2.Error as e:
                print("Error:", e)
                conn.rollback()

            print("Do you want to add another address? (yes/no): ", end="")
            if input().strip().lower() != "yes":
                break

        # --- Credit Card Loop ---
        while True:
            print("Please provide the credit card number (16 digits): ", end="")
            card_number = input().strip()

            print("Please provide the address' road (for credit card): ", end="")
            card_road = input().strip()

            print("Please provide the address' number (for credit card): ", end="")
            card_number_addr = input().strip()

            print("Please provide the address' city (for credit card): ", end="")
            card_city = input().strip()

            cur.execute("SET search_path TO taxi_management;")
            #if credit card already exists
            try: 


                cur.execute("""
                    SELECT * FROM CREDIT_CARD WHERE NUMBER = %s;
                """, (card_number,))
                existing_card = cur.fetchone()

                if existing_card:
                    print("Credit card already exists. Linking to client...")
            except psycopg2.Error() as e:
                conn.rollback()
            #enter in address and inputs into hasaddress as well
            else:
                try:
                    cur.execute("""
                        INSERT INTO CREDIT_CARD (NUMBER, EMAIL, ROAD, NUMBER_ADDR, CITY)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (card_number, email, card_road, card_number_addr, card_city))
                    conn.commit()
                    print("Credit card added successfully!")
                except psycopg2.Error as e:
                    print("Error:", e)
                    conn.rollback()

            try:
                cur.execute("""
                    INSERT INTO HasAddress (EMAIL, ROAD, NUMBER, CITY)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (EMAIL, ROAD, NUMBER, CITY) DO NOTHING;
                """, (email, card_road, card_number_addr, card_city))
                conn.commit()
                print("Credit card linked to client successfully!")
            except psycopg2.Error as e:
                print("Error:", e)
                conn.rollback()

            print("Do you want to add another credit card? (yes/no): ", end="")
            if input().strip().lower() != "yes":
                break



    if command == "login m":
        print("Please provide your SSN (without the dashes): ", end = '')
        inSSN = input()
        
        try:
            cur.execute("SELECT * FROM MANAGER WHERE SSN = %s;", (inSSN,))
            manager = cur.fetchone()

            if manager:
                managerLoop(manager[0])
            else:
                print("Manager not found, please try again.")
                print()
        except psycopg2.Error as e:
            print()
            print("ERROR: ", e)
            print("Please try again.")
            conn.rollback()
            print()
    #login for driver taking in thier name
    elif command == "login d":
        print("Please provide your name: ", end = '')
        inName = input()
        
        try:
            cur.execute("SELECT * FROM DRIVER WHERE NAME = %s;", (inName,))
            driver_name = cur.fetchone()

            if driver_name:
                driverLoop(driver_name[0])
            else:
                print("Driver not found, please try again.")
                print()
        except psycopg2.Error as e:
            print()
            print("ERROR: ", e)
            print("Please try again.")
            conn.rollback()
            print()
    # login for client allowing them to enter thier email
    elif command == "login c":
        print("Please provide your email: ",end="")
        email = input().strip()
        try:
            cur.execute("SELECT * FROM CLIENT WHERE EMAIL = %s;",(email,))
            client = cur.fetchone()
            if client:
                print(f"Welcome {client[0]}! You have successfully logged in.")
                clientLoop(email)
            else: 
                print("Client not found, please try again.")
        except psycopg2.Error() as e:
            print("ERROR: ",e)
            print("Please try again.")
            conn.rollback()
    elif command == "exit":
        print("Thank you and have a great day! Exiting...")
        break
    else:
        displayMainCommands()
        print("Unknown command. Please try again.")
        print()
# END OF MAIN LOOP --------------------------------------------------------------

# Clean up
cur.close()
conn.close()
exit()