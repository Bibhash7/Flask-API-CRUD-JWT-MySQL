from app import app
from model.auth_model import auth_model
from model.user_model import user_model
from flask import request, send_file
from datetime import datetime

obj = user_model()
auth = auth_model()


@app.route("/user/getall")
@auth.token_auth()
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/addone", methods = ['GET','POST'])
@auth.token_auth()
def user_addone_controller():
    return obj.user_addone_model(request.form)

@app.route("/user/update", methods = ['PUT'])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route("/user/delete", methods = ["DELETE"])
def user_delete_controller():
    return obj.user_delete_model(request.form)

@app.route("/user/patch/<id>", methods = ["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form,id)

@app.route("/user/getall/limit/<limit>/page/<page>")
def user_pegination_controller(limit,page):
    return obj.user_pegination_model(limit,page)

@app.route("/user/<uid>/upload/avatar")
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    uniqueTime = datetime.now().timestamp().__str__().replace('.','')
    file.filename = file.filename
    fileNameSplit = file.filename.split(".")
    ext = fileNameSplit[len(fileNameSplit)-1]
    filepath = f"uploads/{uniqueTime}.{ext}"
    file.save(filepath)
    return obj.user_upload_avatar_model(uid,filepath)

@app.route("/uploads/<filename>")
def user_get_avatar_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login", methods = ["POST"])
def user_login_controller():
    return obj.user_login_model(request.form)

