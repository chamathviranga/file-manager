import os
import subprocess
from flask import Flask
from flask import jsonify
from flask import request
from os.path import exists
from modules.command import Command


class Folder:

    def __init__(self,path) -> None:
        self.public_path = path

    #params
    # folder_name : String
    # force_create : String (True , False)
    # backup_old : String (True , False)
    def create(self):

        folder_name = request.form.get('folder_name',None)
        force_create = request.form.get('force_create','False')
        backup_old = request.form.get('backup_old','False')
        if folder_name is not None:

            folder_exist = os.path.isdir(f"{self.public_path}/{folder_name}")

            if(folder_exist != True or (folder_exist and force_create == 'True')):

                if(folder_exist and force_create == 'True' and backup_old == 'True'):
                    Command.run(f"zip -r {self.public_path}/{folder_name}-backup-at-$(date +%s).zip {self.public_path}/{folder_name}")
                
                if(folder_exist and force_create == 'True'):
                    Command.run(f"rm -rf {self.public_path}/{folder_name}")

                (output, error) = Command.run(f"mkdir {self.public_path}/{folder_name}")

                if(error):
                    print(error)
                    return jsonify(status=400,message='Something went wrong',data='')
                else:
                    print(output)
                    #Vyte value convert to string
                    #output.decode("utf-8")
                    return jsonify(status=200,message=f"Folder ({folder_name}) created successfully.",data='')
            else:
                return jsonify(status=400,message=f"Folder ({folder_name}) already exisit.",data='')
                    
        else:
            return jsonify(status=500,message='Invalid folder name',data='')

    def delete():
        pass

    def copy():
        pass

    def move():
        pass

    def rename():
        pass

    def archive():
        pass