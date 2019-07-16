import os
import mysql.connector
from nepc import nepc
from nepc.util import config
import argparse
import platform
import pandas as pd
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

for i in range(0, len(nonstates)):
    mycursor.execute("LOAD DATA LOCAL INFILE'" + NEPC_MYSQL + '"/' + nonstates[i] + ".tsv' "
            "INTO TABLE " + "nepc." + nonstates[i])
    if i == 1:
        mycursor.execute("LOAD DATA LOCAL INFILE" + NEPC_MYSQL + '"/' + nonstates[i] + ".tsv' "
            		 "INTO TABLE " + "nepc." + nonstates[i] +
            	         "IGNORE 2 LINES")
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
            mod_cols['@model']
            #lists types of files - a list of lists will be used
            mod_dict = {mod_file: mod_cols}
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

mycursor.close()

mydb.close()
