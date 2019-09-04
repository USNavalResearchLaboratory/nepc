"""Builds the NEPC database"""
import argparse
import platform
# import os
import mysql.connector
import csv
from nepc import nepc
from nepc.util import config
# from nepc.util import scraper

PARSER = argparse.ArgumentParser(description='Build the NEPC database.')
PARSER.add_argument('--debug', action='store_true',
                    help='print additional debug info')
ARGS = PARSER.parse_args()

if ARGS.debug:
    import time
    T0 = time.time()

HOME = config.user_home()
NEPC_HOME = config.nepc_home()
NEPC_DATA = NEPC_HOME + "/data/"


def print_table(table):
    """print a table
    ARGUMENT
    ========
    table: str
    """
    MYCURSOR.execute("SELECT * FROM " + table + ";")
    table_data = MYCURSOR.fetchall()
    for row in table_data:
        print(row)


def print_timestep(stage):
    """print stage and elapsed time

    ARGUMENT
    ========
    stage: str
    """
    current_time = time.time()
    elapsed = current_time-T0
    print("\n" + stage + ": " + str(round(elapsed, 2)) + " sec\n"
          "===============================================")


########################
# Connect to database
########################


MYDB = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

if ARGS.debug:
    print_timestep("connected to MySQL")

MYCURSOR = MYDB.cursor()

MYCURSOR.execute("DROP DATABASE IF EXISTS `nepc`;")

MYCURSOR.execute("CREATE DATABASE IF NOT EXISTS `nepc` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")

MYCURSOR.execute("SET default_storage_engine = INNODB;")

MYCURSOR.execute("use nepc;")

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

MYDB.commit()

MYCURSOR.execute("CREATE TABLE `nepc`.`models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
                 ");"
                 )

MYDB.commit()

if ARGS.debug:
    print_timestep("created all tables")

#############
# Load data #
#############

TABLES = [("processes",
           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
          ("models",
           "(%s, %s, %s)"),
          ("species",
           "(%s, %s, %s)")]

for table in TABLES:
    table_name = table[0]
    table_format = table[1]
    with open(NEPC_DATA + table_name + '.tsv', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        row_number = 1
        for row in tsvin:
            if row_number > 1:
                MYCURSOR.execute("INSERT INTO " + table_name +
                                 " VALUES " + table_format, row)
            row_number = row_number + 1
    MYDB.commit()
    if ARGS.debug:
        print_timestep("loaded data into " + table_name + " table")

print_table("species")

with open(NEPC_DATA + 'states.tsv', 'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    row_number = 1
    for row in tsvin:
        if row_number > 1:
            MYCURSOR.execute("INSERT INTO states "
                             "(id, specie_id, name, long_name) "
                             "VALUES (%s, 1, %s, %s);",
                             (row[0], row[2], row[3]))
            MYCURSOR.execute("UPDATE states "
                             "SET specie_id = (SELECT id "
                             "FROM nepc.species WHERE NAME = %s) "
                             "WHERE id=%s;",
                             (row[1], row[0]))
        row_number = row_number + 1

MYDB.commit()

if ARGS.debug:
    print_timestep("loaded data into states table")
    print_table("states")

DIR_NAMES = ["/data/cs/n2/itikawa/",
             "/data/cs/n2/zipf/",
             "/data/cs/n/zatsarinny/"]

if platform.node() == 'ppdadamsonlinux':
    CS_DAT_FILENAME = NEPC_DATA + "cs_datfile_prod.tsv"
else:
    CS_DAT_FILENAME = NEPC_DATA + "cs_datfile_local.tsv"

F_CS_DAT_FILE = open(CS_DAT_FILENAME, 'w')
F_CS_DAT_FILE.write("\t".join(["cs_id", "filename"]) + "\n")

insertCS = ("INSERT INTO cs "
            "(cs_id,specie,process,units_e,units_sigma,"
            "ref,lhsA,lhsB,rhsA,rhsB,wavelength,lhs_v,"
            "rhs_v,lhs_j,rhs_j,background,lpu,upu) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s);")

updateCSspecie_id = ("UPDATE cs "
                     "SET specie_id = (SELECT id FROM nepc.species "
                     "WHERE NAME = %s) "
                     "WHERE id=%s;")

"""
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
executeTextCS = ("LOAD DATA LOCAL INFILE %s "
                 "INTO TABLE nepc.cs "
                 "IGNORE 1 LINES "
                 "(cs_id,@specie,@process,units_e,units_sigma,"
                 "ref,@lhsA,@lhsB,@rhsA,@rhsB,wavelength,lhs_v,"
                 "rhs_v,lhs_j,rhs_j,background,lpu,upu) "
                 "SET cs_id = %s, "
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

executeTextCSDATA = ("LOAD DATA LOCAL INFILE %s "
                     "INTO TABLE nepc.csdata "
                     "IGNORE 1 LINES "
                     "(id,e,sigma) "
                     "SET cs_id = %s;")

executeTextCSMODELS = ("LOAD DATA LOCAL INFILE %s "
                       "INTO TABLE nepc.models2cs "
                       "(@model) "
                       "SET cs_id = %s, "
                       "model_id = (select model_id "
                       "            from nepc.models "
                       "            where name LIKE @model);")


for directoryname in DIR_NAMES:
    directory = os.fsencode(NEPC_HOME + directoryname)

    met_data = []
    dat_data = []
    mod_data = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".met") or filename.endswith(".mod"):
            continue
        else:
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

            CS_ID = scraper.get_cs_id_from_met_file(met_file)

            F_CS_DAT_FILE.write(
                "\t".join([str(CS_ID),
                           directoryname + str(filename_wo_ext)]) + "\n"
            )

            met_data.append((met_file, str(CS_ID)))
            dat_data.append((dat_file, str(CS_ID)))
            if os.path.exists(mod_file):
                mod_data.append((mod_file, str(CS_ID)))

    MYCURSOR.executemany(executeTextCS, met_data)

    MYCURSOR.executemany(executeTextCSDATA, dat_data)

    MYCURSOR.executemany(executeTextCSMODELS, mod_data)

F_CS_DAT_FILE.close()

MYDB.commit()
"""

if ARGS.debug:
    print_timestep("loaded data into cs, csdata, and models2cs tables")

if ARGS.debug:
    print_timestep("built NEPC database")
    for table in ["species", "processes", "states", "cs", "models",
                  "models2cs", "csdata"]:
        print(table + ": " + str(nepc.count_table_rows(MYCURSOR, table)) +
              " rows")
else:
    print("\nbuilt NEPC database\n")


MYCURSOR.close()

MYDB.close()
