import duckdb
import os
import pandas as pd

def textToDFconvert():
    # init empty dfs which function returns
    df_prerequisites = pd.DataFrame()
    df_creditHours = pd.DataFrame()
    df_semesters = pd.DataFrame()

    data_path = os.path.join(os.getcwd(), 'data')
    for folder in os.listdir(data_path):
        if not folder.startswith("data") or folder.startswith('.'):         # ignore hidden folders
            continue  

        # go thru every file in folder and convert to CSV
        if folder.startswith('data'):
            folder_path = os.path.join(data_path, folder)

            for filename in sorted(os.listdir(folder_path)):
                if filename.startswith('.'):                                # ignore hidden folders
                    continue
                
                file_path = os.path.join(folder_path, filename)

                if 'prerequisites' in file_path:
                    df_prerequisites = pd.concat([df_prerequisites, pd.read_csv(file_path, sep='\t',header=None, names=['prerequisiteID', 'courseID', 'timeTaken'])])
                elif 'mastercourselist' in file_path:
                    df_creditHours = pd.concat([df_creditHours, pd.read_csv(file_path, sep='\t',header=None, names=['courseId', 'avaliableCredits'])])
                elif 'courseofferings' in file_path:
                    df_semesters = pd.concat([df_semesters, pd.read_csv(file_path, sep='\t',header=None, names=['courseId', 'offeredFall', 'offeredSpring'])])
    
    return df_prerequisites, df_creditHours, df_semesters

def createTables(con):
    con.execute('''
        CREATE OR REPLACE TABLE t_prerequisites (
            prerequisiteID VARCHAR,
            courseID VARCHAR,
            timeTaken INT
        );
        CREATE OR REPLACE TABLE t_creditHours (
            courseId VARCHAR,
            avaliableCredits VARCHAR
        );
        CREATE OR REPLACE TABLE t_courseOfferings (
            courseId VARCHAR,
            offeredFall INT,
            offeredSpring INT
        );
    ''')


def insertIntoTables(con, df_prerequisites, df_creditHours, df_semesters):
    con.register("df_prerequisites", df_prerequisites)
    con.register("df_creditHours", df_creditHours)
    con.register("df_semesters", df_semesters)

    con.execute('''
        INSERT INTO t_prerequisites SELECT * FROM df_prerequisites;
        INSERT INTO t_creditHours SELECT * FROM df_creditHours;
        INSERT INTO t_courseOfferings SELECT * FROM df_semesters;
    ''')


def initDB(db_name = "uic_2425.db"):
    con = duckdb.connect(db_name)

    df_prerequisites, df_creditHours, df_semesters = textToDFconvert()
    
    createTables(con)
    insertIntoTables(con, df_prerequisites, df_creditHours, df_semesters)

    con.close()



if __name__ == "__main__":
    initDB()