"""Employee management CLI using Python and a local SQLite database."""

import sqlite3
conn = sqlite3.connect("staffing.db") # Open the local database, creating it on the first run.
cursor = conn.cursor() # Execute parameterized SQL through this cursor.
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  position TEXT NOT NULL,
  email TEXT UNIQUE,
  hourly_rate REAL NOT NULL
)

""")
# SQLite assigns a unique, increasing employee ID.
# Required fields use NOT NULL; email addresses must be unique.
conn.commit()


def add_employee():
  first_name = input("First name: ")
  last_name = input("Last name: ")
  position = input("Position: ")
  email = input("Email: ")

  try: # Keep the menu running when the rate is not a number.
    hourly_rate = float(input("Hourly rate: "))
  except ValueError:
      print("Hourly rate must be a number.")
      return
  try:
    cursor.execute( # Bind values separately from the SQL statement.
    "INSERT INTO employees (first_name, last_name, position, email, hourly_rate) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, position, email, hourly_rate)
)
    conn.commit() # Persist the new record.
    print("Employee saved.")
  except sqlite3.IntegrityError:
    print("Email is already in use.") # The UNIQUE constraint prevents duplicate emails.

def view_employee():
  cursor.execute("SELECT * FROM employees") # Read all employee records.
  employees = cursor.fetchall()
  if not employees:
    print("No employees found.")
  for employee in employees: # Display one record per line.
    print(
      f"ID: {employee[0]} | "
      f"Name: {employee[1]} {employee[2]} | "
      f"Position: {employee[3]} | "
      f"Email: {employee[4]} | "
      f"Hourly rate: {employee[5]:.2f}" # Display rates to two decimal places.
    )
def search_employee():
  search_name = input("Employee last name: ")
  cursor.execute("SELECT * FROM employees WHERE last_name = ?", # Find an exact last-name match.
                (search_name,)
                )
  results = cursor.fetchall()
  if results: # Display all matching records.
    for employee in results: # Display the results.
      print(
        f"ID: {employee[0]} | "
        f"Name: {employee[1]} {employee[2]} | "
        f"Position: {employee[3]} | "
        f"Email: {employee[4]} | "
        f"Hourly rate: {employee[5]:.2f} "
          )
  else:
    print("No employee found.")

def update_employee(): # Update a record by ID.
  employee_id = input("Employee ID to update: ") # Identify the employee to update.
  new_position = input("New position: ")
  try:
    new_hourly_rate = float(input("New hourly rate: "))
  except ValueError:
    print("Hourly rate must be a number.")
    return
  cursor.execute( # Update only the employee with the requested ID.
    'UPDATE employees SET position = ?, hourly_rate = ? WHERE id = ?', (new_position,new_hourly_rate, employee_id)
  )
  conn.commit()


  if cursor.rowcount > 0: # Report whether an employee matched the ID.
    print("Update successful.")
  else:
    print("No employee found with that ID.")


def delete_employee(): # Delete one employee by ID.
  employee_id = input("Employee ID to delete: ")
  cursor.execute(
    "DELETE FROM employees WHERE id = ?",
    (employee_id,)
  )
  conn.commit()
  if cursor.rowcount > 0:
    print("Employee deleted.")
  else:
    print("No employee found with that ID.")


def main():
  while True: # Return to the menu after each operation.
    print("Staff Management System")
    print("1. Add employee")
    print("2. View employees")
    print("3. Search employees")
    print("4. Update employee")
    print("5. Delete employee")
    print("6. Exit")


    choice = input("Choose an option: ") # Read the menu selection.
    if choice == "1":
      add_employee()
    elif choice == "2":
      view_employee()
    elif choice == "3":
      search_employee()
    elif choice == "4":
      update_employee()
    elif choice == "5":
      delete_employee()
    elif choice == "6":
      break # Exit the menu.
    else:
      print("Enter a valid choice.")

  conn.close()

if __name__ == "__main__":
  main()

