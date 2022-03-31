
from flask import abort, render_template, request, current_app

from werkzeug.utils import secure_filename

import ifcopenshell

from . import public_bp, js, upload
from ..utils import ThreejsRenderer, Append_IFC_Shapes_To_ThreejsRenderer_Object, returnsJS, getOpenGraphImageURL, getFullURL, allowed_file

from os import listdir
from os.path import join, isfile, splitext

@public_bp.route("/")
def landing():
    	
	try:
		path = current_app.config["UPLOAD_FOLDER"]
		file_list = [f for f in listdir(path) if isfile(join(path, f))]
		
			
		image_url = getOpenGraphImageURL(request)
		full_url = getFullURL(request)
			
		owner = current_app.config["OWNER"]
		owner_email = current_app.config["OWNER_EMAIL"]
		occ_version = current_app.config["OCC_VERSION"]
		threejs_release = current_app.config["THREEJS_RELEASE"]

		return render_template(
			"public/html/landing.html",
			owner = owner, 
			owner_email=owner_email, 
			occ_version = occ_version, 
			threejs_release = threejs_release, 
			image_url = image_url, 
			full_url = full_url,
			file_list = file_list
			)
	except Exception as exc:
		print(exc)
		abort(500)


@js.route("/public/js/webGL.js", methods=["GET"])
@returnsJS
def get_js():
	try:	
		file_name = request.args["ifc"]
		filename, file_extension = splitext(file_name)
		if file_extension.replace(".", "") in current_app.config["UPLOADED_EXTENSIONS"]:
			shape_path = current_app.config["SHAPE_DIR"]
			ifc_file = ifcopenshell.open(join(current_app.config["BASE_DIR"],"app","static","ifc",file_name))
			my_ren = ThreejsRenderer(path = shape_path )
			Append_IFC_Shapes_To_ThreejsRenderer_Object(my_ren,ifc_file)
			shape_content = my_ren.generate_shape_import_string()

			return render_template(
				"public/js/webGL.js", 
				shape_content = shape_content
				)
		else:
			print("it is not a valid file extension: it must be '.ifc'")
			abort(400)
	except Exception as exc:
		print(f"ERROR: {exc}")
		if (exc.__module__ == "ifcopenshell"):
			return render_template("public/js/webGL_ERROR.js", error_message=f"ERROR: {exc}")
		else:
			return render_template("public/js/webGL_ERROR.js", error_message="INTERNAL SERVER ERROR")

@upload.route("/fileUpload", methods=["POST"])
def fileUpload():
	try:
		if 'fileName' not in request.files:
			return "Request have wrong data format", 400
		file = request.files['fileName']
		if file.filename == '':
			return "No selected file", 400
		if not allowed_file(file.filename):
			return "File extension must be \".ifc\" format", 400
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(join(current_app.config['UPLOAD_FOLDER'], filename))
			return {"filename":filename}, 200
	except Exception as exc:
		print(f"ERROR: {exc}")
		return f"INTERNAL SERVER ERROR", 500
    
# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass