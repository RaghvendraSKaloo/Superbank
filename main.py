from flask import Flask, render_template, request, session, redirect
from database import DbConnection

app = Flask(__name__)
app.secret_key = 'xyz'

# Page routes start
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/userhome')
def userhome():
    return render_template('userhome.html')

@app.route('/myaccounts')
def myaccounts():
    return render_template('myaccounts.html')

@app.route('/trans')
def trans():
    return render_template('trans.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/funds')
def funds():
    return render_template('funds.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')
# page route end

# Actions routes start
@app.route('/signupUser',methods=['POST','GET'])
def signupUser():
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['temail2']
        pass1 = request.form['tpass2']
        pass2 = request.form['tpass3']
        print(name,email,pass1)
        if pass1 != pass2:
            mess="Password does not match !!"
            return render_template("index.html",message=mess)
        else:
            db = DbConnection()
            if db.signupUser(name,email,pass1) == True:
                mess="Signup Successful !!"
            else:
                mess="Signup Failed !!"
            return render_template("index.html", message=mess)

@app.route('/loginUser',methods=['POST','GET'])
def loginUser():
    if request.method == 'POST':
        email = request.form['temail1']
        pass1 = request.form['tpass1']
        print(email,pass1)
        db = DbConnection()
        if db.loginUser(email,pass1) == True:
            # login is successful
            session['emailid'] = email
            return render_template('userhome.html')
        else:
            mess="Login Failed !!"
        return render_template("index.html", message=mess)

@app.route('/createAccount',methods=['POST','GET'])
def createAccount():
    if request.method == 'POST':

        # acno = int(request.form['tacno'])
        email = request.form['temail']
        amt = float(request.form['tamt'])

        db = DbConnection()
        st = db.createAccount(email,amt)
        if st[0] == True:
            flag = 1
            mess="""Account Created Successfully !! 
            Your account no. is : """ +str(st[1])
            return render_template('userhome.html',message=mess, acno = st[1], flag=1)
        else:
            flag = 0
            mess="User Account Creation Failed !!"
            return render_template("userhome.html", message=mess, flag)
        return redirect(url_for('createAccount')) 

@app.route('/storeTrans',methods=['POST','GET'])
def storeTrans():
    if request.method == 'POST':
        acno = int(request.form['tacno'])
        email = request.form['temail']
        amt = float(request.form['tamt'])
        type = request.form['type']

        db = DbConnection()
        if db.storeTrans(acno,email,amt,type) == True:
            mess="Transactions Successfully !!"
            return render_template('usermessage.html',message=mess)
        else:
            mess="Transaction Failed !!"
        return render_template("usermessage.html", message=mess)

@app.route('/mobileRch',methods=['POST','GET'])
def mobileRch():
    if request.method == 'POST':
        acno = int(request.form['tacno'])
        email = request.form['temail']
        amt = float(request.form['tamt'])
        type = request.form['type']

        db = DbConnection()
        if db.mobileRch(acno,email,amt,type) == True:
            mess="Mobile Recharged Successfully !!"
            return render_template('usermessage.html',message=mess)
        else:
            mess="Mobile Recharged Failed !!"
        return render_template("usermessage.html", message=mess)

@app.route('/fundsTrans',methods=['POST','GET'])
def fundsTrans():
    if request.method == 'POST':
        acno1 = int(request.form['tacno1'])
        acno2 = int(request.form['tacno2'])
        email = request.form['temail']
        amt = float(request.form['tamt'])

        db = DbConnection()
        if db.fundsTrans(acno1,acno2,email,amt) == True:
            mess="Money Transferred Successfully !!"
            return render_template('usermessage.html',message=mess)
        else:
            mess="Money Transferred Failed !!"
        return render_template("usermessage.html", message=mess)

@app.route('/viewBalance',methods=['POST','GET'])
def viewBalance():
    if request.method == 'POST':
        acno = int(request.form['tacno1'])
        email = request.form['temail1']

        db = DbConnection()
        amt = db.viewBalance(acno,email)
        mess="Balance in your account is " + str(amt)
        return render_template('usermessage.html',message=mess)

@app.route('/updatePassword',methods=['POST','GET'])
def updatePassword():
    if request.method == 'POST':
        email = request.form['temail1']
        oldp = request.form['told']
        newp = request.form['tnew']
        newp1 = request.form['tnew1']

        if newp != newp1:
            mess="Password does not match !!"
            return render_template("usermessage.html",message=mess)
        else:
            db = DbConnection()
            if db.updatePassword(email,oldp,newp) == True:
                mess="Password Update Successful !!"
            else:
                mess="Password Update Failed !!"
            return render_template("usermessage.html", message=mess)
# action routes end
if __name__ == '__main__':
    app.run(debug=True)