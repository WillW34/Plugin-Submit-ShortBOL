from flask import Flask, request, abort, send_file, jsonify
import os, shutil, glob, random, string, tempfile, requests
import sys
sys.path.insert(0,'shortbol')
import shortbol.run as shb_run

app = Flask(__name__)
shortbol_libs = os.path.join("shortbol", "templates")

@app.route("/status")
def status():
    return("The Submit ShortBOL Test Plugin Flask Server is up and running")



@app.route("/evaluate", methods=["POST"])
def evaluate():
    #uses MIME types
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    
    eval_manifest = request.get_json(force=True)
    files = eval_manifest['manifest']['files']
    
    eval_response_manifest = {"manifest":[]}
    
    for file in files:
        file_name = file['filename']
        file_type = file['type']
        file_url = file['url']
        
        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        ##IN THE SPECIAL CASE THAT THE EXTENSION HAS NO MIME TYPE USE SOMETHING LIKE THIS
        file_type = file_name.split('.')[-1]
        #
        ##types that can be converted to sbol by this plugin
        acceptable_types = {'txt', 'shb', 'rdfsh'}
    
        #types that can be converted to sbol by this plugin
        #acceptable_types = {'application/vnd.ms-excel',
                            #'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        
        #types that are useful (will be served to the run endpoint too but noted that they won't be converted)
        useful_types = {'txt', 'shb', 'rdfsh'}
        
        file_type_acceptable = file_type in acceptable_types
        file_type_useable = file_type in useful_types
        print(file_type_acceptable,file_type_useable)
        
        ################## END SECTION ####################################
        
        if file_type_acceptable:
            useableness = 2
        elif file_type_useable:
            useableness = 1
        else:
            useableness = 0

        eval_response_manifest["manifest"].append({
            "filename": file_name,
            "requirement": useableness})
             
    return jsonify(eval_response_manifest)
    
@app.route("/run", methods=["POST"])
def run():
    
    #create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    zip_in_dir_name = temp_dir.name
    
    #take in run manifest
    run_manifest = request.get_json(force=True)
    files = run_manifest['manifest']['files']
        
    #initiate response manifest
    run_response_manifest = {"results":[]}

    for a_file in files:
        file_name = a_file['filename']
        file_type = a_file['type']
        file_url = a_file['url']
        data = str(a_file)
        
        converted_file_name = file_name + ".converted"
        file_path_out = os.path.join(zip_in_dir_name, converted_file_name)
        
        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        
        #Retrieve file from manifest
        run_data = requests.get(file_url)
        sbh_input = os.path.join(temp_dir.name,"temp_shb.txt")
        with open(sbh_input,"w") as sbh_file:
            sbh_file.write(run_data.text)
            shb_run.parse_from_file(sbh_file.name, out=file_path_out, optpaths=[shortbol_libs])

        ################## END SECTION ####################################
    
        # add name of converted file to manifest
        run_response_manifest["results"].append({"filename":converted_file_name,
                                "sources":[file_name]})
            



    #create manifest file
    file_path_out = os.path.join(zip_in_dir_name, "manifest.json")
    with open(file_path_out, 'w') as manifest_file:
            manifest_file.write(str(run_response_manifest)) 
      
    with tempfile.NamedTemporaryFile() as temp_file:
        #create zip file of converted files and manifest
        shutil.make_archive(temp_file.name, 'zip', zip_in_dir_name)
        
        #delete zip in directory
        #shutil.rmtree(zip_in_dir_name)
        #return zip file
        return send_file(temp_file.name + ".zip")
