"""
Module for Class class (for Gems of War Data)
"""

import gow_common

class Class:
    """
    Class class to hold data about Gems of War Classes
    """
    def __init__(self, name, kingdom, traitcount, level, sublevel):
        self._vals = {}
        self._vals['name'] = name
        self._vals['traitcount'] = traitcount
        self._vals['level'] = level
        self._vals['sublevel'] = sublevel
        self._vals['kingdom'] = ""

        # Classes all belong to Kingdoms proper, so if we can't find it something is wrong
        if gow_common.is_kingdom(kingdom):
            self._vals['kingdom'] = kingdom
        else:
            print("Error: Couldn't find kingdom:", kingdom)

    @classmethod
    def gen_class_from_json(cls, json_record):
        """
        Alternate constructor.  Allows you pass in a json_record, and it'll parse all the data out

        :param json_record: The json record (from gowdb inventory)
        :return:            The constructed Class object
        """
        if 'traitCount' not in json_record:
            json_record['traitCount'] = 0
        if 'level' not in json_record:
            json_record['level'] = 1

        self = cls(name=json_record['name'],
                   kingdom=json_record['kingdomName'],
                   traitcount=json_record['traitCount'],
                   level=json_record['level'],
                   sublevel=json_record['subLevel'])
        return self

    @staticmethod
    def get_csv_header():
        """
        Returns a string which can be written to a csv file (creates a header row)
        """
        return "Name,Level,Traits,Kingdom,Sublevel"

    def get_csv_record(self):
        """
        Returns a string which can be written to a csv file (creates a row for this class)
        """
        return self._vals['name'] + "," + str(self._vals['level']) + ","\
               + str(self._vals['traitcount']) + ","\
               + self._vals['kingdom'] + "," + str(self._vals['sublevel'])

    def print(self):
        """
        Prints Class information
        """
        # TODO Add a better print function
        print(self._vals['name'])

    @staticmethod
    def print_class_csv(csv_file_name, class_array):
        """
        Helper function to create a full csv file with class information

        :param csv_file_name: filename for the csv file
        :param class_array:   array of classes to print
        """
        with open(csv_file_name, "w") as csv_file:
            csv_file.write(Class.get_csv_header())
            csv_file.write("\n")
            for gow_class in class_array:
                csv_file.write(gow_class.get_csv_record())
                csv_file.write("\n")

    def get_kingdom(self):
        """
        Retrieve the kingdom for this class
        """
        return self._vals['kingdom']

    def get_traitcount(self):
        """
        Retrieve the trait count for this class
        """
        return self._vals['traitcount']
