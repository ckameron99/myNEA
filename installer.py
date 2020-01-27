import os
import dbCreate
def init():
    #try to create the directory savedGames, and if it already exists, then do nothing
    try:
        os.mkdir("savedGames")
    except FileExistsError:
        pass
    #try to open the user database, and if it does not exist, then create it
    try:
        f=open("user.db","rb")
        f.close()
    except FileNotFoundError:
        dbCreate.main()


if __name__=='__main__':
    init()
