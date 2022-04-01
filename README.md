# IFC_WebViewer

A webViewer application that visualize IFC content of a file on web browser. Tested with IFC2X3

* EXAMPLE: [ Visit web ](http://flask-ifc-viewer.herokuapp.com/)

## prerequisites

Has anaconda installed on windows. And configured you system variables ($path) of anaconda on windows: 
* C:\ProgramData\Anaconda3
* C:\ProgramData\Anaconda3\Scripts
* C:\ProgramData\Anaconda3\Library\bin

## Instalation protocol

1. Clone the github repository.
```
$ git clone https://github.com/R-Rijnbeek/IFC_WebViewer.git
```

2. Enter the project folder.
```
$ cd IFC_WebViewer
```

3. Build the virtual environment on the repository by running:
```
$ build.bat
```

4. To activate the environmet and run the scripts:
```
$ activate ./env
$ python entrypoint.py
```

If it works. Than you can open your webbrowser and visualize the IFC content on: http://localhost:8080/

## Notes to know: 

1. The dependencies to use all features of this repository are writed on the environmet.yml file: OCC, ifcopenshell and Flask
2. If you will only use the content of this repository. On a other project than you need to create an virtual environment that include "ifcopenshell", "OCC" and "flask"
    * ANACONDA:
    ```
    conda install -c conda-forge pythonocc-core ifcopenshell
    conda install -c anaconda flask
    ``` 

3. This repository is tested with windows 10 and anaconda version 4.11.0.

## Improvments

1. Uploaded ifc files will must be stored in memory and no on a location of the server.
2. Include multiprocessing to make the process rendering process faster on server site.
3. Put an render process bar on client side when ifc file is processed on server site.
4. Remove all tree.js instances when reloading an new object.
5. Will be fine to include and opacity slider GUI on rendering window.
6. ....
