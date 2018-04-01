#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

"""
# #######################################################################################
    Intervalometro para timelapses v1.0
    
    Este proyecto es una calculadora de timelapses que, en base a la duración del evento, 
    la duración deseada para el timelapse y al número de imágenes por segundo, calcula el 
    intervalo de disparo y el numero de capturas necesarias.
    
    Los parámetros requeridos se pueden introducir a desde la línea de comandos. En su 
    defecto, serán solicitados al usuario.

    En esta versión, el disparo de la imagen se realiza tal como esté configurada la
    cámara, sin tener en cuenta los parámetros. Esto puede ser peligroso porque puede 
    ocurrir, entre otras cosas,  que el tiempo de exposición sea mayor que el intervalo 
    y que, por ello, se produzca un solapamiento

    La forma de invocar el programa en esta primera versión será desde la línea de 
    comandos indicando de lo que se quiere calcular
    
    usage: intervalometro.py [-h] [-e EVENTO] [-v VIDEO] [-n FPS]
    
    optional arguments:
      -h, --help            show this help message and exit
      -e EVENTO, --evento EVENTO
                            duración estimada del evento (en minutos)
      -v VIDEO, --video VIDEO
                            duración deseada para el vídeo (en segundos)
      -n FPS, --fps FPS     número de imágenes por segundo (fps)

# #######################################################################################
"""

# =======================================================================================
# ================================       FUNCIONES       ================================
# =======================================================================================


# ---------------------------------------------------------------------------------------
#  Funcion: camaraConectada()
#  Parametros: 
#    
#  Descripcion:
#    Retorna CIERTO (1) si la cámara está conectada y FALSO (0) si no está conectada
#
#    Para ello, ejecutamos el comando de gphoto2 que detecta si hay alguna cámara
#    conectada. Si la salida del comando devuelve 2 líneas, indica que NO hay ninguna 
#    cámara conectada. Si hay más de 2 líneas, es que hay alguna cámara conectada.
#    Si la cámara está conectada, la desmontamos (de otra forma, no podremos capturar)
#    NOTA:
#    Esto solo sirve para python 2.7. En versiones posteriores se recomienda utilizar
#    llamadas a subprocess
# ---------------------------------------------------------------------------------------
def camaraConectada():
    # readlines() devuelve un array con las líneas leídas de la ejecución del comando
    numPars = os.popen("gphoto2 --auto-detect | wc -l").readlines()
    if int(numPars[0]) > 2:
        # Para poder disparar, antes debemos asegurarnos que la cámara está desmontada
        os.popen("gvfs-mount -s gphoto2 2>&1")
        return 1   # TRUE
    else:
        print('\n+-----------------------------------------------------------------------+')
        print('|     Por favor, asegúrese que la cámara está conectada y en marcha     |')
        print('+-----------------------------------------------------------------------+\n')
        return 0   # FALSE



# ---------------------------------------------------------------------------------------
#  Funcion: entrarParametro()
#  Parametros: 
#    - texto: es el texto que se mostrará cuando se solicite el parámetro
#  Descripcion:
#    Solicita un valor entero y lo devuelve. Si el valor introducido no es entero, da
#    5 intentos para introducirlo correctamente, y de no ser así, lanza una excepción
# ---------------------------------------------------------------------------------------
def entrarParametro(texto):
    i = 0
    while i < 5:
        valor = raw_input(texto)
        try:
            valor = int(valor)
            return valor
        except ValueError:
            i += 1
    raise ValueError, "Valor incorrecto ingresado en 5 intentos"



# ---------------------------------------------------------------------------------------
#  Funcion: calcularIntervalo()
#  Parametros: 
#    - tEvento: duracion estimada del evento que queremos capturar (en minutos)
#    - tVideo : duracion del timelapse resultante (en segundos)
#    - nFps   : número de imágenes por segundo que tendrá el timelapse
#  Descripcion:
#    Dados los parámetros indicados, calculamos el INTervalo de disparo entre fotos
# ---------------------------------------------------------------------------------------
def calcularIntervalo(tEvento, tVideo, nFps):

    assert tEvento >= 0
    assert tVideo >= 0
    assert nFps >=0

    # Calculamos el número de imágenes necesarias
    nImagenes = int(nFps)*int(tVideo)
    # Convertimos el tiempo del evento a segundos
    tEvento_s = int(tEvento)*60
    # Calculamos el intervalo (tiempo del evento en segundos / numero de imagenes)
    intervalo = int(tEvento_s)/int(nImagenes)

    return (intervalo,nImagenes)




# =======================================================================================
# =======================================================================================
# ===================================      MAIN       ===================================
# =======================================================================================
# =======================================================================================

# Sólo procedemos si la cámara está conectada
if camaraConectada():
    # Leemos la informacion de la linea de comandos y la procesamos convenientemente
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--evento", help="duración estimada del evento (en minutos)")
    parser.add_argument("-v", "--video", help="duración deseada para el vídeo (en segundos)")
    parser.add_argument("-n", "--fps", help="número de imágenes por segundo (fps)")
    args = parser.parse_args()
     
    # Procesamos los parámetros de la línea de comandos. 
    # Si alguno de los parámetros no llega el parámetro por la línea de comandos, lo pedimos
    if args.evento:
        tEvento = args.evento
    else:
        tEvento = input(" >>> Introduzca la duración del evento (en minutos): ")
    
    if args.video:
        tVideo = args.video
    else:
        tVideo = input(" >>> Introduzca la duración deseada para el vídeo (en segundos): ")
    
    if args.fps:
        nFps = args.fps
    else:
        nFps = input(" >>> Número de imágenes por segundo (fps): ")
    
    # Una vez tenemos los valores del timelapse, calculamos el intervalo.
    # La llamada devuelve 2 valores: el intervalo entre fotos y el número de imágenes a tomar
    intervalo,nImagenes = calcularIntervalo(tEvento, tVideo, nFps)
    
    # Mostramos un resumen con información del timelapse
    print("\n >>> Duración estimada del evento  : {} minutos".format(tEvento))
    print(" >>> Duración deseada del timelapse: {} segundos".format(tVideo))
    print(" >>> Número de imágenes por segundo: {} fps".format(nFps))
    print("\n     * Número de capturas   : {} imágenes".format(nImagenes))
    print("     * Intervalo entre fotos: {} segundos\n".format(intervalo))
    
    ok = raw_input("\nDe acuerdo con los parámetros indicados, ¿quiere iniciar el disparo del timelapse (s/N)? ")
    if ok == "S" or ok == "s":
        # ----------------------------------------------------------------------------------
        # En esta versión, no tenemos en cuenta los parámetros de disparo de la cámara
        # ---
        # Esto puede conducir a posibles incoherencias como que el tiempo de exposición sea
        # mayor que el intervalo de disparo y que, por tanto, se produzca un solapamiento
        # ----------------------------------------------------------------------------------

        # Configuramos para que se guarden las fotos en la tarjeta de la cámara        
        os.popen("gphoto2 --set-config  capturetarget=1")
        os.system("gphoto2 --capture-image -F " + str(nImagenes) + " -I " + str(intervalo))
    else:
        print "\n***** Proceso de captura de imágenes cancelado por el usuario *****\n"
    
