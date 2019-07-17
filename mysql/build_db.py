import os
import mysql.connector
from nepc import nepc
from nepc.util import config
import argparse
import platform
import pandas as pd
#temporary
import pytest
parser = argparse.ArgumentParser(description='Build the NEPC database.')
parser.add_argument('--debug', action='store_true',
                    help='print additional debug info')
args = parser.parse_args()

if args.debug:
    import time
    t0 = time.time()

# TODO: add threshold table
# TODO: add reference table

HOME = config.home/nehakrispykreme
NEPC_HOME = config.home/nehakrispykreme/projects/nepc/nehawork
NEPC_MYSQL = NEPC_HOME + "/mysql/"

mydb = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS `nepc`;")
mycursor.execute("CREATE DATABASE IF NOT EXISTS `nepc` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")
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

def getKeys(di):
    li = []
    for k, v in di:
        li.append(k)
    return li
def getValues(di):
    li = []
    for k, v in di:
        li.append(v)
    return li

#############
# Load data #
#############

# TODO: refactor code to read each type of file...standardize somehow... - became standardized to a degree
# difficult to do given that electronic states differ
nonstates = ["processes", "models", "states"]
states = ["/n_states.tsv'", "/n+_states.tsv'", "/n++_states.tsv'", "/n2+_states.tsv'", "/n2_states.tsv'"]
beg_exec = '' #beginning statement to execute, used to make code shorter + more readable
for i in nonstates:
    beg_exec = beg_exec + "LOAD DATA LOCAL INFILE'" + NEPC_MYSQL + '"/' + i + ".tsv' "
            "INTO TABLE " + "nepc." + i
    if i == 'models':
        beg_exec = beg_exec + "IGNORE 2 LINES"
mycursor.execute(beg_exec) #query created earlier executed
for i in states:
    mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + i +
                 "	INTO TABLE nepc.states"
                 "	IGNORE 1 LINES"
                 "	(id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)"
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
                 "               where name = i[1:2].upper());"
                 )
mydb.commit()

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
            #lists all of the headers used for met, mod and dat files
            met_cols = ['@temp', '@specie', '@process', 'units_e', 'units_sigma', 'ref', '@lhsA', '@lhsB', '@rhsA', '@rhsB', 'wavelength', 'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j', 'background', 'lpu', 'upu']
            dat_cols = ['id', 'e', 'sigma']
            #lists types of files - a list of lists will be used
            dat_dict = {dat_file:dat_cols}
            met_dict = {met_file:met_cols}
            filetype = [{met_dict:'nepc.cs'}, {dat_dict:'nepc.csdata'}]  #executemany has been shown to work for lists of dictionaries - unsure of if this would work with lists of dictionaries containing lists and dictionaries within them
            exCS = ("LOAD DATA LOCAL INFILE '" + getKeys(filetype) +  #FIXME: instead of using filetype[0], actually find a way to iterate through the file so that executemany will work 
                    "' INTO TABLE  " + getValues(filetype) + 
                    "IGNORE 1 LINES "
                    "(filetype.getKeys().getValues()) " 
                    "SET cs_id = " + str(cs_id) + ", ") #should take in all of the headers as listed as values in dat_dict and met_dict
            
            atSign = []
            for key, val in filetype:
                for k, v in key:
                    if ('@' in key.get(k)):
                       atSign.append(v)
            if (len(atSign) == 0):
                exCS = exCS + ";"
            for i in range(0, len(atSign)):
                if atSign[i] == '@lhsA' or atSign[i] == '@rhsA' or atSign[i] == '@lhsB' or atSign[i] == '@rhsB':
                    exCS = exCS + "(" + atSign[i][1:atSign[i].index("_")] + " id = (select id from nepc.states "
                    "  where name LIKE " + atSign[i] + ")"
                else:
                    exCS = exCS + "(" + atSign[i][1:atSign[i].index("_")] + " id = (select id from nepc." + atSign[i][1:atSign[i].index("_")]
                    "  where name = " + atSign[i] + ")"
                if i == len(atSign) - 1:
                    exCS = exCS + ","
                else:
                    exCS = exCS + ";"

            executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + mod_file +
                                   "' INTO TABLE nepc.models2cs "
                                   "(@model) "
                                   "SET cs_id = " + str(cs_id) + ", "
                                   "model_id = (select model_id "
                                   "            from nepc.models "
                                   "            where name LIKE @model);")
            
            mycursor.executemany(exCS, filetype)

            if os.path.exists(mod_file):
                mycursor.execute(executeTextCSMODELS)

            cs_id = cs_id + 1

f_cs_dat_file.close()

mydb.commit()

mycursor.execute("use nepc;")

# TODO: refactor to create function that prints details of database,
# querying the database for the tables contained therein and then
# summarizing the contents of each table

def table_exists (tablename):
    mycursor.execute("""
        SELECT COUNT (*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'','\'\'')))
    if mycursor.fetchone()[0] == 1:
        return True
    return False

    
def contents_of_db():
    for table in ["species", "processes", "states", "cs", "models", "models2cs", "csdata"]:
        if table_exists(table):
            print (table + " has " + str(nepc.count_table_rows(mycursor, table)) + " lines")
        print("===============================================\n")
       

  
if args.debug:
    t1 = time.time()
    elapsed = t1-t0
    print("\nBuilt NEPC database in " + str(round(elapsed, 2)) + " sec:\n"
          "===============================================")
else:
    print("\nBuilt NEPC database:\n")

contents_of_db()

#CREATE NEPC TEST DATABASE
mycursor.execute("DROP DATABASE IF EXISTS `test`;")
mycursor.execute("CREATE DATABASE IF NOT EXISTS `test` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")
mycursor.execute("SET default_storage_engine = INNODB;") 

mycursor.execute("CREATE TABLE `test`.`test_species`("
                 "`id` INT UNSIGNED NOT NULL auto_increment ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

mycursor.execute("CREATE TABLE `test`.`test_processes`( "
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

mycursor.execute("CREATE TABLE `test`.`test_states`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`specie_id` INT UNSIGNED NOT NULL ,"
                 "	`name` VARCHAR(100) NOT NULL ,"
                 "	`long_name` VARCHAR(100) NOT NULL ,"
                 "	`configuration` JSON NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `SPECIE_ID`(`specie_id` ASC) ,"
                 "	CONSTRAINT `specie_id_STATES` FOREIGN KEY(`specie_id`) "
                 "		REFERENCES `test`.`test_species`(`id`) "
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test`.`test_models`("
                 "	`model_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test`.`test_cs`("
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
                 "		REFERENCES `test`.`test_species`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `PROCESS_ID_CS` FOREIGN KEY(`process_id`)"
                 "		REFERENCES `test`.`test_processes`(`id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE,"
                 "	CONSTRAINT `LHSA_ID_CS` FOREIGN KEY(`lhsA_id`)"
                 "		REFERENCES `test`.`test_states`(`id`),"
                 "	CONSTRAINT `LHSB_ID_CS` FOREIGN KEY(`lhsB_id`)"
                 "		REFERENCES `test`.`test_states`(`id`),"
                 "	CONSTRAINT `RHSA_ID_CS` FOREIGN KEY(`rhsA_id`)"
                 "		REFERENCES `test`.`test_states`(`id`),"
                 "	CONSTRAINT `RHSB_ID_CS` FOREIGN KEY(`rhsB_id`)"
                 "		REFERENCES `test`.`test_states`(`id`)"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test`.`test_csdata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `CS_ID`(`cs_id` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`cs_id`)"
                 "		REFERENCES `test`.`test_cs`(`cs_id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test`.`test_models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
                 ");"
                 )
#establishes an identical copy of the data in 'nepc' database for testing later on
cat = ["species", "processes", "states", "cs", "models", "models2cs", "csdata"]
for t in cat:
    mycursor.execute ("SELECT * FROM nepc.dbo." + t)
    mycursor.execute("CREATE TABLE " + t + " LIKE" + "test_" + t)
    stmt = "SELECT * INTO nepc.dbo." + t_cop + "from test.dbo." + t
    mycursor.execute (stmt)

#############
# Load data #
#############

# TODO: refactor code to read each type of file...standardize somehow...
# difficult to do given that electronic states differ

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/processes.tsv' "
                 "INTO TABLE test.processes "
                 "IGNORE 2 LINES;")

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/models.tsv' "
                 "INTO TABLE test.models;")

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/species.tsv' "
                 "INTO TABLE test.species;")

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/n_states.tsv'"
                 "	INTO TABLE test.states"
                 "	IGNORE 1 LINES"
                 "	(id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)"
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
                 "	specie_id = (select max(id) from test.species "
                 "               where name = 'N');"
                 )

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/n+_states.tsv'"
                 "	INTO TABLE test.states"
                 "	IGNORE 1 LINES"
                 "	(id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)"
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
                 "	specie_id = (select max(id) from test.species"
                 "               where name = 'N+');"
                 )

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/n++_states.tsv'"
                 "	INTO TABLE test.states"
                 "	IGNORE 1 LINES"
                 "	(id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)"
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
                 "	specie_id = (select max(id) from test.species"
                 "               where name = 'N++');"
                 )

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/n2_states.tsv'"
                 "	INTO TABLE test.states"
                 "	IGNORE 1 LINES"
                 "	(id,name,long_name,@o1,@o2,@o3,@o4,@o5,@o6)"
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
                 "	specie_id = (select max(id) from test.species "
                 "               where name = 'N2');")

mydb.commit()

mycursor.execute("LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + "/n2+_states.tsv' "
                 "INTO TABLE test.states "
                 "	IGNORE 1 LINES"
                 "	(id,name,long_name,@o1,@o2,@o3,@o4,@o5,@o6)"
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
                 "	specie_id = (select max(id) from test.species "
                 "               where name = 'N2+');")

mydb.commit()

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
                             "' INTO TABLE test.cs "
                             "IGNORE 1 LINES "
                             "(@temp,@specie,@process,units_e,units_sigma,"
                             "ref,@lhsA,@lhsB,@rhsA,@rhsB,wavelength,lhs_v,"
                             "rhs_v,lhs_j,rhs_j,background,lpu,upu) "
                             "SET cs_id = " + str(cs_id) + ", "
                             "specie_id = (select id from test.species "
                             "  where name = @specie), "
                             "process_id = (select id from test.processes "
                             "  where name = @process), "
                             "lhsA_id = (select id from test.states "
                             "  where name LIKE @lhsA), "
                             "lhsB_id = (select id from test.states "
                             "  where name LIKE @lhsB), "
                             "rhsA_id = (select id from test.states "
                             "  where name LIKE @rhsA), "
                             "rhsB_id = (select id from test.states "
                             "  where name LIKE @rhsB);")

            executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + mod_file +
                                   "' INTO TABLE test.models2cs "
                                   "(@model) "
                                   "SET cs_id = " + str(cs_id) + ", "
                                   "model_id = (select model_id "
                                   "            from test.models "
                                   "            where name LIKE @model);")

            executeTextCSDATA = ("LOAD DATA LOCAL INFILE '" + dat_file +
                                 "' INTO TABLE test.csdata "
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

mycursor.execute("use test;")

# TODO: refactor to create function that prints details of database,
# querying the database for the tables contained therein and then
# summarizing the contents of each table
if args.debug:
    t1 = time.time()
    elapsed = t1-t0
    print("\nBuilt TEST database in " + str(round(elapsed, 2)) + " sec:\n"
          "===============================================")
else:
    print("\nBuilt TEST database:\n")

for table in ["species", "processes", "states", "cs", "models",
              "models2cs", "csdata"]:
    print(table +
          " has " + str(nepc.count_table_rows(mycursor, table)) +
          " lines")
print("===============================================\n")
def table_exists (tablename):  #based off of answer on Stack Overflow - hope it works
    mycursor.execute("""
        SHOW TABLES LIKE 'tablename'""")
    if mycursor.fetchone() == True:
        return True
    return False


def test_same_number_of_rows(local,dbug): #check to see if each table in both databases contain the same number of rows
    test_num = 0
    tst = ["test_species", "test_processes", "test_states", "test_cs", "test_models", "test_models2cs", "test_csdata"]
    noeq = 0
    for i in range (0, len(tst)-1):
        tnum = nepc.count_table_rows(mycursor, tst[i])
        num = nepc.count_table_rows(mycursor, cat[i])
        if tnum == num:
            noeq = noeq + 1
    assert noeq == len(tst)


def test_same_number_of_tables(local, dbug): #checks to see if both databases contain the same number of tables
    test_num = 0
    #TEST DATABASE
    for table in ["test_species", "test_processes", "test_states", "test_cs", "test_models", "test_models2cs", "test_data"]:
        if table_exists(table):
            test_num = test_num + 1
        else:
            continue
    #NEPC DATABASE
    for t in ["species", "processes", "states", "cs", "models", "models2cs", "csdata"]:
        if table_exists(t):
            db_num = db_num + 1
        else:
            continue
    assert test_num == db_num

def test_same_values(local, dbug): #check to see that each table in the test database is equivalent to each table in the nepc database
    test_num = 0
    tst = ["test_species", "test_processes", "test_states", "test_cs", "test_models", "test_models2cs", "test_csdata"]
    for i in range (0, len(tst)-1):
        ident = table_as_df(mycursor, tst[i]).equals(table_as_df(mycursor, cat[i]))
    assert ident == True

mycursor.close()

mydb.close()
