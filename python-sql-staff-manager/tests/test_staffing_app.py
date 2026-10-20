"""Exercise the real CLI with fictional records in temporary databases."""

import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


class StaffManagerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.workdir = Path(self.directory.name)
        shutil.copyfile(PROJECT / "staffing_app.py", self.workdir / "staffing_app.py")

    def run_cli(self, *answers):
        result = subprocess.run(
            [sys.executable, str(self.workdir / "staffing_app.py")],
            input="\n".join(answers) + "\n",
            text=True,
            capture_output=True,
            cwd=self.workdir,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def rows(self):
        with sqlite3.connect(self.workdir / "staffing.db") as connection:
            return connection.execute(
                "SELECT first_name, last_name, position, email, hourly_rate "
                "FROM employees ORDER BY id"
            ).fetchall()

    def add_alex(self):
        return self.run_cli(
            "1", "Alex", "Rivera", "Support Specialist",
            "alex.rivera@example.com", "24.50", "6",
        )

    def test_employee_lifecycle_and_persistence(self):
        self.assertIn("Employee saved.", self.add_alex())
        output = self.run_cli("2", "3", "Rivera", "4", "1", "Team Lead", "28", "6")
        self.assertGreaterEqual(output.count("Name: Alex Rivera"), 2)
        self.assertIn("Update successful.", output)
        self.assertEqual(self.rows(), [
            ("Alex", "Rivera", "Team Lead", "alex.rivera@example.com", 28.0)
        ])
        self.assertIn("Hourly rate: 28.00", self.run_cli("2", "6"))
        output = self.run_cli("5", "1", "2", "6")
        self.assertIn("Employee deleted.", output)
        self.assertIn("No employees found.", output)
        self.assertEqual(self.rows(), [])

    def test_duplicate_email_and_invalid_rate_do_not_change_records(self):
        self.add_alex()
        output = self.run_cli(
            "1", "Taylor", "Reed", "Analyst", "alex.rivera@example.com", "30",
            "1", "Morgan", "Lee", "Analyst", "morgan.lee@example.com", "invalid",
            "4", "1", "Changed", "invalid", "6",
        )
        self.assertIn("Email is already in use.", output)
        self.assertEqual(output.count("Hourly rate must be a number."), 2)
        self.assertEqual(self.rows(), [
            ("Alex", "Rivera", "Support Specialist", "alex.rivera@example.com", 24.5)
        ])

    def test_parameterized_names_and_missing_records(self):
        output = self.run_cli(
            "1", "Sam", "O'Neil", "Developer", "sam.oneil@example.com", "25",
            "3", "O'Neil", "3", "Missing", "4", "999", "Lead", "30",
            "5", "999", "invalid", "6",
        )
        self.assertIn("Name: Sam O'Neil", output)
        self.assertIn("No employee found.", output)
        self.assertEqual(output.count("No employee found with that ID."), 2)
        self.assertIn("Enter a valid choice.", output)
        self.assertEqual(self.rows()[0][1], "O'Neil")


if __name__ == "__main__":
    unittest.main()
