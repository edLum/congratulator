from db_conn import engine
import sqlalchemy

class SqlExecutioner:
    def __init__(self, engine=None):
        self.engine = engine
    
    def connect_to_db(self):
        self.conn = self.engine.connect()

    def close_connection(self):
        self.conn.close()

    def run(self, query):
        self.connect_to_db()
        self.conn.execute(query)
        self.close_connection()
        return True

    def get_query_results(self, query):
        self.connect_to_db()
        results = []
        for row in self.conn.execute(query):
            results.append(list(row))
        self.close_connection()
        return results


QUERIES = {'ins_answers': ("INSERT INTO `tfrresultsfull`( `supporter_id`, `operator_id`, `program`, `date`, " 
                                   "`answer`, `answer_comments`) "
                                   "SELECT `supporter_id`, `operator_id`, `program`, `date`, "
                                   "`answer`, `comments` "
                                   "FROM  `tfranswers`;"),

           'ins_contact_changes': ("INSERT INTO `tfrresultsfull`(`supporter_id`, `operator_id`, `program`, " 
                                   "`date`, `phone1`, `phone2`, `phone3`, `email`, `address`, `city`, `postal`, " 
                                   "`name`, `surname`, `contant_comment`) "
                                   "SELECT `supporter_id`, `operator_id`, `program`, `date_added`, `phone1`, "
                                   "`phone2`, `phone3`, `email`, `address`, `city`, `postal`, `name`, `surname`, "
                                   "`comment` "
                                   "FROM  `tfrcontactchanges`;"),

           'ins_finance_changes': ("INSERT INTO `tfrresultsfull`(`supporter_id`, `operator_id`, `program`, " 
                                   "`date`, `amount`, `frequency`, `card_type`, `expire`, `card_number`, " 
                                   "`card_cvv`, `bank`, `iban`, `finance_comment`) "
                                   "SELECT `supporter_id`, `operator_id`, `program`, `datetime`, `amount`, " 
                                   "`frequency`, `card_type`,`expire`, `card_number`, `card_cvv`, `bank`, "
                                   "`iban`, `comment` " 
                                   "FROM  `tfrfinancechanges`;"),

           'changes_select_all': ("SELECT c.supname, t. * "
                                  "FROM tfrresultsfull AS t "
                                  "LEFT JOIN constituents AS c ON t.supporter_id = c.lookupid "
                                  "ORDER BY `t`.`program` ASC, t.supporter_id ASC;"),

           'changes_backup': ("INSERT INTO `tfrresultsfull_Backup`(`fullresult_id`, `supporter_id`, "
                              "`operator_id`, `program`, `date`, `answer`, `answer_comments`, `phone1`, "
                              "`phone2`, `phone3`, `email`, `address`, `city`, `postal`, `name`, `surname`, "
                              "`contant_comment`, `amount`, `frequency`, `card_type`, `expire`, `card_number`, "
                              "`card_cvv`, `bank`, `iban`, `finance_comment`) "
                              "SELECT `fullresult_id`, `supporter_id`, `operator_id`, `program`, `date`, "
                              "`answer`, `answer_comments`, `phone1`, `phone2`, `phone3`, `email`, `address`, "
                              "`city`, `postal`, `name`, `surname`, `contant_comment`, `amount`, `frequency`, "
                              "`card_type`, `expire`, `card_number`, `card_cvv`, `bank`, `iban`, "
                              "`finance_comment` " 
                              "FROM `tfrresultsfull` "
                              "ORDER BY `supporter_id`;"),
                                 
           'changes_truncate': ("DELETE FROM  `tfrresultsfull`;"
                                "DELETE FROM `tfranswers`;"
                                "DELETE FROM  `tfrcontactchanges`;"
                                "DELETE FROM`tfrfinancechanges`;"),
                
           'interactions_select_all': ("SELECT * FROM tfrresults;"),

           'interactions_backup': ("INSERT INTO `tfrresults_Backup`(`Constituent Lookup ID`, `Constituent Name`, "
                                   "`Summary`, `Status`, `Contact Method`, `Category`, `Subcategory`, `Expected Date`, "
                                   "`Actual Date`, `Comment`, `RG Increase/Decrease Amount`, `RG New Frequency`, "
                                   "`One off Donation`, `Number of Calls`, `Owner`) "
                                   "SELECT `Constituent Lookup ID`, `Constituent Name`, `Summary`, `Status`, "
                                   "`Contact Method`, `Category`, `Subcategory`, `Expected Date`, `Actual Date`, "
                                   "`Comment`, `RG Increase/Decrease Amount`, `RG New Frequency`, `One off Donation`, "
                                   "`Number of Calls`, `Owner` "
                                   "FROM `tfrresults`;"),

           'interactions_truncate': ("DELETE FROM `tfrresults`;"),
           }



