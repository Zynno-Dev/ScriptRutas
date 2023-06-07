@echo OFF
title Ejecucion Proceso de Generacion de Ruteo

set CUR_YYYY=%date:~11,4%
set CUR_MM=%date:~5,2%
set CUR_DD=%date:~8,2%

set CUR_HH=%time:~0,2%
if "%CUR_HH:~0,1%" == " " set CUR_HH=0%hour:~1,1%
set CUR_NN=%time:~3,2%
if "%CUR_NN:~0,1%" == " " set CUR_NN=0%min:~1,1%
set CUR_SS=%time:~6,2%
if "%CUR_SS:~0,1%" == " " set CUR_SS=0%secs:~1,1%

set fileName= %~d0%~p0\Logs\log-%CUR_YYYY%%CUR_MM%%CUR_DD%-%CUR_HH%%CUR_NN%%CUR_SS%.txt

set server=https://portalsigpae-desa.domainba.com/server
set u=admin
set p=4rcg1s2020

set service=SIGPAE_NQN/Ruteo_Caminos_NQN

echo  ---------- Deteniendo el servicio de Ruteo ----------- >>%fileName%
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o stop
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o status>>%fileName%

echo  ---------- Refrescando todos los Locators ----------- >>%fileName%
call %~d0%~p0\Ruteo.py NQN >>%fileName%

echo  ---------- Iniciando servicio de Ruteo ----------- >>%fileName%
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o start
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o status>>%fileName%

set service=SIGPAE_GSJ/Ruteo_Caminos_GSJ

echo  ---------- Deteniendo el servicio de Ruteo ----------- >>%fileName%
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o stop
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o status>>%fileName%

echo  ---------- Refrescando todos los Locators ----------- >>%fileName%
call %~d0%~p0\Ruteo.py GSJ >>%fileName%

echo  ---------- Iniciando servicio de Ruteo ----------- >>%fileName%
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o start
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o status>>%fileName%

set service=SIGPAE_ACA/Ruteo_Caminos_ACA

echo  ---------- Deteniendo el servicio de Ruteo ----------- >>%fileName%
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o stop
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o status>>%fileName%

echo  ---------- Refrescando todos los Locators ----------- >>%fileName%
call %~d0%~p0\Ruteo.py ACA >>%fileName%

echo  ---------- Iniciando servicio de Ruteo ----------- >>%fileName%
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o start
%~d0%~p0\manageservice.py -u %u% -p %p% -s %server% -n %service% -o status>>%fileName%