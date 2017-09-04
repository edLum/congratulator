import csv, logging
from time import strftime, localtime

from db_conn import engine
from csv_handler import UnicodeWriter
from sql_interface import QUERIES, TABLE_HEADERS, SqlExecutioner


class Exporter:
    """Abstraction of exporter, to be inherited by actual exporters."""
    def __init__(self):
        self.executioner = SqlExecutioner(engine)

    def select_all(self, query):
        """Select all rows to be exported using query."""
        return self.executioner.get_query_results(query)
    
    def backup(self, query):
        """Backup the table to be exported, using query."""
        print("Running backup queries...\n")
        self.executioner.run(query)
        print("Done.\n")

    def truncate(self, query):
        """Truncate tables involved in export after backup, using query."""
        print("Running truncate queries...\n")
        self.executioner.run(query)
        print("Done.\n")

class InteractionsExporter(Exporter):
    queries = {'select_all': QUERIES['interactions_select_all'],
               'backup': QUERIES['interactions_backup'],     
               'truncate': QUERIES['interactions_truncate'],
              } 

    table_header = TABLE_HEADERS['tfrresults']
    
    def __init__(self):
        Exporter.__init__(self)
        self.queries = InteractionsExporter.queries
        self.filename  = "tfr-interactions-" + strftime("%Y%m%d", localtime()) + ".csv"


    def generate_export(self):
        """Generate TFR interactions export as a list of table rows."""
        self.backup(self.queries['backup'])
        export_list = self.select_all(self.queries['select_all'])
        self.truncate(self.queries['truncate'])
        # insert table header
        export_list.insert(0, self.table_header)

        return export_list
     
    def create_interactions_csv(self):
        """Create the csv containging the tfr changes."""
        changes_list = self.generate_export()
        c = CsvCreator(changes_list, self.filename)
        c.create_csv()   


class ChangesExporter(Exporter):
    queries = {'select_all': QUERIES['changes_select_all'],
               'backup': QUERIES['changes_backup'],
               'truncate': QUERIES['changes_truncate'],
               'ins_answers': QUERIES['ins_answers'],
               'ins_contact': QUERIES['ins_contact_changes'],
               'ins_finance': QUERIES['ins_finance_changes'],
              }

    table_header = TABLE_HEADERS['tfrresultsfull']

    def __init__(self):
        Exporter.__init__(self)
        self.queries = ChangesExporter.queries
        self.filename  = "tfr-changes-" + strftime("%Y%m%d", localtime()) + ".csv"

    def initialization_queries(self):
        print("Running initialization queries...\n")
        self.executioner.run(self.queries['ins_answers'])
        self.executioner.run(self.queries['ins_contact'])
        self.executioner.run(self.queries['ins_finance'])
        print("Done.\n")
    
    def generate_export(self):
        """Generate TFR changes export as a list of table rows."""
        self.initialization_queries()
        self.backup(self.queries['backup'])
        export_list = self.select_all(self.queries['select_all'])
        self.truncate(self.queries['truncate'])
        # insert table header
        export_list.insert(0, self.table_header)
        return export_list
    
    def create_changes_csv(self):
        """Create the csv containging the tfr changes."""
        changes_list = self.generate_export()
        c = CsvCreator(changes_list, self.filename)
        c.create_csv()


# TODO: This shit needs fixing
class CsvCreator:

    def __init__(self, export_list, filename):
        self.export_list = export_list
        self.csv_filename = filename

    def convert_to_utf(self, list_to_convert):
        """Convert all non utf-8 fields of a results list to utf-8."""
        converted_list = []
        for result in list_to_convert:
            result = [field if isinstance(field, unicode) else str(field).decode('utf-8') for field in result]
            converted_list.append(result)
        return converted_list
    
    def create_csv(self):
        """Write to given csv filename some_list."""
        export_list = self.convert_to_utf(self.export_list)
        with open(self.csv_filename, 'wb') as csvfile:
            u = UnicodeWriter(csvfile, quoting=csv.QUOTE_ALL)
            u.writerows(export_list)

