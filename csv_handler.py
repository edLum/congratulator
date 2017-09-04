import csv, codecs, cStringIO

# Define pythonas csv dialect
csv.register_dialect('pythonas_dialect', delimiter=',', quoting=csv.QUOTE_NONE)

class csvHandler:
    """Handling csv files."""
    def __init__(self, csv_file=None):
        self.csv_file = csv_file

    def read_from_file(self):
        """Read csv and return a list with its contents."""
        csv_to_list = []
        with open(self.csv_file, 'rb') as f:
           reader = csv.reader(f, 'pythonas_dialect')
           for row in reader:
               csv_to_list.append(row)
        return csv_to_list
    
    def write_to_file(self, list_to_csv):
        """Write from list to csv."""
        with open(self.csv_file, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(list_to_csv)

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
