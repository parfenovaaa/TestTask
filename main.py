import random
import sqlite3

database_path = "originDataBase.db"


def create_conn(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    return conn, cursor


def create_database():
    conn, cursor = create_conn(database_path)
    cursor.execute("""CREATE TABLE Weapons
                          (weapon TEXT PRIMARY KEY,
                           reload_speed INT, 
                           rotation_speed INT,
                           diameter INT, 
                           power_volley INT,
                           count INT)
                       """)

    cursor.execute("""CREATE TABLE Hulls
                          (hull TEXT PRIMARY KEY,
                           armor INT, 
                           type INT,
                           capacity INT)
                       """)

    cursor.execute("""CREATE TABLE Engines
                          (engine TEXT PRIMARY KEY,
                           power INT, 
                           type INT)
                       """)

    cursor.execute("""CREATE TABLE Ships
                          (ship TEXT PRIMARY KEY,
                           weapon TEXT, 
                           hull TEXT, 
                           engine TEXT,
                           FOREIGN KEY (weapon)  REFERENCES Weapons (weapon),
                           FOREIGN KEY (hull)  REFERENCES Hulls (hull),
                           FOREIGN KEY (engine)  REFERENCES Engines (engine))
                       """)


def add_data_to_ships_table(n):
    conn, cursor = create_conn(database_path)
    for i in range(n):
        ship = "ship-" + str(i+1)
        weapon = "weapon-" + get_random_number_from_1_to_n(20)
        hull = "hull-" + get_random_number_from_1_to_n(5)
        engine = "engine-" + get_random_number_from_1_to_n(6)
        new_ship = (ship, weapon, hull, engine)
        cursor.execute("INSERT INTO Ships VALUES(?, ?, ?, ?);", new_ship)
        conn.commit()


def add_data_to_weapons_table(n):
    conn, cursor = create_conn(database_path)
    for i in range(n):
        weapon = "weapon-" + str(i+1)
        reload_speed = get_random_number_from_1_to_n(20)
        rotation_speed = get_random_number_from_1_to_n(20)
        diameter = get_random_number_from_1_to_n(20)
        power_volley = get_random_number_from_1_to_n(20)
        count = get_random_number_from_1_to_n(20)
        new_weapon = (weapon, reload_speed, rotation_speed, diameter, power_volley, count)
        cursor.execute("INSERT INTO Weapons VALUES(?, ?, ?, ?, ?, ?);", new_weapon)
        conn.commit()


def add_data_to_hulls_table(n):
    conn, cursor = create_conn(database_path)
    for i in range(n):
        hull = "hull-" + str(i+1)
        armor = get_random_number_from_1_to_n(20)
        type = get_random_number_from_1_to_n(20)
        capacity = get_random_number_from_1_to_n(20)
        new_hull = (hull, armor, type, capacity)
        cursor.execute("INSERT INTO Hulls VALUES(?, ?, ?, ?);", new_hull)
        conn.commit()


def add_data_to_engines_table(n):
    conn, cursor = create_conn(database_path)
    for i in range(n):
        engine = "engine-" + str(i+1)
        power = random.randint(1, 20)
        type = random.randint(1, 20)
        new_engine = (engine, power, type)
        cursor.execute("INSERT INTO Engines VALUES(?, ?, ?);", new_engine)
        conn.commit()


def get_random_number_from_1_to_n(n):
    return str(random.randint(1, n))


if __name__ == '__main__':
    create_database()
    add_data_to_ships_table(200)
    add_data_to_weapons_table(20)
    add_data_to_hulls_table(5)
    add_data_to_engines_table(6)
