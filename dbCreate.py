import sqlite3,os
def main():
    try:
        os.remove("user.db")
    except:
        pass
    db=sqlite3.connect("user.db")
    print("created database")
    stmt='''CREATE TABLE User
        (
        UserID INT PRIMARY KEY NOT NULL,
        Forename TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Kudos INT NOT NULL,
        Hash TEXT NOT NULL
        )'''
    db.execute(stmt)
    db.close()
    print("exited successfully")

if __name__=='__main__':
    main()
