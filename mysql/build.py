"""Builds the NEPC database"""
import argparse
import platform
import os
import mysql.connector
from nepc import nepc
from nepc.util import config
from nepc.util import scraper

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

########################
# Connect to database
########################
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

MYCURSOR.execute("CREATE TABLE `nepc`.`models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
                 ");"
                 )

#############
# Load data #
#############

TABLES = ["processes", "models", "species"]

for table in TABLES:
    MYCURSOR.execute("LOAD DATA LOCAL INFILE '" + NEPC_DATA + table + ".tsv' "
                     "INTO TABLE nepc." + table + " IGNORE 1 LINES;")

MYDB.commit()

MYCURSOR.execute("LOAD DATA LOCAL INFILE '" + NEPC_DATA + "/states.tsv' "
                 "INTO TABLE nepc.states "
                 "IGNORE 1 LINES "
                 "(id,@specie,name,long_name) "
                 "set specie_id = (select max(id) from nepc.species where name like @specie);")

MYDB.commit()

DIR_NAMES = ["/data/cs/n2/itikawa/",
             "/data/cs/n2/zipf/",
             "/data/cs/n/zatsarinny/"]

if platform.node() == 'ppdadamsonlinux':
    CS_DAT_FILENAME = NEPC_DATA + "cs_datfile_prod.tsv"
else:
    CS_DAT_FILENAME = NEPC_DATA + "cs_datfile_local.tsv"

F_CS_DAT_FILE = open(CS_DAT_FILENAME, 'w')
F_CS_DAT_FILE.write("\t".join(["cs_id", "filename"]) + "\n")

for directoryname in DIR_NAMES:
    directory = os.fsencode(NEPC_HOME + directoryname)

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

        CS_ID = scraper.get_cs_id_from_met_file(met_file)

        if filename.endswith(".met") or filename.endswith(".mod"):
            continue
        else:
            F_CS_DAT_FILE.write(
                "\t".join([str(CS_ID),
                           directoryname + str(filename_wo_ext)]) + "\n"
            )
            executeTextCS = ("LOAD DATA LOCAL INFILE '" + met_file +
                             "' INTO TABLE nepc.cs "
                             "IGNORE 1 LINES "
                             "(cs_id,@specie,@process,units_e,units_sigma,"
                             "ref,@lhsA,@lhsB,@rhsA,@rhsB,wavelength,lhs_v,"
                             "rhs_v,lhs_j,rhs_j,background,lpu,upu) "
                             "SET cs_id = " + str(CS_ID) + ", "
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
                                   "SET cs_id = " + str(CS_ID) + ", "
                                   "model_id = (select model_id "
                                   "            from nepc.models "
                                   "            where name LIKE @model);")

            executeTextCSDATA = ("LOAD DATA LOCAL INFILE '" + dat_file +
                                 "' INTO TABLE nepc.csdata "
                                 "IGNORE 1 LINES "
                                 "(id,e,sigma) "
                                 "SET cs_id = " + str(CS_ID) + ";")

            MYCURSOR.execute(executeTextCS)

            MYCURSOR.execute(executeTextCSDATA)

            if os.path.exists(mod_file):
                MYCURSOR.execute(executeTextCSMODELS)

F_CS_DAT_FILE.close()

MYDB.commit()


if ARGS.debug:
    T1 = time.time()
    ELAPSED = T1-T0
    print("\nBuilt NEPC database in " + str(round(ELAPSED, 2)) + " sec\n"
          "===============================================")
    for table in ["species", "processes", "states", "cs", "models", "models2cs", "csdata"]:
        print(table + " has " + str(nepc.count_table_rows(MYCURSOR, table)) + " rows")
        print("===============================================\n")
else:
    print("\nBuilt NEPC database\n")


MYCURSOR.close()

MYDB.close()
