"""from nepc import nepc
import os
from nepc.util import config
import argparse
import platform
import pandas as pd

parser = argparse.ArgumentParser(description = 'Build test database used to check against the NEPC database.')
parser.add_argument('--debug', action='store_true', help='print additional debug info')

args = parser.parse_args()

if args.debug:
    import time
    t0 = time.time()

HOME = config.userHome()
NEPC_HOME = config.nepc_home()
NEPC_MYSQL = NEPC_HOME + "/mysql/"

mydb = mysql.connector.connect(
        host = 'localhost'
        option_files = HOME + '/.mysql/defaults'
)
mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS `test_nepc`;")
mycursor.execute("CREATE DATABASE IF NOT EXISTS `test_nepc` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")
mycursor.execute("SET default_storage_engine = INNODB;")

mycursor.execute("CREATE TABLE `test_nepc`.`test_species`("
                 "`test_id` INT UNSIGNED NOT NULL auto_increment ,"
                 "`test_name` VARCHAR(40) NOT NULL ,"
                 "`test_long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`test_id`)"
                 ");")

mycursor.execute("CREATE TABLE `test_nepc`.`test_processes`( "
                 "`test_id` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                 "`test_name` VARCHAR(40) NOT NULL, "
                 "`test_long_name` VARCHAR(240) NOT NULL, "
                 "`test_lhs` INT, "
                 "`test_rhs` INT, "
                 "`test_lhs_e` INT, "
                 "`test_rhs_e` INT, "
                 "`test_lhs_hv` INT, "
                 "`test_rhs_hv` INT, "
                 "`test_lhs_v` INT, "
                 "`test_rhs_v` INT, "
                 "`test_lhs_j` INT, "
                 "`test_rhs_j` INT, "
                 "PRIMARY KEY(`test_id`) "
                 ");"
                 )

mycursor.execute("CREATE TABLE `test_nepc`.`test_states`("
                 "	`test_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`test_specie_id` INT UNSIGNED NOT NULL ,"
                 "	`test_name` VARCHAR(100) NOT NULL ,"
                 "	`test_long_name` VARCHAR(100) NOT NULL ,"
                 "	`test_configuration` JSON NOT NULL ,"
                 "	PRIMARY KEY(`test_id`) ,"
                 "	INDEX `TEST_SPECIE_ID`(`test_specie_id` ASC) ,"
                 "	CONSTRAINT `test_specie_id_STATES` FOREIGN KEY(`test_specie_id`) "
                 "		REFERENCES `test_nepc`.`test_species`(`test_id`) " #not sure if I should change the references name here
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )


mycursor.execute("CREATE TABLE `test_nepc`.`test_models`("
                 "	`test_model_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`test_name` VARCHAR(40) NOT NULL ,"
                 "	`test_long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`test_model_id`)"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test_nepc`.`test_cs`("
                 "	`test_cs_id` INT UNSIGNED NOT NULL, "
                 "	`test_specie_id` INT UNSIGNED NOT NULL, "
                 "	`test_process_id` INT UNSIGNED NOT NULL, "
                 "	`test_units_e` DOUBLE NOT NULL,"
                 "	`test_units_sigma` DOUBLE NOT NULL,"
                 "	`test_ref` VARCHAR(1000),"
                 "	`test_lhsA_id` INT UNSIGNED NULL ,"
                 "	`test_lhsB_id` INT UNSIGNED NULL ,"
                 "	`test_rhsA_id` INT UNSIGNED NULL ,"
                 "	`test_rhsB_id` INT UNSIGNED NULL ,"
                 "	`test_wavelength` DOUBLE NULL ,"
                 "	`test_lhs_v` INT NULL ,"
                 "	`test_rhs_v` INT NULL ,"
                 "	`test_lhs_j` INT NULL ,"
                 "	`test_rhs_j` INT NULL ,"
                 "	`test_background` VARCHAR(10000) ,"
                 "	`test_lpu` DOUBLE NULL ,"
                 "	`test_upu` DOUBLE NULL ,"
                 "	PRIMARY KEY(`cs_id`) ,"
                 "	INDEX `TEST_SPECIE_ID`(`specie_id` ASC) ,"
                 "	INDEX `TEST_PROCESS_ID`(`process_id` ASC) ,"
                 "	CONSTRAINT `TEST_SPECIE_ID_CS` FOREIGN KEY(`test_specie_id`)"
                 "		REFERENCES `test_nepc`.`test_species`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `TEST_PROCESS_ID_CS` FOREIGN KEY(`test_process_id`)"
                 "		REFERENCES `test_nepc`.`test_processes`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `TEST_LHSA_ID_CS` FOREIGN KEY(`test_lhsA_id`)"
                 "		REFERENCES `test_nepc`.`test_states`(`id`),"
                 "	CONSTRAINT `TEST_LHSB_ID_CS` FOREIGN KEY(`test_lhsB_id`)"
                 "		REFERENCES `test_nepc`.`test_states`(`id`),"
                 "	CONSTRAINT `TEST_RHSA_ID_CS` FOREIGN KEY(`test_rhsA_id`)"
                 "		REFERENCES `test_nepc`.`test_states`(`id`),"
                 "	CONSTRAINT `TEST_RHSB_ID_CS` FOREIGN KEY(`test_rhsB_id`)"
                 "		REFERENCES `test_nepc`.`test_states`(`id`)"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test_nepc`.`test_csdata`("
                 "	`test_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`test_cs_id` INT UNSIGNED NOT NULL ,"
                 "	`test_e` DOUBLE NOT NULL ,"
                 "	`test_sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `TEST_CS_ID`(`test_cs_id` ASC) ,"
                 "	CONSTRAINT `TEST_CS_ID_CSDATA` FOREIGN KEY(`test_cs_id`)"
                 "		REFERENCES `test_nepc`.`test_cs`(`test_cs_id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test_nepc`.`test_models2cs`("
                 "	`test_cs_id` INT UNSIGNED NOT NULL ,"
                 "	`test_model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (test_cs_id, test_model_id)"
                 ");"
                 )
"""


