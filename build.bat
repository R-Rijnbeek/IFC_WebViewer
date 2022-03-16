( 
    echo FLASK_APP=hello.py 
    if  "%DEVELOP_HOST%"=="" ( echo FLASK_RUN_HOST=localhost ) else ( echo FLASK_RUN_HOST=%DEVELOP_HOST% ) 
    if  "%DEVELOP_PORT%"=="" ( echo FLASK_RUN_HOST=localhost ) else ( echo FLASK_RUN_HOST=%DEVELOP_PORT% )
) > .flaskenv

conda env create -f environment.yml --prefix env