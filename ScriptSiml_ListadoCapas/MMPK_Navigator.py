# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Navigator.py
# Uso: Navigator <Tool> <PAE>
# Descripcion: Tool para crear los MMPK para el Navigator
# ---------------------------------------------------------------------------

# Importar arcpy module
import os
import io
import datetime
import arcpy
import time
from datetime import date
import sys
from arcgis.gis import GIS
import shutil

############################################################
# Definicion de funcion de log
def log(message):
	global STARTUP_PATH
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
STARTUP_PATH = os.path.dirname(sys.argv[0])

timestr = time.strftime("%Y%m%d-%H%M%S")
file_output = "\\logs\\MMPK-Exp-" + timestr + ".txt"

if (len(sys.argv) < 6):
	log('-' * 40)
	log(' [ARGUMENTS] ')
	log('**Error: Faltan argumentos')
	sys.exit()

#log(str(sys.argv))
#sys.exit()

#UG
UG = sys.argv[1]
GR = sys.argv[2]

#Conexion SDE
SOURCE = STARTUP_PATH + "/conn_" + UG + ".sde"
#Base File temporal para almacenar los Features
BASE = STARTUP_PATH + "/" + UG + "/"
SERV = STARTUP_PATH + "/" + UG + "/"
#Carpeta de Salida de los Locators
SALIDA = STARTUP_PATH + "/Script/"
#Owner de la Base de Datos.
owner = "/"
#Nombre de los Feateures de Redes
FD_Red_Caminos = "FD_Red_Caminos"
FD_Cartografia_General = "FD_Cartografia_General"
#Datos Portal y Servicio
URL = sys.argv[3] #"https://gis.pan-energy.com/portal" #https://portalsigpae-desa.domainba.com/portal
USR = sys.argv[4] #
PSS = sys.argv[5] #

GROUP = GR + UG
MMPK = "Navigator_" + UG
MAPA = "M_Navigator_" + UG

if GROUP.find('Seguridad') > -1:
	MMPK = MMPK + "_Seguridad"
	MAPA = MAPA + "_Seguridad"
else:
	MMPK = MMPK + "_Yacimiento"
	MAPA = MAPA + "_Yacimiento"

FOLDER = UG + "_Map & App"

servicios = ["FC_Campamentos", "FC_POZOS_PI_INFOPROD", "FC_POZOS_PCG_LTP", "FC_POZOS_PCG_PRESUPUESTO", "FC_PuestoControl", "FC_Ele_Reconectadores", "FC_Ele_Seccionadores", "FC_Ele_Seccionalizadores", "FC_Ele_Interruptores", "FC_Manifolds", "FC_CargaderosAgua", "FC_Poblaciones", "FC_Tranqueras", "FC_Plantas", "FC_Compresores_Campo", "FC_Baterias", "FC_UnidadLACT", "FC_Punto_Venta_Gas", "FC_Puntos_Venteo", "FC_PMedicion_EMP", "FC_Canteras", "FC_Pozos_Dirigidos"]

try:
	log('-' * 40)
	log(" [INICIO] " + GR)
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

	if not os.path.isdir(STARTUP_PATH + "/" + UG + "/"):
		log("Create Folder UG: " + STARTUP_PATH + "/" + UG + "/")
		os.mkdir(STARTUP_PATH + "/" + UG + "/")
	#else:
	#	log("Delete Folder UG: " + STARTUP_PATH + "/" + UG + "/")
	#	shutil.rmtree(STARTUP_PATH + "/" + UG + "/", ignore_errors=True)

	if os.path.exists(os.path.join(SERV,"Servicios.gdb")):
		log("Delete Temp FGDB: " + os.path.join(SERV,"Servicios.gdb"))
		arcpy.Delete_management(in_data=os.path.join(SERV,"Servicios.gdb"), data_type="")

	log("Create Temp FGDB: " + os.path.join(SERV,"Servicios.gdb"))
	arcpy.CreateFileGDB_management(SERV, "Servicios.gdb")

	SERV = os.path.join(SERV,"Servicios.gdb")

	if os.path.exists(os.path.join(BASE,"Mapa base.gdb")):
		log("Delete Temp FGDB: " + os.path.join(BASE,"Mapa base.gdb"))
		arcpy.Delete_management(in_data=os.path.join(BASE,"Mapa base.gdb"), data_type="")

	log("Create Temp FGDB: " + os.path.join(BASE,"Mapa base.gdb"))
	arcpy.CreateFileGDB_management(BASE, "Mapa base.gdb")

	BASE = os.path.join(BASE,"Mapa base.gdb")

	if not os.path.isdir(SALIDA):
		log("Create Folder Script: " + SALIDA)
		os.mkdir(SALIDA)

	arcpy.env.workspace = SOURCE

	log('-' * 40)
	log(" [REFRESH DATA] ")
	log('-' * 40)

	log("Create DataSet: FD_Red_Caminos")
	arcpy.Copy_management(in_data=SOURCE + owner + FD_Red_Caminos, out_data=BASE + "/" + FD_Red_Caminos, data_type="FeatureDataset")

	log("Create DataSet: FD_Cartografia_General")
	arcpy.Copy_management(in_data=SOURCE + owner + FD_Cartografia_General, out_data=BASE + "/" + FD_Cartografia_General, data_type="FeatureDataset")

	
	for f in servicios:
		try:
			if arcpy.Exists(f):
				if arcpy.Exists(SERV + "/" + f):
					arcpy.Delete_management(SERV + "/" + f)

				arcpy.Select_analysis(in_features=SOURCE + owner + f, out_feature_class= SERV + "/" + f, where_clause="")
				log("Create Feature: " + f)
			else:
				log("Feature Class not exists: " + f)
				continue
		except Exception as e:
		    log("Create Feature " + f + ": " + str(e))

		log("Count: " + str(int(arcpy.GetCount_management(SERV + "/" + f).getOutput(0))))
	
	fc = "FC_Cam_Caminos"
	fccam = FD_Red_Caminos + "/" + fc

	try:
		if arcpy.Exists(fccam):
			if arcpy.Exists(BASE + "/" + fccam):
				log("Delete Network")
				arcpy.Delete_management(BASE + "/" + FD_Red_Caminos + "/" + FD_Red_Caminos + "_ND")
				log("Delete Feature: " + fc)
				arcpy.Delete_management(BASE + "/" + fccam)

			#Si es de Seguridad
			if GROUP.find('Seguridad') > -1:
				arcpy.Select_analysis(in_features=SOURCE + owner + fccam, out_feature_class=BASE + "/" + fccam, where_clause="")
				log("Create Feature: " + fc)
			#Si es de Yacimiento
			else:
				arcpy.Select_analysis(in_features=SOURCE + owner + fccam, out_feature_class=BASE + "/" + fccam, where_clause="SEGURIDAD = 'NO' OR SEGURIDAD = 'No' OR SEGURIDAD = 'no' OR SEGURIDAD = 'nO'")
				log("Create Feature: " + fc)

			log("Count: " + str(int(arcpy.GetCount_management(BASE + "/" + fccam).getOutput(0))))

		else:
			log("Feature Class not exists: " + fc)
	except Exception as e:
	    log("Create Feature: " + fc + ": " + str(e))
	
	log('-' * 40)
	log(" [CREATE NETWORK] ")
	log('-' * 40)
	
	try:
		if os.path.exists(SALIDA + "/Plantilla_Red_" + UG + ".xml"):
			log("Create Network Dataset From Template")
			log('-' * 40)
			arcpy.CreateNetworkDatasetFromTemplate_na(network_dataset_template= SALIDA + "/Plantilla_Red_" + UG + ".xml", output_feature_dataset=BASE + "/" + FD_Red_Caminos)

			log("Build Network")
			log('-' * 40)
			arcpy.BuildNetwork_na(in_network_dataset=BASE + "/" + FD_Red_Caminos + "/" + FD_Red_Caminos + "_ND")

			log("CheckIn Extension: Network Analyst")
			arcpy.CheckInExtension("Network")
		else:
			log("Not Exist XML: " + "/Plantilla_Red_" + UG + ".xml")
	except Exception as e:
	    log("Error in Create Network: " + str(e))

	#aprx = arcpy.mp.ArcGISProject(SALIDA + "\\Navigator_GSJ.aprx")
	#for m in aprx.listMaps():
	#	print("Map: " + m.name)
	#	for lyr in m.listLayers():
	#		print("  " + lyr.name)
	
	log('-' * 40)
	log(" [CREATE MOBILE MAP PACKAGE] ")
	log('-' * 40)

	if os.path.exists(SALIDA + "\\" + MMPK + ".mmpk"):
		log(" [Delete MMPK] ")
		os.remove(SALIDA + "\\" + MMPK + ".mmpk")

	# Process: Create Mobile Map Package
	log(" [Create MMPK] ")
	arcpy.management.CreateMobileMapPackage(in_map=SALIDA + "\\" + MAPA + ".mapx", output_file=SALIDA + "\\" + MMPK + ".mmpk")
	
	log('-' * 40)
	log(" [SING IN TO PORTAL] ")
	log('-' * 40)
	gis = GIS(URL, USR, PSS, verify_cert=False)
	
	log(" [Search Package] ")
	search_result = gis.content.search('title:' + MMPK, item_type='Mobile Map Package')

	if len(search_result) > 0:
		item = gis.content.get(search_result[0].itemid)
		item.delete()
		log(" [Delete Package] ")

	log(" [Add Package] ")
	tpk_item = gis.content.add({}, data=SALIDA + "\\" + MMPK + ".mmpk", folder=FOLDER)
	log(" [Move Package] ")
	tpk_item.move(FOLDER)

	log(" [SHARE Package] ")
	log(" [Get Groups] ")
	search_group = gis.groups.search('title:' + GROUP)
	if len(search_group) > 0:
		log(" [Share to group] ")
		tpk_item.share(groups=search_group[0].id)
	
	log('-' * 40)
	log(" [END] - OK")
	log('-' * 40)
except Exception as e:
	log("|Error!!\n   " + str(e) + ']')

	raise