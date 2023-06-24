# this file handles the message csv

import csv
import os.path


class MessageModel:

    # file path
    file_path = None

    def __init__(self):
        """
        this is the constructor of the MessageModel class
        """
        self.file_path = "public/message_data.csv"

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
        """
        # check if the file exists
        if not os.path.isfile(self.file_path):
            # create the file
            file = open(self.file_path, "w+")
            # write the header
            writer = csv.DictWriter(file, fieldnames=record.keys())
            writer.writeheader()
            # close the file
            file.close()
        # open the file in append mode, create if not exists
        file = open(self.file_path, "a+")

        # insert the record to the file
        writer = csv.DictWriter(file, fieldnames=record.keys())
        writer.writerow(record)

        # close the file
        file.close()

    # get a record by sender
    def get_record_by_sender(self, sender):
        """
        this method returns a record by sender
        """
        records = self.read_csv()
        for r in records:
            if r["sender"] == sender:
                return r
        return -1

    # get a record by receiver
    def get_record_by_receiver(self, receiver):
        """
        this method returns a record by receiver
        """
        records = self.read_csv()
        for r in records:
            if r["receiver"] == receiver:
                return r
        return -1

    # get a record by sender and receiver
    def get_record_by_sender_and_receiver(self, sender, receiver):
        """
        this method returns a record by sender and receiver
        """
        records = self.read_csv()
        returned_record = []
        for r in records:
            if r["sender"] == sender and r["receiver"] == receiver:
                # add the record to the returned record\
                returned_record.append(r)

        # return the returned record
        return returned_record

    # get a record by sender or receiver
    def get_record_by_sender_or_receiver(self, sender, receiver):
        """
        this method returns a record by sender or receiver
        """
        records = self.read_csv()
        returned_record = []

        for r in records:
            if r["sender"] == sender or r["receiver"] == receiver:
                # add the record to the returned record
                returned_record.append(r)

        # return the returned record
        return returned_record
