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
# current.execute(drop_table)
# current.execute(create_table)

insert_into = 'INSERT INTO Phonebook VALUES(%s, %s, %s);'
delete = 'DELETE FROM Phonebook WHERE person_name = %s;'
update = 'UPDATE Phonebook SET phone_number = %s WHERE person_name = %s'

# try:
#     with open("PhoneBook.csv", 'r') as f:
#         reader = csv.reader(f, delimiter=",")
#         for row in reader:
#             current.execute(insert_into, row)
# except Exception as e:
#     name = input("Enter the name: ")
#     phone_number = input("Enter the number: ")
#     city = input("Enter the city: ")
#     current.execute(insert_into, (name, phone_number, city))

mode = int(input("What you want to do?\nMode 1 - Delete name from PhoneBook.\nMode 2 - Update number.\nMode 3 - Add new contact.\nMode 4 - Show PhoneBook.\n"))
# mode = 1 - Delete name.
# mode = 2 - Update number.
# mode = 3 - Add new user.
# mode = 4 - Show phonebook.

if mode == 1:
    delete_name = input("Which name you want to delete: ")
    current.execute(delete, (delete_name,))
    print("Success.")
elif mode == 2:
    update_name = input("Whose phone number you want to update: ")
    phone_number = input("Enter new number: ")
    current.execute(update, (phone_number, update_name))
    print("Success.")
elif mode == 3:
    insert_name = input("Whose name do you want to add?\n")
    insert_number = input(f"Please, insert {insert_name}'s phone number : ")
    insert_city = input(f"Please, insert {insert_name}'s city : ")
    current.execute(insert_into, (insert_name, insert_number, insert_city))
    print("Success.")
elif mode == 4 :
    get = '''
        SELECT * from phonebook;
    '''
    current.execute(get)
    output = current.fetchall()
    print(*output, sep='\n')
else:
    print("Error.")

current.close()
config.commit()
config.close()