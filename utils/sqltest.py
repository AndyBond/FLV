import sqlite3

def createteble(conn):
    create_table="""
    CREATE TABLE IF NOT EXISTS events (
    id INTEGER RRIMARY KEY,
    event DATE, 
    s_sitename text, 
    s_computername  text, 
    s_ip  text, 
    cs_method text, 
    cs_uri_stem text, 
    cs_uri_query text, 
    s_port INT, 
    cs_username text, 
    c_ip text, 
    cs_version text, 
    cs_User_Agent text, 
    cs_Referer text, 
    cs_host text, 
    sc_status INT, 
    sc_substatus INT, 
    sc_win32_status INT, 
    sc_bytes INT, 
    cs_bytes INT, 
    time_taken INT, 
    X_Forwarded_For text
    );
    """
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(create_table)   
            conn.commit()
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
