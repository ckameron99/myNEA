import sqlite3, hashlib, binascii, os
class User:
    def __init__(self,id,forename=None,surname=None,password=None):
        self.id=id
        self.symbol=self.id[:2]
        db=sqlite3.connect("user.db")
        stmt=f"SELECT * FROM User WHERE UserID=?"
        results=[result for result in db.execute(stmt,(self.id,))]
        db.close()
        if len(results)==0:
            self.loaded= False
            self.userFound=False
        else:
            self.userFound=True
            user=results[0]
            self.loaded= self.load(user,password)

    def authenticate(self,hash,pwd=None):
        if pwd==None:
            pwd=input("please enter your password to authenticate: ")
        salt = hash[:64].encode("ascii")
        hash = hash[64:]
        pwd=pwd.encode("utf-8")
        pwdhash = hashlib.pbkdf2_hmac('sha512', pwd, salt, 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == hash

    def storePwd(self,newPwd=None):
        if newPwd==None:
            newPwd=input("please enter a new password: ")
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        newPwd=newPwd.encode('utf-8')
        pwdhash = hashlib.pbkdf2_hmac('sha512', newPwd, salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def load(self,user,password):
        if self.authenticate(user[4],password):
            self.forename=user[1]
            self.surname=user[2]
            self.Kudos=user[3]
            self._hash=user[4]
            return True
        else:
            return False

    def authenticationError(self,error):
        raise NotImplementedError(error)

    def create(self,forename=None,surname=None,password=None):
        db=sqlite3.connect("user.db")
        if forename==None:
            forename=input("please enter your forename: ")
        if surname==None:
            surname=input("please enter your surname: ")
        self.forename=forename
        self.surname=surname
        self.Kudos=0
        pwdHash=self.storePwd(password)
        stmt=f"""INSERT INTO User (UserID,forename,Surname,Kudos,Hash)
        VALUES (?,?,?,?,?)"""
        db.execute(stmt,(self.id,self.forename,self.surname,self.Kudos,pwdHash))
        db.commit()
        db.close()

    def save(self,id):
        db=sqlite3.connect("user.db")
        stmt="UPDATE User set forename = ? WHERE UserID=?"
        db.execute(stmt,(self.forename,self.id))
        stmt="UPDATE User set Surname = ? WHERE UserID=?"
        db.execute(stmt,(self.surname,self.id))
        stmt="UPDATE User set Kudos = ? WHERE UserID=?"
        db.execute(stmt,(self.kudos,self.id))
