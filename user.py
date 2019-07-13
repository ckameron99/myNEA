import sqlite3, hashlib, binascii, os
class User:
    def __init__(self,id,forname=None,surname=None,DOB=None):
        self.id=id
        db=sqlite3.connect("user.db")
        stmt=f"SELECT * FROM User WHERE UserID='{self.id}'"
        results=[result for result in db.execute(stmt)]
        db.close()
        if len(results)==0:
            if forname==None:
                forname=input("please enter your forname: ")
            if surname==None:
                surname=input("please enter your surname: ")
            if DOB==None:
                DOB=input("please enter your DOB: ")
            self.create(forname,surname,DOB)
        else:
            user=results[0]
            self.load(user)

    def authenticate(self,hash,pwd=None):
        if pwd==None:
            pwd=input("please enter your password to authenticate: ")
        salt = hash[:64]
        hash = hash[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == hash

    def storePwd(self,newPwd=None):
        if newPwd==None:
            newPwd=input("please enter a new password: ")
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', newPwd.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def load(self,user):
        if self.authenticate(user[5]):
            self.forname=user[1]
            self.surname=user[2]
            self.DOB=user[3]
            self.Kudos=user[4]
        else:
            raise NotImplementedError("incorrect password")

    def create(self,forname=None,surname=None,DOB=None):
        db=sqlite3.connect("user.db")
        if forname==None:
            forname=input("please enter your forname: ")
        if surname==None:
            surname=input("please enter your surname: ")
        if DOB==None:
            DOB=input("please enter your DOB: ")
        self.forname=forname
        self.surname=surname
        self.DOB=DOB
        self.Kudos=0
        pwdHash=self.storePwd()
        stmt=f"""INSERT INTO User (UserID,Forname,Surname,DOB,Kudos,Hash) VALUES ('{self.id}','{self.forname}','{self.surname}','{self.DOB}',{self.Kudos},'{pwdHash}')"""
        db.execute(stmt)
        db.commit()
        db.close()

    def save(self,id):
        db=sqlite3.connect("user.db")
        stmt="UPDATE User set Forname = {self.forname} WHERE UserID={self.id}"
        db.execute(stmt)
        stmt="UPDATE User set Surname = {self.forname} WHERE UserID={self.surname}"
        db.execute(stmt)
        stmt="UPDATE User set DOB = {self.forname} WHERE UserID={self.DOB}"
        db.execute(stmt)
        stmt="UPDATE User set Kudos = {self.forname} WHERE UserID={self.Kudos}"
        db.execute(stmt)
