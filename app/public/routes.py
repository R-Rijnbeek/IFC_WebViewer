# =============== IMPORTS ==============

from flask import abort, render_template, request, current_app
from werkzeug.utils import secure_filename
import ifcopenshell

from os import listdir, remove
from os.path import join, isfile, splitext

from . import public_bp, js, upload
from ..utils import ThreejsRenderer, Append_IFC_Shapes_To_ThreejsRenderer_Object, returnsJS, getOpenGraphImageURL, getFullURL, allowed_file, methodLogging
from ..shared import LOG

# =============== DEFINE ENTRYPOINTS ==============

@public_bp.route("/")
@methodLogging
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
def get_js():
	try:	
		file_name = request.args["ifc"]
		filename, file_extension = splitext(file_name)
		if file_extension.replace(".", "") in current_app.config["UPLOADED_EXTENSIONS"]:
			shape_path = current_app.config["SHAPE_DIR"]
			try:
				ifc_file = ifcopenshell.open(join(current_app.config["EXPOSITION_FOLDER"],file_name))
			except:
				ifc_file = ifcopenshell.open(join(current_app.config["UPLOAD_FOLDER"],file_name))
				remove(join(current_app.config["UPLOAD_FOLDER"],file_name))
			my_ren = ThreejsRenderer(path = shape_path )
			Append_IFC_Shapes_To_ThreejsRenderer_Object(my_ren,ifc_file)
			shape_content = my_ren.generate_shape_import_string()
			return render_template(
				"public/js/webGL.js", 
				shape_content = shape_content
				)
		else:
			message = "it is not a valid file extension: it must be '.ifc'"
			LOG.warning(f"WARNING: {LOG.getFunctionName()}: {message}")
			return render_template(
				"public/js/webGL_ERROR.js", 
				error_message= message
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

@upload.route("/fileUpload", methods=["POST"])
@methodLogging
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
			filename = secure_filename("".join(["temp_",file.filename]))
			file_location = join(current_app.config['UPLOAD_FOLDER'],filename)
			file.save(file_location)
			try:
				ifcopenshell.open(file_location)
				return {"filename":filename}, 200
			except Exception as exc:
				LOG.warning(f"WARNING: {LOG.getFunctionName()}: {exc}")
				remove(file_location)
				return f"Problems parcing IFC file", 500
	except Exception as exc:
		LOG.error(f"ERROR: {LOG.getFunctionName()}: {exc}")
		return f"INTERNAL SERVER ERROR", 500

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass