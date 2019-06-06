import mysql.connector

def connect(local=False):
    if (local==True):
        hostname = 'localhost'
    else:
        hostname = '132.250.158.124'

    config = {'user': 'nepc',
              'password': 'nepc',
              'host': hostname,
              'database': 'nepc',
              'raise_on_warnings': True}

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx, cursor

def printTable(cursor, table):
    print("\n=========================\n " + table + ":\n=========================")
    cursor.execute("select * from " + table + ";")
    for x in cursor:
        print(x)

def countTableRows(cursor, table):
    print("\nRows in " + table + ": ")
    cursor.execute("select count(*) from " + table + ";")
    for x in cursor:
        print(x)

def model(cursor, model_name):
    cs_dicts = []
    cursor.execute("SELECT cs.cs_id as cs_id " +
                   "FROM cs " +
                   "JOIN models2cs m2cs ON (cs.cs_id = m2cs.cs_id) " +
                   "JOIN models m ON (m2cs.model_id = m.model_id) " +
                   "WHERE m.name LIKE '" + model_name + "'")
    cs_array = cursor.fetchall()

    for cs_item in cs_array:
        cs_id = cs_item[0]

        cursor.execute("SELECT A.`cs_id` , "
                       "B.`name` , "
                       "C.`name` , "
                       "A.`units_e`, A.`units_sigma`, A.`ref`, "
                       "D.`name`, E.`name`, "
                       "F.`name`, G.`name`, "
                       "A.`wavelength`, A.`lhs_v`, A.`rhs_v`, A.`lhs_j`, A.`rhs_j`, "
                       "A.`background`, A.`lpu`, A.`upu` "
                       "FROM `cs` AS A "
                       "LEFT JOIN `species` AS B "
                       "ON B.`id` = A.`specie_id` "
                       "LEFT JOIN `processes` AS C "
                       "ON C.`id` = A.`process_id` "
                       "LEFT JOIN `states` AS D "
                       "ON D.`id` = A.`lhsA_id` "
                       "LEFT JOIN `states` AS E "
                       "ON E.`id` = A.`lhsB_id` "
                       "LEFT JOIN `states` AS F "
                       "ON F.`id` = A.`rhsA_id` "
                       "LEFT JOIN `states` AS G "
                       "ON G.`id` = A.`rhsB_id` "
                       "WHERE A.`cs_id` = " + str(cs_id))

        metadata = cursor.fetchall()[0]

        cursor.execute("SELECT e, sigma FROM csdata WHERE cs_id = " + str(cs_id))
        cs = cursor.fetchall()
        e = [i[0] for i in cs]
        sigma = [i[1] for i in cs]

        cs_dicts.append({"cs_id":metadata[0],
                         "specie":metadata[1],
                         "process":metadata[2],
                         "units_e":metadata[3],
                         "units_sigma":metadata[4],
                         "ref":metadata[5],
                         "lhsA":metadata[6],
                         "lhsB":metadata[7],
                         "rhsA":metadata[8],
                         "rhsB":metadata[9],
                         "wavelength":metadata[10],
                         "lhs_v":metadata[11],
                         "rhs_v":metadata[12],
                         "lhs_j":metadata[13],
                         "rhs_j":metadata[14],
                         "background":metadata[15],
                         "lpu":metadata[16],
                         "upu":metadata[17],
                         "e":e,
                         "sigma":sigma})

    return cs_dicts
