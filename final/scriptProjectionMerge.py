# -*- #################
# ---------------------------------------------------------------------------
# scriptProjectionMerge.py
# Uso: Transformacion/Fusion <Tool> <PAE>
# Descripcion: Tool para Cambiar referencia geografica, y fusionarlos en un .gdb
# ---------------------------------------------------------------------------

# Importar arcpy module
import os
import io
import datetime
import arcpy
import time
import sys
from datetime import date
from shutil import rmtree

global text_file

############################################################
# Definicion de funcion de log

def log(message):
	strFile = STARTUP_PATH
	strFile = strFile + file_output
	global text_file
	if text_file == None:
		arcpy.AddMessage('-' * 40)
		arcpy.AddMessage(" [CREATE LOG FILE] ")
		text_file = open(strFile, "w")
	text_file.write("\n" + str(datetime.datetime.now()) + " " + message)
	text_file.flush()

	arcpy.AddMessage(message)

text_file = None
STARTUP_PATH = os.path.dirname(__file__)
timestr = time.strftime("%Y%m%d-%H%M%S")
file_output = "\\logs\\Transf-" + timestr + ".txt"
carpeta_actual = os.path.dirname(os.path.abspath(__file__))

############################################################
# Creacion .gtf

try:
    log("Create Custom Transformation GSJ: PampaToWGS")
    arcpy.CreateCustomGeoTransformation_management(geot_name="PampaToWGS", in_coor_system="GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',-232],PARAMETER['Y_Axis_Translation',6],PARAMETER['Z_Axis_Translation',173]]")               
except Exception as e:
    log("Custom Transformation GSJ: " + "PampaToWGS, Already exists")

try:
    log("Create Custom Transformation ACA: ArgentinaZone4ToWGS")
    arcpy.CreateCustomGeoTransformation_management(geot_name="ArgentinaZone4ToWGS", in_coor_system="GEOGCS['GCS_Campo_Inchauspe',DATUM['D_Campo_Inchauspe',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Geocentric_Translation'],PARAMETER['X_Axis_Translation',-148.0],PARAMETER['Y_Axis_Translation',136.0],PARAMETER['Z_Axis_Translation',90.0]]")
except Exception as e:
    log("Custom Transformation ACA: " + "ArgentinaZone4ToWGS, Already exists")

try:
    log("Create Custom Transformation NQN: ChosmalalToWGS")
    arcpy.CreateCustomGeoTransformation_management(geot_name="ChosmalalToWGS", in_coor_system="GEOGCS['GCS_Chos_Malal_1914',DATUM['D_Chos_Malal_1914',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',10.0],PARAMETER['Y_Axis_Translation',163.0],PARAMETER['Z_Axis_Translation',131.0]]")
except Exception as e:
    log("Custom Transformation NQN: " + "ChosmalalToWGS, Already exists")

############################################################
# Transformacion

gdb_path = os.path.join(carpeta_actual, 'Servicios_NQN.gdb')

proyectado_gdb_path = os.path.join(carpeta_actual, 'proyectado.gdb')

# arcpy.env.workspace = "C:/Users/xnas02/Desktop/Script Ruteo Caminos/final"
# arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 18N")
# arcpy.env.geographicTransformations = "ChosMalalToWGS; PampaToWGS"

custom_transform = "ChosMalalToWGS"

feature_classes = []
for dirpath, dirnames, filenames in arcpy.da.Walk(gdb_path, datatype="FeatureClass"):
    for filename in filenames:
        feature_classes.append(os.path.join(dirpath, filename))
    log("Se obtuvieron todas las FC")

if not arcpy.Exists(proyectado_gdb_path):
    arcpy.CreateFileGDB_management(os.path.dirname(proyectado_gdb_path), os.path.basename(proyectado_gdb_path))
    log("Se creo la geodatabase de destino")

for fc_path in feature_classes:
    projected_fc_name = f"{os.path.splitext(os.path.basename(fc_path))[0]}_proyectada"

    projected_fc_path = os.path.join(proyectado_gdb_path, projected_fc_name)

    arcpy.Project_management(fc_path, projected_fc_path, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],AUTHORITY['EPSG',4326]]", custom_transform)
    
    print(f"La clase de entidad {fc_path} ha sido proyectada como {projected_fc_name} en la geodatabase de destino.")
    log(f"La clase de entidad {fc_path} ha sido proyectada como {projected_fc_name} en la geodatabase de destino.")

gdb_path = os.path.join(carpeta_actual, 'Servicios_GSJ.gdb')

proyectado_gdb_path = os.path.join(carpeta_actual, 'proyectado2.gdb')

custom_transform = "PampaToWGS"

feature_classes = []
for dirpath, dirnames, filenames in arcpy.da.Walk(gdb_path, datatype="FeatureClass"):
    for filename in filenames:
        feature_classes.append(os.path.join(dirpath, filename))
    log("Se obtuvieron todas las FC de la geodatabase original")

if not arcpy.Exists(proyectado_gdb_path):
    arcpy.CreateFileGDB_management(os.path.dirname(proyectado_gdb_path), os.path.basename(proyectado_gdb_path))

for fc_path in feature_classes:
    projected_fc_name = f"{os.path.splitext(os.path.basename(fc_path))[0]}_proyectada"

    projected_fc_path = os.path.join(proyectado_gdb_path, projected_fc_name)

    arcpy.Project_management(fc_path, projected_fc_path, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],AUTHORITY['EPSG',4326]]", custom_transform)

    print(f"La clase de entidad {fc_path} ha sido proyectada como {projected_fc_name} en la geodatabase de destino.")
    log(f"La clase de entidad {fc_path} ha sido proyectada como {projected_fc_name} en la geodatabase de destino.")
    
############################################################
# Fusion

geodatabase1 = os.path.join(carpeta_actual, 'proyectado.gdb')
geodatabase2 = os.path.join(carpeta_actual, 'proyectado2.gdb')
geodatabase_salida = os.path.join(carpeta_actual, 'Servicios_GSW.gdb')

if not arcpy.Exists(geodatabase_salida):
    arcpy.CreateFileGDB_management(os.path.dirname(geodatabase_salida), os.path.basename(geodatabase_salida))
    log("Se creo la geodatabase de salida")

arcpy.env.workspace = geodatabase1
lista_fc_geodatabase1 = arcpy.ListFeatureClasses()

arcpy.env.workspace = geodatabase2
lista_fc_geodatabase2 = arcpy.ListFeatureClasses()

if not arcpy.Exists(geodatabase_salida):
    arcpy.CreateFileGDB_management(os.path.dirname(geodatabase_salida), os.path.basename(geodatabase_salida))
    log("Se creo la geodatabase de salida")

arcpy.env.workspace = geodatabase1
for fc in lista_fc_geodatabase1:
    nombre_fc = os.path.splitext(fc)[0]

    arcpy.Merge_management([geodatabase1 + '\\' + fc, geodatabase2 + '\\' + fc], geodatabase_salida + '\\' + nombre_fc)

log("Se fusionaron las feature classes de las geodatabases de origen")

arcpy.env.workspace = geodatabase2
for fc in lista_fc_geodatabase2:
    try:
        nombre_fc = os.path.splitext(fc)[0]

        arcpy.Merge_management([geodatabase1 + '\\' + fc, geodatabase2 + '\\' + fc], geodatabase_salida + '\\' + nombre_fc)
    except:
        log("No se pudo fusionar la feature class " + fc)
        continue

rmtree(os.path.join(carpeta_actual, 'proyectado.gdb'))
rmtree(os.path.join(carpeta_actual, 'proyectado2.gdb'))