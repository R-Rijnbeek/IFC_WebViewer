# =============== IMPORTS ==============

from flask import make_response, url_for, current_app
from OCC.Core.Tesselator import ShapeTesselator
from OCC.Extend.TopologyUtils import is_edge, is_wire, discretize_edge, discretize_wire
import ifcopenshell.geom

from functools import wraps
import os
import sys
import glob
import json
from uuid import uuid4

from .shared import LOG

# ============= DECORATORS ==========

def returnsJS(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs),200)
        resp.headers['Content-Type'] = 'application/javascript'
        return resp
    return decorated_function

def methodLogging(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        uniqueID = uuid4()
        LOG.info(json.dumps({"uniqueID":str(uniqueID), "metodo": f.__name__ ,"type":str(f.__class__), "path":f.__code__.co_filename, "arg": str(args) , "kwargs": str(kwargs)}))
        output = f(*args, **kwargs)
        LOG.info(json.dumps({"uniqueID":str(uniqueID), "metodo": f.__name__ , "output": str(output)}))
        return output
    return decorated_function

# =============== PROCESS ===============

def GetTextureFromIfcProduct(IFC_PRODUCT,MODE=""):
    """
    INPUT:
        - PRODUCT => IfcProduct object
    OUTPUT:
        - Typle of lenght 4
            COLOR FOUND: True
                - [0] RED => Float in range (0,1)
                - [1] GREEN => Float in range (0,1)
                - [2] BLUE => Float in range (0,1)
                - [3] OPACITY => Float in range (0,1)
            COLOR FOUND: False
                - [0] RED     = 1. Float 
                - [1] GREEN   = 1. Float 
                - [2] BLUE    = 1. Float
                - [3] OPACITY = 1. Float
    """
    try:
        representation=IFC_PRODUCT.Representation
        representations=representation.Representations
        for the_representation in representations:
            if (the_representation.RepresentationIdentifier in ["Body","Facetation"]):
                #the_representation=representations[0]
                Items=the_representation.Items
                Item=Items[0]
                StyledByItems=Item.StyledByItem
                if len(StyledByItems)>0:
                    StyledByItem=StyledByItems[0]
                    Styles=StyledByItem.Styles
                    Style=Styles[0]
                    Styles_2=Style.Styles
                    Style_2=Styles_2[0]
                    Styles_3=Style_2.Styles
                    Style_3=Styles_3[0]
                    Surface_Colour=Style_3.SurfaceColour
                    Red=Surface_Colour.Red
                    Green=Surface_Colour.Green
                    Blue=Surface_Colour.Blue
                    if "Transparency" in list(Style_3.__dict__):
                        transparency = Style_3.Transparency
                        if transparency is None:
                            opacity = 1.
                        else:
                            if MODE == "Sketchup":
                                opacity = transparency
                            else:
                                opacity = 1-transparency
                    else:
                        opacity = 1.
                    return Red, Green, Blue, opacity
        Red=1.
        Green=1.
        Blue=1.
        opacity=1.
        return Red, Green, Blue, opacity
    except:
        Red=1.
        Green=1.
        Blue=1.
        opacity=1.
        return Red, Green, Blue, opacity

@methodLogging
def DeleteJSONFilesFromDirectory(PATH):
    try:
        files = glob.glob(f'{PATH}*.json')
        for f in files:
            os.remove(f)
        return True
    except Exception as exc:
        LOG.error(f"ERROR {LOG.getFunctionName()}: {exc}")
        return False

@methodLogging
def CreateDirectoryIfItNotExist(PATH):
    try:
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        return True
    except Exception as exc:
        LOG.error(f"ERROR {LOG.getFunctionName()}: {exc}")
        return False

@methodLogging
def Append_IFC_Shapes_To_ThreejsRenderer_Object(THREEJS_RENDERER_OBJECT,IFC_FILE):
    settings=ifcopenshell.geom.settings( )
    settings.set( settings.USE_PYTHON_OPENCASCADE , True)
    products = IFC_FILE.by_type( "IfcProduct" )
    for product in products :
        if product.is_a("IfcOpeningElement") or product.is_a("IfcAnnotation") or product.is_a("IfcSpace"):
            continue
        if product.Representation:
            print(product.is_a())

            r,g,b,o = GetTextureFromIfcProduct(product)
            shape = ifcopenshell.geom.create_shape(settings, product).geometry
            THREEJS_RENDERER_OBJECT.DisplayShape(shape, export_edges=False,color = (r,g,b),transparency = 0.5)

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def color_to_hex(rgb_color):
    """ Takes a tuple with 3 floats between 0 and 1.
    Returns a hex. Useful to convert occ colors to web color code
    """
    r, g, b = rgb_color
    if not (0 <= r <= 1. and 0 <= g <= 1. and 0 <= b <= 1.):
        raise AssertionError("rgb values must be between 0.0 and 1.0")
    rh = int(r * 255.)
    gh = int(g * 255.)
    bh = int(b * 255.)
    return "0x%.02x%.02x%.02x" % (rh, gh, bh)

def export_edgedata_to_json(edge_hash, point_set):
    """ Export a set of points to a LineSegment buffergeometry
    """
    # first build the array of point coordinates
    # edges are built as follows:
    # points_coordinates  =[P0x, P0y, P0z, P1x, P1y, P1z, P2x, P2y, etc.]
    points_coordinates = []
    for point in point_set:
        for coord in point:
            points_coordinates.append(coord)
    # then build the dictionnary exported to json
    edges_data = {"metadata": {"version": 4.4,
                               "type": "BufferGeometry",
                               "generator": "pythonocc"},
                  "uuid": edge_hash,
                  "type": "BufferGeometry",
                  "data": {"attributes": {"position": {"itemSize": 3,
                                                       "type": "Float32Array",
                                                       "array": points_coordinates}
                                         }
                          }
                  }
    return json.dumps(edges_data)


class ThreejsRenderer:
    def __init__(self, path=None):
        self._path = path
        #self._html_filename = os.path.join(self._path, "index.html")
        self._3js_shapes = {}
        self._3js_edges = {}
        self.spinning_cursor = spinning_cursor()
        #print("## threejs %s webgl renderer" % THREEJS_RELEASE)

    
    def DisplayShape(self,
                     shape,
                     export_edges=False,
                     color=(0.65, 0.65, 0.7),
                     specular_color=(0.2, 0.2, 0.2),
                     shininess=0.9,
                     transparency=0.,
                     line_color=(0, 0., 0.),
                     line_width=1.,
                     mesh_quality=1.):
        # if the shape is an edge or a wire, use the related functions
        if is_edge(shape):
            print("discretize an edge")
            pnts = discretize_edge(shape)
            edge_hash = "edg%s" % uuid4().hex
            str_to_write = export_edgedata_to_json(edge_hash, pnts)
            edge_full_path = os.path.join(self._path, edge_hash + '.json')
            with open(edge_full_path, "w") as edge_file:
                edge_file.write(str_to_write)
            # store this edge hash
            self._3js_edges[edge_hash] = [color, line_width]
            return self._3js_shapes, self._3js_edges
        elif is_wire(shape):
            print("discretize a wire")
            pnts = discretize_wire(shape)
            wire_hash = "wir%s" % uuid4().hex
            str_to_write = export_edgedata_to_json(wire_hash, pnts)
            wire_full_path = os.path.join(self._path, wire_hash + '.json')
            with open(wire_full_path, "w") as wire_file:
                wire_file.write(str_to_write)
            # store this edge hash
            self._3js_edges[wire_hash] = [color, line_width]
            return self._3js_shapes, self._3js_edges
        shape_uuid = uuid4().hex
        shape_hash = "shp%s" % shape_uuid
        # tesselate
        tess = ShapeTesselator(shape)
        tess.Compute(compute_edges=export_edges,
                     mesh_quality=mesh_quality,
                     parallel=True)
        # update spinning cursor
        sys.stdout.write("\r%s mesh shape %s, %i triangles     " % (next(self.spinning_cursor),
                                                                    shape_hash,
                                                                    tess.ObjGetTriangleCount()))
        sys.stdout.flush()
        # export to 3JS
        shape_full_path = os.path.join(self._path, shape_hash + '.json')
        # add this shape to the shape dict, sotres everything related to it
        self._3js_shapes[shape_hash] = [export_edges, color, specular_color, shininess, transparency, line_color, line_width]
        # generate the mesh
        #tess.ExportShapeToThreejs(shape_hash, shape_full_path)
        # and also to JSON
        with open(shape_full_path, 'w') as json_file:
            json_file.write(tess.ExportShapeToThreejsJSONString(shape_uuid))
        # draw edges if necessary
        if export_edges:
            # export each edge to a single json
            # get number of edges
            nbr_edges = tess.ObjGetEdgeCount()
            for i_edge in range(nbr_edges):
                # after that, the file can be appended
                str_to_write = ''
                edge_point_set = []
                nbr_vertices = tess.ObjEdgeGetVertexCount(i_edge)
                for i_vert in range(nbr_vertices):
                    edge_point_set.append(tess.GetEdgeVertex(i_edge, i_vert))
                # write to file
                edge_hash = "edg%s" % uuid4().hex
                str_to_write += export_edgedata_to_json(edge_hash, edge_point_set)
                # create the file
                edge_full_path = os.path.join(self._path, edge_hash + '.json')
                with open(edge_full_path, "w") as edge_file:
                    edge_file.write(str_to_write)
                # store this edge hash, with black color
                self._3js_edges[edge_hash] = [(0, 0, 0), line_width]
        return self._3js_shapes, self._3js_edges

    @methodLogging
    def generate_shape_import_string(self):
        """ Generate the HTML file to be rendered by the web browser
        """
        #global BODY_PART0

        # loop over shapes to generate html shapes stuff
        # the following line is a list that will help generating the string
        # using "".join()
        string_to_export = ""
        shape_string_list = []
        shape_string_list.append("loader = new THREE.BufferGeometryLoader();\n")
        shape_idx = 0
        for shape_hash in self._3js_shapes:
            # get properties for this shape
            export_edges, color, specular_color, shininess, transparency, line_color, line_width = self._3js_shapes[shape_hash]
            # creates a material for the shape
            shape_string_list.append('\t\t\t%s_phong_material = new THREE.MeshPhongMaterial({' % shape_hash)
            shape_string_list.append('color:%s,' % color_to_hex(color))
            shape_string_list.append('specular:%s,' % color_to_hex(specular_color))
            shape_string_list.append('shininess:%g,' % shininess)
            # force double side rendering, see issue #645
            shape_string_list.append('side: THREE.DoubleSide,')
            if transparency > 0.:
                shape_string_list.append('transparent: true, premultipliedAlpha: true, opacity:%g,' % transparency)
            #var line_material = new THREE.LineBasicMaterial({color: 0x000000, linewidth: 2});
            shape_string_list.append('});\n')
            # load json geometry files
            shape_string_list.append("\t\t\tloader.load('static/shapes/%s.json', function(geometry) {\n" % shape_hash)
            shape_string_list.append("\t\t\t\tmesh = new THREE.Mesh(geometry, %s_phong_material);\n" % shape_hash)
            # enable shadows for object
            shape_string_list.append("\t\t\t\tmesh.castShadow = true;\n")
            shape_string_list.append("\t\t\t\tmesh.receiveShadow = true;\n")
            # add mesh to scene
            shape_string_list.append("\t\t\t\tscene.add(mesh);\n")
            # last shape, we request for a fit_to_scene
            if shape_idx == len(self._3js_shapes) - 1:
                shape_string_list.append("\tfit_to_scene();});\n")
            else:
                shape_string_list.append("\t\t\t});\n\n")
            shape_idx += 1
        # Process edges
        edge_string_list = []
        
        for edge_hash in self._3js_edges:
            color, line_width = self._3js_edges[edge_hash]
            edge_string_list.append("\tloader.load('static/shapes/%s.json', function(geometry) {\n" % edge_hash)
            edge_string_list.append("\tline_material = new THREE.LineBasicMaterial({color: %s, linewidth: %s});\n" % ((color_to_hex(color), line_width)))
            edge_string_list.append("\tline = new THREE.Line(geometry, line_material);\n")
        # add mesh to scene
            edge_string_list.append("\tscene.add(line);\n")
            edge_string_list.append("\t});\n")
        # write the string for the shape
        string_to_export += "".join(shape_string_list)
        string_to_export += "".join(edge_string_list)
        return string_to_export

# ============== REQUEST FUNCTIONS ============

def getOpenGraphImageURL(REQUEST):
    return "".join([REQUEST.host_url[:-1], url_for( 'static', filename='image/Image_IFC_Viewer.png' )])

def getFullURL(REQUEST):
    return REQUEST.base_url

# =============== Upload file ===============

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["UPLOADED_EXTENSIONS"]

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass