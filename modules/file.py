import os
import subprocess
from flask import Flask
from flask import jsonify
from flask import request
from os.path import exists
from modules.command import Command


class File:

    def __init__(self,path) -> None:
        self.public_path = path

    def list(self):
        fields = ['permissions','links','owner','group','size','date','time','name']
    
        manupulated_output = []

        # command_str = f"ls -lha --time-style=long-iso {public_path}"
        # command = subprocess.Popen([command_str], stdout=subprocess.PIPE, shell=True)
        # (output, error) = command.communicate()
        
        (output,error) = Command.run(command_str = f"ls -lha --time-style=long-iso {self.public_path}")

        if(error):
            print(error)
            return jsonify(status=400,message='Something went wrong',data='')
        else:
            output_json = output.decode('utf8').replace("'", '"').split("\n")
            
            #Remove directory count from list
            output_json.pop(0)
            #Remove empty values from list - last val
            filtered_output_json = list(filter(None,output_json))

            for index,detail_row in enumerate(filtered_output_json):
                
                detail_fields = detail_row.split(" ")
                
                #Remove empty values from list
                filtered_detail_fields = list(filter(None,detail_fields))
                
                #https://stackoverflow.com/questions/53668976/list-append-is-overwriting-my-previous-values
                #Should create new dictionary in eacg iterate, otherwise, it will pass refference of same dictionary
                
                named_details = {}
                for index,detail_field in enumerate(filtered_detail_fields):
                    
                    #print(f"{index} : {detail_field}")
                    named_details[fields[index]] = detail_field
                
                manupulated_output.insert(index,named_details)
                print("\n --------------------------- \n")
                print(manupulated_output)
                    

            return jsonify(status=200,message='',data=manupulated_output)


    #params
    # file_name : String
    # force_create : String (True , False)
    # backup_old : String (True , False)
    def create(self):
        file_name = request.form.get('file_name',None)
        force_create = request.form.get('force_create','False')
        backup_old = request.form.get('backup_old','False')
        if file_name is not None:

            file_exist = exists(f"{self.public_path}/{file_name}")

            if(file_exist != True or (file_exist and force_create == 'True')):

                if(file_exist == True and force_create == 'True' and backup_old == 'True'):
                    Command.run(f"cp {file_name} {file_name}-backup-at-$(date +%s)")

                (output, error) = Command.run(f"touch {self.public_path}/{file_name}")

                if(error):
                    print(error)
                    return jsonify(status=400,message='Something went wrong',data='')
                else:
                    print(output)
                    #Vyte value convert to string
                    #output.decode("utf-8")
                    return jsonify(status=200,message=f"{file_name} created successfully.",data='')
            else:
                return jsonify(status=400,message=f"{file_name} already exisit.",data='')
                    
        else:
            return jsonify(status=500,message='Invalid file name',data='')


    def delete():
        pass

    #params
    # file_names : String Array
    # destination : String
    # force_copy : String
    # backup_old : String
    def copy():
        pass

    def move():
        pass

    def rename():
        pass

    def archive():
        pass