import os
import random
import shutil
import sqlite3

import pytest
from pytest_check import check_func

import randomize_data

original_database_path = "originDataBase.db"
backup_database_path = "originDataBase_backup.db"


@pytest.fixture(scope='session')
def check_and_copy_database():
    shutil.copyfile(original_database_path, backup_database_path)
    change_ships_in_backup_database("Ships")
    change_ships_in_backup_database("Weapons")
    change_ships_in_backup_database("Hulls")
    change_ships_in_backup_database("Engines")
    yield
    os.remove(backup_database_path)


def get_column(database, column_name, i):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    row = "ship-" + str(i + 1)
    query = "SELECT * FROM Ships  WHERE ship = ?"
    cursor.execute(query, (row,))
    result = cursor.fetchone()
    if column_name == "weapon":
        return result[1]
    elif column_name == "hull":
        return result[2]
    elif column_name == "engine":
        return result[3]


def get_tables_size(table_name):
    query = ("SELECT * FROM %s" % table_name)

    origin_db = sqlite3.connect(original_database_path)
    cursor_origin = origin_db.cursor()
    cursor_origin.execute(query)
    origin_results = cursor_origin.fetchall()
    origin_size = len(origin_results)

    backup_db = sqlite3.connect(backup_database_path)
    cursor_backup = backup_db.cursor()
    cursor_backup.execute(query)
    backup_results = cursor_backup.fetchall()
    backup_size = len(backup_results)

    assert origin_size == backup_size

    return origin_size


def get_component(database, table_name, i):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT Ships.ship, %s.* FROM %s LEFT OUTER JOIN `Ships` ON %s.%s = Ships.%s  WHERE Ships.ship = 'ship-%s" \
            % (table_name, table_name, table_name, table_name.lower()[:-1], table_name.lower()[:-1], str(i + 1)) + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    results = {}
    columns_names = [i[0] for i in cursor.description]
    for j in range(len(cursor.description)):
        if table_name.lower()[:-1] in str(result[j]) or "ship" in str(result[j]):
            results.update({j: str(result[j])})
        else:
            results.update({j: columns_names[j] + " " + str(result[j])})

    return results


def change_ships_in_backup_database(table_name):
    conn = sqlite3.connect(original_database_path)
    cursor = conn.cursor()
    query = ("SELECT * FROM %s" % table_name)
    cursor.execute(query, ())
    results = cursor.fetchall()
    size_of_table = len(results)
    for i in range(size_of_table):

        col_to_change = str(randomize_data.table_columns(table_name))

        if col_to_change == "weapon":
            new_value = col_to_change + "-" + str(random.randint(1, 20))
        elif col_to_change == "hull":
            new_value = col_to_change + "-" + str(random.randint(1, 5))
        elif col_to_change == "engine":
            new_value = col_to_change + "-" + str(random.randint(1, 6))
        else:
            new_value = str(random.randint(1, 20))

        row = table_name.lower()[:-1] + "-" + str(i + 1)

        update_value = (new_value, row)
        query = "UPDATE %s SET %s = ? Where %s = ?" % (table_name, col_to_change, table_name.lower()[:-1])
        cursor.execute(query, update_value)
        conn.commit()


@check_func
def asserts_components(origin_data, backup_data):
    for j in range(len(origin_data) - 2):
        j = j + 2
        try:
            assert origin_data.get(j) == backup_data.get(j), "Assert"
        except AssertionError:
            raise(AssertionError(str(backup_data.get(0)) + ", " + str(backup_data.get(1)) +
                                 ": \n Expected " + str(origin_data.get(j)) +
                                 ", was " + str(backup_data.get(j)) + "\n "))


@check_func
def asserts_ships(origin_data, backup_data, i):
    try:
        assert origin_data == backup_data, "Assert"
    except AssertionError:
        raise(AssertionError("Ship-" + str(i + 1) + ", " + backup_data +
                             ":\n Expected " + origin_data + ", was " + backup_data + "\n"))


@pytest.mark.parametrize("table_name,column_name", [("Weapons", "weapon"), ("Hulls", "hull"), ("Engines", "engine")])
def test_ship_data(check_and_copy_database, table_name, column_name):
    size = get_tables_size("Ships")
    for i in range(size):
        origin_weapon = get_column(original_database_path, column_name, i)
        backup_weapon = get_column(backup_database_path, column_name, i)
        asserts_ships(origin_weapon, backup_weapon, i)

        origin_weapons = get_component(original_database_path, table_name, i)
        backup_weapons = get_component(backup_database_path, table_name, i)
        asserts_components(origin_weapons, backup_weapons)
