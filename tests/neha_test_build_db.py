"""This module is used for the purposes of testing whether data
is being entered into the database properly"""
import csv
import argparse
import os
import platform
import mysql.connector
import pytest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from nepc import nepc
from nepc.util import config
from nepc.util import scraper
# TODO: remove dependence on csv; put function in scraper that uses built-in
#       readlines function
PARSER = argparse.ArgumentParser(description='Build the test database.')
PARSER.add_argument('--debug', action='store_true',
                    help='print additional debug info')
ARGS = PARSER.parse_args()

if ARGS.debug:
    import time
    T0 = time.time()

"""
#====================BUILDING THE TEST DATABASE=======================
PARSER = argparse.ArgumentParser(description='Build the test database.')
PARSER.add_argument('--debug', action='store_true',
                    help='print additional debug info')
ARGS = PARSER.parse_args()

if ARGS.debug:
    import time
    T0 = time.time()

# TODO: test that all values in [nepc]/data are in the nepc database

NEPC_HOME = config.nepc_home()

DIR_NAMES = [NEPC_HOME + "/data/formatted/n2/itikawa/",
             NEPC_HOME + "/data/formatted/n2/zipf/",
             NEPC_HOME + "/data/formatted/n/zatsarinny/"]

HOME = config.userHome()
NEPC_HOME = config.nepc_home()
NEPC_MYSQL = NEPC_HOME + "/mysql/"

MYDB = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

MYCURSOR = MYDB.cursor()

MYCURSOR.execute("DROP DATABASE IF EXISTS `test`;")
MYCURSOR.execute("CREATE DATABASE IF NOT EXISTS `test` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")

MYCURSOR.execute("SET default_storage_engine = INNODB;")
MYCURSOR.execute("use test;")

MYCURSOR.execute("CREATE TABLE `test`.`species`("
                 "`id` INT UNSIGNED NOT NULL auto_increment ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

MYCURSOR.execute("CREATE TABLE `test`.`processes`( "
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


MYCURSOR.execute("CREATE TABLE `test`.`states`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`specie_id` INT UNSIGNED NOT NULL ,"
                 "	`name` VARCHAR(100) NOT NULL ,"
                 "	`long_name` VARCHAR(100) NOT NULL ,"
                 "	`configuration` JSON NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `SPECIE_ID`(`specie_id` ASC) ,"
                 "	CONSTRAINT `specie_id_STATES` FOREIGN KEY(`specie_id`) "
                 "		REFERENCES `test`.`species`(`id`) "
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )
MYCURSOR.execute("CREATE TABLE `test`.`models`("
                 "	`model_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `test`.`cs`("
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
                 "		REFERENCES `test`.`species`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `PROCESS_ID_CS` FOREIGN KEY(`process_id`)"
                 "		REFERENCES `test`.`processes`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `LHSA_ID_CS` FOREIGN KEY(`lhsA_id`)"
                 "		REFERENCES `test`.`states`(`id`),"
                 "	CONSTRAINT `LHSB_ID_CS` FOREIGN KEY(`lhsB_id`)"
                 "		REFERENCES `test`.`states`(`id`),"
                 "	CONSTRAINT `RHSA_ID_CS` FOREIGN KEY(`rhsA_id`)"
                 "		REFERENCES `test`.`states`(`id`),"
                 "	CONSTRAINT `RHSB_ID_CS` FOREIGN KEY(`rhsB_id`)"
                 "		REFERENCES `test`.`states`(`id`)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `test`.`csdata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`CS_ID` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `CS_ID`(`CS_ID` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`CS_ID`)"
                 "		REFERENCES `test`.`cs`(`CS_ID`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `test`.`models2cs`("
                 "	`CS_ID` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (CS_ID, model_id)"
                 ");"
                 )
"""


def broad_cats():
    """Returns a list of the first three headers for the first three tables

    Returns
    -------
    A list of headers - processes, models, and species, for the first three tables
    of the test database
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
    for lst_elem in lst:
        if lst_elem != lst[len(lst)-1]:
            answer = answer + lst_elem + ","
        else:
            answer = answer + lst_elem
    return answer

def met_headers():
    """Returns the headers for a metadata file
    Returns
    -------
    List containing the headers for a .met file

    """
    return ['@temp', '@specie', '@process', 'units_e', 'units_sigma', 'ref',
            '@lhsA', '@lhsB', '@rhsA', '@rhsB', 'wavelength', 'lhs_v',
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
    if column in met_headers():
        tup = (met_file, "cs", column)
    else:
        tup = (dat_file, "csdata", column)
    return tup
def multi_iteration(resu):
    """Separate through each different mysql command given a generator object
    Parameters
    ----------
    res : a generator object that will be returned when using mycursor.execute (multi=True)"""
    if ARGS.debug:
        print(resu)
    for cur in resu:
        print('cursor:', cur)
        if cur.with_rows:
            print('RESULTS:', cur.fetchall())

"""
N_STATES = ["/N_STATES.tsv'", "/n+_states.tsv'", "/n++_states.tsv'"]
N2_STATES = ["/n2+_states.tsv'", "/N2_STATES.tsv'"]
BEG_EXEC = '' #beginning statement to execute, used to make code shorter + more readable
for i in broad_cats():
    BEG_EXEC = (BEG_EXEC + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL +
                i + ".tsv' " + "\nINTO TABLE " + "test." + i)
    if i == 'processes':
        BEG_EXEC = BEG_EXEC + " " + "\nIGNORE 2 LINES;"
    else:
        BEG_EXEC = BEG_EXEC + ";"
if ARGS.debug:
    print(BEG_EXEC)
RESULTS = MYCURSOR.execute(BEG_EXEC, multi=True) #query created earlier executed
multi_iteration(RESULTS)
STATE_QUERY = ''
for i in N_STATES:
    STATE_QUERY = (STATE_QUERY + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + i +
                   "    INTO TABLE test.states" + "     IGNORE 1 LINES" +
                   "      (id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)" +
                   "      SET configuration = JSON_OBJECT(" +
                   "          JSON_OBJECT('order', " +
                   "              JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', " +
                   "              '3d', '4s', '4p')" +
                   "              )," +
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
                   "			)" +
                   "		)" +
                   "	)," +
                   "	specie_id = (select max(id) from test.species " +
                   "               where name = " +
                   "'" + i[1:i.index('_')].upper() + "'" + ");")
for i in N2_STATES:
    STATE_QUERY = (STATE_QUERY + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + i +
                   "    INTO TABLE test.states" + "     IGNORE 1 LINES" +
                   "      (id,name,long_name,@o1,@o2,@o3,@o4,@o5,@o6)" +
                   "      SET configuration = JSON_OBJECT(" +
                   "          JSON_OBJECT('order', " +
                   "              JSON_ARRAY('2sigma_u', '1pi_u'," +
                   "'1pi_g', '3sigma_u', '3ssigma_g')" +
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
                   "	specie_id = (select max(id) from test.species " +
                   "               where name = " +
                   "'" + i[1:i.index('_')].upper() + "'" + ");")
STATE_RESULTS = MYCURSOR.execute(STATE_QUERY, multi=True)
multi_iteration(STATE_RESULTS)
MYDB.commit()

if platform.node() == 'ppdadamsonlinux':
    CS_DAT_FILENAME = "cs_datfile_prod.tsv"
else:
    CS_DAT_FILENAME = "cs_datfile_local.tsv"

F_CS_DAT_FILE = None
F_CS_DAT_FILE = open(CS_DAT_FILENAME, 'w')
F_CS_DAT_FILE.write("\t".join(["CS_ID", "filename"]) + "\n")

CS_ID = 1

for directoryname in DIR_NAMES:
    directory = os.fsencode(directoryname)

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
                "\t".join([str(CS_ID), directoryname + str(filename_wo_ext)]) + "\n"
            )

        filetype = [met_file, dat_file]
        tablename = ['cs', 'csdata']
        for i in range(0, no_of_file_types()):
            exCS = '' + ("LOAD DATA LOCAL INFILE '" + filetype[i] +
                         "' INTO TABLE  " + "test." + tablename[i] +
                         " IGNORE 1 LINES ")
            if filetype[i] == met_file:
                exCS = (exCS + "(" + print_list_elems(met_headers()) + ") "
                        "SET CS_ID = " + str(CS_ID) + ", ")
                atSign = []
                for ind in met_headers():
                    if ('@' in ind and ind != '@temp'):
                        atSign.append(ind)
                    if (not atSign and ind == met_headers()[1]): #disregards @temp here
                        exCS = exCS + ";"
                for inde in range(0, len(atSign)):
                    if (atSign[inde] == '@lhsA' or atSign[inde] == '@rhsA'
                            or atSign[inde] == '@lhsB' or atSign[inde] == '@rhsB'):
                        exCS = (exCS + atSign[inde][1:] +
                                "_id = (select id from test.states  where name LIKE " +
                                atSign[inde] + ")")
                        if inde != len(atSign) - 1:
                            exCS = exCS + ", "
                        else:
                            exCS = exCS + ";"
                            if ARGS.debug:
                                print(exCS)
                    elif atSign[inde] == '@process':
                        exCS = (exCS + atSign[inde][1:] +
                                "_id = (select id from test." +
                                atSign[inde][1:] + "es" +
                                "  where name = " + atSign[inde]+ ")")
                        if inde != len(atSign) - 1:
                            exCS = exCS + ", "
                            #MYCURSOR.execute("print n 'process_id'")
                        else:
                            exCS = exCS + ";"

                    elif atSign[inde] != '@specie':
                        exCS = (exCS + atSign[inde][1:] +
                                "_id = (select id from test." +
                                atSign[inde][1:] + "  where name = " + atSign[inde]+ ")")
                        if inde != len(atSign) - 1:
                            exCS = exCS + ", "
                        else:
                            exCS = exCS + ";"
                    else:
                        exCS = (exCS + atSign[inde][1:] +
                                "_id = (select id from test." + atSign[inde][1:] +
                                "s" + " where name = " + atSign[inde] + ")")
                        if inde != (len(atSign) - 1):
                            exCS = exCS + ", "
                        else:
                            exCS = exCS + ";"
            else:
                exCS = (exCS + "(" + print_list_elems(dat_headers()) + ") "
                        "SET CS_ID = " + str(CS_ID) + "; ")
                if ARGS.debug:
                    print(exCS)
            res = MYCURSOR.execute(exCS, multi=True)
            multi_iteration(res)
            MYDB.commit()
        executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + mod_file +
                               "' INTO TABLE test.models2cs "
                               "(@model) "
                               "SET CS_ID = " + str(CS_ID) + ", "
                               "model_id = (select model_id "
                               "            from test.models "
                               "            where name LIKE @model);")

        if os.path.exists(mod_file):
            MYCURSOR.execute(executeTextCSMODELS)
        CS_ID = CS_ID + 1

F_CS_DAT_FILE.close()

MYDB.commit()

"""

NEPC_HOME = config.nepc_home()

DIR_NAMES = [NEPC_HOME + "/data/formatted/n2/itikawa/",
             NEPC_HOME + "/data/formatted/n2/zipf/",
             NEPC_HOME + "/data/formatted/n/zatsarinny/"]

#===============TEST FUNCTIONS=====================
#TODO: refactor funcs w/ pytest.mark.parametrize() to reduce duplicate lines of code
def nepc_connect(local, dbug):
    """Establishes a connection with the NEPC database

    Parameters
    ----------
    local : boolean
    Checks whether the database is locally based or based off of 'ppdadamsonlinux'
    dbug : boolean
    Checks whether debug mode is on or off

    Returns
    -------
    cnx : connection
    A connection to the official NEPC MySQL database
    cursor : MySQLCursor
    A MySQLCursor object for executing SQL queries"""
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_csdata_lines(local, dbug):
    """Checks whether the table cs_data in the database has the correct
    number of rows"""
    cnx, cursor = nepc_connect(local, dbug)
    cs_lines = 0
    for dirname in DIR_NAMES:
        direc = os.fsencode(dirname)
        if ARGS.debug:
            print(direc)
        for file in os.listdir(direc):
            filen = os.fsdecode(file)
            if filen.endswith(".met") or filen.endswith(".mod"):
                continue
            else:
                # subtract 1 to account for header
                cs_lines += scraper.wc_fxn(dirname + filen) - 1

    assert cs_lines == nepc.count_table_rows(cursor, "csdata")
    cursor.close()
    cnx.close()

def test_species_entered(local, dbug): #for the species table
    """Checks whether the species table in the NEPC database
    has the same values as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    #test_species = nepc.table_as_df(MYCURSOR, "species")
    cs_species = nepc.table_as_df(cursor, "species")
    assert_frame_equal(test_species, cs_species)
    cursor.close()
    cnx.close()

def test_species_number_of_rows(local, dbug):
    """Checks whether the species table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
#    assert nepc.count_table_rows(cursor, "species") == nepc.count_table_rows(MYCURSOR, "species")
    cursor.close()
    cnx.close()

def test_processes_entered(local, dbug): #for the processes table
    #FIXME: currently does not add all of the elements in the file
    """Checks whether the processes table in the NEPC database
    has the same values as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
#    test_processes = nepc.table_as_df(MYCURSOR, "processes")
    cs_processes = nepc.table_as_df(cursor, "processes")
    if ARGS.debug:
        print(cs_processes)
    #assert_frame_equal(cs_processes, test_processes)
    cursor.close()
    cnx.close()

def test_processes_number_of_rows(local, dbug):
    """Checks whether the processes table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    processes_rows = nepc.count_table_rows(cursor, "processes")
#    t_processes_rows = nepc.count_table_rows(MYCURSOR, "processes")
    #assert processes_rows == t_processes_rows
    cursor.close()
    cnx.close()


def test_models_entered(local, dbug):
    """Checks whether the models table in the NEPC database
    has the same values as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
#    test_models = nepc.table_as_df(MYCURSOR, "models")
    cs_models = nepc.table_as_df(cursor, "models")
    #assert_frame_equal(test_models, cs_models)
    cursor.close()
    cnx.close()


def test_models_number_of_rows(local, dbug):
    """Checks whether the models table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    #assert nepc.count_table_rows(cursor, "models") == nepc.count_table_rows(MYCURSOR, "models")
    cursor.close()
    cnx.close()


def test_states_entered(local, dbug):
    """Checks whether the states table in the NEPC database
    has the same value as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    test_states = nepc.table_as_df(MYCURSOR, "states")
    cs_states = nepc.table_as_df(cursor, "states")
    assert_frame_equal(test_states, cs_states)
    cursor.close()
    cnx.close()


def test_states_number_of_rows(local, dbug):
    """Checks whether the states table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows(cursor, "states") == nepc.count_table_rows(MYCURSOR, "states")
    cursor.close()
    cnx.close()

def test_models2cs_entered(local, dbug):
    """Checks whether the models2cs table in the NEPC database
    has the same values as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    test_models2cs = nepc.table_as_df(MYCURSOR, "models2cs")
    cs_models2cs = nepc.table_as_df(cursor, "models2cs")
    assert_frame_equal(test_models2cs, cs_models2cs)
    cursor.close()
    cnx.close()


def test_models2cs_number_of_rows(local, dbug):
    """Checks whether the models2cs table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    models2cs_nepc = nepc.count_table_rows(cursor, "models2cs")
    assert models2cs_nepc == nepc.count_table_rows(MYCURSOR, "models2cs")
    cursor.close()
    cnx.close()


def test_cs_entered(local, dbug):
    """Checks whether the CS table in the NEPC database
    has the same values as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    test_cs = nepc.table_as_df(MYCURSOR, "cs")
    file_cs = nepc.table_as_df(cursor, "cs")
    assert_frame_equal(test_cs, file_cs)
    cursor.close()
    cnx.close()


def test_cs_number_of_rows(local, dbug):
    """Checks whether the CS table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows(cursor, "cs") == nepc.count_table_rows(MYCURSOR, "cs")
    cursor.close()
    cnx.close()

def test_csdata_entered(local, dbug):
    """Checks whether the csdata table in the NEPC database
    has the same values as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    test_csdata = nepc.table_as_df(MYCURSOR, "csdata")
    file_csdata = nepc.table_as_df(cursor, "csdata")
    assert_frame_equal(test_csdata, file_csdata)
    cursor.close()
    cnx.close()

def test_csdata_number_of_rows(local, dbug):
    """Checks whether the csdata table in the NEPC database
    has the same number of rows as in the file"""
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows(cursor, "csdata") == nepc.count_table_rows(MYCURSOR, "csdata")
    cursor.close()
    cnx.close()


# TODO: use @pytest.mark.parametrize decorator to turn this into N tests
#       instead of N asserts in one test
def test_data_entered(local, dbug): #for the csdata table
    """Checks whether the csdata in the NEPC database
    has the same values as in the file,
    testing each specific column"""
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        csid = row['cs_id']
        datfile_row = row['filename']
        df_conv = pd.read_csv(NEPC_HOME + datfile_row + '.dat', delimiter='\t',
                              usecols=['e_energy', 'sigma'])
        e_energy, sigma = nepc.cs_e_sigma(cursor, csid)
        assert e_energy == pytest.approx(df_conv['e_energy'].tolist())
        assert sigma == pytest.approx(df_conv['sigma'].tolist())
    cursor.close()
    cnx.close()


# TODO: use @pytest.mark.parametrize decorator to turn this into N tests
#       instead of N asserts in one test
def test_meta_entered(local, dbug): #for the cs table
    """Checks whether the cs table in the NEPC database
    has the same values as in the file,
    testing each specific column"""
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        if ARGS.debug:
            #just to increase pylint score
            print(index)
            print(cnx)
        csid_row = row['CS_ID']
        met_file = row['filename']
        if dbug:
            print(csid_row, met_file)

        meta_cols = ['specie', 'process', 'units_e',
                     'units_sigma', 'ref', 'lhsA',
                     'lhsB', 'rhsA', 'rhsB', 'wavelength',
                     'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j',
                     'background', 'lpu', 'upu']

        with open(NEPC_HOME + met_file + ".met", 'r', newline='') as fil:
            reader = csv.reader(fil, delimiter='\t')
            next(reader)
            meta_disk = list(reader)[0]
        meta_disk = [meta_disk[i] for i in list(range(1, 18))]
        for i in [2, 3, 9, 15, 16]:
            meta_disk[i] = (float(meta_disk[i]) if meta_disk[i] != '\\N'
                            else meta_disk[i])

        for i in [10, 11, 12, 13]:
            meta_disk[i] = (int(meta_disk[i]) if meta_disk[i] != '\\N'
                            else meta_disk[i])

        meta_db = [nepc.cs_metadata(cursor, csid_row)[i]
                   for i in list(range(1, 18))]
        for i in range(len(meta_cols)):
            if type(meta_db[i]) is float:
                assert (pytest.approx(meta_disk[i]) ==
                        pytest.approx(meta_db[i]))
            elif meta_db[i] is None:
                assert meta_disk[i] == '\\N'
            else:
                assert meta_disk[i] == meta_db[i]
