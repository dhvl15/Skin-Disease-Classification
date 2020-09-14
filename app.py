from flask import Flask, render_template, request
from dbconnect import connection
from pat_reg import pat_reg,register
from passlib.hash import md5_crypt

app = Flask(__name__)

cur,conn = connection()

@app.route('/')
def index():
    return render_template('index1.html')

def getinfo(lpin):
    cur, conn = connection()
    sql = ("select * from doctor where pin = %s") #address phone
    p = (lpin,)
    cur.execute(sql,p)
    doc_id = cur.fetchall()[0][0]
    name = cur.fetchall()[0][1]
    return doc_id, name

@app.route('/login',methods=["GET","POST"])
def login():
    try:
        #print(md5_crypt.hash('modi'))
        cur, conn = connection()
        lpin = request.form['pin']
        entered_pass = request.form['password']
        sql = ("select password from doctor where pin = %s")
        p = (lpin,)
        cur.execute(sql,p)
        data = cur.fetchall()[0]
        print(data[0])
        if md5_crypt.verify(entered_pass,data[0]):
            doc_id, name = getinfo(lpin)
            return "Success" #return render_template
        else:
            return "false"
    except Exception as e:
        return(str(e))
    


@app.route('/patient_login')
def pat_login():
    return render_template('login.html',title='login')

if __name__ == "__main__":
    app.run(debug=True)

    