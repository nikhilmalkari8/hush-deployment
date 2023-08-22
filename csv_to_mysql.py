import os
import pandas as pd
import mysql.connector

# MySQL database connection settings
db_config = {
    'host': 'localhost',
    'user': 'personalproject',
    'password': 'student',
    'database': 'hushproject'
}


# Path to the folder containing CSV files
csv_folder = '/Users/nikhilmalkari/Documents/PROJECTS/Hush/FinalData'

# List all CSV files in the folder
csv_files = [file for file in os.listdir(csv_folder) if file.endswith('.csv')]

# Connect to the MySQL database
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Loop through each CSV file and insert data into the database
for csv_file in csv_files:
    file_path = os.path.join(csv_folder, csv_file)
    encoding = "ISO-8859-1"  # Replace with the actual encoding of your files
    
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        # Perform operations on the DataFrame 'df' here
    except UnicodeDecodeError:
        print(f"Error reading {csv_file} due to encoding issue.")
    
    table_name = csv_file[:-4]  # Remove ".csv" extension for table name
    

    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
    create_table_query += ', '.join([f'`{col}` LONGTEXT' for col in df.columns])
    create_table_query += ")"
    cursor.execute(create_table_query)
    db_connection.commit()  

    print(f"Table '{table_name}' creating and data inserted.")
    
    # Insert data row by row
    for index, row in df.iterrows():
        # Replace 'nan' values with None (NULL in MySQL)
        row = [None if pd.isna(value) else value for value in row]
        
        insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s' for _ in df.columns])})"
        cursor.execute(insert_query, tuple(row))
        db_connection.commit()
    
    print(f"Table '{table_name}' created and data inserted.")
    
cursor.close()
db_connection.close()
