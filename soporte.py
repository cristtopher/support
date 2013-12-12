#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
import os.path
import shutil
import serial
import glob
import smtplib
import base64
from datetime import date
sys.path.append('/usr/bin/fixtunnel')
from innovex.configuration import Configuration


def synchronize(cfg):
    os.system('synchronize_db_http')
    connection = ProxyConnection(cfg.key, cfg.server, cfg.proxy)
    synchronize_oxygen(cfg.database, connection)
    synchronize_currents(cfg.database, connection)
    synchronize_weather(cfg.database, connection)
    synchronize_salinity(cfg.database, connection)
    connection.close()


def scan():
    return glob.glob('/dev/serial/by-id/*')


def check_serial_port(cfg):
    if scan() != []:
        for name in scan():
            if name.startswith('/dev/serial/by-id/usb-FTDI'):
                port = name
        if not cfg.serialport is port:
            print "Puerto cfg ---------------------> Correcto."
            os.system('sudo chmod 777 ' + port)
            print "Privilegios Puerto serial ------> Realizado."
        else:
            print "Puerto cfg ---------------------> Incorrecto."
            cfg.serialport = port
            print "Puerto cfg ---------------------> Correcto."
    else:
        print 'Antena Receptora ---------------> Desconectada o Muerta.'


def check_conectivity(host):
    if os.system("ping -c 1 %s" % host) == 0:
        return True
    else:
        return False


def check_comunication(cfg):
    serial_port = serial.Serial(cfg.serialport,
    baudrate=cfg.baudrate, timeout=0.3)
    while 1:
        try:
            l = serial_port.read(2)
            if not l:
                continue
            print l
        except(IOError):
            print "Error"
    serial_port.close()


def check_vpn():
    # server
    pass


def initilize_openvpn():
    os.system("sudo /etc/init.d/openvpn start")
    if check_conectivity('10.8.0.1'):
        return True
    elif check_conectivity('10.9.0.1'):
        return True
    else:
        return False


def config_vpn(cfg):
    key = "%s/%s.key" % (os.getenv("HOME"), cfg.key)
    crt = "%s/%s.crt" % (os.getenv("HOME"), cfg.key)
    conf = "%s/%s.conf" % (os.getenv("HOME"), cfg.key)
    ca = "%s/ca.crt" % os.getenv("HOME")
    if os.path.isdir('/etc/openvpn/'):
        print "OpenVPN -----------------------------> Ya Instalado."
    else:
        os.system('sudo apt-get install openvpn x11vnc -y')
    if os.path.isfile(key) or os.path.isfile(key) or \
    os.path.isfile(key) or os.path.isfile(key):
        shutil.move(key, 'etc/openvpn/')
        shutil.move(crt, 'etc/openvpn/')
        shutil.move(conf, 'etc/openvpn/')
        shutil.move(ca, 'etc/openvpn/')
        if initilize_openvpn():
            print "Vpn ------------------------> Configurado."
        else:
            print "VPN ------------------------> Error."
    else:
        print "Archivos de configuración -----------> No encontrados en HOME."


def db_backup(cfg):
    db = cfg.get('Database', 'dbname')
    d = date.today()
    if os.path.isfile(db):
        shutil.move(db, db + '.%s%s%s' % (d.day, d.month, d.year))
    if os.path.isfile(db + '.%s%s%s' % (d.day, d.month, d.year)):
        os.system('synchronize_db_http')
        print "Base de datos ------------------------> Respaldada"


def reset_wise(cfg):
    # Kill multireceiver
    os.system("pkill multireceiver")
    try:
        serial_port = serial.Serial(config.serialport,
        baudrate = config.baudrate, timeout = 0.3)
        while 1:
            try:
                l = serial_port.read(2)
                if(not l):
                    continue
                print l
                if(l.startswith('#>')):
                    serial_port.write('RST')
                    serial_port.flush()
                    os.system('minicom -b %s -D %s' % (config.baudrate,
                    config.serialport))
                    break
            except(IOError):
                print "Error, no se puede leer"
        serial_port.close()
    except:
        print 'Unable to open serial port.'
        sys.exit()

if __name__ == '__main__':
    print '\033[93m'  # Change font color
    sys.stderr.write("\x1b[2J\x1b[H")  # Clear
    if not os.geteuid() is 0:
        print 'Ejecutar con sudo!'
        sys.exit(1)
    else:
        try:
            fp = open('/etc/innovex.cfg')
            cfg = Configuration(fp)
            option = None
            while option < 1 or option > 4:
                print '1) Verificar conectividad *Wise.'
                print '2) Verificar conectividad internet.'
                print '3) Verificar conectividad VPN'
                print '4) Abrir Túnel.'
                print '5) Configurar VPN.'
                print '6) Reparar Base de Datos.'
                print '7) Sincronizar Base de datos.'
                print '8) Resetear *Wise'
                #print '8) Crear Tabla.'
                #print '9) Solicitar Soporte.'
                print '10) Chequeo Completo.'
                print '11) Salir. '
                option = input('\nSelecciona una opción: ')
                print "\n"
                if option == 1:
                    check_serial_port(cfg)
                    check_comunication(cfg)
                elif option == 2:
                    if check_conectivity('www.innovex.cl'):
                        print '\nConectividad internet ----------> Correcta.'
                    else:
                        print '\nConectividad internet ----------> Nula.'
                elif option == 3:
                    if initilize_openvpn():
                        print 'VPN ------------------> OK'
                    else:
                        print 'VPN ------------------> Sin respuesta.'
                        config_vpn(cfg)
                elif option == 4:
                    import fixtunnel
                elif option == 5:
                    config_vpn(cfg)
                elif option == 6:
                    db_backup(cfg)
                elif option == 7:
                    synchronize(cfg)
                elif option == 8:
                    reset_wise(cfg)
                elif option == 9:
                    help_me(cfg)
                elif option == 10:
                    if check_conectivity('www.innovex.cl'):
                        print '\nConectividad internet ----------> Correcta.'
                        if initilize_openvpn():
                            print 'VPN ------------------> OK'
                        else:
                            print 'VPN ------------------> Sin respuesta.'
                            config_vpn(cfg)
                    else:
                        print '\nConectividad internet ----------> Nula.'
                    check_serial_port(cfg)
                    check_comunication(cfg)
                elif option == 11:
                    sys.exit(1)
                print "\n"
        except(IOError):
            print 'El archivo /etc/innovex.cfg no existe.'
