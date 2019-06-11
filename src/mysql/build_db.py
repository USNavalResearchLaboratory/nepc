import os
from subprocess import check_output
import mysql.connector
import config
import nepc

DBUG = True

def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])

#TODO: add threshold table
#TODO: add reference table

HOME = config.userHome()

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

mycursor.execute("CREATE TABLE `nepc`.`processes`("
"	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
"	`name` VARCHAR(40) NOT NULL ,"
"	`long_name` VARCHAR(240) NOT NULL ,"
"	`lhs` INT,"
"	`rhs` INT,"
"	`lhs_e` INT,"
"	`rhs_e` INT,"
"	`lhs_hv` INT,"
"	`rhs_hv` INT,"
"	`lhs_v` INT,"
"	`rhs_v` INT,"
"	`lhs_j` INT,"
"	`rhs_j` INT,"
"	PRIMARY KEY(`id`)"
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


#################
### Load data ###
#################

mycursor.execute("LOAD DATA LOCAL INFILE 'processes.tsv'"
"	INTO TABLE nepc.processes"
"	IGNORE 2 LINES;")

mycursor.execute("LOAD DATA LOCAL INFILE 'models.tsv'"
"	INTO TABLE nepc.models;")

mycursor.execute("LOAD DATA LOCAL INFILE 'species.tsv'"
"	INTO TABLE nepc.species;")

mycursor.execute("LOAD DATA LOCAL INFILE 'n_states.tsv'"
"	INTO TABLE nepc.states"
"	IGNORE 1 LINES"
"	(id,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,name,long_name)"
"	SET configuration = JSON_OBJECT("
"		JSON_OBJECT('order', "
"			JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', '3d','4s')"
"		),"
"		JSON_OBJECT('occupations',"
"			JSON_OBJECT("
"				'2s',@2s,"
"				'2p',@2p,"
"				'CoreTerm',@CoreTerm,"
"				'3s',@3s,"
"				'3p',@3p,"
"				'3d',@3d,"
"				'4s',@4s"
"			)"
"		)"
"	),"
"	specie_id = (select max(id) from nepc.species where name = 'N');"
)

mycursor.execute("LOAD DATA LOCAL INFILE 'n+_states.tsv'"
"	INTO TABLE nepc.states"
"	IGNORE 1 LINES"
"	(id,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,name,long_name)"
"	SET configuration = JSON_OBJECT("
"		JSON_OBJECT('order', "
"			JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', '3d','4s')"
"		),"
"		JSON_OBJECT('occupations',"
"			JSON_OBJECT("
"				'2s',@2s,"
"				'2p',@2p,"
"				'CoreTerm',@CoreTerm,"
"				'3s',@3s,"
"				'3p',@3p,"
"				'3d',@3d,"
"				'4s',@4s"
"			)"
"		)"
"	),"
"	specie_id = (select max(id) from nepc.species where name = 'N+');"
)

mycursor.execute("LOAD DATA LOCAL INFILE 'n2_states.tsv'"
"	INTO TABLE nepc.states"
"	IGNORE 1 LINES"
"	(id,@o1,@o2,@o3,@o4,@o5,@o6,name,long_name)"
"	SET configuration = JSON_OBJECT("
"		JSON_OBJECT('order', "
"			JSON_ARRAY('2sigma_u', '1pi_u', '3sigma_g', '1pi_g', '3sigma_u', '3ssigma_g')"
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
"	specie_id = (select max(id) from nepc.species where name = 'N2');")

mycursor.execute("LOAD DATA LOCAL INFILE 'n2+_states.tsv' "
                 "INTO TABLE nepc.states "
"	IGNORE 1 LINES"
"	(id,@o1,@o2,@o3,@o4,@o5,@o6,name,long_name)"
"	SET configuration = JSON_OBJECT("
"		JSON_OBJECT('order', "
"			JSON_ARRAY('2sigma_u', '1pi_u', '3sigma_g', '1pi_g', '3sigma_u', '3ssigma_g')"
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
"	specie_id = (select max(id) from nepc.species where name = 'N2+');")

directorynames = [HOME + "/projects/nepc/data/formatted/n2/itikawa/",
                  HOME + "/projects/nepc/data/formatted/n2/zipf/"]

cs_id = 1
cs_lines = 0
for directoryname in directorynames:
    directory = os.fsencode(directoryname)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename_wo_ext = filename.rsplit(".", 1)[0]
        if filename.endswith(".met") or filename.endswith(".mod"):
            continue
        else:
            cs_lines += wc(directoryname + filename)
            #print(filename + ": " + str(file_lines))

            executeTextCS = ("LOAD DATA LOCAL INFILE '" + directoryname +
                             filename_wo_ext + ".met' INTO TABLE nepc.cs "
                             "(@temp,@specie,@process,units_e,units_sigma,ref,@lhsA,@lhsB,@rhsA,@rhsB,wavelength,lhs_v,rhs_v,lhs_j,rhs_j,background,lpu,upu) "
                             "SET cs_id = " + str(cs_id) + ", "
                             "specie_id = (select id from nepc.species where name = @specie), "
                             "process_id = (select id from nepc.processes where name = @process), "
                             "lhsA_id = (select id from nepc.states where name LIKE @lhsA), "
                             "lhsB_id = (select id from nepc.states where name LIKE @lhsB), "
                             "rhsA_id = (select id from nepc.states where name LIKE @rhsA), "
                             "rhsB_id = (select id from nepc.states where name LIKE @rhsB);")

            executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + directoryname +
                                   filename_wo_ext + ".mod' INTO TABLE nepc.models2cs "
                                   "(@model) "
                                   "SET cs_id = " + str(cs_id) + ", "
                                   "model_id = (select model_id from nepc.models where name LIKE @model);")

            executeTextCSDATA = ("LOAD DATA LOCAL INFILE '" + directoryname +
                                 filename_wo_ext + ".dat' INTO TABLE nepc.csdata "
                                 "(id,e,sigma) "
                                 "SET cs_id = " + str(cs_id) + ";")

            mycursor.execute(executeTextCS)

            mycursor.execute(executeTextCSDATA)

            if os.path.exists(directoryname + filename_wo_ext + '.mod'):
                mycursor.execute(executeTextCSMODELS)

            cs_id = cs_id + 1


mydb.commit()

mycursor.execute("use nepc;")

#nepc.print_table(mycursor, "species")
#nepc.print_table(mycursor, "processes")
#nepc.print_table(mycursor, "states")
#nepc.print_table(mycursor, "cs")
#nepc.print_table(mycursor, "models")
#nepc.print_table(mycursor, "models2cs")
#printTable(mycurcor, "csdata")

if DBUG:
    #TODO: perhaps do testing in a more elegant way

    def test_lines_equals_rows(lines, table):
        "test that all of the lines in cs datafiles made it to the cs table"
        assert lines == nepc.count_table_rows(mycursor, table), table + ": failed"
        return table + ": passed"

    print(test_lines_equals_rows(cs_lines, 'csdata'))

mycursor.close()

mydb.close()
