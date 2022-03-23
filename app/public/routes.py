
from flask import abort, render_template, current_app

import ifcopenshell

from . import public_bp
from ..utils import ThreejsRenderer, Append_IFC_Shapes_To_ThreejsRenderer_Object

from os.path import join

@public_bp.route("/")
def landing():

	owner = current_app.config["OWNER"]
	owner_email = current_app.config["OWNER_EMAIL"]
	occ_version = current_app.config["OCC_VERSION"]
	threejs_release = current_app.config["THREEJS_RELEASE"]
	shape_path = current_app.config["SHAPE_DIR"]

	ifc_file = ifcopenshell.open(join(current_app.config["BASE_DIR"],"app","static","ifc","AC20-FZK-Haus.ifc"))
	my_ren = ThreejsRenderer(path = shape_path )
	Append_IFC_Shapes_To_ThreejsRenderer_Object(my_ren,ifc_file)
	shape_content = my_ren.generate_shape_imort_string()

	return render_template("public/landing.html",owner = owner, owner_email=owner_email,occ_version = occ_version, threejs_release = threejs_release, shape_content = shape_content)

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass