# -*- #################
# ---------------------------------------------------------------------------
# Ruteo.py
# Uso: Ruteo <Tool> <PAE>
# Descripcion: Tool para crear los Ruteos
# ---------------------------------------------------------------------------

# Importar arcpy module
import os
import io
import datetime
import arcpy
import time
import sys
from datetime import date

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

############################################################
# MAIN
text_file = None
STARTUP_PATH = os.path.dirname(__file__)
timestr = time.strftime("%Y%m%d-%H%M%S")
file_output = "\\logs\\Ruteo-" + timestr + ".txt"

if (len(sys.argv) < 2):
	log('-' * 40)
	log(' [ARGUMENTS] ')
	log('**Error: Debe ingresar una UG como argumento')
	sys.exit()

#UG
UG = sys.argv[1]
#Conexion SDE
SOURCE = STARTUP_PATH + "/conn_" + UG + ".sde"
#Base File temporal para almacenar los Features
BASE = STARTUP_PATH
BASE_T = STARTUP_PATH
#Carpeta de Salida de los Ruteos
SALIDA = STARTUP_PATH + "/Ruteo/"
#Owner de la Base de Datos.
#owner = "/RNSL."
owner = "/"
#Nombre de Geocoder Compuesto
Geocod_Composite_MRS = SALIDA + "Ruteo_" + UG
#FeatureDataSet de Caminos
FD = "FD_Red_Caminos"

if not os.path.exists(SOURCE):
	log('-' * 40)
	log('** Error: No existe la conexion: ' + SOURCE)
	log('-' * 40)
	log(" [END] - OK")
	log('-' * 40)
	sys.exit()

try:
	log('-' * 40)
	log(" [INICIO UG: " + UG +  "] ")
	log('-' * 40)

	log("CheckOut Extension: Network Analyst")
	log('-' * 40)

	if arcpy.CheckExtension("Network") != "Available":
		log("Not Available License: Network Analyst")
		log('-' * 40)
		log(" [END] - OK")
		log('-' * 40)
		sys.exit()
	else:
		arcpy.CheckOutExtension("Network")
	
	bd = "Ruteo_" + UG + ".gdb"

	if os.path.exists(os.path.join(BASE,bd)):
		log("Delete FGDB: " + os.path.join(BASE,bd))
		arcpy.Delete_management(os.path.join(BASE,bd))

	log("Create FGDB: " + os.path.join(BASE,bd))
	arcpy.CreateFileGDB_management(BASE, bd)

	if os.path.exists(os.path.join(BASE,"Ruteo_temp.gdb")):
		log("Delete Temp FGDB: " + os.path.join(BASE,"Ruteo_temp.gdb"))
		arcpy.Delete_management(os.path.join(BASE,"Ruteo_temp.gdb"))

	log("Create Temp FGDB: " + os.path.join(BASE,"Ruteo_temp.gdb"))
	arcpy.CreateFileGDB_management(BASE, "Ruteo_temp.gdb")

	BASE = os.path.join(BASE,bd)
	BASE_T = os.path.join(BASE_T,"Ruteo_temp.gdb")

	arcpy.env.workspace = SOURCE

	if UG == "GSJ":
		features = ["FC_Cam_Bloqueos", "FC_Cam_Caminos", "FC_Cam_Giros", "FC_Cam_Obras", "FC_Cam_Bifurcaciones", "FC_Cam_Mojones"]
	elif UG == "ACA":
		features = ["FC_Cam_Bloqueos", "FC_Cam_Caminos", "FC_Cam_Giros", "FC_Captura_Agua", "FC_Obras_Arte", "FC_Cam_Mojones"]
	elif UG == "NQN":
		features = ["FC_Cam_Bloqueos", "FC_Cam_Caminos", "FC_Cam_Giros", "FC_Cam_Obras", "FC_Cam_PuestosControl", "FC_Cam_Bifurcaciones", "FC_Cam_Mojones"]
	else:
		features = []
		log("UG not exists: " + UG)
	
	try:
		log("Create Custom Transformation GSJ: PampaToWGS")
		#La transformacion Custon se genera en la siguiente Ruta.
		#C:\Users\[USER]\AppData\Roaming\Esri\Desktop10.8\ArcToolbox\CustomTransformations

		#Con decimales
		#arcpy.CreateCustomGeoTransformation_management(geot_name="PampaToMercator", in_coor_system="PROJCS['Pampa_del_Castillo_Argentina_2',GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',-232.567],PARAMETER['Y_Axis_Translation',6.6637],PARAMETER['Z_Axis_Translation',173.928]]")
		#Sin decimales
		#arcpy.CreateCustomGeoTransformation_management(geot_name="PampaToMercator", in_coor_system="PROJCS['Pampa_del_Castillo_Argentina_2',GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',-232],PARAMETER['Y_Axis_Translation',6],PARAMETER['Z_Axis_Translation',173]]")
		#WGS
		arcpy.CreateCustomGeoTransformation_management(geot_name="PampaToWGS", in_coor_system="GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',-232],PARAMETER['Y_Axis_Translation',6],PARAMETER['Z_Axis_Translation',173]]")               
	except Exception as e:
		log("Custom Transformation GSJ: " + "PampaToWGS, Already exists")

	try:
		log("Create Custom Transformation ACA: ArgentinaZone4ToWGS")
		#La transformacion Custon se genera en la siguiente Ruta.
		#C:\Users\[USER]\AppData\Roaming\Esri\Desktop10.8\ArcToolbox\CustomTransformations

		#Con decimales
		#arcpy.CreateCustomGeoTransformation_management(geot_name="PampaToMercator", in_coor_system="PROJCS['Pampa_del_Castillo_Argentina_2',GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',-232.567],PARAMETER['Y_Axis_Translation',6.6637],PARAMETER['Z_Axis_Translation',173.928]]")
		#Sin decimales
		#arcpy.CreateCustomGeoTransformation_management(geot_name="ArgentinaZone4ToMercator", in_coor_system="PROJCS['Argentina_Zone_4',GEOGCS['GCS_Campo_Inchauspe',DATUM['D_Campo_Inchauspe',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',4500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-63.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Geocentric_Translation'],PARAMETER['X_Axis_Translation',-148.0],PARAMETER['Y_Axis_Translation',136.0],PARAMETER['Z_Axis_Translation',90.0]]")
		arcpy.CreateCustomGeoTransformation_management(geot_name="ArgentinaZone4ToWGS", in_coor_system="GEOGCS['GCS_Campo_Inchauspe',DATUM['D_Campo_Inchauspe',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Geocentric_Translation'],PARAMETER['X_Axis_Translation',-148.0],PARAMETER['Y_Axis_Translation',136.0],PARAMETER['Z_Axis_Translation',90.0]]")
	except Exception as e:
		log("Custom Transformation ACA: " + "ArgentinaZone4ToWGS, Already exists")

	try:
		log("Create Custom Transformation NQN: ChosmalalToWGS")
		#La transformacion Custon se genera en la siguiente Ruta.
		#C:\Users\[USER]\AppData\Roaming\Esri\Desktop10.8\ArcToolbox\CustomTransformations

		#Con decimales
		#arcpy.CreateCustomGeoTransformation_management(geot_name="ChosmalalToMercator", in_coor_system="PROJCS['Chos_Malal_1914_Argentina_2',GEOGCS['GCS_Chos_Malal_1914',DATUM['D_Chos_Malal_1914',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',10.04400],PARAMETER['Y_Axis_Translation',163.96700],PARAMETER['Z_Axis_Translation',131.71800]]")
		#Sin decimales
		arcpy.CreateCustomGeoTransformation_management(geot_name="ChosmalalToWGS", in_coor_system="GEOGCS['GCS_Chos_Malal_1914',DATUM['D_Chos_Malal_1914',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", custom_geot="GEOGTRAN[METHOD['Molodensky'],PARAMETER['X_Axis_Translation',10.0],PARAMETER['Y_Axis_Translation',163.0],PARAMETER['Z_Axis_Translation',131.0]]")
	except Exception as e:
		log("Custom Transformation NQN: " + "ChosmalalToWGS, Already exists")

	log('-' * 40)
	log(" [REFRESH DATA] ")
	log('-' * 40)

	try:
		log("Create DataSet")
		log('-' * 40)

		#arcpy.CreateFeatureDataset_management(out_dataset_path=BASE, out_name=FD, spatial_reference="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision")
		#arcpy.CreateFeatureDataset_management(out_dataset_path=BASE, out_name=FD, spatial_reference="PROJCS['WGS_1984',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137 .0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision")
		arcpy.CreateFeatureDataset_management(out_dataset_path=BASE, out_name=FD, spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision")
		log("Copy FeaturesClasses")
		log('-' * 40)
		for fc in features:
			Origen = SOURCE + "/" + UG + "." + FD + "/" + UG + "."
			log("Copy Feature: " + fc)
			arcpy.FeatureClassToGeodatabase_conversion(Input_Features=Origen + fc, Output_Geodatabase=BASE_T + "/")
	except Exception as e:
	    log("Error in Copy FeatureDataSet: " + FD + ": " + str(e))

	log('-' * 40)
	log(" [PROJECT DATA] ")
	log('-' * 40)

	try:
		for fc in features:
			if UG == "GSJ":
				log("Project Feature: " + fc)
				#arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="PampaToWGS", in_coor_system="PROJCS['Pampa_del_Castillo_Argentina_2',GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
				#arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="PROJCS['WGS_1984',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method="PampaToWGS", in_coor_system="PROJCS['Pampa_del_Castillo_Argentina_2',GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
				arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],AUTHORITY['EPSG',4326]]", transform_method="PampaToWGS", in_coor_system="PROJCS['Pampa_del_Castillo_Argentina_2',GEOGCS['GCS_Pampa_del_Castillo',DATUM['D_Pampa_del_Castillo',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]] NO_PRESERVE_SHAPE # NO_VERTICAL")
			elif UG == "ACA":
				log("Project Feature: " + fc)
				#arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="ArgentinaZone4ToMercator", in_coor_system="PROJCS['Argentina_Zone_4',GEOGCS['GCS_Campo_Inchauspe',DATUM['D_Campo_Inchauspe',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',4500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-63.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
				arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],AUTHORITY['EPSG',4326]]", transform_method="ArgentinaZone4ToWGS", in_coor_system="PROJCS['Argentina_Zone_4',GEOGCS['GCS_Campo_Inchauspe',DATUM['D_Campo_Inchauspe',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',4500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-63.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
			elif UG == "NQN":
				log("Project Feature: " + fc)
				#arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", transform_method="ChosmalalToMercator", in_coor_system="PROJCS['Chos_Malal_1914_Argentina_2',GEOGCS['GCS_Chos_Malal_1914',DATUM['D_Chos_Malal_1914',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
				arcpy.Project_management(in_dataset=BASE_T + "/" + fc, out_dataset=BASE + "/" + FD + "/" + fc, out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],AUTHORITY['EPSG',4326]]", transform_method="ChosmalalToWGS", in_coor_system="PROJCS['Chos_Malal_1914_Argentina_2',GEOGCS['GCS_Chos_Malal_1914',DATUM['D_Chos_Malal_1914',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-90.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
			else:
				log("UG not exists: " + UG)
	except Exception as e:
	    log("Error in Copy Feature: " + FD + ": " + str(e))

	log('-' * 40)
	log(" [CREATE NETWORK] ")
	log('-' * 40)
	
	try:
		if os.path.exists(STARTUP_PATH + "/Plantilla_Red_" + UG + ".xml"):
			log("Create Network Dataset From Template")
			log('-' * 40)
			arcpy.CreateNetworkDatasetFromTemplate_na(network_dataset_template= STARTUP_PATH + "/Plantilla_Red_" + UG + ".xml", output_feature_dataset=BASE + "/" + FD)

			log("Build Network")
			log('-' * 40)
			arcpy.BuildNetwork_na(in_network_dataset=BASE + "/" + FD + "/" + FD + "_ND")

			arcpy.CheckInExtension("Network")
		else:
			log("Not Exist XML: " + "/Plantilla_Red_" + UG + ".xml")
	except Exception as e:
	    log("Error in Create Network: " + str(e))
            
	if os.path.exists(BASE_T):
		log("Delete Temp FGDB: " + BASE_T)
		arcpy.Delete_management(BASE_T)
               
	log('-' * 40)
	log(" [END] - OK")
	log('-' * 40)
except Exception, e:
	log("|Error!!\n   " + str(e) + ']')

	raise
