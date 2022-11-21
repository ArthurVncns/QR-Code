import PIL as pil
from PIL import Image
from PIL import ImageTk 

def nbrCol(mat): #renvoie le nombre de colonne d'une matrice
    return len(mat[0])

def nbrLig(mat): #renvoie le nombre de ligne d'une matrice
    return len(mat)

def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat

def creer_symbole(): #Fonction qui crée une matrice avec le symbole du coin d'un QR code en bas a droite
    mat = []
    for i in range(0,25):
        l=[]
        for j in range(0,25):
            l.append(1)
        mat.append(l)
    for i in range(18,25):
        for j in range(18,25):
            mat[i][j] = 0
    for i in range(19,24):
        for j in range(19,24):
            mat[i][j] = 1
    for i in range(20,23):
        for j in range(20,23):
            mat[i][j] = 0
    return mat

def rotate(mat): #Fonction qui tourne la matrice de 90°
    mat_rotate = []
    for i in range(nbrLig(mat)):
        l=[]
        for j in range(nbrCol(mat)):
            l.append(mat[j][i])
        l.reverse()
        mat_rotate.append(l)
    return mat_rotate

def coins(mat): #Fonction qui renvoie les coins de la matrice creer_symbole() et celle du QR code que l'on veut decoder
    mat1 = creer_symbole()
    mat2 = []
    for i in range(18,25):
        l=[]
        for j in range(18,25):
            l.append(mat1[i][j])
        mat2.append(l)
    mat3=[]
    for i in range(18,25):
        l=[]
        for j in range(18,25):
            l.append(mat[i][j])
        mat3.append(l)
    return mat2, mat3

def sens_QRcode(mat): #Fonction qui compare les deux coins et tourne la matrice si les coins sont les memes
    tourner = True
    while tourner:
        mat = rotate(mat)
        mat2, mat3 = coins(mat)
        for i in range(0,len(mat2)):
            for j in range(0,len(mat2[i])):
                if mat2[i][j] != mat3[i][j]:
                    tourner = False
    return mat


def read_bitQRcode(bits): #Fonction qui renvoie la liste des 4 bits d'informations a partir des 7 bits
    p1 = bits[0] ^ bits[1] ^ bits[3]
    p2 = bits[0] ^ bits[2] ^ bits[3]
    p3 = bits[1] ^ bits[2] ^ bits[3]
    if p1!=bits[4] and p2!=bits[5] and p3!=bits[6]:
        if bits[3]==0:
            bits[3]=1
        else:
            bits[3]=0
    if p1!=bits[4] and p2!=bits[5]:
        if bits[0]==0:
            bits[0]=1
        else:
            bits[0]=0
    if p1!=bits[4] and p3!=bits[6]:
        if bits[1]==0:
            bits[1]=1
        else:
            bits[1]=0
    if p2!=bits[5] and p3!=bits[6]:
        if bits[2]==0:
            bits[2]=1
        else:
            bits[2]=0
    return bits[:4]

def read_info2(mat): #Fonction qui lit les blocs du QR code et renvoie une liste de listes de 14 bits
    info = []
    bloc = []
    floor = nbrCol(mat) - 3
    print(nb_blocs(mat)) #Affiche le nombre de blocs a decoder dans le terminal
    while len(info) < nb_blocs(mat):
        for j in range(24,17,-1): #On lit le 1er bloc de la droite vers la gauche
            for i in range(floor+2,floor,-1):
                bloc.append(mat[i][j])
        info.append(bloc)
        bloc = []
        if len(info) >= nb_blocs(mat):
            break
        for j in range(17,10,-1): #On lit le 2eme bloc de la droite vers la gauche
            for i in range(floor+2,floor,-1):
                bloc.append(mat[i][j])
        info.append(bloc)
        floor -= 2  #On augmente d'etage pour lire les blocs suivants qui sont au dessus
        bloc = []
        if len(info) >= nb_blocs(mat):
            break
        for j in range(11,18): #On lit le 3eme bloc de la gauche vers la droite
            for i in range(floor+2,floor,-1):
                bloc.append(mat[i][j])
        info.append(bloc)
        bloc = []
        if len(info) >= nb_blocs(mat):
            break
        for j in range(18,25): #On lit le 4eme bloc de la gauche vers la droite
            for i in range(floor+2,floor,-1):
                bloc.append(mat[i][j])
        info.append(bloc)
        floor -= 2
        bloc = []
    return info

def to_ascii(bits): #Fonction qui convertit les bits en ascii
    ascii = ""
    message = ""
    for i in range(0, len(bits)):
        ascii += str(bits[i])
        if len(ascii) == 8:
            message += chr(int(ascii, 2))
            ascii = ""
    return message

def bin_to_dec(bits): #Fonction qui convertit les bits en decimale
    j, decimal, a = 0, 0, len(bits)-1
    for i in range(0,len(bits)):
        decimal += bits[i+a] * (2**j)
        j += 1
        a -= 2
    return decimal

def dec_to_hexa(dec): #Fonction qui convertit le decimale en hexadecimale
    if dec >= 10:
        if dec == 10:
            return "A"
        elif dec == 11:
            return "B"
        elif dec == 12:
            return "C"
        elif dec == 13:
            return "D"
        elif dec == 14:
            return "E"
        elif dec == 15:
            return "F"
    else:
        return str(dec)

def to_hexa(bits): #Fonction qui convertit les bits en hexadecimale en utilisant les deux fonctions precedentes
    decimal = bin_to_dec(bits)
    hexa = dec_to_hexa(decimal)
    return hexa

def filtre(mat): #Fonction qui applique un filtre si besoin au QR code
    matFiltre = []
    for i in range(0,25):
        l=[]
        for j in range(0,25):
            l.append(1)
        matFiltre.append(l)
    if mat[22][8] == 0 and mat[23][8] ==0:
        mat = mat
    else:
        if mat[22][8]==0 and mat[23][8]==1: #Damier --> Le bloc en haut a gauche est noir
            for i in range(9,25):
                for j in range(11,25):
                    if (i+j)%2==1:
                        matFiltre[i][j]=1
                    else:
                        matFiltre[i][j]=0
        elif mat[22][8]==1 and mat[23][8]==0: #Lignes horizontales qui alternent noire/blanche --> La ligne tout en haut est noire
            for i in range(9,25):
                for j in range(11,25):
                    if i%2==1:
                        matFiltre[i][j]=0
                    else:
                        matFiltre[i][j]=1
        elif mat[22][8]==1 and mat[23][8]==1: #Lignes verticales qui alternent noire/blance --> La colonne tout a gauche est noire
            for i in range(9,25):
                for j in range(11,25):
                    if j%2==1:
                        matFiltre[i][j]=0
                    else:
                        matFiltre[i][j]=1
        for i in range(9,25): #On applique le filtre sur le QR code
            for j in range(11,25):
                mat[i][j] = mat[i][j] ^ matFiltre[i][j]
    return mat

def nb_blocs(mat): #Fonction qui renvoie le nombre de blocs necessaires pour lire le QR code
    l = []
    for i in range(13,18):
        l.append(mat[i][0])
    nb = bin_to_dec(l)
    return nb
    
def decodageQRcode(mat): #Fonction qui decode le QR code
    mat = sens_QRcode(mat) #On met le QR code dans le bon sens
    mat = filtre(mat) #On applique le filtre si necessaire
    bits = read_info2(mat) #On lit les blocs du QR code
    l = []
    b = []
    decodage = ""
    for i in range(0, len(bits)):
        l.append(read_bitQRcode(bits[i][:7]))
        l.append(read_bitQRcode(bits[i][7:]))
    if mat[24][8] == 1:
        for i in range(0, len(l), 2):
            b.append(l[i]+l[i+1])
        for i in range(0, len(b)):
            decodage += to_ascii(b[i])
    else :
        for i in range(0, len(l)):
            decodage += to_hexa(l[i])
    return decodage

matrice = loading("qr_code_ssfiltre_ascii.png")
print(decodageQRcode(matrice))                       #Pour tester le decodage du QR code
# CELA DONNE "j'aime les qr" ou "vive les damiers" EN FONCTION DU QR CODE