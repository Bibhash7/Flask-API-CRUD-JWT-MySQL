import json
import mysql.connector
from flask import make_response
from datetime import datetime, timedelta
import jwt

from configs.config import dbconfig


class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],password=dbconfig['password'], database=dbconfig['database'])
            self.cur = self.con.cursor(dictionary=True)
            self.con.autocommit = True
            print('Connection Successful')
        except:
            print('Some error')
    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        print(result)
        if len(result) > 0:
            return {"payload":result}
        else:
            return "No Data Found"

    def user_addone_model(self,data):
        try:
            print(data)
            self.cur.execute(f"INSERT INTO users(name, email, phone, role, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')")
        except Exception as error:
                print("An exception occurred:", error)
        res = make_response({"message":"CREATED_SUCCESSFULLY"},201)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


    def user_update_model(self,data):
        try:
            print(data)
            self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}' WHERE id={data['id']}")
            if self.cur.rowcount > 0:
                return make_response({"message":f"{self.cur.rowcount} row(s) effected"},201)
            else:
                return make_response({"message":"Nothing to Update"},202)
        except Exception as error:
                print("An exception occurred:", error)
                return make_response({"Error": error},404)
    def user_delete_model(self,data):
        try:
            print(data)
            self.cur.execute(f"DELETE FROM users WHERE id={data['id']}")
            print(f"{self.cur.rowcount} row(s) effected")
        except Exception as error:
                print("An exception occurred:", error)
        return "Data Deleted Successfully"
    def user_patch_model(self,data,id):
        qry = "UPDATE users SET "
        for key in data:
            qry+=f"{key} = '{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {id};"
        print(qry)
        self.cur.execute(qry)
        if self.cur.rowcount > 0:
            return make_response({"message": f"{self.cur.rowcount} row(s) effected"}, 201)
        else:
            return make_response({"message": "Nothing to Update"}, 202)

    def  user_pegination_model(self,limit,page):
        page = int(page)
        limit = int(limit)
        start = page*limit-limit
        self.cur.execute(f"SELECT * FROM users LIMIT {start},{limit}")
        result = self.cur.fetchall()
        if(self.cur.rowcount> 0):
            return make_response({"page": page, "per_page": limit, "this_page": len(result), "payload": result})
        else:
            return make_response({"message": "No Data Found"}, 204)

    def user_upload_avatar_model(self,uid,filepath):
        self.cur.execute(f"UPDATE users SET avatar = '{filepath}' WHERE id ={uid}")
        if self.cur.rowcount > 0:
            return make_response({"message": f"{self.cur.rowcount} row(s) effected"}, 201)
        else:
            return make_response({"message": "Nothing to Update"}, 202)

    def user_login_model(self,data):
        self.cur.execute(f"SELECT id,name,email,phone,avatar,role_id FROM users WHERE email = '{data['email']}' and password = '{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exptime = datetime.now() + timedelta(minutes=10)
        exp_epoch_time = int(exptime.timestamp())
        payload = {
            "payload":userdata,
            "exp": exp_epoch_time
        }
        jwtoken = jwt.encode(payload,"Bibhash","HS256")
        return make_response({"token":jwtoken},200)
