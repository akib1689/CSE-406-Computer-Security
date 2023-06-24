# file that interacts with the user data

# import the necessary packages
import csv
import os.path

# define the class


class UserModel:
    # file path to the user data
    file_path = None

    def __init__(self):
        """
        this is the constructor of the UserModel class
        """
        self.file_path = "public/user_data.csv"

    # read the csv
    def read_csv(self):
        """
        this method reads the csv file
        caller should handle the exception of not existing file
        """
        records = []
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
        return records

    # write the csv

    def write_csv(self, records):
        """
        this method writes the csv file
        caller should handle the exception of not existing file
        """
        fieldnames = records[0].keys() if records else []
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    # insert a record

    def insert_record(self, record):
        """
        this method inserts a record to the csv file
        caller should handle the exception of not existing file
        returns the inserted record
                -1 if the record already exists
        """
        # create the file if not exists
        if not os.path.exists(self.file_path):
            open(self.file_path, "w+").close()

        records = self.read_csv()
        for r in records:
            if r["username"] == record["username"]:
                return -1
        records.append(record)
        self.write_csv(records)
        return record

    # get a record by username
    def get_record_by_username(self, username):
        """
        this method gets a record by username
        caller should handle the exception of not existing file
        returns the record if exists
                -1 if the record does not exist
        """
        records = self.read_csv()
        for r in records:
            if r["username"] == username:
                return r
        return -1
