@echo OFF

set CUR_YYYY=%date:~11,4%
set CUR_MM=%date:~5,2%
set CUR_DD=%date:~8,2%
set CUR_HH=%time:~0,2%
set CUR_NN=%time:~3,2%
set CUR_SS=%time:~6,2%
if "%CUR_HH:~0,1%" == " " set CUR_HH=0%time:~1,1%

set fileName= %~d0%~p0\logs\log-MMPK.txt

set server=https://portalsigpae-desa.domainba.com/portal
set u=admin
set p=4rcg1s2020
set gy=GIS_CAMYac_
set gs=GIS_CAMSeguridad_
set ge=GG_APP_GIS_ExpGral_

echo  ---------- Refrescando MMPK Navigator GSJ ----------- >>%fileName%
rem call "d:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK.py >>%fileName%
"D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Navigator.py GSJ %gy% %server% %u% %p% >>%fileName%
"D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Navigator.py GSJ %gs% %server% %u% %p% >>%fileName%

echo  ---------- Refrescando MMPK Navigator NQN ----------- >>%fileName%
rem call "d:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK.py >>%fileName%
rem "D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Navigator.py NQN %gy% %server% %u% %p% >>%fileName%
rem "D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Navigator.py NQN %gs% %server% %u% %p% >>%fileName%

echo  ---------- Refrescando MMPK Explorer GSJ ----------- >>%fileName%
"D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Explorer.py GSJ %ge% %server% %u% %p% >>%fileName%
echo  ---------- Refrescando MMPK Explorer NQN ----------- >>%fileName%
"D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Explorer.py NQN %ge% %server% %u% %p% >>%fileName%
echo  ---------- Refrescando MMPK Explorer ACA ----------- >>%fileName%
"D:\Apps\ArcGIS\bin\Python\envs\arcgispro-py3\python.exe" %~d0%~p0\MMPK_Explorer.py ACA %ge% %server% %u% %p% >>%fileName%
pause