import argparse
import platform
import os
import mysql.connector
from nepc import nepc
from nepc.util import config

PARSER = argparse.ArgumentParser(description='Build the NEPC database.')
PARSER.add_argument('--debug', action='store_true',
                    help='print additional debug info')
ARGS = PARSER.parse_args()

if ARGS.debug:
    import time
    T0 = time.time()

# TODO: add threshold table
# TODO: add reference table

HOME = config.userHome()
NEPC_HOME = config.nepc_home()
NEPC_MYSQL = NEPC_HOME + "/mysql/"

MYDB = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

MYCURSOR = MYDB.cursor()

MYCURSOR.execute("DROP DATABASE IF EXISTS `nepc`;")
MYCURSOR.execute("CREATE DATABASE IF NOT EXISTS `nepc` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")

MYCURSOR.execute("SET default_storage_engine = INNODB;")

MYCURSOR.execute("use nepc;") #NEHA EDIT

MYCURSOR.execute("CREATE TABLE `nepc`.`species`("
                 "`id` INT UNSIGNED NOT NULL auto_increment ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

MYCURSOR.execute("CREATE TABLE `nepc`.`processes`( "
                 "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                 "`name` VARCHAR(40) NOT NULL, "
                 "`long_name` VARCHAR(240) NOT NULL, "
                 "`lhs` INT, "
                 "`rhs` INT, "
                 "`lhs_e` INT, "
                 "`rhs_e` INT, "
                 "`lhs_hv` INT, "
                 "`rhs_hv` INT, "
                 "`lhs_v` INT, "
                 "`rhs_v` INT, "
                 "`lhs_j` INT, "
                 "`rhs_j` INT, "
                 "PRIMARY KEY(`id`) "
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`states`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`specie_id` INT UNSIGNED NOT NULL ,"
                 "	`name` VARCHAR(100) NOT NULL ,"
                 "	`long_name` VARCHAR(100) NOT NULL ,"
                 "	`configuration` JSON NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `SPECIE_ID`(`specie_id` ASC) ,"
                 "	CONSTRAINT `specie_id_STATES` FOREIGN KEY(`specie_id`) "
                 "		REFERENCES `nepc`.`species`(`id`) "
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`models`("
                 "	`model_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`cs`("
                 "	`CS_ID` INT UNSIGNED NOT NULL, "
                 "	`specie_id` INT UNSIGNED NOT NULL, "
                 "	`process_id` INT UNSIGNED NOT NULL, "
                 "	`units_e` DOUBLE NOT NULL,"
                 "	`units_sigma` DOUBLE NOT NULL,"
                 "	`ref` VARCHAR(1000),"
                 "	`lhsA_id` INT UNSIGNED NULL ,"
                 "	`lhsB_id` INT UNSIGNED NULL ,"
                 "	`rhsA_id` INT UNSIGNED NULL ,"
                 "	`rhsB_id` INT UNSIGNED NULL ,"
                 "	`wavelength` DOUBLE NULL ,"
                 "	`lhs_v` INT NULL ,"
                 "	`rhs_v` INT NULL ,"
                 "	`lhs_j` INT NULL ,"
                 "	`rhs_j` INT NULL ,"
                 "	`background` VARCHAR(10000) ,"
                 "	`lpu` DOUBLE NULL ,"
                 "	`upu` DOUBLE NULL ,"
                 "	PRIMARY KEY(`CS_ID`) ,"
                 "	INDEX `SPECIE_ID`(`specie_id` ASC) ,"
                 "	INDEX `PROCESS_ID`(`process_id` ASC) ,"
                 "	CONSTRAINT `SPECIE_ID_CS` FOREIGN KEY(`specie_id`)"
                 "		REFERENCES `nepc`.`species`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `PROCESS_ID_CS` FOREIGN KEY(`process_id`)"
                 "		REFERENCES `nepc`.`processes`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `LHSA_ID_CS` FOREIGN KEY(`lhsA_id`)"
                 "		REFERENCES `nepc`.`states`(`id`),"
                 "	CONSTRAINT `LHSB_ID_CS` FOREIGN KEY(`lhsB_id`)"
                 "		REFERENCES `nepc`.`states`(`id`),"
                 "	CONSTRAINT `RHSA_ID_CS` FOREIGN KEY(`rhsA_id`)"
                 "		REFERENCES `nepc`.`states`(`id`),"
                 "	CONSTRAINT `RHSB_ID_CS` FOREIGN KEY(`rhsB_id`)"
                 "		REFERENCES `nepc`.`states`(`id`)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`csdata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`CS_ID` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `CS_ID`(`CS_ID` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`CS_ID`)"
                 "		REFERENCES `nepc`.`cs`(`CS_ID`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`models2cs`("
                 "	`CS_ID` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (CS_ID, model_id)"
                 ");"
                 )

#############
# Load data #
#############


def broad_cats():
    """Returns a list of the first three headers for the first three tables

    Returns
    -------
    A list of headers - processes, models, and species, for the first three tables
    of the NEPC database
    """
    return ["processes", "models", "species"]

def print_list_elems(lst):
    """Converts a list of elements into a string, with values separated by commas

    Parameters
    ----------
    lst : list
    A list of elements to be converted into a string

    Returns
    -------
    answer : str
    A string containing all of the elements of lst, separated by commas
    """
    answer = ''
    for val in lst:
        if val != lst[len(lst)-1]:
            answer = answer + val + ","
        else:
            answer = answer + val
    return answer

def met_headers():
    """Returns the headers for a metadata file
    Returns
    -------
    List containing the headers for a .met file

    """
    return ['@temp', '@specie', '@process', 'units_e', 'units_sigma',
            'ref', '@lhsA', '@lhsB', '@rhsA', '@rhsB', 'wavelength', 'lhs_v',
            'rhs_v', 'lhs_j', 'rhs_j', 'background', 'lpu', 'upu']

def dat_headers():
    """Returns the headers for a data file

    Returns
    -------
    List containing the headers of .dat file
    """
    return ['id', 'e', 'sigma']

def all_headers():
    """Returns a list containing both the headers for data and for metadata
    Returns
    -------
    total_heads : list
    List containing the combination of met_headers() and dat_headers()
    """
    total_heads = met_headers()
    for dat_elem in dat_headers():
        total_heads.append(dat_elem)
    return total_heads

def number_of_columns():
    """Return the number of columns in dat and met files
    Returns
    -------
    The length of all_headers(), the function that returns a list
    containing both the headers for data and metadata"""
    return len(all_headers())

def no_of_file_types():
    """Returns the number of file types covered by exCS

    Returns
    -------
    An integer representing the number of file types covered
    """
    return 2 #for dat and met

def construct_headers(column):
    """Returns the three headers used to construct the table
    
    Parameters
    ----------
    column : str
    A string representing the column name

    Returns
    -------
    A tuple containing the columns that will be used to construct the table
    """
    for metelem in met_headers():
        if column == metelem:
            return (met_file, "cs", column)
        else:
            continue
    return (dat_file, "csdata", column)

def multi_iteration(res):
    """Separate through each different mysql command given a generator object
    Parameters
    ----------
    res : a generator object that will be returned when using mycursor.execute (multi=True)"""
    for cur in res:
        print('cursor:', cur)
        if cur.with_rows:
            print('results:', cur.fetchall())

N_STATES = ["/n_states.tsv'", "/n+_states.tsv'", "/n++_states.tsv'"]
N2_STATES = ["/n2+_states.tsv'", "/n2_states.tsv'"]
BEG_EXEC = '' #beginning statement to execute, used to make code shorter + more readable
for i in broad_cats():
    BEG_EXEC = ('' + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL
                + i + ".tsv' " + "\nINTO TABLE " + "nepc." + i)
    if i == 'processes':
        BEG_EXEC = BEG_EXEC + " " + "\nIGNORE 2 LINES;"
    else:
        BEG_EXEC = BEG_EXEC + ";"
RESULTS = MYCURSOR.execute(BEG_EXEC, multi=True) #query created earlier executed
multi_iteration(RESULTS)
STATE_QUERY = ''
for i in N_STATES:
    STATE_QUERY = (STATE_QUERY + "LOAD DATA LOCAL INFILE '" +
                   NEPC_MYSQL + i + "    INTO TABLE nepc.states" +
                   "     IGNORE 1 LINES" +
                   "      (id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)" +
                   "      SET configuration = JSON_OBJECT(" +
                   "          JSON_OBJECT('order', " +
                   "              JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', " +
                   "              '3d', '4s', '4p')" + "              )," +
                   "          JSON_OBJECT('occupations'," +
                   "          JSON_OBJECT(" +
                   "				'2s',@2s," +
                   "				'2p',@2p," +
                   "				'CoreTerm',@CoreTerm," +
                   "				'3s',@3s," +
                   "				'3p',@3p," +
                   "				'3d',@3d," +
                   "				'4s',@4s," +
                   "				'4p',@4p" +
                   "			)" + "		)" +
                   "	)," +
                   "	specie_id = (select max(id) from nepc.species " +
                   "               where name = " + "'" +
                   i[1:i.index('_')].upper() + "'" + ");")
for i in N2_STATES:
    STATE_QUERY = (STATE_QUERY + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL +
                   i + "    INTO TABLE nepc.states" +
                   "     IGNORE 1 LINES" +
                   "      (id,name,long_name,@o1,@o2,@o3,@o4,@o5,@o6)" +
                   "      SET configuration = JSON_OBJECT(" +
                   "          JSON_OBJECT('order', " +
                   "              JSON_ARRAY('2sigma_u', " +
                   "'1pi_u', '1pi_g', '3sigma_u', '3ssigma_g')" +
                   "              )," +
                   "          JSON_OBJECT('occupations'," +
                   "          JSON_OBJECT(" +
                   "				'2sigma_u',@o1," +
                   "				'1pi_u',@o2," +
                   "				'3sigma_g',@o3," +
                   "				'1pi_g',@o4," +
                   "				'3sigma_u',@o5," +
                   "				'3ssigma_g',@o6" +
                   "			)" +
                   "		)" +
                   "	)," +
                   "	specie_id = (select max(id) from nepc.species " +
                   "               where name = " +
                   "'" + i[1:i.index('_')].upper() + "'" +
                   ");")
STATE_RESULTS = MYCURSOR.execute(STATE_QUERY, multi=True)
multi_iteration(STATE_RESULTS)
MYDB.commit()

DIR_NAMES = ["/data/formatted/n2/itikawa/",
             "/data/formatted/n2/zipf/",
             "/data/formatted/n/zatsarinny/"]


if platform.node() == 'ppdadamsonlinux':
    CS_DAT_FILENAME = "cs_datfile_prod.tsv"
else:
    CS_DAT_FILENAME = "cs_datfile_local.tsv"

F_CS_DAT_FILE = open(CS_DAT_FILENAME, 'w')
F_CS_DAT_FILE.write("\t".join(["CS_ID", "filename"]) + "\n")

CS_ID = 1
for directoryname in DIR_NAMES:
    directory = os.fsencode(NEPC_HOME + directoryname)

    # TODO: speed up by reading data into memory and using the
    #       MySQLCursor.executemany() method
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename_wo_ext = filename.rsplit(".", 1)[0]
        mod_file = "".join([os.fsdecode(directory),
                            filename_wo_ext,
                            ".mod"])
        met_file = "".join([os.fsdecode(directory),
                            filename_wo_ext,
                            ".met"])
        dat_file = "".join([os.fsdecode(directory),
                            filename_wo_ext,
                            ".dat"])
        if filename.endswith(".met") or filename.endswith(".mod"):
            continue
        else:
            F_CS_DAT_FILE.write(
                "\t".join([str(CS_ID), directoryname + str(filename_wo_ext)]) + "\n")

                        #lists types of files - a list of lists will be used
            filetype = [met_file, dat_file]
            tn = ['cs', 'csdata']
            exCS = ''
            for i in range(0, no_of_file_types()):
                exCS = exCS + ("LOAD DATA LOCAL INFILE '" + filetype[i] +
                               "' INTO TABLE  " + "nepc." + tn[i] +
                               " IGNORE 1 LINES ")
                if filetype[i] == met_file:
                    exCS = (exCS + "(" + print_list_elems(met_headers()) + ") " +
                            "SET CS_ID = " + str(CS_ID) + ", ")
                    atSign = []
                    for head in met_headers():
                        if ('@' in head and head != '@temp'):
                            atSign.append(head)
                        if (not atSign and head == met_headers()[1]): #disregards @temp here
                            exCS = exCS + ";"
                    for ind in range(0, len(atSign)):
                        if (atSign[ind] == '@lhsA' or atSign[ind] == '@rhsA'
                                or atSign[ind] == '@lhsB' or atSign[ind] == '@rhsB'):
                            exCS = (exCS + atSign[ind][1:] +
                                    "_id = (select id from nepc.states  where name LIKE " +
                                    atSign[ind] + ")")
                            if ind != len(atSign) - 1:
                                exCS = exCS + ", "
                            else:
                                exCS = exCS + ";"
                        elif atSign[ind] == '@process':
                            exCS = (exCS + atSign[ind][1:] +
                                    "_id = (select id from nepc." +
                                    atSign[ind][1:] + "es" + "  where name = " +
                                    atSign[ind]+ ")")
                            if ind != len(atSign) - 1:
                                exCS = exCS + ", "
                                #MYCURSOR.execute("print n 'process_id'")
                            else:
                                exCS = exCS + ";"

                        elif atSign[ind] != '@specie':
                            exCS = (exCS + atSign[ind][1:] +
                                    "_id = (select id from nepc." +
                                    atSign[ind][1:] + "  where name = " +
                                    atSign[ind]+ ")")
                            if ind != len(atSign) - 1:
                                exCS = exCS + ", "
                            else:
                                exCS = exCS + ";"
                        else:
                            exCS = (exCS + atSign[ind][1:] +
                                    "_id = (select id from nepc." +
                                    atSign[ind][1:] + "s"
                                    + " where name = " + atSign[ind] + ")")
                            if ind != (len(atSign) - 1):
                                exCS = exCS + ", "
                            else:
                                exCS = exCS + ";"
                else:
                    exCS = (exCS + "(" + print_list_elems(dat_headers()) + ") "
                            "SET CS_ID = " + str(CS_ID) + "; ")
                resu = MYCURSOR.execute(exCS, multi=True)
                multi_iteration(resu)
                MYDB.commit()

        executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + mod_file +
                               "' INTO TABLE nepc.models2cs "
                               "(@model) "
                               "SET CS_ID = " + str(CS_ID) + ", "
                               "model_id = (select model_id "
                               "            from nepc.models "
                               "            where name LIKE @model);")

        if os.path.exists(mod_file):
            MYCURSOR.execute(executeTextCSMODELS)
        CS_ID = CS_ID + 1

F_CS_DAT_FILE.close()

MYDB.commit()

def table_exists(tablename):
    """Checks whether a table exists in the NEPC database

    Parameters
    ----------
    tablename : str
        The name of the table in NEPC
    Returns
    -------
    True or False value : boolean
        Boolean value of True or False depending on the existence of the table
        in the NEPC database
    """
    MYCURSOR.execute("""
        SELECT count(*)
        FROM information_schema.TABLES
        WHERE table_name = """ + "'" + tablename + "'")
    if MYCURSOR.fetchone()[0] == 1:
        return True
    return False


def contents_of_db():
    """Prints out the number of rows in each table of the NEPC database"""
    for table in ["species", "processes", "states", "cs", "models", "models2cs", "csdata"]:
        print(table + " has " + str(nepc.count_table_rows(MYCURSOR, table)) + " lines")
        print("===============================================\n")



if ARGS.debug:
    T1 = time.time()
    ELAPSED = T1-T0
    print("\nBuilt NEPC database in " + str(round(ELAPSED, 2)) + " sec:\n"
          "===============================================")
else:
    print("\nBuilt NEPC database:\n")

contents_of_db()

MYCURSOR.close()

MYDB.close()
