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
                 "`id` INT UNSIGNED NOT NULL ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

MYCURSOR.execute("CREATE TABLE `nepc`.`processes`( "
                 "`id` INT UNSIGNED NOT NULL , "
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

MYCURSOR.execute("CREATE TABLE `nepc`.`states`( "
                 "`id` INT UNSIGNED NOT NULL, "
                 "`specie_id` INT UNSIGNED NOT NULL, "
                 "`name` VARCHAR(100) NOT NULL, "
                 "`long_name` VARCHAR(100) NOT NULL, "
                 "`configuration` JSON NOT NULL, "
                 "PRIMARY KEY(`id`), "
                 "INDEX `SPECIE_ID`(`specie_id` ASC), "
                 "CONSTRAINT `specie_id_STATES` FOREIGN KEY(`specie_id`) "
                 "REFERENCES `nepc`.`species`(`id`) "
                 "ON DELETE RESTRICT ON UPDATE CASCADE "
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`models`("
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`cs`("
                 "	`CS_ID` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
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
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `cs_id`(`cs_id` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`cs_id`)"
                 "		REFERENCES `nepc`.`cs`(`cs_id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `nepc`.`models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
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
    tup : tuple
    A tuple containing the columns that will be used to construct the table
    """
    for metelem in met_headers():
        if column == metelem:
            tup = (met_file, "cs", column)
        else:
            tup = (dat_file, "csdata", column)
    return tup

def multi_iteration(res):
    """Separate through each different mysql command given a generator object
    Parameters
    ----------
    res : a generator object that will be returned when using MYCURSOR.execute (multi=True)"""
    for cur in res:
        print('cursor:', cur)
        if cur.with_rows:
            print('results:', cur.fetchall())

"""
BEG_EXEC = ''
for i in broad_cats():
    BEG_EXEC = ('' + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL
                + i + ".tsv' " + "\nINTO TABLE " + "nepc." + i)
    if i == 'processes':
        BEG_EXEC = BEG_EXEC + " " + "\nIGNORE 2 LINES;"
    else:
        BEG_EXEC = BEG_EXEC + ";"
print(BEG_EXEC)
RESULTS = MYCURSOR.execute(BEG_EXEC, multi=True)
multi_iteration(RESULTS)
"""

MYCURSOR.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/processes.tsv' "
                 "INTO TABLE nepc.processes "
                 "IGNORE 2 LINES;")

if ARGS.debug:
    print("processes:")
    print(nepc.table_as_df(MYCURSOR, "processes"))

MYCURSOR.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/models.tsv' "
                 "INTO TABLE nepc.models;")

if ARGS.debug:
    print("models:")
    print(nepc.table_as_df(MYCURSOR, "models"))

MYCURSOR.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/species.tsv' "
                 "INTO TABLE nepc.species "
                 "IGNORE 1 LINES;")

if ARGS.debug:
    print("species:")
    print(nepc.table_as_df(MYCURSOR, "species"))

MYDB.commit()

MYCURSOR.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/states.tsv' "
                 "INTO TABLE nepc.states "
                 "IGNORE 1 LINES "
                 "(id,@specie,name,long_name) "
                 "set specie_id = (select max(id) from nepc.species where name like @specie);")

if ARGS.debug:
    print("states:")
    print(nepc.table_as_df(MYCURSOR, "states"))

MYDB.commit()

DIR_NAMES = ["/data/formatted/n2/itikawa/",
             "/data/formatted/n2/zipf/",
             "/data/formatted/n/zatsarinny/"]

if platform.node() == 'ppdadamsonlinux':
    cs_dat_filename = "cs_datfile_prod.tsv"
else:
    cs_dat_filename = "cs_datfile_local.tsv"

f_cs_dat_file = open(cs_dat_filename, 'w')
f_cs_dat_file.write("\t".join(["cs_id", "filename"]) + "\n")

cs_id = 1
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
            f_cs_dat_file.write(
                "\t".join([str(cs_id),
                           directoryname + str(filename_wo_ext)]) + "\n"
            )
            executeTextCS = ("LOAD DATA LOCAL INFILE '" + met_file +
                             "' INTO TABLE nepc.cs "
                             "IGNORE 1 LINES "
                             "(@temp,@specie,@process,units_e,units_sigma,"
                             "ref,@lhsA,@lhsB,@rhsA,@rhsB,wavelength,lhs_v,"
                             "rhs_v,lhs_j,rhs_j,background,lpu,upu) "
                             "SET cs_id = " + str(cs_id) + ", "
                             "specie_id = (select id from nepc.species "
                             "  where name = @specie), "
                             "process_id = (select id from nepc.processes "
                             "  where name = @process), "
                             "lhsA_id = (select id from nepc.states "
                             "  where name LIKE @lhsA), "
                             "lhsB_id = (select id from nepc.states "
                             "  where name LIKE @lhsB), "
                             "rhsA_id = (select id from nepc.states "
                             "  where name LIKE @rhsA), "
                             "rhsB_id = (select id from nepc.states "
                             "  where name LIKE @rhsB);")

            executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + mod_file +
                                   "' INTO TABLE nepc.models2cs "
                                   "(@model) "
                                   "SET cs_id = " + str(cs_id) + ", "
                                   "model_id = (select model_id "
                                   "            from nepc.models "
                                   "            where name LIKE @model);")

            executeTextCSDATA = ("LOAD DATA LOCAL INFILE '" + dat_file +
                                 "' INTO TABLE nepc.csdata "
                                 "IGNORE 1 LINES "
                                 "(id,e,sigma) "
                                 "SET cs_id = " + str(cs_id) + ";")

            MYCURSOR.execute(executeTextCS)

            MYCURSOR.execute(executeTextCSDATA)

            if os.path.exists(mod_file):
                MYCURSOR.execute(executeTextCSMODELS)

            cs_id = cs_id + 1

f_cs_dat_file.close()

MYDB.commit()

MYCURSOR.execute("use nepc;")








"""
DIR_NAMES = ["/data/formatted/n2/itikawa/",
             "/data/formatted/n2/zipf/",
             "/data/formatted/n/zatsarinny/"]


if platform.node() == 'ppdadamsonlinux':
    CS_DAT_FILENAME = "cs_datfile_prod.tsv"
else:
    CS_DAT_FILENAME = "cs_datfile_local.tsv"

F_CS_DAT_FILE = open(CS_DAT_FILENAME, 'w')
F_CS_DAT_FILE.write("\t".join(["cs_id", "filename"]) + "\n")

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
"""



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
