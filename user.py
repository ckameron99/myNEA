import sqlite3, hashlib, binascii, os
class User:
    def __init__(self,id,forename=None,surname=None,DOB=None,password=None):
        self.id=id
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
        if self.authenticate(user[5],password):
            self.forename=user[1]
            self.surname=user[2]
            self.DOB=user[3]
            self.Kudos=user[4]
            self._hash=user[5]
            return True
        else:
            return False

    def authenticationError(self,error):
        raise NotImplementedError(error)

    def create(self,forename=None,surname=None,DOB=None,password=None):
        db=sqlite3.connect("user.db")
        if forename==None:
            forename=input("please enter your forename: ")
        if surname==None:
            surname=input("please enter your surname: ")
        if DOB==None:
            DOB=input("please enter your DOB: ")
        self.forename=forename
        self.surname=surname
        self.DOB=DOB
        self.Kudos=0
        pwdHash=self.storePwd(password)
        stmt=f"""INSERT INTO User (UserID,forename,Surname,DOB,Kudos,Hash)
        VALUES (?,?,?,?,?,?)"""
        db.execute(stmt,(self.id,self.forename,self.surname,self.DOB,self.Kudos,pwdHash))
        db.commit()
        db.close()

    def save(self,id):
        db=sqlite3.connect("user.db")
        stmt="UPDATE User set forename = {self.forename} WHERE UserID={self.id}"
        db.execute(stmt)
        stmt="UPDATE User set Surname = {self.surname} WHERE UserID={self.id}"
        db.execute(stmt)
        stmt="UPDATE User set DOB = {self.DOB} WHERE UserID={self.id}"
        db.execute(stmt)
        stmt="UPDATE User set Kudos = {self.kudos} WHERE UserID={self.id}"
        db.execute(stmt)
