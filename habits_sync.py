#!/usr/bin/python3

#imports
import sqlite3
import sys

#functions
def extract_habits_from_db(database):
    #connect to db
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    #pull habit names and ids from the Habits table
    cursor.execute("SELECT id, name FROM Habits")
    habits_data = cursor.fetchall()

    #map to dict
    habits_dict = {habit_id: habit_name for habit_id, habit_name in habits_data}

    #extract repetitions data
    cursor.execute("SELECT habit, timestamp, value FROM Repetitions")
    rep_data = cursor.fetchall()

    #remap habit names from id
    rep_with_names = [
        (habits_dict.get(habit_id, "Unknown").replace(" ","_").lower(), timestamp, value)
        for habit_id, timestamp, value in rep_data
    ]
    return rep_with_names

def push_formated_sequence(data):
# data format is an array of tupple
    sequence = []
    for habit in data:
        sequence.append(f"habit,people=rqz {habit[0]}={habit[2]} {habit[1]*1000000000}")
    
    print(sequence)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: this python scrit only use a database path as the unique argument.")
    else:
        print(extract_habits_from_db(sys.argv[1]))
        print(push_formated_sequence(extract_habits_from_db(sys.argv[1])))
