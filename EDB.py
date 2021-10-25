import pymysql as p

def getConnect():
    return p.connect(host="localhost",user="root",password='',database="siddhesh_db")

def getUserList():
    sql="select * from employee"
    db=getConnect()
    cr=db.cursor()
    cr.execute(sql)
    ulist=cr.fetchall()
    db.commit()
    db.close()
    return ulist

def deleteUser(user_id):
    db=getConnect()
    cr=db.cursor()
    sql="delete from employee where user_id=%s"
    cr.execute(sql,user_id)
    db.commit()
    db.close()

def getUserById(user_id):
    sql="select * from employee where user_id=%s"
    db=getConnect()
    cr=db.cursor()
    cr.execute(sql,user_id)
    ulist=cr.fetchall()
    db.commit()
    db.close()
    return ulist[0]

def updateUser(t):
    db=getConnect()
    cr=db.cursor()
    sql="update employee set name=%s,contact=%s,email=%s,address=%s,password=%s where user_id=%s"
    cr.execute(sql,t)
    db.commit()
    db.close()
