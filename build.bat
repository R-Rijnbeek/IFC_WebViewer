if not exist ".\.vscode\" mkdir .\.vscode

( 
    echo {
    echo     // Use IntelliSense to learn about possible attributes.
    echo     // Hover to view descriptions of existing attributes.
    echo     // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    echo     "version": "0.2.0",
    echo     "configurations": [
    echo         {
    echo             "name": "Python: Archivo actual",
    echo             "type": "python",
    echo             "request": "launch",
    echo             "program": "${file}",
    echo             "console": "integratedTerminal"
    echo         }
    echo     ]
    echo }
) > .\.vscode\launch.json

( 
    echo {
    echo     "python.defaultInterpreterPath": ".\\env\\python.exe",
    echo }
) > .\.vscode\settings.json

conda env create -f environment.yml --prefix env