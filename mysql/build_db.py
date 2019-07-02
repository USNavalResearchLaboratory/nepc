import os
import mysql.connector
from nepc import nepc
from nepc.util import config
import argparse
import platform

parser = argparse.ArgumentParser(description='Build the NEPC database.')
parser.add_argument('--debug', action='store_true',
                    help='print additional debug info')
args = parser.parse_args()

if args.debug:
    import time
    t0 = time.time()

# TODO: add threshold table
# TODO: add reference table

HOME = config.userHome()
NEPC_HOME = config.nepc_home()

mydb = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS `nepc`;")
mycursor.execute("CREATE DATABASE IF NOT EXISTS `nepc`;")
mycursor.execute("SET default_storage_engine = INNODB;")


mycursor.execute("CREATE TABLE `nepc`.`species`("
                 "`id` INT UNSIGNED NOT NULL auto_increment ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

mycursor.execute("CREATE TABLE `nepc`.`processes`( "
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

mycursor.execute("CREATE TABLE `nepc`.`states`("
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

mycursor.execute("CREATE TABLE `nepc`.`models`("
                 "	`model_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

mycursor.execute("CREATE TABLE `nepc`.`cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL, "
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
                 "	PRIMARY KEY(`cs_id`) ,"
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

mycursor.execute("CREATE TABLE `nepc`.`csdata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `CS_ID`(`cs_id` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`cs_id`)"
                 "		REFERENCES `nepc`.`cs`(`cs_id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

mycursor.execute("CREATE TABLE `nepc`.`models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
                 ");"
                 )


#############
# Load data #
#############

# TODO: refactor code to read each type of file...standardize somehow...
# difficult to do given that electronic states differ

mycursor.execute("LOAD DATA LOCAL INFILE 'processes.tsv' "
                 "INTO TABLE nepc.processes "
                 "IGNORE 2 LINES;")

mycursor.execute("LOAD DATA LOCAL INFILE 'models.tsv' "
                 "INTO TABLE nepc.models;")

mycursor.execute("LOAD DATA LOCAL INFILE 'species.tsv' "
                 "INTO TABLE nepc.species;")

mycursor.execute("LOAD DATA LOCAL INFILE 'n_states.tsv'"
                 "	INTO TABLE nepc.states"
                 "	IGNORE 1 LINES"
                 "	(id,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p,name,long_name)"
                 "	SET configuration = JSON_OBJECT("
                 "		JSON_OBJECT('order', "
                 "			JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', "
                 "                     '3d', '4s', '4p')"
                 "		),"
                 "		JSON_OBJECT('occupations',"
                 "			JSON_OBJECT("
                 "				'2s',@2s,"
                 "				'2p',@2p,"
                 "				'CoreTerm',@CoreTerm,"
                 "				'3s',@3s,"
                 "				'3p',@3p,"
                 "				'3d',@3d,"
                 "				'4s',@4s,"
                 "				'4p',@4p"
                 "			)"
                 "		)"
                 "	),"
                 "	specie_id = (select max(id) from nepc.species "
                 "               where name = 'N');"
                 )

mycursor.execute("LOAD DATA LOCAL INFILE 'n+_states.tsv'"
                 "	INTO TABLE nepc.states"
                 "	IGNORE 1 LINES"
                 "	(id,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p,name,long_name)"
                 "	SET configuration = JSON_OBJECT("
                 "		JSON_OBJECT('order', "
                 "			JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', "
                 "                     '3d','4s', '4p')"
                 "		),"
                 "		JSON_OBJECT('occupations',"
                 "			JSON_OBJECT("
                 "				'2s',@2s,"
                 "				'2p',@2p,"
                 "				'CoreTerm',@CoreTerm,"
                 "				'3s',@3s,"
                 "				'3p',@3p,"
                 "				'3d',@3d,"
                 "				'4s',@4s,"
                 "				'4p',@4p"
                 "			)"
                 "		)"
                 "	),"
                 "	specie_id = (select max(id) from nepc.species"
                 "               where name = 'N+');"
                 )

mycursor.execute("LOAD DATA LOCAL INFILE 'n2_states.tsv'"
                 "	INTO TABLE nepc.states"
                 "	IGNORE 1 LINES"
                 "	(id,@o1,@o2,@o3,@o4,@o5,@o6,name,long_name)"
                 "	SET configuration = JSON_OBJECT("
                 "		JSON_OBJECT('order', "
                 "			JSON_ARRAY('2sigma_u', '1pi_u', '3sigma_g',"
                 "                     '1pi_g', '3sigma_u', '3ssigma_g')"
                 "		),"
                 "		JSON_OBJECT('occupations',"
                 "			JSON_OBJECT("
                 "				'2sigma_u',@o1,"
                 "				'1pi_u',@o2,"
                 "				'3sigma_g',@o3,"
                 "				'1pi_g',@o4,"
                 "				'3sigma_u',@o5,"
                 "				'3ssigma_g',@o6"
                 "			)"
                 "		)"
                 "	),"
                 "	specie_id = (select max(id) from nepc.species "
                 "               where name = 'N2');")

mycursor.execute("LOAD DATA LOCAL INFILE 'n2+_states.tsv' "
                 "INTO TABLE nepc.states "
                 "	IGNORE 1 LINES"
                 "	(id,@o1,@o2,@o3,@o4,@o5,@o6,name,long_name)"
                 "	SET configuration = JSON_OBJECT("
                 "		JSON_OBJECT('order', "
                 "			JSON_ARRAY('2sigma_u', '1pi_u', '3sigma_g', "
                 "                     '1pi_g', '3sigma_u', '3ssigma_g')"
                 "		),"
                 "		JSON_OBJECT('occupations',"
                 "			JSON_OBJECT("
                 "				'2sigma_u',@o1,"
                 "				'1pi_u',@o2,"
                 "				'3sigma_g',@o3,"
                 "				'1pi_g',@o4,"
                 "				'3sigma_u',@o5,"
                 "				'3ssigma_g',@o6"
                 "			)"
                 "		)"
                 "	),"
                 "	specie_id = (select max(id) from nepc.species "
                 "               where name = 'N2+');")

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

            mycursor.execute(executeTextCS)

            mycursor.execute(executeTextCSDATA)

            if os.path.exists(mod_file):
                mycursor.execute(executeTextCSMODELS)

            cs_id = cs_id + 1

f_cs_dat_file.close()

mydb.commit()

mycursor.execute("use nepc;")

# TODO: refactor to create function that prints details of database,
# querying the database for the tables contained therein and then
# summarizing the contents of each table
if args.debug:
    t1 = time.time()
    elapsed = t1-t0
    print("\nBuilt NEPC database in " + str(round(elapsed, 2)) + " sec:\n"
          "===============================================")
else:
    print("\nBuilt NEPC database:\n")

for table in ["species", "processes", "states", "cs", "models",
              "models2cs", "csdata"]:
    print(table +
          " has " + str(nepc.count_table_rows(mycursor, table)) +
          " lines")
print("===============================================\n")

mycursor.close()

mydb.close()
