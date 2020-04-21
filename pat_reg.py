from flask import Flask, render_template, request
from dbconnect import connection
from passlib.hash import md5_crypt

app = Flask(__name__)

cur,conn = connection()

@app.route('/patient_register')
def index():
    return render_template('patient_reg.html')


@app.route('/register',methods=["GET","POST"]) 
def register():
    try:
        cur, conn = connection()
        rname = request.form['name']
        rnum = request.form['num']
        remail = request.form['email']
        rsex = request.form['sex']   
        rdoc_email = request.form['doc_email'] 
        entered_pass = request.form['password']
        hashed_password = md5_crypt.hash(entered_pass)
        cur.execute("INSERT INTO patient (p_name,p_num,p_email,p_gender,p_doc_email,p_password) VALUES (%s,%s,%s,%s,%s,%s)",(rname,rnum,remail,rsex,rdoc_email,hashed_password))
        conn.commit()
        return "success"
       

if __name__ == "__main__":
    app.run(debug=True)
