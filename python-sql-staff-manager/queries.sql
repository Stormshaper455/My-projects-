-- Run after schema.sql in a fresh, in-memory SQLite session.
-- All values are fictional. ROLLBACK leaves the database unchanged.
BEGIN TRANSACTION;

-- CREATE: add an employee.
INSERT INTO employees (first_name, last_name, position, email, hourly_rate)
VALUES ('Alex', 'Rivera', 'Support Specialist', 'alex.rivera@example.com', 24.50);

-- READ: list employees and find an exact last-name match.
SELECT id, first_name, last_name, position, email, hourly_rate
FROM employees
ORDER BY id;

SELECT id, first_name, last_name, position, email, hourly_rate
FROM employees
WHERE last_name = 'Rivera';

-- UPDATE: change the example employee's role and pay.
UPDATE employees
SET position = 'Team Lead', hourly_rate = 28.00
WHERE email = 'alex.rivera@example.com';

SELECT first_name, last_name, position, hourly_rate
FROM employees
WHERE email = 'alex.rivera@example.com';

-- DELETE: remove the example employee.
DELETE FROM employees
WHERE email = 'alex.rivera@example.com';

ROLLBACK;
