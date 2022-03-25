
from flask import render_template, request, current_app

import ifcopenshell

from . import public_bp, js
from ..utils import ThreejsRenderer, Append_IFC_Shapes_To_ThreejsRenderer_Object, returnsJS, getOpenGraphImageURL, getFullURL

from os.path import join

@public_bp.route("/")
def landing():
    	
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
		full_url = full_url
		)

@js.route("/public/js/webGL.js", methods=["GET"])
@returnsJS
def get_js():
    	
	shape_path = current_app.config["SHAPE_DIR"]
	ifc_file = ifcopenshell.open(join(current_app.config["BASE_DIR"],"app","static","ifc","AC20-FZK-Haus.ifc"))
	my_ren = ThreejsRenderer(path = shape_path )
	Append_IFC_Shapes_To_ThreejsRenderer_Object(my_ren,ifc_file)
	shape_content = my_ren.generate_shape_imort_string()

	return render_template("public/js/webGL.js", shape_content = shape_content)

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass