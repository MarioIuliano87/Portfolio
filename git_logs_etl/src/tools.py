import pandas as pd
import pyexasol
import urllib.parse
import os
import subprocess
import re
import os
import urllib.parse
from datetime import datetime


## Define functions ##
def data_types_convertor(df, primary_key = None):
    '''Accepts a dataframe and returns dimension data types in dictionary format. 
    key: column_name
    value: data type

    '''

    data_types= {}
    floats_dim = []
    for c in df.columns: 
        if df[c].dtypes=='object': 
            data_types[c] = 'VARCHAR(10000)'
        elif df[c].dtypes == 'float64' or  df[c].dtypes == 'float32': 
            floats_dim.append(c)
            data_types[c] = 'DECIMAL(10,3)'
        elif df[c].dtypes == 'int64':  
            data_types[c] = 'DECIMAL(19,0)'

    if primary_key: 
        data_types[primary_key] = data_types[primary_key] + ' primary key'
        return data_types    
    else: 
        return data_types

# Create function to generate table creation string
def create_table_string(username, password,df, dns, schema, table_name, primary_key=None): 
    '''Generates a DDL string statement to create or replace table into a database. 
     
      schema (string):  database schema where to store the new table 
      table_name (string): table name :D 
      dimensions_and_types (dictionary): dictionary containing dimension names and related data type
      
      '''
    # Create connection to Exasol 
    C = pyexasol.connect(dsn=dns, user=username, password=password)
    # Extract df dimensions data types
    dimensions_and_dtypes = data_types_convertor(df, primary_key)
    # Create ddl statement
    create_table_string = "Create or replace TABLE {}.{}".format(schema,table_name)+"("+' '.join("""{} {},""".format(k,v)for k,v in dimensions_and_dtypes.items())[:-1]+')'
    # Execute ddl
    print('Executing the DDL: \n {}'.format(create_table_string))
    C.execute(create_table_string)
    print('Table created')
    return create_table_string

def run_git_diff_command(is_forked_repo:bool = False): 
    ''' Executes bash commands. More specifically git diff to extract file name and file name status: 

    It returns a touple of 2 elements: 
        - index[0] --> list of all edited file names 
        - index[1] --> list of status 
    '''    
    if is_forked_repo == False: 
        # Create bash commands for non-forked repositories
        name_only_bash_command = 'git diff --name-only HEAD@{1} HEAD'.split() # File Name extractor
        name_status_bash_command = 'git diff --name-status HEAD@{1} HEAD'.split()  # Extract name status
    else: 
        # Create bash commands for forked repositories
        name_only_bash_command = 'git diff --name-only main upstream/main'.split() # File Name extractor
        name_status_bash_command = 'git diff --name-status main upstream/main'.split()  # Extract name status
    try: 
        name_only = subprocess.run(name_only_bash_command,capture_output=True, text=True, check=True)
        name_status_subprocess = subprocess.run(name_status_bash_command,capture_output=True, text=True, check=True)
        return name_only.stdout, name_status_subprocess.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff command: {e}")
        return None

def create_hyperlink(file_name): 
    """ Accepts a string and returns an hyperlink"""

    # Define paths 
    learning_ground_path = 'https://domain/folder/repo/blob/main'
    airflow_path = 'https://domain/folder/tree/main/'
    processes_path = 'https://domain/folder/repo/blob/main'

    # Parse string with url format
    name_parser = urllib.parse.quote(file_name)
    # Assess current directory
    curr_path = os.getcwd()

    if 'repo_a' in curr_path: 
        hyperlink_str = learning_ground_path + '/' + name_parser
        #hyperlink = make_clickable(hyperlink_str)
        return hyperlink_str
    elif 'repo_b' in curr_path: 
        hyperlink_str = airflow_path + '/' + name_parser
        #hyperlink = make_clickable(hyperlink_str)
        return hyperlink_str
    elif 'rebo_c' in curr_path: 
        hyperlink_str = processes_path + '/' + name_parser
        #hyperlink = make_clickable(hyperlink_str)
        return hyperlink_str
    else: 
        return None

def extract_objects(is_forked_repo:bool = False): 
    ''' Returns a list with file names edited, status, hyperlinks and repository name'''

    if is_forked_repo == False:
        # Extract file names only
        names_only = run_git_diff_command()[0].split('\n')[:-1]
        # Split all diff objects by 'diff' token and store into list 
        names_status_tmp = run_git_diff_command()[1].split('\n')[:-1]
        # Extract status only from the beginning of the string 
    else: 
        # Extract file names only
        names_only = run_git_diff_command(is_forked_repo = True)[0].split('\n')[:-1]
        # Split all diff objects by 'diff' token and store into list 
        names_status_tmp = run_git_diff_command(is_forked_repo = True)[1].split('\n')[:-1]
        # Extract status only from the beginning of the string 

    status_compiler = re.compile(r'^[A-Z 0-9]+')
    names_status = [re.match(status_compiler, name).group() for name in names_status_tmp]
    # Generate repo_name and extraction date
    repo_name = [os.getcwd().split('/')[-1] for obj in range(len(names_only))]
    # Create  hyperlinks
    hyperlinks = [create_hyperlink(file_name) for file_name in names_only]
    # Create objects list 
    objects = list(zip(names_only, names_status, hyperlinks, repo_name))
    return objects

def upload_to_db(username, password, df):
     ''' 
     Writes data to database. Function is specifcally made to upload data from git
     '''

     # Establish Exasol connection 
     C = pyexasol.connect(dsn=123, user=username, password=password)
     print('Connected to Exasol')   
     
     C.execute("delete from schema_tmp.table_name where EXTRACTION_DATE = current_date()" )

     C.import_from_pandas(src=df, 
                         table=('schema', 'table_name'), 
                         callback_params={'decimal': ','}
                         )
     
     print(pd.DataFrame(df.REPO_NAME.value_counts()).rename(columns={'count':'total edits'}).reset_index())
     # Extract distinct files
     daily_extract = """
                        WITH base AS (
                                    SELECT 
                                        git.*, max(extraction_date) OVER (PARTITION BY edited_file) AS last_edited_at
                                    FROM schema.table_name git
                                ) 
                                SELECT * 
                                FROM base 
                                WHERE extraction_date  = last_edited_at

                    """
        
     # Remove all adata from workarea 
     C.execute("delete from schema_workarea.table_name where EXTRACTION_DATE = current_date()" )
     # insert distinct edits by has id 
     C.execute('''insert into schema_workarea.table_name {}'''.format(daily_extract))
     print('Imported data into schema_workarea.table_name') 


def from_git_to_df(git_directories = [], write_to_db = True,username = None, password = None):
     ''' 
     Extract relevant data from git commands and stores them into a dataframe. If write_to_db is True, it will also upload into db. 

     - git_directories = list of local git repositories
     - write_to_db (bool, Default True) = if false simply returns df 
     - username (string) 
     - password (string) 

     '''
     
     # Initiate dataframe 
     changes_df = pd.DataFrame(columns = [  'EDITED_FILE'
                                          , 'STATUS'
                                          , 'LINK'
                                          , 'REPO_NAME'
                                          , 'EXTRACTION_DATE']
                            )
   
    # Iterate through git directories and identify edits
     for git_dir in git_directories: 
          os.chdir(git_dir) 
          if 'airflow' in git_dir: 
          # Extract data 
            changes = extract_objects(is_forked_repo = True)
          else: 
            changes = extract_objects() 
          if len(changes) != 0:
            for obj in changes:
                obj = list(obj)
                # Generate repo_name and extraction date
                #repo_name = os.getcwd().split('/')[-1]
                extraction_date = datetime.now().strftime('%Y-%m-%d')
                # Append new repo_name and extraction_date to extract_objects() list
                #changes.append(repo_name)
                obj.append(extraction_date)
                # Initiate dictionary 
                new_data_dict = {}
                # Initiate indexer, this will be used to access new_data list element
                index_iter = 0
                for key in changes_df.columns:
                    # Append each col as a key and assign the changes list element at position index_iter
                    new_data_dict[key] = [obj[index_iter]]
                    index_iter +=1
                
                # Convert new data dict into a dataframe to union to the pre-define one
                new_data = pd.DataFrame.from_dict(new_data_dict)
                changes_df = pd.concat([changes_df, new_data])
     #changes_df = changes_df.explode(column='AFFECTED_TABLES')
     if write_to_db:
         upload_to_db(username, password, changes_df)
     else: 
         return changes_df     