from mmap import PAGESIZE
import os
import glob
import json
import ntpath
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from datetime import datetime
import datetime
from reportlab.lib.styles import ParagraphStyle as PS


# Définis la couleur de chaque ligne du tableau
def set_couleur_ligne_tableau(tableau_data, liste_data):
    nb_row = len(liste_data)
    # Changement de la couleurs une ligne sur deux
    for i in range(1, nb_row):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
        
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        tableau_data.setStyle(ts)

def set_style_tableau(tableau_data, taille_texte):
    style = TableStyle([
    ('BACKGROUND', (0,0), (11,0), colors.green), # Background de la premiere ligne du tableau
    
    # Le reste du code et pour changer le style du tableau
        # ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke), # Couleur du text

        # ('ALIGN',(0,0),(-1,-1),'CENTER'), #~Alignement, centré

        # ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'), # Police du text
        ('FONTSIZE', (0,0), (-1,0), taille_texte), # taille du texte

        # ('BOTTOMPADDING', (0,0), (-1,0), 12), # Rembourrage inférieur

        # ('BACKGROUND',(0,1),(-1,-1),colors.beige), # Background beige une ligne sur deux
    ])
    tableau_data.setStyle(style)


# Fonction permettant de calculer la quatité de donnée par Mb/s avec comme paramètre la date de depart, la date d'arriver et le nombre de donnée envoyé
def calcule_mbps(data, time_start, time_end):
    time_start = str(time_start)
    time_end = str(time_end)
    time_start = time_start.replace(",", ".")
    time_end =time_end.replace(",", ".")
    
    time_start_splited = str.split(ntpath.basename(time_start), ":")
    time_end_splited =  str.split(ntpath.basename(time_end), ":")
    
    time_start_hours = int(time_start_splited[0])
    time_start_minutes = int(time_start_splited[1])
    
    time_start_second_dixiemesecond_centiemesecond = str.split(ntpath.basename(time_start_splited[2]), ".")
    time_start_second = int(time_start_second_dixiemesecond_centiemesecond[0])
    time_start_dixiemesecond_centiemesecond = int(time_start_second_dixiemesecond_centiemesecond[1]) * 10000
    
    time_end_hours = int(time_end_splited[0])
    time_end_minutes = int(time_end_splited[1])
    time_end_second_dixiemesecond_centiemesecond = str.split(ntpath.basename(time_end_splited[2]), ".")
    time_end_second = int(time_end_second_dixiemesecond_centiemesecond[0])
    time_end_dixiemesecond_centiemesecond = int(time_end_second_dixiemesecond_centiemesecond[1]) * 10000
    
    totaltime_start_second = datetime.datetime(2000,1,12,time_start_hours,time_start_minutes,time_start_second,time_start_dixiemesecond_centiemesecond)
    totaltime_end_second = datetime.datetime(2000,1,12,time_end_hours,time_end_minutes,time_end_second,time_end_dixiemesecond_centiemesecond)
    
    time_second = (totaltime_end_second - totaltime_start_second).total_seconds()
    mbps = (int(data)*8)/time_second
    
    return mbps

# Récuperer les informations du json pour chaque agences

path_data_agences = "C:\\Cofidoc\\rapport_reseau_python" # Chemin d'accès aux repertoires où ce trouve les jsons

target_pattern = path_data_agences + "\*[0-9].json" # pattern pour récupérer les json classique qui utilise speed test
target_pattern_cloud = path_data_agences + "\*Cloud.json" # pattern pour récupérer les json contenant l'informations upload/download pour le cloud

list_file_json = glob.glob(target_pattern) # liste de tous les fichiers json classique dans le repertoire
list_file_json.sort() # tri de la liste avant de les avoir dans l'ordre alphabétique
list_file_json_cloud = glob.glob(target_pattern_cloud) # Liste de tous les fichier json contenant l'informations uplaod/download pour le cloud
list_file_json_cloud.sort() # Tri de la liste contenant l'informations uplaod/download pour le cloud

name_file_json_actuelle = list_file_json[0] # récupération du premier fichier json de la liste classique
name_file_json_cloud_actuelle = list_file_json_cloud[0] # récupération du premier fichier json de la liste uplaod/download
name_file_json = str.split(ntpath.basename(name_file_json_actuelle), "_") # récupération de la ville dans le nom du fichier json
name_file_json_cloud_actuelle = str.split(ntpath.basename(name_file_json_cloud_actuelle), "_") # récupération de la ville dans le nom du fichier json contenant les informations upload/download pour le cloud
tableau_data = [["Agence", "ISP", "Q.d.http", "Q.d.ftp", "Q.u.ftp", "Q.latence", "B.d.http", "B.u.http", "B.latence", "S.d.http", "S.u.http", "S.latence"]] # Entete du tableau, liste des colonnes

# Initialisation des colonnes pour les tableaux Max/Min pour Quadria, Bouygues, SpeedTest
tableau_max_min_quadria = [[
    "Agence", 
    "Quadria.d.http Max", 
    "Quadria.d.http Min", 
    "Quadria.d.ftp Max", 
    "Quadria.d.ftp Min", 
    "Quadria.u.ftp Max", 
    "Quadria.u.ftp Min", 
    "Quadria.latence Max", 
    "Quadria.latence Min" 
    ]]
tableau_max_min_bouygues = [[
    "Agence", 
    "Bouygues d.http Max", 
    "Bouygues d.http Min", 
    "Bouygues u.http Max", 
    "Bouygues u.http Min", 
    "Bouygues latence Max",
    "Bouygues latence Min", 
    ]]

tableau_max_min_speedtest = [[
    "Agence", 
    "Speedtest d.http Max", 
    "Speedtest d.http Min", 
    "Speedtest u.http Max", 
    "Speedtest u.http Min", 
    "Speedtest latence Max", 
    "Speedtest latence Min"
    ]]

tableau_resume = [[
    "Agence", 
    "Quadria d.http", 
    "Latence Quadria", 
    "Bouygues d.http", 
    "Bouygues u.http", 
    "Latence Bouygues", 
    ]]

# Initialisation des variables qui vont contenir la latnece, l'upload, le download, les informations dans le json, le nombre de fichier pour une agence
data_json = 0
nb_file_json_agence = 1
dict_data_agence = dict()
dict_data_cloud_agence = dict()
# Parcour de tous les fichiers json

for file_json_cloud in list_file_json_cloud:
    try:
        # Ouverture et lecture du fichier en cour de traitement
        with open(file_json_cloud) as mon_fichier:
            data_json = json.load(mon_fichier) # Récupération du json dans la variable data_json
        name_file_json = str.split(ntpath.basename(file_json_cloud), "_") # Récupération du nom de la ville pour le fichier json traiter en cours
        nom_agence_encourdetraitement = name_file_json[0] # Récupération de la ville que l'on ai en train de traiter. Si la ville est différente le traitement l'est aussi
        print(nom_agence_encourdetraitement)
        if data_json == None or "error" in data_json:
            continue
        
        if (nom_agence_encourdetraitement in list(dict_data_agence.keys())) == False: # Si c'est la première agence ou une agence différente de la précédente, alors on initialise le dictionnaire avec le nom de l'agence en clès
            dict_data_agence[nom_agence_encourdetraitement] = {} # Initialisation en déclarant le dictionnaire
        if ("dataup" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est les premières données pour quadria traité pour cette agence, on initialise la clès avec un tableau
            dict_data_agence[nom_agence_encourdetraitement]["dataup"] = 0 # Initialisation 
        if ("startup" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la date de depart upload ftp quadria traité pour cette agence, on initialise la clès avec un tableau
            dict_data_agence[nom_agence_encourdetraitement]["startup"] = [] # Initialisation en déclarant la liste
        if ("stopup" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la date de depart upload ftp quadria traité pour cette agence, on initialise la clès avec un tableau  
            dict_data_agence[nom_agence_encourdetraitement]["stopup"] = [] # Initialisation en déclarant la liste
        if ("datadown" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la date de fin upload ftp quadria traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["datadown"] = [] # Initialisation en déclarant la liste
        if ("startdown" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la date de depart download ftp quadria traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["startdown"] = [] # Initialisation en initialisant la variable par la première valeur de de depart download ftp quadria de l'agence concerné 
        if ("stopdown" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la date de fin download ftp quadria traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["stopdown"] = [] # Initialisation en initialisant la variable par la première valeur de de depart download ftp quadria de l'agence concerné 
        if ("httpdownloadtemps100megaoquadria" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["httpdownloadtemps100megaoquadria"] = [] # Initialisation en initialisant la variable par la première valeur de latence de l'agence concerné 
        if ("httpdownloadtemps100megaobouygues" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["httpdownloadtemps100megaobouygues"] = [] # Initialisation en initialisant la variable par la première valeur de latence de l'agence concerné 
        if ("httpuploadtemps10megaobouygues" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["httpuploadtemps10megaobouygues"] = [] # Initialisation en initialisant la variable par la première valeur de latence de l'agence concerné 
        if ("latencequadria" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["latencequadria"] = [] # Initialisation en initialisant la variable par la première valeur de latence de l'agence concerné 
        if ("latencebouygues" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["latencebouygues"] = [] # Initialisation en initialisant la variable par la première valeur de latence de l'agence concerné 
        if ("Quadria u.ftp" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False:
            dict_data_agence[nom_agence_encourdetraitement]["Quadria u.ftp"] = []
        if ("Quadria d.ftp" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False:
            dict_data_agence[nom_agence_encourdetraitement]["Quadria d.ftp"] = []
    

        # Ci-dessous, calcul de Mbs/s en http pour Bougyes et quadria 
        http_download_mb_ar_seconde_quadria = 800 / float(data_json["httpdownloadtemps100megaoquadria"]) 
        http_download_mb_ar_seconde_bouygues = 800 / float(data_json["httpdownloadtemps100megaobouygues"])
        
        if ("httpuploadtemps10megaobouygues" in data_json) == True:
            http_upload_mb_ar_seconde_bouygues = 800 / float(data_json["httpuploadtemps10megaobouygues"]) / 10
        else:
            http_upload_mb_ar_seconde_bouygues = 800 / float(data_json["httpuploadtemps100megaobouygues"]) / 10
        
        latence_quadria = float(data_json["latencequadria"]) # récupération de la latence de l'agence avec Quadria
        latence_bouygues = float(data_json["latencebouygues"]) # récupération de la latence de l'agence avec Bougues
        
        # Ajout des latences, download, upload dans le dictionnaire contenant toutes les inforamtiosn de toutes les agences
        dict_data_agence[nom_agence_encourdetraitement]["httpdownloadtemps100megaoquadria"].append(http_download_mb_ar_seconde_quadria) 
        dict_data_agence[nom_agence_encourdetraitement]["httpdownloadtemps100megaobouygues"].append(http_download_mb_ar_seconde_bouygues)
        dict_data_agence[nom_agence_encourdetraitement]["httpuploadtemps10megaobouygues"].append(http_upload_mb_ar_seconde_bouygues)
        dict_data_agence[nom_agence_encourdetraitement]["latencequadria"].append(latence_quadria)
        dict_data_agence[nom_agence_encourdetraitement]["latencebouygues"].append(latence_quadria) 

        data_upload = data_json["dataup"]
        time_start_upload = data_json["startup"]
        time_end_upload = data_json["stopup"]
        data_download = data_json["datadown"]
        time_start_download = data_json["startdown"]
        time_end_download = data_json["stopdown"]
        
        mbps_upload = calcule_mbps(data_upload, time_start_upload, time_end_upload)
        mbps_download = calcule_mbps(data_download, time_start_download, time_end_download)

        dict_data_agence[nom_agence_encourdetraitement]["Quadria u.ftp"].append(mbps_upload)
        dict_data_agence[nom_agence_encourdetraitement]["Quadria d.ftp"].append(mbps_download)
        
        if ("Min Quadria d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria d.http"] = http_download_mb_ar_seconde_quadria # Initialisation en initialisant la variable par la première valeur d'upload de l'agence concerné 
        if ("Max Quadria d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria d.http"] = 0
        if ("Min Quadria d.ftp" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria d.ftp"] = mbps_download # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Max Quadria d.ftp" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria d.ftp"] = 0 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Min Quadria u.ftp" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria u.ftp"] = mbps_upload # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Max Quadria u.ftp" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria u.ftp"] = 0 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Min Quadria latence" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria latence"] = latence_quadria # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Max Quadria latence" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria latence"] = 0 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
            
        if ("Min Bouygues d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues d.http"] = http_download_mb_ar_seconde_bouygues # Initialisation en initialisant la variable par la première valeur d'upload de l'agence concerné 
        if ("Max Bouygues d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues d.http"] = 0
        if ("Min Bouygues u.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues u.http"] = http_upload_mb_ar_seconde_bouygues # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Max Bouygues u.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues u.http"] = 0 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Min Bouygues latence" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues latence"] = latence_bouygues # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Max Bouygues latence" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues latence"] = 0 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        
        
        # Une fois l'initialisation de toutes les clès, nous pouvons tester chaque clès afin d'insérer le Max/min de chaque data 
        if dict_data_agence[nom_agence_encourdetraitement]["Min Quadria d.http"] > http_download_mb_ar_seconde_quadria:
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria d.http"] = http_download_mb_ar_seconde_quadria
        if dict_data_agence[nom_agence_encourdetraitement]["Max Quadria d.http"] < http_download_mb_ar_seconde_quadria:
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria d.http"] = http_download_mb_ar_seconde_quadria
        if dict_data_agence[nom_agence_encourdetraitement]["Min Quadria d.ftp"] > mbps_download:
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria d.ftp"] = mbps_download
        if dict_data_agence[nom_agence_encourdetraitement]["Max Quadria d.ftp"] < mbps_download:
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria d.ftp"] = mbps_download
        if dict_data_agence[nom_agence_encourdetraitement]["Min Quadria u.ftp"] > mbps_upload:
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria u.ftp"] = mbps_upload
        if dict_data_agence[nom_agence_encourdetraitement]["Max Quadria u.ftp"] < mbps_upload:
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria u.ftp"] = mbps_upload
        if dict_data_agence[nom_agence_encourdetraitement]["Min Quadria latence"] > latence_quadria:
            dict_data_agence[nom_agence_encourdetraitement]["Min Quadria latence"] = latence_quadria
        if dict_data_agence[nom_agence_encourdetraitement]["Max Quadria latence"] < latence_quadria:
            dict_data_agence[nom_agence_encourdetraitement]["Max Quadria latence"] = latence_quadria
            
        
        if dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues d.http"] > http_download_mb_ar_seconde_bouygues:
            dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues d.http"] = http_download_mb_ar_seconde_bouygues
        if dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues d.http"] < http_download_mb_ar_seconde_bouygues:
            dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues d.http"] = http_download_mb_ar_seconde_bouygues
        if dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues u.http"] > http_upload_mb_ar_seconde_bouygues:
            dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues u.http"] = http_upload_mb_ar_seconde_bouygues
        if dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues u.http"] < http_upload_mb_ar_seconde_bouygues:
            dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues u.http"] = http_upload_mb_ar_seconde_bouygues
        if dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues latence"] > latence_bouygues:
            dict_data_agence[nom_agence_encourdetraitement]["Min Bouygues latence"] = latence_bouygues
        if dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues latence"] < latence_bouygues:
            dict_data_agence[nom_agence_encourdetraitement]["Max Bouygues latence"] = latence_bouygues
    except ValueError:
        continue
 
for file_json in list_file_json:
    # Ouverture et lecture du fichier en cour de traitement
    try:
        with open(file_json) as mon_fichier:
            data_json = json.load(mon_fichier) # Récupération du json dans la variable data_json
        name_file_json = str.split(ntpath.basename(file_json), "_") # Récupération du nom de la ville pour le fichier json traiter en cours
        nom_agence_encourdetraitement = name_file_json[0] # Récupération de la ville que l'on ai en train de traiter. Si la ville est différente le traitement l'est aussi
        
        if data_json == None or "error" in data_json:
            continue
        
        # Initialisation de chaque clès du dictionnaire si c'est la première valeur
        if (nom_agence_encourdetraitement in list(dict_data_agence.keys())) == False: # Si c'est la première agence ou une agence différente de la précédente, alors on initialise le dictionnaire avec le nom de l'agence en clès
            dict_data_agence[nom_agence_encourdetraitement] = {} # Initialisation en déclarant le dictionnaire
        if ("latencyspeedtest" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès avec un tableau
            dict_data_agence[nom_agence_encourdetraitement]["latencyspeedtest"] = [] # Initialisation en déclarant la liste
        if ("speedtest u.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès avec un tableau
            dict_data_agence[nom_agence_encourdetraitement]["speedtest u.http"] = [] # Initialisation en déclarant la liste
        if ("speedtest d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est le premier download traité pour cette agence, on initialise la clès avec un tableau  
            dict_data_agence[nom_agence_encourdetraitement]["speedtest d.http"] = [] # Initialisation en déclarant la liste
        if ("Max latencyspeedtest" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["Max latencyspeedtest"] = 0 # Initialisation en déclarant la liste
        if ("Min latencyspeedtest" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première latence traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["Min latencyspeedtest"] = data_json["ping"]["latency"] # Initialisation en initialisant la variable par la première valeur de latence de l'agence concerné 
        if ("Max speedtest u.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès
            dict_data_agence[nom_agence_encourdetraitement]["Max speedtest u.http"] = 0 # Initialisation en initialisant la variable par la première valeur d'upload de l'agence concerné 
        if ("Min speedtest u.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première upload traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min speedtest u.http"] = data_json["upload"]["bandwidth"]/data_json["upload"]["elapsed"]/10 # Initialisation en initialisant la variable par la première valeur d'upload de l'agence concerné
        if ("Max speedtest d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Max speedtest d.http"] = 0 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("Min speedtest d.http" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["Min speedtest d.http"] = data_json["download"]["bandwidth"]/data_json["download"]["elapsed"]/10 # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        if ("ISP" in list(dict_data_agence[nom_agence_encourdetraitement].keys())) == False: # Si c'est la première download traité pour cette agence, on initialise la clès 
            dict_data_agence[nom_agence_encourdetraitement]["ISP"] = data_json["isp"] # Initialisation en initialisant la variable par la première valeur download de l'agence concerné
        
        
        0 # récupération de la latence
        dict_data_agence[nom_agence_encourdetraitement]["speedtest u.http"].append(data_json["upload"]["bandwidth"]/data_json["upload"]["elapsed"]/10) # Récupération de l'upload en MBps
        dict_data_agence[nom_agence_encourdetraitement]["speedtest d.http"].append(data_json["download"]["bandwidth"]/data_json["download"]["elapsed"]/10) # Récupération du download en MBps
        
        

        # Mis à jour de chaque valeur Max/Min si celle-ci doit être remplacer
        if dict_data_agence[nom_agence_encourdetraitement]["Max latencyspeedtest"] < data_json["ping"]["latency"]:
            dict_data_agence[nom_agence_encourdetraitement]["Max latencyspeedtest"] = data_json["ping"]["latency"]
        if dict_data_agence[nom_agence_encourdetraitement]["Min latencyspeedtest"] > data_json["ping"]["latency"]:
            dict_data_agence[nom_agence_encourdetraitement]["Min latencyspeedtest"] = data_json["ping"]["latency"]
        if dict_data_agence[nom_agence_encourdetraitement]["Max speedtest u.http"] < data_json["upload"]["bandwidth"]/data_json["upload"]["elapsed"]/10:
            dict_data_agence[nom_agence_encourdetraitement]["Max speedtest u.http"] = data_json["upload"]["bandwidth"]/data_json["upload"]["elapsed"]/10
        if dict_data_agence[nom_agence_encourdetraitement]["Min speedtest u.http"] > data_json["upload"]["bandwidth"]/data_json["upload"]["elapsed"]/10:
            dict_data_agence[nom_agence_encourdetraitement]["Min speedtest u.http"] = data_json["upload"]["bandwidth"]/data_json["upload"]["elapsed"]/10
        if dict_data_agence[nom_agence_encourdetraitement]["Max speedtest d.http"] < data_json["download"]["bandwidth"]/data_json["download"]["elapsed"]/10:
            dict_data_agence[nom_agence_encourdetraitement]["Max speedtest d.http"] = data_json["download"]["bandwidth"]/data_json["download"]["elapsed"]/10
        if dict_data_agence[nom_agence_encourdetraitement]["Min speedtest d.http"] > data_json["download"]["bandwidth"]/data_json["download"]["elapsed"]/10:
            dict_data_agence[nom_agence_encourdetraitement]["Min speedtest d.http"] = data_json["download"]["bandwidth"]/data_json["download"]["elapsed"]/10
    except ValueError:
        pass
liste_nom_agence = list(dict_data_agence.keys()) # récupération de la liste des agences

# Récupérer les information de chaques agences afin de créer le tableau 
for nom_agence in liste_nom_agence:
    try:
        # Initialisation des moyenne pour la latence, l'upload, le download
        moyenne_latency_speedtest = 0 
        moyenne_upload_http_speedtest = 0
        moyenne_download_http_speedtest = 0
        
        moyenne_latency_quadria = 0
        moyenne_upload_ftp_quadria = 0
        moyenne_download_ftp_quadria = 0
        moyenne_download_http_quadria = 0
        
        moyenne_latency_bouygues = 0
        moyenne_upload_http_bouygues = 0
        moyenne_download_http_bouygues = 0
        
        # Initilisaiton du nombres de données à traité pour la latence, upload, download
        print("1111111111111111111111111111111")
        print(nom_agence)
        print("1111111111111111111111111111111")
        print("2222222222222222222222222")
        print(dict_data_agence[nom_agence])
        print("2222222222222222222222222")
        print("3333333333333333333333333333333333")
        print(dict_data_agence[nom_agence]["latencyspeedtest"])
        print("3333333333333333333333333333333333")
        nb_data_latency_speedtest = len(dict_data_agence[nom_agence]["latencyspeedtest"])
        nb_data_upload_http_speedtest = len(dict_data_agence[nom_agence]["speedtest u.http"])
        nb_data_download_http_speedtest = len(dict_data_agence[nom_agence]["speedtest d.http"])
        
        nb_data_latency_quadria = len(dict_data_agence[nom_agence]["latencequadria"])
        nb_data_upload_ftp_quadria = len(dict_data_agence[nom_agence]["Quadria u.ftp"])
        nb_data_download_ftp_quadria = len(dict_data_agence[nom_agence]["Quadria u.ftp"])
        nb_data_download_http_quadria = len(dict_data_agence[nom_agence]["httpdownloadtemps100megaoquadria"])
        
        nb_data_latency_bouygues = len(dict_data_agence[nom_agence]["latencebouygues"])
        nb_data_upload_http_bouygues = len(dict_data_agence[nom_agence]["httpuploadtemps10megaobouygues"])
        nb_data_download_http_bouygues = len(dict_data_agence[nom_agence]["httpdownloadtemps100megaobouygues"])
        
        # Ajout de toute les valeurs pour la latence, l'upload, le download afin de calculée la moyenne
        for latency in dict_data_agence[nom_agence]["latencyspeedtest"]:
            moyenne_latency_speedtest += latency
        for upload in dict_data_agence[nom_agence]["speedtest u.http"]:
            moyenne_upload_http_speedtest += upload 
        for download in dict_data_agence[nom_agence]["speedtest d.http"]:
            moyenne_download_http_speedtest += download 
            
        for latency in dict_data_agence[nom_agence]["latencequadria"]:
            moyenne_latency_quadria += latency
        for download_http in dict_data_agence[nom_agence]["httpdownloadtemps100megaoquadria"]:
            moyenne_download_http_quadria += download_http 
        for upload_ftp in dict_data_agence[nom_agence]["Quadria u.ftp"]:
            moyenne_upload_ftp_quadria += upload_ftp 
        for download_ftp in dict_data_agence[nom_agence]["Quadria d.ftp"]:
            moyenne_download_ftp_quadria += download_ftp  
            
        for latency in dict_data_agence[nom_agence]["latencebouygues"]:
            moyenne_latency_bouygues += latency
        for download_http in dict_data_agence[nom_agence]["httpdownloadtemps100megaobouygues"]:
           moyenne_download_http_bouygues += download_http 
        for upload_http in dict_data_agence[nom_agence]["httpuploadtemps10megaobouygues"]:
            moyenne_upload_http_bouygues += upload_http
        
        
        # Calcul de la moyenne pour la latence, l'upload, le download
        moyenne_latency_speedtest = moyenne_latency_speedtest/nb_data_latency_speedtest
        moyenne_upload_http_speedtest = moyenne_upload_http_speedtest/nb_data_upload_http_speedtest
        moyenne_download_http_speedtest = moyenne_download_http_speedtest/nb_data_download_http_speedtest
            
        moyenne_latency_quadria = moyenne_latency_quadria/nb_data_latency_quadria
        moyenne_upload_ftp_quadria = moyenne_upload_ftp_quadria/nb_data_upload_ftp_quadria
        moyenne_download_ftp_quadria = moyenne_download_ftp_quadria/nb_data_download_ftp_quadria
        moyenne_download_http_quadria = moyenne_download_http_quadria/nb_data_download_http_quadria
        
        moyenne_latency_bouygues = moyenne_latency_bouygues/nb_data_latency_bouygues
        moyenne_upload_http_bouygues = moyenne_upload_http_bouygues/nb_data_upload_http_bouygues
        moyenne_download_http_bouygues = moyenne_download_http_bouygues/nb_data_download_http_bouygues

        
        
        # Ajout des data pour le premier tableau
        tableau_data.append(
                [
                    nom_agence, # Ville de l'agence en cours de traitement
                    dict_data_agence[nom_agence]["ISP"],
                    round(moyenne_download_http_quadria), # Upload min
                    round(moyenne_download_ftp_quadria), # Upload max
                    round(moyenne_upload_ftp_quadria, 2), # Latence min
                    round(moyenne_latency_quadria), # Latence max
                    round(moyenne_download_http_bouygues),
                    round(moyenne_upload_http_bouygues, 2), # Download min
                    round(moyenne_latency_bouygues), # Download max
                    round(moyenne_download_http_speedtest), # upload en MBps moyen de la ville 
                    round(moyenne_upload_http_speedtest, 2), # download en MBps moyen de la ville
                    round(moyenne_latency_speedtest), # Latence moyenne de la ville
                ]
            ) 
        tableau_max_min_quadria.append(
                [
                    nom_agence, # Ville de l'agence en cours de traitement
                    round(dict_data_agence[nom_agence]["Max Quadria d.http"]),
                    round(dict_data_agence[nom_agence]["Min Quadria d.http"]),
                    round(dict_data_agence[nom_agence]["Max Quadria d.ftp"]),
                    round(dict_data_agence[nom_agence]["Min Quadria d.ftp"]),
                    round(dict_data_agence[nom_agence]["Max Quadria u.ftp"], 2),
                    round(dict_data_agence[nom_agence]["Min Quadria u.ftp"], 2),
                    round(dict_data_agence[nom_agence]["Max Quadria latence"]),
                    round(dict_data_agence[nom_agence]["Min Quadria latence"]),
                ]
                )
        tableau_max_min_bouygues.append(
                [   
                    nom_agence, # Ville de l'agence en cours de traitement
                    round(dict_data_agence[nom_agence]["Max Bouygues d.http"]),
                    round(dict_data_agence[nom_agence]["Min Bouygues d.http"]),
                    round(dict_data_agence[nom_agence]["Max Bouygues u.http"], 2),
                    round(dict_data_agence[nom_agence]["Min Bouygues u.http"], 2),
                    round(dict_data_agence[nom_agence]["Max Bouygues latence"]),
                    round(dict_data_agence[nom_agence]["Min Bouygues latence"]),
                ]
            )    
        tableau_max_min_speedtest.append(
                [   
                    nom_agence, # Ville de l'agence en cours de traitement     
                    round(dict_data_agence[nom_agence]["Max speedtest d.http"]),
                    round(dict_data_agence[nom_agence]["Min speedtest d.http"]),
                    round(dict_data_agence[nom_agence]["Max speedtest u.http"], 2),
                    round(dict_data_agence[nom_agence]["Min speedtest u.http"], 2),
                    round(dict_data_agence[nom_agence]["Max latencyspeedtest"]),
                    round(dict_data_agence[nom_agence]["Min latencyspeedtest"]),
                ]
            )
        
        tableau_resume.append(
            [
                nom_agence,
                round(moyenne_download_http_quadria),
                round(moyenne_latency_quadria),
                round(moyenne_download_http_bouygues),
                round(moyenne_upload_http_bouygues,2),
                round(moyenne_latency_bouygues)
            ]
        )
    except ValueError:
        pass  
# List of Lists

file_name_pdf = 'rapport_etat_reseau.pdf' # nom du fichier pdf

# Création du template pour créer le tableau et le pdf 
pdf = SimpleDocTemplate(
    file_name_pdf, # nom du pdf
    pagesize=letter # taille de la page
)

table = Table(tableau_data) # Création du tableau génréale
table_quadria = Table(tableau_max_min_quadria) # Création tableau Max/Min Quadria
table_bouygues = Table(tableau_max_min_bouygues) # Création tableau Max/Min Bouygues
table_speedtest = Table(tableau_max_min_speedtest) # Création tableau Max/Min SpeedTest
table_resume = Table(tableau_resume)

set_style_tableau(table, 7)
set_style_tableau(table_quadria, 6)
set_style_tableau(table_bouygues, 7)
set_style_tableau(table_speedtest, 7)
set_style_tableau(table_resume, 8)

set_couleur_ligne_tableau(table, tableau_data)
set_couleur_ligne_tableau(table_quadria, tableau_max_min_quadria)
set_couleur_ligne_tableau(table_bouygues, tableau_max_min_bouygues)
set_couleur_ligne_tableau(table_speedtest, tableau_max_min_speedtest)
set_couleur_ligne_tableau(table_resume, tableau_resume)
#Création du style h1 (titre n°1)
h1 = PS(
    name = 'Heading1',
    alignment=1,
    fontSize = 14,
    leading = 16,
    )
 
elems = [] 
#Création du paragraphe




# Ajout le tableau parmis la liste des elements du pdsf

elems.append(Paragraph("Moyenne des informations de destination pour Quadria, bouygues, speedtest", h1))
elems.append(Paragraph('<br />\n', h1))
elems.append(table)
elems.append(Paragraph("Quadria Maximum et minimum des données", h1))
elems.append(table_quadria)
elems.append(Paragraph("Bouygues Maximum et minimum des données", h1))
elems.append(Paragraph('<br />\n', h1))
elems.append(table_bouygues)
elems.append(Paragraph("Speedtest Maximum et minimum des données", h1))
elems.append(Paragraph('<br />\n', h1))
elems.append(table_speedtest)
elems.append(PageBreak())
elems.append(Paragraph("Résumé", h1))
elems.append(table_resume)
# Ajout de la lsite des elements dans le pdf


pdf.build(elems)

print("c'est finis")