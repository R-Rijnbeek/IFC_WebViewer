# =============== IMPORTS ==============

from flask import abort, render_template, request, current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import ifcopenshell

from . import public_bp, js, upload
from ..shared import LOG, BULK
from ..utils import ( 	ThreejsRenderer, 
						Append_IFC_Shapes_To_ThreejsRenderer_Object, 
						returnsJS, 
						getOpenGraphImageURL, 
						getFullURL, 
						allowed_file, 
						methodLogging, 
						argument_check
						)


from os import listdir
from os.path import join, isfile, exists
from uuid import uuid4

# =============== DEFINE ENTRYPOINTS ==============

@public_bp.route("/")
@methodLogging
@argument_check()
def landing():	
	try:
		path = current_app.config["EXPOSITION_FOLDER"]
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
		LOG.error(f"ERROR {LOG.getFunctionName()}: {exc}")
		abort(500)


@js.route("/public/js/webGL.js", methods=["GET"])
@returnsJS
@methodLogging
@argument_check()
def get_js():
	try:
		file_name = request.args["ifc"]
		shape_path = current_app.config["SHAPE_DIR"]
		ifc_file = BULK.get_bulk_Key(file_name)
		BULK.del_bulk_Key(file_name)
		my_ren = ThreejsRenderer(path = shape_path )
		Append_IFC_Shapes_To_ThreejsRenderer_Object(my_ren,ifc_file)
		shape_content = my_ren.generate_shape_import_string()
		return render_template(
			"public/js/webGL.js", 
			shape_content = shape_content
			)
	except Exception as exc:
		if (hasattr(exc, '__module__') and ( exc.__module__== "ifcopenshell")):
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: {exc}")
			return render_template(
				"public/js/webGL_ERROR.js", 
				error_message=f"ERROR: {exc}"
				)
		else:
			LOG.error(f"ERROR: {LOG.getFunctionName()}: {exc}")
			return render_template(
				"public/js/webGL_ERROR.js", 
				error_message="INTERNAL SERVER ERROR"
				)

@upload.route("/fileSelect", methods=["POST"])
@methodLogging
@argument_check()
def fileSelect():
	try:
		data = request.get_json()
		if 'filename' not in data:
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: Request have wrong data format")
			return "Request have wrong data format", 400
		filename = data["filename"]
		if filename == '':
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: No selected file")
			return "No selected file", 400
		if not allowed_file(filename):
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: File extension must be \".ifc\" format")
			return "File extension must be \".ifc\" format", 400
		file_path = join(current_app.config["EXPOSITION_FOLDER"],filename)
		if not exists(file_path) :
			LOG.warning(f"ERROR: {LOG.getFunctionName()}: File does not exist on path")
			return "INTERNAL SERVER ERROR", 500
		try:
			ifc_file = ifcopenshell.open(file_path)
			uniqueKey = str(uuid4())
			BULK.set_bulk_Key(uniqueKey, ifc_file)
			return {"key":uniqueKey}, 200
		except Exception as exc:
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: {exc}")
			return f"Problems parcing IFC file", 400
	except Exception as exc:
		if isinstance(exc, HTTPException):
			if (exc.code == 413) :
				LOG.warning(f"Warning: {LOG.getFunctionName()}: {exc}")
				return f"File is to large", 413
			else: 
				return f"Somthing went wrong processing ifc file", exc.code
		else:
			LOG.error(f"ERROR: {LOG.getFunctionName()}: {exc}")
			return f"INTERNAL SERVER ERROR", 500


@upload.route("/fileUpload", methods=["POST"])
@methodLogging
@argument_check()
def fileUpload():
	try:
		if 'fileName' not in request.files:
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: Request have wrong data format")
			return "Request have wrong data format", 400
		file = request.files['fileName']
		if file.filename == '':
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: No selected file")
			return "No selected file", 400
		if not allowed_file(file.filename):
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: File extension must be \".ifc\" format")
			return "File extension must be \".ifc\" format", 400
		if file and allowed_file(file.filename):
			try:
				filename = secure_filename("".join(["temp_",file.filename]))
				uniqueKey = str(uuid4())
				ifc = ifcopenshell.file.from_string(file.stream.read().decode())
				if ifc.schema == "IFC2X3":
					BULK.set_bulk_Key(uniqueKey, ifc)
					return {"key":uniqueKey}, 200
				else:
					LOG.warning(f"WARNING: {LOG.getFunctionName()}: IFC file must be 'IFC2X3'")
					return f"IFC file must be 'IFC2X3'", 400
			except Exception as exc:
				LOG.warning(f"WARNING: {LOG.getFunctionName()}: {exc}")
				return f"Problems parcing IFC file", 500
	except Exception as exc:
		if isinstance(exc, HTTPException):
			if (exc.code == 413) :
				LOG.warning(f"Warning: {LOG.getFunctionName()}: {exc}")
				return f"File is to large", 413
			else:
				return f"Somthing went wrong processing ifc file", exc.code
		else:
			LOG.error(f"ERROR: {LOG.getFunctionName()}: {exc}")
			return f"INTERNAL SERVER ERROR", 500

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass