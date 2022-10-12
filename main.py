from flask import Flask
from modules.file import File
from modules.folder import Folder

# import subprocess
# from flask import jsonify
# from flask import request
# import os
# from os.path import exists


# Have to do
# List file and folder
# Copy , move , rename, delete, edit, etc ..


app = Flask(__name__)

public_path = "/home/chamath/Projects/file-manager-flask/"

@app.route('/list',methods=['GET', 'POST'])
def list():
    return File(public_path).list()

@app.route('/archive',methods=['GET', 'POST'])
def archive():
    pass
  
@app.route('/file/create',methods=['GET', 'POST'])
#params
# file_name : String
# force_create : String (True , False)
# backup_old : String (True , False)
def file_create():
    return File(public_path).create()

@app.route('/file/delete',methods=['GET', 'POST'])
#params
# file_name : String
# backup_old : String (True , False)
def file_delete():
    pass

@app.route('/file/copy',methods=['GET', 'POST'])
#params
# file_names : String Array
# destination : String
# force_copy : String
# backup_old : String
def file_copy():
    pass

@app.route('/file/move',methods=['GET', 'POST'])
#params
# file_names : String Array
# destination : String
# force_copy : String
# backup_old : String
def file_move():
    pass

@app.route('/file/rename',methods=['GET', 'POST'])
#params
# file_name : String
# backup_old : String
def file_rename():
    pass


@app.route('/folder/create',methods=['GET', 'POST'])
#params
# folder_name : String
# force_create : String (True , False)
# backup_old : String (True , False)
def folder_create():
    return Folder(public_path).create()

@app.route('/folder/delete',methods=['GET', 'POST'])
#params
# folder_name : String
# backup_old : String (True , False)
def folder_delete():
    pass

@app.route('/folder/copy',methods=['GET', 'POST'])
#params
# folder_names : String Array
# destination : String
# force_copy : String
# backup_old : String
def folder_copy():
    pass

@app.route('/folder/move',methods=['GET', 'POST'])
#params
# folder_names : String Array
# destination : String
# force_move : String
# backup_old : String
def folder_move():
    pass

@app.route('/folder/rename',methods=['GET', 'POST'])
#params
# folder_name : String
# backup_old : String
def folder_rename():
    pass

