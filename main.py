from flask import Flask
import subprocess
from flask import jsonify
from flask import request
import os

# Have to do
# List file and folder
# Copy , move , rename, delete, edit, etc ..


app = Flask(__name__)

public_path = "/home/chamath/Projects/file-manager-flask/"


def command (command_str):
    command_str = command_str
    command = subprocess.Popen([command_str], stdout=subprocess.PIPE, shell=True)
    (output, error) = command.communicate()

    # print(f"\n----------------------\n {output} \n----------------------\n")
    # print(f"\n----------------------\n {error} \n----------------------\n")
    return (output,error)

@app.route('/list-files',methods=['GET', 'POST'])
def list_files():

    fields = ['permissions','links','owner','group','size','date','time','name']
    
    manupulated_output = []

    # command_str = f"ls -lha --time-style=long-iso {public_path}"
    # command = subprocess.Popen([command_str], stdout=subprocess.PIPE, shell=True)
    # (output, error) = command.communicate()
    
    (output,error) = command(f"ls -lha --time-style=long-iso {public_path}")

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
  
@app.route('/create-file',methods=['GET', 'POST'])
#params
# file_name : string
# force_create : String (True , False)
# backup_old : String (True , False)
def create_file():
    if request.method == 'POST' or request.method == 'GET':
        file_name = request.form.get('file_name',None)
        force_create = request.form.get('force_create','False')
        backup_old = request.form.get('backup_old','False')
        if file_name is not None:

            file_exist = exists(f"{public_path}/{file_name}")

            if(file_exist != True or (file_exist and force_create == 'True')):

                if(file_exist == True and force_create == 'True' and backup_old == 'True'):
                    command(f"cp {file_name} {file_name}-backup-at-$(date +%s)")

                (output, error) = command(f"touch {public_path}/{file_name}")

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
    else:
        return jsonify(status=500,message='Invalid request method',data='')


@app.route('/create-folder',methods=['GET', 'POST'])
#params
# folder_name : string
# force_create : String (True , False)
# backup_old : String (True , False)
def create_folder():
    if request.method == 'POST' or request.method == 'GET':
        folder_name = request.form.get('folder_name',None)
        force_create = request.form.get('force_create','False')
        backup_old = request.form.get('backup_old','False')
        if folder_name is not None:

            folder_exist = os.path.isdir(f"{public_path}/{folder_name}")

            if(folder_exist != True or (folder_exist and force_create == 'True')):
    
                if(folder_exist and force_create == 'True' and backup_old == 'True'):
                    command(f"zip -r {public_path}/{folder_name}-backup-at-$(date +%s).zip {public_path}/{folder_name}")
                
                if(folder_exist and force_create == 'True'):
                    command(f"rm -rf {public_path}/{folder_name}")

                (output, error) = command(f"mkdir {public_path}/{folder_name}")

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
    else:
        return jsonify(status=500,message='Invalid request method',data='')



