#! /usr/bin/python3
"""


"""
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix

VDW_RADIUS = {'H':1.20, 'C':1.7, 'N':1.55, 'O':1.52, 'CL':1.75, 'F':1.47, 'P':1.80, 
'S':1.80, 'CU':1.40, 'HE':1.40, 'LI':1.82, 'BE':1.53, 'B':1.92, 'NE':1.54, 'NA':2.27,
'MG':1.73, 'AL':1.84, 'SI':2.10, 'AR':1.88, 'K':2.75, 'CA':2.31, 'SC':2.11, 'NI':1.63,
'ZN':1.39, 'GA':1.87, 'GE':2.11, 'AS':1.85, 'SE':1.90, 'BR':1.85, 'KR':2.02, 'RB':3.03,
'SR':2.49, 'PD':1.63, 'AG':1.72, 'CD':1.58, 'IN':1.93, 'SN':2.17, 'SB':2.06, 'TE':2.06,
'I':1.98, 'XE':2.16, 'CS':3.43, 'BA':2.68, 'PT':1.75, 'AU':1.66, 'HG':1.55, 'TL':1.96, 
'PB':2.02, 'BI':2.07, 'PO':1.97, 'AT':2.02, 'RN':2.20, 'FR':3.48, 'RA':2.83, 'U':1.86}

def coord(fichier_pdb):
    """
	the function that reads the pdb file and extracts the atoms coordinates
	it returns as a result a list of lists containing the atom name and its 
	coordinates
    
	"""

    with open(fichier_pdb, "r") as f_pdb:
        coor_lst = []
        for ligne in f_pdb :
            if ligne[0:4] == "ATOM":
            
                # Création du dictionnaire vide.
                dico = {}
                
                # Extraction de l'atome
                dico["atom"] = str(ligne[76:].strip())
                
                # Extraction du nom du résidu.
                dico["residu "] = str(ligne[17:21])
                
                # Extraction du numéro du résidu.
                dico["N° resid"] = int(ligne[22:26])
                
                # Extraction de la coordonnée x.
                dico["x"] = float(ligne[30:38])
                
                # Extraction de la coordonnée y.
                
                dico["y"] = float(ligne[38:46])
                # Extraction de la coordonnée z.
                
                dico["z"] = float(ligne[46:54])
                coor_lst.append(dico)
                
        DF_coord = pd.DataFrame(coor_lst)
        
    return DF_coord
    
def spheres(n):#atom_tpl, n):
	"""
	"""
	indices = np.arange(0, n, dtype=float) + 0.5
	golden_angle = np.pi * (1 + 5**0.5)
	phi = np.arccos(1 - 2*indices/n)
	theta = golden_angle * indices
	#center = atom_tpl['coor']#atom_tpl[1][2]
	#radius = VDW_RADIUS[atom_tpl['atom']] + VDW_RADIUS['O']#VDW_RADIUS[atom_tpl[1][1]]
	points = np.zeros((n, 3))
	points[:,0] = np.cos(theta) * np.sin(phi) #radius * np.cos(theta) * np.sin(phi) + center[0]
	points[:,1] = np.sin(theta) * np.sin(phi) #radius * np.sin(theta) * np.sin(phi) + center[1]
	points[:,2] = np.cos(phi) #radius * np.cos(phi) + center[2]
	return points
    
def roll_sphere(DF_coord,n):
    sphere_pts = spheres(n)
    for row in DF_coord.iterrows():
        radius = VDW_RADIUS[row[1][0]]
        sphere_pts[:,0] = sphere_pts[:,0] * radius + row[1][3]
        sphere_pts[:,1] = sphere_pts[:,1] * radius + row[1][4]
        sphere_pts[:,2] = sphere_pts[:,2] * radius + row[1][5]
    return sphere_pts
	
def pts_dist(pt1, pt2):
	squared_dist = np.sum((pt1-pt2)**2, axis = 0)
	dist = np.sqrt(squared_dist)
	return dist
    
def atom_dist_matrix(DF_coord):
    """ Fonction, qui lit un dataframe et retourne une matrice de distance. 
    Cette fonction va calculer les distances entre chaque atome. 
    """
    mtx = pd.DataFrame(distance_matrix(DF_coord.iloc[:,3:],DF_coord.iloc[:,3:]), index=DF_coord.iloc[:,3:].index, columns=DF_coord.iloc[:,3:].index)
    return mtx
    
def mtx_sd(mtx):
    """ Fonction qui lit la demi matrice sans la diagonale et qui retourne un nouveau dataframe de distances.
    On sélécctionnera les atomes dont la distances est inférieur a 2A
    """
    
    for i in range(1,len(mtx)):
        for j in range(i+1, len(mtx)+1):
            if mtx[mtx.iloc[i,j] > 2].values : 
                mtx.drop(mtx.iloc[i,j], inplace=True)
                
    mtx = mat_sans_diag
    return mat_sans_diag      
                
        
        
        
    
    
    
    
    
    