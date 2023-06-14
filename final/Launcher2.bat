@echo off
setlocal
title scriptProjectionMerge                                                                                                                                                                                                                                

:input
set "UGs="

set /p "UGs=Ingrese las UGs a migrar separadas por ';' : "

if "%UGs%"=="" (
    echo El campo de UGs esta vacio. Por favor, ingrese un valor valido.
    goto input
)

cls

C:\Windows\System32\cmd.exe /k "D:\Apps\ArcGIS\Pro\bin\Python\Scripts\propy.bat" scriptProjectionMerge2.py %UGs%

pause