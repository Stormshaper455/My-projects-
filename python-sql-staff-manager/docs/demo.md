# Try the employee workflow

Run `python3 staffing_app.py` from the project directory. These examples assume a new, empty database. All names and contact details below are fictional.

## 1. Add a record

Choose **1** and enter:

```text
First name: Alex
Last name: Rivera
Position: Support Specialist
Email: alex.rivera@example.com
Hourly rate: 24.50
Employee saved.
```

## 2. View and search

Choose **2** to list the record:

```text
ID: 1 | Name: Alex Rivera | Position: Support Specialist | Email: alex.rivera@example.com | Hourly rate: 24.50
```

Choose **3**, then enter `Rivera` to find it by last name. Search uses an exact match.

## 3. Update the employee

Choose **4** and enter the ID shown by option 2:

```text
Employee ID to update: 1
New position: Team Lead
New hourly rate: 28
Update successful.
```

Choose **2** again:

```text
ID: 1 | Name: Alex Rivera | Position: Team Lead | Email: alex.rivera@example.com | Hourly rate: 28.00
```

## 4. Check persistence

Choose **6** to exit, run the app again from the same directory, and choose **2**. The updated record is still there because SQLite saves it in `staffing.db`.

## 5. Delete the record

Choose **5** and enter `1`. The app reports `Employee deleted.` Choose **2** to confirm that it reports `No employees found.`

Deleting a record takes effect immediately. Use fictional data when trying the demo.
