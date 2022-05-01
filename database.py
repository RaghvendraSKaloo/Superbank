# this the model of the application to manage the database
import pymysql as pm

an = 11001200

class DbConnection:
    def __init__(self):
        self.con = pm.connect(host='localhost', user='root',database='superbank')
        self.cursor = self.con.cursor()

    def signupUser(self,name,email,passw):
        self.query = "insert into users values('%s','%s','%s')" % (name,email,passw)
        self.cursor.execute(self.query)
        try:
            self.con.commit()
            self.status=True
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def createAccount(self,email,amt):
        self.cursor.execute('select * from account')
        count = self.cursor.rowcount
        acno = (an + count + 1)
        self.query = "insert into account values('%d','%f','%s')" % (acno,amt,email)
        self.cursor.execute(self.query)
        try:
            self.con.commit()
            self.status=(True, acno)
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def storeTrans(self,acno,email,amt,type):
        if type=='Deposit':
            self.query = "update account set balance = balance + '%f' where acno ='%d'" % (amt,acno)
        else:
            self.query = "update account set balance = balance - '%f' where acno ='%d'" % (amt, acno)
        self.cursor.execute(self.query)
        try:
            self.con.commit()
            self.status=True
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def mobileRch(self,acno,email,amt,type):
        self.query = "update account set balance = balance - '%f' where acno ='%d'" % (amt, acno)
        self.cursor.execute(self.query)
        try:
            self.con.commit()
            self.status=True
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def fundsTrans(self,acno1,acno2,email,amt):
        self.query = "update account set balance = balance - '%f' where acno ='%d'" % (amt, acno1)
        self.cursor.execute(self.query)
        try:
            self.con.commit()
            self.query = "update account set balance = balance + '%f' where acno ='%d'" % (amt, acno2)
            self.cursor.execute(self.query)
            self.con.commit()
            self.status=True
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def updatePassword(self,email,oldp,newp):
        self.query = "update users set password = '%s' where emailid ='%s' and password = '%s'" \
                     % (newp, email, oldp)
        self.cursor.execute(self.query)
        try:
            self.con.commit()
            self.status=True
        except:
            self.con.rollback()
            self.status=False
        return self.status

    def loginUser(self,email,passw):
        print(email,passw)
        self.query = "select * from users where emailid='%s' and password='%s'" % (email,passw)
        self.cursor.execute(self.query)
        if self.cursor.rowcount >0:
            self.status=True
        else:
            self.status=False
        return self.status

    def viewBalance(self,acno,email):
        self.query = "select * from account where acno='%d' and emailid='%s'" % (acno,email)
        self.cursor.execute(self.query)
        self.data = self.cursor.fetchone()
        self.amt = self.data[1]
        return self.amt