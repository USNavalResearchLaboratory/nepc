from nepc import nepc
from nepc.util import config
from nepc.util import scraper
import pandas as pd
import mysql.connector
import argparse
from pandas.util.testing import assert_frame_equal
import os
import pytest
import platform
# TODO: remove dependence on csv; put function in scraper that uses built-in
#       readlines function
import csv
#====================BUILDING THE TEST DATABASE=======================
parser = argparse.ArgumentParser(description='Build the test database.')
parser.add_argument('--debug', action='store_true',
                    help='print additional debug info')
args = parser.parse_args()

if args.debug:
    import time
    t0 = time.time()

# TODO: test that all values in [nepc]/data are in the nepc database

NEPC_HOME = config.nepc_home()

DIR_NAMES = [NEPC_HOME + "/data/formatted/n2/itikawa/",
             NEPC_HOME + "/data/formatted/n2/zipf/",
             NEPC_HOME + "/data/formatted/n/zatsarinny/"]

HOME = config.userHome()
NEPC_HOME = config.nepc_home()
NEPC_MYSQL = NEPC_HOME + "/mysql/"

mydb = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS `test`;")
mycursor.execute("CREATE DATABASE IF NOT EXISTS `test` "
                 "CHARACTER SET utf8 "
                 "COLLATE utf8_general_ci;")

mycursor.execute("SET default_storage_engine = INNODB;")
mycursor.execute ("use test;")

mycursor.execute("CREATE TABLE `test`.`species`("
                 "`id` INT UNSIGNED NOT NULL auto_increment ,"
                 "`name` VARCHAR(40) NOT NULL ,"
                 "`long_name` VARCHAR(100) NOT NULL ,"
                 "PRIMARY KEY(`id`)"
                 ");")

mycursor.execute("CREATE TABLE `test`.`processes`( "
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


mycursor.execute("CREATE TABLE `test`.`states`("
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
mycursor.execute("CREATE TABLE `test`.`models`("
                 "	`model_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,"
                 "	`name` VARCHAR(40) NOT NULL ,"
                 "	`long_name` VARCHAR(240) NOT NULL ,"
                 "	PRIMARY KEY(`model_id`)"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test`.`cs`("
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

mycursor.execute("CREATE TABLE `test`.`csdata`("
                 "	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`e` DOUBLE NOT NULL ,"
                 "	`sigma` DOUBLE NOT NULL ,"
                 "	PRIMARY KEY(`id`) ,"
                 "	INDEX `CS_ID`(`cs_id` ASC) ,"
                 "	CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`cs_id`)"
                 "		REFERENCES `test`.`cs`(`cs_id`)"
                 "		ON DELETE RESTRICT ON UPDATE CASCADE"
                 ");"
                 )

mycursor.execute("CREATE TABLE `test`.`models2cs`("
                 "	`cs_id` INT UNSIGNED NOT NULL ,"
                 "	`model_id` INT UNSIGNED NOT NULL ,"
                 "	PRIMARY KEY pk_models2cs (cs_id, model_id)"
                 ");"
                 )
def broad_cats():
    return ["processes", "models", "species"]

def print_list_elems(lst):
    answer = ''
    for i in lst:
        if i != lst[len(lst)-1]:
            answer = answer + i + ","
        else:
            answer = answer + i
    return answer

def met_headers():
    return ['@temp', '@specie', '@process', 'units_e', 'units_sigma', 'ref', '@lhsA', '@lhsB', '@rhsA', '@rhsB', 'wavelength', 'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j', 'background', 'lpu', 'upu']

def dat_headers():
    return ['id', 'e', 'sigma']

def all_headers():
    total_heads = met_headers()
    for i in dat_headers():
        total_heads.append(i)
    return total_heads

def number_of_columns():
    return len(all_headers())

def noOfFileTypes():
    return 2 #for dat and met

def construct_headers(column):
    if column in met_headers:
        return (met_file, "cs", column)
    elif column in dat_headers:
        return (dat_file, "csdata", column)

def multi_iteration(results):
    if args.debug:
        print (results)
    for cur in results:
        print('cursor:', cur)
        if cur.with_rows:
            print('results:', cur.fetchall())


def broad_cats():
    return ["processes", "models", "species"]


n_states = ["/n_states.tsv'", "/n+_states.tsv'", "/n++_states.tsv'"]
n2_states = ["/n2+_states.tsv'", "/n2_states.tsv'"]
beg_exec = '' #beginning statement to execute, used to make code shorter + more readable
for i in broad_cats():
    beg_exec = beg_exec + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + i + ".tsv' " + "\nINTO TABLE " + "test." + i
    if i == 'processes':
        beg_exec = beg_exec + " " + "\nIGNORE 2 LINES;"
    else:
        beg_exec = beg_exec + ";"
if args.debug:
    print(beg_exec)
results = mycursor.execute(beg_exec, multi = True) #query created earlier executed
multi_iteration(results)
state_query = ''
for i in n_states:
    state_query = (state_query + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + i + "    INTO TABLE test.states" + "     IGNORE 1 LINES" + "      (id,name,long_name,@2s,@2p,@CoreTerm,@3s,@3p,@3d,@4s,@4p)" + "      SET configuration = JSON_OBJECT(" + "          JSON_OBJECT('order', " + "              JSON_ARRAY('2s', '2p', 'CoreTerm', '3s', '3p', " + "              '3d', '4s', '4p')" + "              )," + "          JSON_OBJECT('occupations'," + "          JSON_OBJECT(" + "				'2s',@2s," + "				'2p',@2p," + "				'CoreTerm',@CoreTerm," + "				'3s',@3s," + "				'3p',@3p," + "				'3d',@3d," + "				'4s',@4s," + "				'4p',@4p" + "			)" + "		)" + "	)," + "	specie_id = (select max(id) from test.species " + "               where name = " + "'" + i[1:i.index('_')].upper() + "'" + ");")
for i in n2_states:
    state_query = (state_query + "LOAD DATA LOCAL INFILE '" + NEPC_MYSQL + i + "    INTO TABLE test.states" + "     IGNORE 1 LINES" + "      (id,name,long_name,@o1,@o2,@o3,@o4,@o5,@o6)" + "      SET configuration = JSON_OBJECT(" + "          JSON_OBJECT('order', " + "              JSON_ARRAY('2sigma_u', '1pi_u', '1pi_g', '3sigma_u', '3ssigma_g')" + "              )," + "          JSON_OBJECT('occupations'," + "          JSON_OBJECT(" + "				'2sigma_u',@o1," + "				'1pi_u',@o2," + "				'3sigma_g',@o3," + "				'1pi_g',@o4," + "				'3sigma_u',@o5," + "				'3ssigma_g',@o6" + "			)" + "		)" + "	)," + "	specie_id = (select max(id) from test.species " + "               where name = " + "'" + i[1:i.index('_')].upper() + "'" + ");") 
state_results = mycursor.execute(state_query, multi = True)
multi_iteration(state_results)
mydb.commit()

if platform.node() == 'ppdadamsonlinux':
    cs_dat_filename = "cs_datfile_prod.tsv"
else:
    cs_dat_filename = "cs_datfile_local.tsv"

f_cs_dat_file = None 
f_cs_dat_file = open(cs_dat_filename, 'w')
f_cs_dat_file.write("\t".join(["cs_id", "filename"]) + "\n")

cs_id = 1

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
            f_cs_dat_file.write(
                    "\t".join([str(cs_id),
                           directoryname + str(filename_wo_ext)]) + "\n"
            )

        filetype = [met_file, dat_file]
        tablename = ['cs', 'csdata']
        for i in range (0, noOfFileTypes()):
            exCS = '' + ("LOAD DATA LOCAL INFILE '" + filetype[i]+ "' INTO TABLE  " + "test." + tablename[i] + " IGNORE 1 LINES ")
            if filetype[i] == met_file:
                exCS = (exCS + "(" + print_list_elems(met_headers()) + ") "
                "SET cs_id = " + str(cs_id) + ", ") #should take in all of the headers as listed as values in dat_dict and met_dict
                atSign = []
                for i in met_headers():
                    if ('@' in i and i != '@temp'):
                        atSign.append(i)
                    if (len(atSign) == 0 and i == met_headers()[1]): #disregards @temp here
                        exCS = exCS + ";"
                for i in range(0, len(atSign)):
                    if atSign[i] == '@lhsA' or atSign[i] == '@rhsA' or atSign[i] == '@lhsB' or atSign[i] == '@rhsB':
                        exCS = exCS + atSign[i][1:] + "_id = (select id from test.states  where name LIKE " + atSign[i] + ")"
                        if i != len(atSign) - 1:
                            exCS = exCS + ", "
                        else: 
                            exCS = exCS + ";"
                            if args.debug:
                                print (exCS)
                    elif atSign[i] == '@process':
                        exCS = (exCS + atSign[i][1:] + "_id = (select id from test." + atSign[i][1:] + "es" + "  where name = " + atSign[i]+ ")")
                        if i != len(atSign) - 1: 
                            exCS = exCS + ", "
                            #mycursor.execute("print n 'process_id'")
                        else: 
                            exCS = exCS + ";"

                    elif atSign[i] != '@specie':
                        exCS = (exCS + atSign[i][1:] + "_id = (select id from test." + atSign[i][1:] + "  where name = " + atSign[i]+ ")")
                        if i != len(atSign) - 1: 
                            exCS = exCS + ", " 
                        else: 
                            exCS = exCS + ";"
                    else:
                        exCS = (exCS + atSign[i][1:] + "_id = (select id from test." + atSign[i][1:] + "s" + " where name = " + atSign[i] + ")")
                        if i != (len(atSign) - 1): 
                            exCS = exCS + ", "
                        else: 
                            exCS = exCS + ";"
            else:
                exCS = (exCS + "(" + print_list_elems(dat_headers()) + ") "
                "SET cs_id = " + str(cs_id) + "; ")
                if args.debug:
                    print (exCS)
            
            res = mycursor.execute(exCS, multi = True) #currently temporary w/ how it is designed, make this an executemany later
            multi_iteration(res)
            mydb.commit()

     

        executeTextCSMODELS = ("LOAD DATA LOCAL INFILE '" + mod_file +
                                "' INTO TABLE test.models2cs "
                                "(@model) "
                                "SET cs_id = " + str(cs_id) + ", "
                                "model_id = (select model_id "
                                "            from test.models "
                                "            where name LIKE @model);")

        if os.path.exists(mod_file):
            mycursor.execute(executeTextCSMODELS)
        cs_id = cs_id + 1

f_cs_dat_file.close()

mydb.commit()


#===============TEST FUNCTIONS=====================
#TODO: refactor with pytest.mark.parametrize() to reduce duplicate lines of code
def nepc_connect(local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_csdata_lines(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    cs_lines = 0
    for directoryname in DIR_NAMES:
        directory = os.fsencode(directoryname)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".met") or filename.endswith(".mod"):
                continue
            else:
                # subtract 1 to account for header
                cs_lines += scraper.wc_fxn(directoryname + filename) - 1

    assert cs_lines == nepc.count_table_rows(cursor, "csdata")
    cursor.close()
    cnx.close()

def test_species_entered(local, dbug): #for the species table
    cnx, cursor = nepc.connect(local, dbug)
    test_species = nepc.table_as_df (mycursor, "species")
    cs_species = nepc.table_as_df (cursor, "species")
    assert_frame_equal (test_species, cs_species)
    cursor.close()
    cnx.close()

def test_species_number_of_rows(local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows (cursor, "species") == nepc.count_table_rows (mycursor, "species")
    cursor.close()
    cnx.close()

    
def test_processes_entered(local, dbug): #for the processes table
    #FIXME: currently does not add all of the elements in the file
    cnx, cursor = nepc.connect(local, dbug)
    test_processes = nepc.table_as_df (mycursor, "processes")
    cs_processes = nepc.table_as_df (cursor, "processes")
    assert_frame_equal(cs_processes, test_processes)
    cursor.close()
    cnx.close()

def test_processes_number_of_rows (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows(cursor, "processes") == nepc.count_table_rows (mycursor, "processes")
    cursor.close()
    cnx.close()


def test_models_entered(local, dbug): #for the models table - actually works
    cnx, cursor = nepc.connect(local, dbug)
    test_models = nepc.table_as_df (mycursor, "models")
    cs_models = nepc.table_as_df (cursor, "models")
    assert_frame_equal (test_models, cs_models)
    cursor.close()
    cnx.close()
    
def test_models_number_of_rows (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows (cursor, "models") == nepc.count_table_rows (mycursor, "models")
    cursor.close()
    cnx.close()


def test_states_entered(local, dbug): #TODO: create a test database and table b/c this is the only way it will work
    cnx, cursor = nepc.connect(local, dbug)
    test_states = nepc.table_as_df (mycursor, "states")
    cs_states = nepc.table_as_df (cursor, "states")
    assert_frame_equal (test_states, cs_states)
    cursor.close()
    cnx.close()

def test_states_number_of_rows (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows (cursor, "states") == nepc.count_table_rows (mycursor, "states")
    cursor.close()
    cnx.close()



def test_models2cs_entered (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    test_models2cs = nepc.table_as_df (mycursor, "models2cs")
    cs_models2cs = nepc.table_as_df (cursor, "models2cs")
    assert_frame_equal (test_models2cs, cs_models2cs)
    cursor.close()
    cnx.close()


def test_models2cs_number_of_rows (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows (cursor, "models2cs") == nepc.count_table_rows (mycursor, "models2cs")
    cursor.close()
    cnx.close()


def test_cs_entered (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    test_cs = nepc.table_as_df (mycursor, "cs")
    file_cs = nepc.table_as_df (cursor, "cs")
    assert_frame_equal (test_cs, file_cs)
    cursor.close()
    cnx.close()


def test_cs_number_of_rows (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows (cursor, "cs") == nepc.count_table_rows (mycursor, "cs")
    cursor.close()
    cnx.close()

def test_csdata_entered (local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    test_csdata = nepc.table_as_df (mycursor, "csdata")
    file_csdata = nepc.table_as_df (cursor, "csdata")
    assert_frame_equal (test_csdata, file_csdata)
    cursor.close()
    cnx.close()

def test_csdata_number_of_rows(local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    assert nepc.count_table_rows (cursor, "csdata") == nepc.count_table_rows (mycursor, "csdata")
    cursor.close()
    cnx.close()


# TODO: use @pytest.mark.parametrize decorator to turn this into N tests
#       instead of N asserts in one test
def test_data_entered(local, dbug): #for the csdata table
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        dat_file = row['filename']
        df = pd.read_csv(NEPC_HOME + dat_file + '.dat', delimiter='\t',
                         usecols=['e_energy', 'sigma'])
        e_energy, sigma = nepc.cs_e_sigma(cursor, cs_id)
        assert e_energy == pytest.approx(df['e_energy'].tolist())
        assert sigma == pytest.approx(df['sigma'].tolist())
    cursor.close()
    cnx.close()


# TODO: use @pytest.mark.parametrize decorator to turn this into N tests
#       instead of N asserts in one test
def test_meta_entered(local, dbug): #for the cs table
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        met_file = row['filename']
        if dbug:
            print(cs_id, met_file)
        e, sigma = nepc.cs_e_sigma(cursor, cs_id)

        meta_cols = ['specie', 'process', 'units_e',
                     'units_sigma', 'ref', 'lhsA',
                     'lhsB', 'rhsA', 'rhsB', 'wavelength',
                     'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j',
                     'background', 'lpu', 'upu']

        with open(NEPC_HOME + met_file + ".met", 'r', newline='') as f:
                reader = csv.reader(f, delimiter='\t')
                next(reader)
                meta_disk = list(reader)[0]
        meta_disk = [meta_disk[i] for i in list(range(1, 18))]
        for i in [2, 3, 9, 15, 16]:
            meta_disk[i] = (float(meta_disk[i]) if meta_disk[i] != '\\N'
                            else meta_disk[i])

        for i in [10, 11, 12, 13]:
            meta_disk[i] = (int(meta_disk[i]) if meta_disk[i] != '\\N'
                            else meta_disk[i])

        meta_db = [nepc.cs_metadata(cursor, cs_id)[i]
                   for i in list(range(1, 18))]
        for i in range(len(meta_cols)):
            if (type(meta_db[i]) is float):
                assert (pytest.approx(meta_disk[i]) ==
                        pytest.approx(meta_db[i]))
            elif meta_db[i] is None:
                assert meta_disk[i] == '\\N'
            else:
                assert meta_disk[i] == meta_db[i]
