import psycopg2
import csv
from config import params

config = psycopg2.connect(**params)
current = config.cursor()

drop_table = '''
    DROP TABLE Phonebook;
'''

create_table = '''
    CREATE TABLE Phonebook(
        person_name VARCHAR(255),
        phone_number VARCHAR(32),
        city VARCHAR(32)
    );
'''
current.execute(drop_table)
current.execute(create_table)

insert_into = 'INSERT INTO Phonebook VALUES(%s, %s, %s);'
delete = 'DELETE FROM Phonebook WHERE person_name = %s;'
update = 'UPDATE Phonebook SET phone_number = %s WHERE person_name = %s'

mode = int(input("What you want to do?\nMode 1 - Add name number, city.\nMode 2 - Delete name from PhoneBook.\nMode 3 - Update number.\n"))
# mode = 1 - Add name, number, city
# mode = 2 - Delete name
# mode = 3 - Update number

if mode == 1:
    try:
        with open("PhoneBook.csv", 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                current.execute(insert_into, row)
    except Exception as e:
        name = input("Enter the name: ")
        phone_number = input("Enter the number: ")
        city = input("Enter the city: ")
        current.execute(insert_into, (name, phone_number, city))
    print("Success.")

elif mode == 2:
    delete_name = input("Which name you want to delete: ")
    current.execute(delete, (delete_name,))

elif mode == 3:
    update_name = input("Whose phone number you want to update: ")
    current.execute(update, (update_name,))
else:
    print("Error.")

current.close()
config.commit()
config.close()