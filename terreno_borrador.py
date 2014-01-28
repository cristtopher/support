#!/usr/bin/python
# -*- coding: UTF-8 -*-


# DescripciC3n: Script python de instalaciC3n y configuraciC3n enviroview
# Fecha: 7/12/2012
# Autor: Cristtopher Quintana T.
# INNOVEX
# Production: Off

import os    
import sys   
import urllib
import shutil
from array import *
from innovex.configuration import Configuration

  # Path donde se alojan los archivos.

#url = "http://download.innovex.cl/debian/"
url = "192.168.1.119/public/files/support/"


def download_status(bloque, tamano_bloque, tamano_total):
    cant_descargada = bloque * tamano_bloque
    print "Cantidad descargada: %s Bytes de %s Bytes totales" \
    % (cant_descargada, tamano_total)


def download(name):
        urllib.urlretrieve(url + name, name, reporthook=download_status)


def write(url, type_, text):
            file_ = open(url, type_, text)
            file_.write(text)
            file_.close()


  # Se solicitan datos para modificar el archivo innovex.cfg
def conf_file(cfg):

    while True:
        empresa = raw_input("Ingrese nombre de la empresa : ")
        if empresa is not "":
            break

            while True:  
                localidad = raw_input("Ingrese localidad del centro : ")
                if localidad is not "":
                    break

                    while True:  
                        key = raw_input("Ingrese llave para la sincronizacion con OxiWeb: ")
                        if key is not "":
                            break

                            while True:
                                beatru = int(raw_input('Ingrese beatru (2500 por defecto) : '))
                                break
                            except ValueError:
                                print "Favor de ingresar un numero"

                                while True:
                                    level = float(raw_input('Ingrese nivel (4.5 por defecto) : '))
                                    break
                                except ValueError:
                                    print "Favor de ingresar un numero"

                                    while True:
                                        salinity = float(raw_input("Ingrese salinidad (32.0 por defecto): "))
                                        break
                                    except ValueError:
                                        print "Favor de ingresar un numero"

  # Se cambia el nombre de host a key

   hostname = open("/etc/hostname", "w")
   hostname.write(key.lower(key))   
   hostname.close()
    
  # Aplicamos los cambios en el archivo de configuraciC3n.

    cfg.key = key.lower(key)

    # os.system("sed -i 's/localidad=/'localidad=" + localidad + "'/g' " + cfg)
    # os.system("sed -i 's/empresa=/'empresa=" + empresa + "'/g' " + cfg)

    # Verficamos si variables estan por defecto.
    if level is not "":             # Si no ingresa algo queda porfecto en 4.5.
        # os.system("sed -i 's/low_level=5.0/'low_level=" +
        #  level + "'/g' " + cfg)
    if salinity is not "":      # Si no ingresa algo queda por defecto en 32.0.
        # os.system("sed -i 's/salinity=32.0/'salinity=" +
        #  salinity + "'/g' " + cfg)

  # Agregamos sensores al archivo de configuracion.
    while 1:
        sensores = raw_input("Ingrese numero de sensores: ")
        if sensores.isdigit():
            sensores = int(sensores)
            break
        count = 1       # Contador de sensores.
        count_display = 1          # Contador de displays.
        for numero in range(0, sensores):
            salir = 's'
            archivo = open(cfg, "a")
            archivo.write("\n[Oxygen " + str(count) + "]\n")
            while salir is 's' or salir is 'S':
                # Si no ingresa un valor de profundidad correcto no sale del while.
                depth = 0
                while depth is not 3 and depth is not 5 and depth is not 8 and \
                depth is not 10 and depth is not 15 and depth is not 20 and \  
                depth is not 30:
                depth = input("Ingrese profundidad para el display" + \
                   str(count_display) + " del Oxygen " + str(count) + \  
                   " en metros [3,5,8,10,15]: ")
                archivo.write("display" + str(count_display) + "=Jaula A " +
                   str(depth) + "m\n")
                count_display += 1  
                salir = raw_input("Desea agregar otra profundidad? [s/n]: ")
                archivo.close()
                count += 1
                count_display = 1

  # installer()
    # remover()  
    # inicio()   
    # intentos = 0
    # while intentos <= 10:
    #     if os.path.isfile(os.path.expanduser('~') +
    #      "/Escritorio/calibracion.pdf") and\
    #      os.path.isfile(os.path.expanduser('~') +
    #      "/Escritorio/minititlt.pdf") and\
    #      os.path.isfile(os.path.expanduser('~') +
    #      "/Escritorio/oxiwise.pdf"):
    #         print "Manuales descargados correctamente"
    #     else:
    #         man()
    #         intentos += 1
    # if intentos is 10:   
    #     print "Error al intentar descargar manuales, favor de intentar nuevamente (verifique conecciC3n)"


def config():
    # Comprobar si ya existe repositorio en sources.list.
    if buscar("Innovex", "/etc/apt/sources.list") > 0:   
        print "Repositorio ya existe"
    else:
        # Agregamos repositorio.
        write("/etc/apt/sources.list", "a", "\n# Innovex repository\ndeb " +
           url + " stable main")
    # Agregamos llave de APT. 
    os.system("wget -q " + url + "innovex_key.asc -O- | sudo apt-key add -")
    # Para ambos casos actualizamos repositorios.
    os.system("sudo apt-get update")
    # Validamos si ya existe el archivo de configuraciC3n.
    if os.path.isfile("/etc/innovex.cfg"):
        answ = raw_input("Archivo de configuraciC3n ya existe, desea sobreescribir [s/n]: ")
        if answ is 's' or answ is 'S':
            download("innovex.cfg")   
            if os.path.isfile("innovex.cfg"):
                # Movemos el archivo descargado a /etc/.
                shutil.copy("innovex.cfg", "/etc/")
                conf_file()
            else:
                print "No se ha descargado EnviroView, vuelva a intentar nuevamente (compruebe conecciC3n)"
                sys.exit(0)
            else:
                config()
    # Configuracion usb
    # if os.path.isfile("/etc/udev/rules.d/z99_innovex.rules"):
    #     resp = raw_input("Regla usb ya existe, desea sobreescribir [s/n]: ")
    #     # Si desea sobreescribir.
    #     if resp is 's' or resp is 'S':
    #         # print os.system("lsusb")
    #         for i in range(1, 9):
    #             print os.system("cat /sys/bus/usb/devices/" + i + "-" +
    #             i + "/serial")
    #         oxigeno = raw_input("Ingrese el bus del oxigeno: ")
    #         corriente = raw_input("Ingrese el bus de corriente: ")
    #         write("/etc/udev/rules.d/z99_innovex.rules", "w",
    #          "SUBSYSTEMS==\"usb\", KERNEL==\"ttyUSB*\", ATTRS{busnum}==\"" +
    #          oxigeno + "\", SYMLINK+=\"oxigeno\"\nSUBSYSTEMS==\"usb\", KERNEL==\"ttyUSB*\", ATTRS{busnum}==\"" +
    #          corriente + "\", SYMLINK+=\"corriente\"")
 # Creamos script.
 if os.path.isfile("/home/innovex/oxigenometro"):
    print "oxigenometro ya existe!"
else:
    write("/home/innovex/oxigenometro", "wget",
       "#!/bin/sh\nsleep 20\nmultireceiver -a &\noxiview &\nstreamview &")
    # Creamos tunel security shell si es que no existe.
    if os.path.isfile("/bin/tunel"):
        print "tunel ya existe"
    else:
        write("/bin/tunel", "w",
           "gnome-terminal -e 'ssh -R 8888:localhost:22 tunel@tunel.innovex.cl")
    # Agregamos enlace simbolico al escritorio.
    os.system("ln -s /bin/tunel " + os.path.expanduser('~') +
       "/Escritorio/Tunel")
    # Damos permiso de ejecucion.
    os.system("sudo chmod +x " + os.path.expanduser('~') + "/Escritorio/Tunel")
    # Personalizamos icono del enlace con imagen de tunel.

    # Cambiamos fondo escritorio.
    download("oxiwise-7.jpg")
    shutil.copy("oxiwise-7.jpg", os.path.expanduser('~') +
       "/ImC!genes/oxiwise-7.jpg")
    os.system("sudo gsettings set org.gnome.desktop.background picture-uri file://" +
       os.path.expanduser('~') + "/ImC!genes/oxiwise-7.jpg")
    # Descargamos y agregamos permisos para tunel security shell.
    download("ssh-info.tar.gz")
    shutil.copy("ssh-info.tar.gz", os.path.expanduser('~') +
       "/ssh-info.tar.gz")
    os.chdir("/home/innovex")
    os.system("tar xvf ssh-info.tar.gz")
    s.chdir(os.path.expanduser('~') + "/Escritorio")
    # Dando permiso de dialout a usuario innovex.
    os.system("sudo adduser innovex dialout")

    # Creamos tablas.
    # eliminar /var/lib/enviroview/measurements.db
    os.system("create_tables") # Susituir este bash por python, llamar a la funcion de oxiview

    # Creamos el usuario.
    os.system("sudo passwd root")

# Se crea una lista de los programas a instalar.
def installer():

   """ Por cada programa en la lista, se ejecuta apt-get install 
   (-y sin confirmacion; -s simulacion (sacar -s en produccion)) """

  programs = ['enviroview', 'gnome-panel', 'non-free-codecs',
   'w32codecs', 'rar', 'unrar', 'seyon', 'libxss1', 'x11vnc', 'openvpn',
   'openssh-server', 'joe', 'gstreamer0.10-ffmpeg',
   'gstreamer0.10-plugins-bad', 'gstreamer0.10-plugins-good',
   'gstreamer0.10-plugins-ugly', 'gstreamer0.10-tools', 'mencoder', 'python-gst0.10']

   
   """ programas[programa] ?"""

    for program in programs:
    os.system("sudo apt-get install " + programs[program] + " -y")

  # Se comprueba la existencia de enviroview, si no existiese, se instala
    path="/usr/share/apps/enviroview/"
    if os.path.isdir(path):
      print "EnviroView instalado correctamente en "+path
    else:
      print "EnviroView no ha sido instalado correctamente"
        raw_input("Presione la tecla enter para comenzar la instalacion")
        os.system("sudo apt-get install enviroview -y")  
    if os.path.isdir(path):
      print "EnviroView fue instalado correctamente"
    elif:
            os.system("sudo apt-get -f install enviroview")
    else:
      print "EnviroView no puede ser instalado en este momento, vuelva a intentar nuevamente. (compruebe conecciC3n)"
            sys.exit(0)

    # Instalar PREY
    urllib.urlretrieve("https://preyproject.com/releases/0.5.9/prey_0.5.9-ubuntu2_all.deb", "prey.deb", reporthook = download_status)
    if os.path.isfile("prey.deb"):
        os.system("sudo dpkg -i prey.deb")
    # Instalar Skype
    urllib.urlretrieve("http://download.skype.com/linux/skype-ubuntu-precise_4.1.0.20-1_i386.deb", "skype.deb", reporthook = download_status)
    if os.path.isfile("skype.deb"):
        os.system("sudo apt-get update")
        os.system("sudo dpkg -i skype.deb")


def remover():
    # Creamos arreglo de los programas a remover y purgar.
    programas = ['unity-2d']             # Comprobar aplicaciones a desintalar.
    """ Recorremos la tabla y ejecutamos apt-get remove --purge

    (-y sin confirmaciC3n; -s simulaciC3n (sacar en producciC3n)).

    """
    for programa in programas:
        os.system("sudo apt-get remove --purge " + programas[programa] + " -y -s")


def inicio():
    # Agregar apps al inicio de ubuntu.
    os.system("cd /etc/xdg/autostart/")
    os.system("sudo sed --in-place 's/NoDisplay=true/NoDisplay=false/g' *.desktop")
    # Agregar correntometro a inicio
    os.system("chkconfig vsftpd on")
    print "no encuentro soluciC3n!" 

def buscar(texto, archivo):
        file_ = open(archivo, 'r')
        coincidencias = 0
        for texto in file_.readlines():
            if i.find(texto) >= 0: 
                coincidencias += 1 
                file_.close()
                return coincidencias

def man():
  manuals = ['calibracion.pdf', 'minititlt.pdf', 'oxiwise.pdf']
        for manual in manuals:
              download(manuales[manual])

            if __name__ == '__main__':
                try:
                  fp = open('/etc/innovex.cfg')
                  cfg = Configuration(fp)
                  conf_file(cfg)

    # config(cfg)
    # installer()
    # remover()  
    # inicio()   
    # intentos = 0
    # while intentos <= 10:
    #     if os.path.isfile(os.path.expanduser('~') +
    #      "/Escritorio/calibracion.pdf") and\
    #      os.path.isfile(os.path.expanduser('~') +
    #      "/Escritorio/minititlt.pdf") and\
    #      os.path.isfile(os.path.expanduser('~') +
    #      "/Escritorio/oxiwise.pdf"):
    #         print "Manuales descargados correctamente"
    #     else:
    #         man()
    #         intentos += 1
    # if intentos is 10:   
    #     print "Error al intentar descargar manuales, favor de intentar nuevamente (verifique conecciC3n)"




