"""Builds the NEPC database"""
import argparse
import platform
import os
import mysql.connector
import pandas as pd
from nepc import nepc
from nepc.util import config
import time

NA_VALUES = []
PARSER = argparse.ArgumentParser(description='Build the NEPC database.')
PARSER.add_argument('--debug', action='store_true',
                    help='print additional debug info')
PARSER.add_argument('--test', action='store_true',
                    help='build test database')
ARGS = PARSER.parse_args()

if ARGS.debug:
    MAX_CS = 50
    MAX_RATE = 50
else:
    MAX_CS = 2000000
    MAX_RATE = 2000000

if ARGS.test:
    database = 'nepc_test'
    NEPC_DATA = config.nepc_home() + "/tests/data/"
    DIR_NAMES = ["/cs/n2/fict/",
                 "/cs/n2/fict_total/"]
else:
    database = 'nepc'
    NEPC_DATA = config.nepc_cs_home() + "/data/"
    DIR_NAMES = ["/cs/n2/itikawa/",
                 "/cs/n2/zipf/",
                 "/cs/n/zatsarinny/",
                 "/cs/n2/phelps/",
                 "/cs/n2/phelps_total/",
                 "/cs/n2/little/"]

T0 = time.time()

HOME = config.user_home()

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


def insert_command(table_name, variable_list):
    variable_list_str = ", ".join(variable_list)
    data_format_str = ", ".join(["%s"]*len(variable_list))
    return ("INSERT INTO " + table_name +
            "(" + variable_list_str + ") " +
            "VALUES (" + data_format_str + ");")


####################
# Connect to MySQL #
####################

MYDB = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

MYCURSOR = MYDB.cursor()

if ARGS.debug:
    print_timestep("connected to MySQL")

##############################
# Create empty NEPC database #
##############################

MYCURSOR.execute("DROP DATABASE IF EXISTS `" + database + "`;")

MYCURSOR.execute("CREATE DATABASE IF NOT EXISTS `" + database + "` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")

MYCURSOR.execute("SET default_storage_engine = INNODB;")

MYCURSOR.execute("use " + database + ";")

MYCURSOR.execute("CREATE TABLE `" + database + "`.`species`("
                 "`id` INT UNSIGNED NOT NULL ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

MYCURSOR.execute("CREATE TABLE `" + database + "`.`processes`( "
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

MYCURSOR.execute("CREATE TABLE `" + database + "`.`states`( "
                 "`id` INT UNSIGNED NOT NULL, "
                 "`specie_id` INT UNSIGNED NOT NULL, "
                 "`name` VARCHAR(100) NOT NULL, "
                 "`long_name` VARCHAR(100) NOT NULL, "
                 "PRIMARY KEY(`id`), "
                 "INDEX `SPECIE_ID`(`specie_id` ASC), "
                 "CONSTRAINT `specie_id_STATES` FOREIGN KEY(`specie_id`) "
                 "REFERENCES `" + database + "`.`species`(`id`) "
                 "ON DELETE RESTRICT ON UPDATE CASCADE "
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `" + database + "`.`models`("
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	`ref` VARCHAR(40) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `" + database + "`.`cs`("
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
                 "	`threshold` DOUBLE NULL ,"
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
                 "	REFERENCES `" + database + "`.`species`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	INDEX `PROCESS_ID`(`process_id` ASC) ,"
                 "	CONSTRAINT `PROCESS_ID_CS` FOREIGN KEY(`process_id`)"
                 "	REFERENCES `" + database + "`.`processes`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `LHSA_ID_CS` FOREIGN KEY(`lhsA_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `LHSB_ID_CS` FOREIGN KEY(`lhsB_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `RHSA_ID_CS` FOREIGN KEY(`rhsA_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `RHSB_ID_CS` FOREIGN KEY(`rhsB_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE "
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `" + database + "`.`csdata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `cs_id`(`cs_id` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`cs_id`)"
                 "		REFERENCES `" + database + "`.`cs`(`cs_id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE "
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `" + database + "`.`rate`("
                 "	`rate_id` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                 "	`specie_id` INT UNSIGNED NOT NULL, "
                 "	`process_id` INT UNSIGNED NOT NULL, "
                 "	`ref` VARCHAR(1000),"
                 "	`lhsA_id` INT UNSIGNED NULL ,"
                 "	`lhsB_id` INT UNSIGNED NULL ,"
                 "	`rhsA_id` INT UNSIGNED NULL ,"
                 "	`rhsB_id` INT UNSIGNED NULL ,"
                 "	`threshold` DOUBLE NULL ,"
                 "	`wavelength` DOUBLE NULL ,"
                 "	`lhs_v` INT NULL ,"
                 "	`rhs_v` INT NULL ,"
                 "	`lhs_j` INT NULL ,"
                 "	`rhs_j` INT NULL ,"
                 "	`background` VARCHAR(10000), "
                 "      `form` VARCHAR(100) NOT NULL, "
                 "	PRIMARY KEY(`RATE_ID`) ,"
                 "	INDEX `SPECIE_ID`(`specie_id` ASC) ,"
                 "	CONSTRAINT `SPECIE_ID_RATE` FOREIGN KEY(`specie_id`)"
                 "	REFERENCES `" + database + "`.`species`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	INDEX `PROCESS_ID`(`process_id` ASC) ,"
                 "	CONSTRAINT `PROCESS_ID_RATE` FOREIGN KEY(`process_id`)"
                 "	REFERENCES `" + database + "`.`processes`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `LHSA_ID_RATE` FOREIGN KEY(`lhsA_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `LHSB_ID_RATE` FOREIGN KEY(`lhsB_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `RHSA_ID_RATE` FOREIGN KEY(`rhsA_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE, "
                 "	CONSTRAINT `RHSB_ID_RATE` FOREIGN KEY(`rhsB_id`)"
                 "		REFERENCES `" + database + "`.`states`(`id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE "
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `" + database + "`.`ratedata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`rate_id` INT UNSIGNED NOT NULL ,"
                 "	`num` DOUBLE NOT NULL ,"
                 "	`constant` DOUBLE NOT NULL ,"
                 "	`lau` DOUBLE NOT NULL ,"
                 "	`uau` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `rate_id`(`rate_id` ASC) ,"
                 "	CONSTRAINT `RATE_ID_RATEDATA` FOREIGN KEY(`rate_id`)"
                 "		REFERENCES `" + database + "`.`rate`(`rate_id`)"
                 "  ON DELETE RESTRICT ON UPDATE CASCADE "
                 ");"
                 )

MYDB.commit()

MYCURSOR.execute("CREATE TABLE `" + database + "`.`models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
                 ");"
                 )

MYCURSOR.execute("CREATE TABLE `" + database + "`.`models2rate`("
                 "	`rate_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2rate (rate_id, model_id)"
                 ");"
                 )

MYDB.commit()

if ARGS.debug:
    print_timestep("created empty NEPC database and all tables")

#############
# Load data #
#############

if ARGS.debug:
    print_timestep("starting to load data into processes table")

PROCESSES_VARIABLE_LIST = ["id", "name", "long_name", "lhs", "rhs",
                           "lhs_e", "rhs_e", "lhs_hv", "rhs_hv",
                           "lhs_v", "rhs_v", "lhs_j", "rhs_j"]
INSERT_COMMAND_PROCESSES = insert_command("processes",
                                          PROCESSES_VARIABLE_LIST)
PROCESSES_DTYPE = {"id": int,
                   "name": str,
                   "long_name": str,
                   "lhs": int,
                   "rhs": int,
                   "lhs_e": int,
                   "rhs_e": int,
                   "lhs_hv": int,
                   "rhs_hv": int,
                   "lhs_v": int,
                   "rhs_v": int,
                   "lhs_j": int,
                   "rhs_j": int}
PROCESSES_FILE = NEPC_DATA + "processes.tsv"
PROCESSES_DATA_LIST = list(pd.read_csv(PROCESSES_FILE,
                                       sep='\t',
                                       dtype=PROCESSES_DTYPE,
                                       na_values=NA_VALUES).itertuples(
                                           index=False,
                                           name=None))
MYCURSOR.executemany(INSERT_COMMAND_PROCESSES, PROCESSES_DATA_LIST)
if ARGS.debug:
    print_timestep("loaded data into processes table")
    # print_table("processes")

MODELS_VARIABLE_LIST = ["model_id", "name", "long_name", "ref"]
INSERT_COMMAND_MODELS = insert_command("models",
                                       MODELS_VARIABLE_LIST)
MODELS_DTYPE = {"model_id": int,
                "name": str,
                "long_name": str,
                "ref": str}
MODELS_FILE = NEPC_DATA + "models.tsv"
MODELS_DATA_LIST = list(pd.read_csv(MODELS_FILE,
                                    sep='\t',
                                    dtype=MODELS_DTYPE,
                                    na_values=NA_VALUES).itertuples(
                                        index=False,
                                        name=None))
if ARGS.debug:
    print_timestep("loading data into models table")
    print(MODELS_DATA_LIST)
MYCURSOR.executemany(INSERT_COMMAND_MODELS, MODELS_DATA_LIST)
if ARGS.debug:
    print_timestep("loaded data into models table")
    print_table("models")

SPECIES_VARIABLE_LIST = ["id", "name", "long_name"]
INSERT_COMMAND_SPECIES = insert_command("species",
                                        SPECIES_VARIABLE_LIST)
SPECIES_DTYPE = {"id": int,
                 "name": str,
                 "long_name": str}
SPECIES_FILE = NEPC_DATA + "species.tsv"
SPECIES_DATA_LIST = list(pd.read_csv(SPECIES_FILE,
                                     sep='\t',
                                     dtype=SPECIES_DTYPE,
                                     na_values=NA_VALUES).itertuples(
                                         index=False,
                                         name=None))
MYCURSOR.executemany(INSERT_COMMAND_SPECIES, SPECIES_DATA_LIST)
if ARGS.debug:
    print_timestep("loaded data into species table")
    # print_table("species")

STATES_VARIABLE_LIST = ["id", "name", "long_name", "specie"]
INSERT_COMMAND_STATES = ("INSERT INTO states "
                         "SET "
                         "  id = %s, "
                         "  name = %s, "
                         "  long_name = %s, "
                         "  specie_id = (SELECT id FROM " + database + ".species "
                         "              WHERE NAME = %s);")

STATES_DTYPE = {"id": int,
                "name": str,
                "long_name": str,
                "specie": str}

STATES_FILE = NEPC_DATA + "states.tsv"
STATES_DATA_LIST = list(pd.read_csv(STATES_FILE,
                                    sep='\t',
                                    dtype=STATES_DTYPE,
                                    na_values=NA_VALUES).itertuples(
                                        index=False,
                                        name=None))
MYCURSOR.executemany(INSERT_COMMAND_STATES, STATES_DATA_LIST)
if ARGS.debug:
    print_timestep("loaded data into states table")
    # print_table("states")

if ARGS.debug:
    print_timestep("starting to load cross section data")


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
                    "threshold",
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
            "threshold": float,
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

UPDATE_COMMAND_CS = ("INSERT INTO cs " +
                     "SET "
                     "  cs_id = %s, "
                     "  units_e = %s, "
                     "  units_sigma = %s, "
                     "  ref = %s, "
                     "  threshold = %s, "
                     "  wavelength = %s, "
                     "  lhs_v = %s, "
                     "  rhs_v = %s, "
                     "  lhs_j = %s, "
                     "  rhs_j = %s, "
                     "  background = %s, "
                     "  lpu = %s, "
                     "  upu = %s, "
                     "  specie_id = (SELECT id FROM " + database + ".species "
                     "    WHERE NAME=%s), "
                     "  process_id = (select id from " + database + ".processes "
                     "    WHERE NAME=%s), "
                     "  lhsA_id = (select id from " + database + ".states "
                     "    WHERE NAME=%s), "
                     "  lhsB_id = (select id from " + database + ".states "
                     "    WHERE NAME=%s), "
                     "  rhsA_id = (select id from " + database + ".states "
                     "    WHERE NAME=%s), "
                     "  rhsB_id = (select id from " + database + ".states "
                     "    WHERE NAME=%s);")

INSERT_COMMAND_CSDATA = insert_command("csdata", CSDATA_VARIABLE_LIST)

INSERT_COMMAND_MODELS2CS = ("INSERT INTO models2cs "
                            "SET "
                            " cs_id=%s, "
                            " model_id=(SELECT model_id "
                            "           FROM " + database + ".models "
                            "           WHERE NAME=%s);")

file_number = 1
for directoryname in DIR_NAMES:
    if ARGS.debug:
        print_timestep('entering directory: {}'.format(directoryname))
    directory = os.fsencode(NEPC_DATA + directoryname)
    for file in os.listdir(directory):
        if file_number >= MAX_CS:
            print("WARNING: only processed " + str(file_number) +
                  " cross section files. There appears to be addtional "
                  "data not processed.")
            break
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

            met_data = pd.read_csv(met_file,
                                   sep='\t',
                                   dtype=CS_DTYPE,
                                   na_values=NA_VALUES)
            dat_data = pd.read_csv(dat_file,
                                   sep='\t',
                                   dtype=CSDATA_DTYPE,
                                   na_values=NA_VALUES)

            F_CS_DAT_FILE.write(
                "\t".join([str(met_data.iloc[0]['cs_id']),
                           directoryname + str(filename_wo_ext)]) + "\n"
            )

            MYCURSOR.execute(UPDATE_COMMAND_CS,
                             (int(met_data.iloc[0]['cs_id']),
                              met_data.iloc[0]['units_e'],
                              met_data.iloc[0]['units_sigma'],
                              met_data.iloc[0]['ref'],
                              met_data.iloc[0]['threshold'],
                              met_data.iloc[0]['wavelength'],
                              int(met_data.iloc[0]['lhs_v']),
                              int(met_data.iloc[0]['rhs_v']),
                              int(met_data.iloc[0]['lhs_j']),
                              int(met_data.iloc[0]['rhs_j']),
                              met_data.iloc[0]['background'],
                              met_data.iloc[0]['lpu'],
                              met_data.iloc[0]['upu'],
                              np_str(met_data, 0, 'specie'),
                              np_str(met_data, 0, 'process'),
                              np_str(met_data, 0, 'lhs_a'),
                              np_str(met_data, 0, 'lhs_b'),
                              np_str(met_data, 0, 'rhs_a'),
                              np_str(met_data, 0, 'rhs_b')))
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

MYDB.commit()
F_CS_DAT_FILE.close()

if ARGS.debug:
    print_timestep("loaded data into cs, csdata, and models2cs tables")
    # print_table("cs")

# DIR_NAMES = ["/data/rate/n2/peterson/"]
DIR_NAMES = []

if platform.node() == 'ppdadamsonlinux':
    RATE_DAT_FILENAME = NEPC_DATA + "rate_datfile_prod.tsv"
else:
    RATE_DAT_FILENAME = NEPC_DATA + "rate_datfile_local.tsv"

F_RATE_DAT_FILE = open(RATE_DAT_FILENAME, 'w')
F_RATE_DAT_FILE.write("\t".join(["rate_id", "filename"]) + "\n")

RATE_VARIABLE_LIST = ["rate_id", "specie_id", "process_id",
                      "ref",
                      "lhsA_id", "lhsB_id", "rhsA_id", "rhsB_id",
                      "threshold",
                      "wavelength",
                      "lhs_v", "rhs_v", "lhs_j", "rhs_j", "background",
                      "form"]
RATE_DTYPE = {"rate_id": int,
              "specie": str,
              "process": str,
              "ref": str,
              "lhs_a": str,
              "lhs_b": str,
              "rhs_a": str,
              "rhs_b": str,
              "threshold": float,
              "wavelength": float,
              "lhs_v": int,
              "rhs_v": int,
              "lhs_j": int,
              "rhs_j": int,
              "background": str,
              "form": str
              }
RATEDATA_VARIABLE_LIST = ["id", "rate_id", "num", "constant", "lau", "uau"]
RATEDATA_DTYPE = {"ratedata_id": int,
                  "num": int,
                  "constant": float,
                  "lau": float,
                  "uau": float}
MOD_DTYPE = {"model_name": str}

UPDATE_COMMAND_RATE = ("INSERT INTO rate " +
                       "SET "
                       "  rate_id = %s, "
                       "  ref = %s, "
                       "  threshold = %s, "
                       "  wavelength = %s, "
                       "  lhs_v = %s, "
                       "  rhs_v = %s, "
                       "  lhs_j = %s, "
                       "  rhs_j = %s, "
                       "  background = %s, "
                       "  form = %s, "
                       "  specie_id = (SELECT id FROM " + database + ".species "
                       "    WHERE NAME=%s), "
                       "  process_id = (select id from " + database + ".processes "
                       "    WHERE NAME=%s), "
                       "  lhsA_id = (select id from " + database + ".states "
                       "    WHERE NAME=%s), "
                       "  lhsB_id = (select id from " + database + ".states "
                       "    WHERE NAME=%s), "
                       "  rhsA_id = (select id from " + database + ".states "
                       "    WHERE NAME=%s), "
                       "  rhsB_id = (select id from " + database + ".states "
                       "    WHERE NAME=%s);")

INSERT_COMMAND_RATEDATA = insert_command("ratedata", RATEDATA_VARIABLE_LIST)

INSERT_COMMAND_MODELS2RATE = ("INSERT INTO models2rate "
                              "SET "
                              " rate_id=%s, "
                              " model_id=(SELECT model_id "
                              "           FROM " + database + ".models "
                              "           WHERE NAME=%s);")

file_number = 1
for directoryname in DIR_NAMES:
    directory = os.fsencode(NEPC_DATA + directoryname)
    for file in os.listdir(directory):
        if file_number >= MAX_RATE:
            print("WARNING: only processed " + str(file_number) +
                  " rate files. There appears to be addtional "
                  "data not processed.")
            break
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

            met_data = pd.read_csv(met_file,
                                   sep='\t',
                                   dtype=RATE_DTYPE,
                                   na_values=NA_VALUES)
            dat_data = pd.read_csv(dat_file,
                                   sep='\t',
                                   dtype=RATEDATA_DTYPE,
                                   na_values=NA_VALUES)

            F_RATE_DAT_FILE.write(
                "\t".join([str(met_data.iloc[0]['rate_id']),
                           directoryname + str(filename_wo_ext)]) + "\n"
            )

            MYCURSOR.execute(UPDATE_COMMAND_RATE,
                             (int(met_data.iloc[0]['rate_id']),
                              met_data.iloc[0]['ref'],
                              met_data.iloc[0]['threshold'],
                              met_data.iloc[0]['wavelength'],
                              int(met_data.iloc[0]['lhs_v']),
                              int(met_data.iloc[0]['rhs_v']),
                              int(met_data.iloc[0]['lhs_j']),
                              int(met_data.iloc[0]['rhs_j']),
                              met_data.iloc[0]['background'],
                              np_str(met_data, 0, 'form'),
                              np_str(met_data, 0, 'specie'),
                              np_str(met_data, 0, 'process'),
                              np_str(met_data, 0, 'lhs_a'),
                              np_str(met_data, 0, 'lhs_b'),
                              np_str(met_data, 0, 'rhs_a'),
                              np_str(met_data, 0, 'rhs_b')))
            dat_data.insert(1, 'rate_id', met_data.iloc[0]['rate_id'])
            dat_data_list = list(dat_data.itertuples(index=False,
                                                     name=None))
            MYCURSOR.executemany(INSERT_COMMAND_RATEDATA, dat_data_list)

            if os.path.exists(mod_file):
                mod_data = pd.read_csv(mod_file,
                                       sep='\t',
                                       dtype=MOD_DTYPE,
                                       na_values=NA_VALUES)
                mod_data.insert(0, 'rate_id', met_data.iloc[0]['rate_id'])
                mod_data_list = list(mod_data.itertuples(index=False,
                                                         name=None))
                MYCURSOR.executemany(INSERT_COMMAND_MODELS2RATE,
                                     mod_data_list)

            MYDB.commit()

MYDB.commit()
F_RATE_DAT_FILE.close()

if ARGS.debug:
    print_timestep("loaded data into rate, ratedata, and models2rate tables")
    # print_table("rate")

print_timestep("built " + database + " database")
for table in ["species", "processes", "states", "cs", "models",
              "models2cs", "csdata", "rate", "models2rate", "ratedata"]:
    print(table + ": " + str(nepc.count_table_rows(MYCURSOR, table)) +
          " rows")

####################
# Close connection #
####################

MYCURSOR.close()

MYDB.close()
