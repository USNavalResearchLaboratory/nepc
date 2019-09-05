"""Builds the NEPC database"""
import argparse
import platform
import os
import mysql.connector
import csv
import pandas as pd
from nepc import nepc
from nepc.util import config
from nepc.util import scraper

# NA_VALUES = ['\\N']
NA_VALUES = []
MAX_CS = 2000000
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


def np_str(df, row, name):
    if df.iloc[row][name] == "\\N":
        return "Null"
    else:
        return df.iloc[row][name]


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
                 "	`cs_id` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
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
                 "	CONSTRAINT `SPECIE_ID_CS` FOREIGN KEY(`specie_id`)"
                 "	REFERENCES `nepc`.`species`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	INDEX `PROCESS_ID`(`process_id` ASC) ,"
                 "	CONSTRAINT `PROCESS_ID_CS` FOREIGN KEY(`process_id`)"
                 "	REFERENCES `nepc`.`processes`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `LHSA_ID_CS` FOREIGN KEY(`lhsA_id`)"
                 "		REFERENCES `nepc`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `LHSB_ID_CS` FOREIGN KEY(`lhsB_id`)"
                 "		REFERENCES `nepc`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `RHSA_ID_CS` FOREIGN KEY(`rhsA_id`)"
                 "		REFERENCES `nepc`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `RHSB_ID_CS` FOREIGN KEY(`rhsB_id`)"
                 "		REFERENCES `nepc`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE "
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
                 "  ON DELETE RESTRICT ON UPDATE CASCADE "
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


def insert_command(table_name, variable_list):
    variable_list_str = ", ".join(variable_list)
    data_format_str = ", ".join(["%s"]*len(variable_list))
    return ("INSERT INTO " + table_name +
            "(" + variable_list_str + ") " +
            "VALUES (" + data_format_str + ");")


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

# print_table("species")

STATES_VARIABLE_LIST = ["id", "specie_id", "name", "long_name"]
INSERT_COMMAND_STATES = insert_command("states", STATES_VARIABLE_LIST)
UPDATE_COMMAND_STATES = ("UPDATE states " +
                         "SET specie_id = (SELECT id " +
                         "FROM nepc.species WHERE NAME = %s) " +
                         "WHERE id=%s;")

with open(NEPC_DATA + 'states.tsv', 'r') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    row_number = 1
    for row in tsvin:
        if row_number > 1:
            MYCURSOR.execute(INSERT_COMMAND_STATES,
                             (row[0], 1, row[2], row[3]))
            MYCURSOR.execute(UPDATE_COMMAND_STATES,
                             (row[1], row[0]))
        row_number = row_number + 1

MYDB.commit()

if ARGS.debug:
    print_timestep("loaded data into states table")
    # print_table("states")

DIR_NAMES = ["/data/cs/n2/itikawa/",
             "/data/cs/n2/zipf/",
             "/data/cs/n/zatsarinny/"]

if platform.node() == 'ppdadamsonlinux':
    CS_DAT_FILENAME = NEPC_DATA + "cs_datfile_prod.tsv"
else:
    CS_DAT_FILENAME = NEPC_DATA + "cs_datfile_local.tsv"

F_CS_DAT_FILE = open(CS_DAT_FILENAME, 'w')
F_CS_DAT_FILE.write("\t".join(["cs_id", "filename"]) + "\n")

CS_VARIABLE_LIST = ["cs_id", "specie_id", "process_id",
                    "units_e", "units_sigma",
                    "ref",
                    "lhsA_id", "lhsB_id", "rhsA_id", "rhsB_id",
                    "wavelength",
                    "lhs_v", "rhs_v", "lhs_j", "rhs_j", "background",
                    "lpu", "upu"]
CS_DTYPE = {"cs_id": int,
            "specie": str,
            "process": str,
            "units_e": float,
            "units_sigma": float,
            "ref": str,
            "lhs_a": str,
            "lhs_b": str,
            "rhs_a": str,
            "rhs_b": str,
            "wavelength": float,
            "lhs_v": int,
            "rhs_v": int,
            "lhs_j": int,
            "rhs_j": int,
            "background": str,
            "lpu": float,
            "upu": float
            }
CSDATA_VARIABLE_LIST = ["id", "cs_id", "e", "sigma"]
CSDATA_DTYPE = {"csdata_id": int,
                "e_energy": float,
                "sigma": float}
MOD_DTYPE = {"model_name": str}


def insert_table(insert_command_str, data_list):
    return 0


def update_table_ext_id(table_name, ext_table_name, id_value_pair_list):
    return 0


INSERT_COMMAND_CS = insert_command("cs", CS_VARIABLE_LIST)
UPDATE_COMMAND_CS = ("UPDATE cs " +
                     "SET "
                     "  specie_id = (SELECT id FROM nepc.species "
                     "    WHERE NAME=%s), "
                     "  process_id = (select id from nepc.processes "
                     "    WHERE NAME=%s), "
                     "  lhsA_id = (select id from nepc.states "
                     "    WHERE NAME=%s), "
                     "  lhsB_id = (select id from nepc.states "
                     "    WHERE NAME=%s), "
                     "  rhsA_id = (select id from nepc.states "
                     "    WHERE NAME=%s), "
                     "  rhsB_id = (select id from nepc.states "
                     "    WHERE NAME=%s) "
                     "WHERE cs_id=%s;")

INSERT_COMMAND_CSDATA = insert_command("csdata", CSDATA_VARIABLE_LIST)

INSERT_COMMAND_MODELS2CS = ("INSERT INTO models2cs "
                            "SET "
                            " cs_id=%s, "
                            " model_id=(SELECT model_id "
                            "           FROM nepc.models "
                            "           WHERE NAME=%s);")

file_number = 1
for directoryname in DIR_NAMES:
    directory = os.fsencode(NEPC_HOME + directoryname)
    for file in os.listdir(directory):
        if file_number < MAX_CS:
            filename = os.fsdecode(file)
            if filename.endswith(".met") or filename.endswith(".mod"):
                continue
            else:
                # print("file_number: " + str(file_number))
                file_number = file_number + 1
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

                met_data = pd.read_csv(met_file,
                                       sep='\t',
                                       dtype=CS_DTYPE,
                                       na_values=NA_VALUES)
                dat_data = pd.read_csv(dat_file,
                                       sep='\t',
                                       dtype=CSDATA_DTYPE,
                                       na_values=NA_VALUES)

                MYCURSOR.execute(INSERT_COMMAND_CS,
                                 (int(met_data.iloc[0]['cs_id']), 1, 1,
                                  met_data.iloc[0]['units_e'],
                                  met_data.iloc[0]['units_sigma'],
                                  met_data.iloc[0]['ref'], 1, 1, 1, 1,
                                  met_data.iloc[0]['wavelength'],
                                  int(met_data.iloc[0]['lhs_v']),
                                  int(met_data.iloc[0]['rhs_v']),
                                  int(met_data.iloc[0]['lhs_j']),
                                  int(met_data.iloc[0]['rhs_j']),
                                  met_data.iloc[0]['background'],
                                  met_data.iloc[0]['lpu'],
                                  met_data.iloc[0]['upu']))
                MYCURSOR.execute(UPDATE_COMMAND_CS,
                                 (np_str(met_data, 0, 'specie'),
                                  np_str(met_data, 0, 'process'),
                                  np_str(met_data, 0, 'lhs_a'),
                                  np_str(met_data, 0, 'lhs_b'),
                                  np_str(met_data, 0, 'rhs_a'),
                                  np_str(met_data, 0, 'rhs_b'),
                                  int(met_data.iloc[0]['cs_id'])))
                MYDB.commit()

                dat_data.insert(1, 'cs_id', met_data.iloc[0]['cs_id'])
                dat_data_list = list(dat_data.itertuples(index=False,
                                                         name=None))
                MYCURSOR.executemany(INSERT_COMMAND_CSDATA, dat_data_list)

                if os.path.exists(mod_file):
                    mod_data = pd.read_csv(mod_file,
                                           sep='\t',
                                           dtype=MOD_DTYPE,
                                           na_values=NA_VALUES)
                    mod_data.insert(0, 'cs_id', met_data.iloc[0]['cs_id'])
                    mod_data_list = list(mod_data.itertuples(index=False,
                                                             name=None))
                    MYCURSOR.executemany(INSERT_COMMAND_MODELS2CS,
                                         mod_data_list)

MYDB.commit()
F_CS_DAT_FILE.close()

if ARGS.debug:
    print_timestep("loaded data into cs, csdata, and models2cs tables")
    # print_table("cs")

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
