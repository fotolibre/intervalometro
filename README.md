# Intervalometro para timelapses


La técnica de [cámara rápida](https://es.wikipedia.org/wiki/C%C3%A1mara_r%C3%A1pida) (en inglés time-lapse) es una técnica fotográfica muy popular usada en cinematografía y fotografía para mostrar diferentes motivos o sucesos que por lo general suceden a velocidades muy lentas e imperceptibles al ojo humano. El efecto visual que se logra en cámara rápida consiste en que todo lo que se haya capturado se mueva muy rápidamente, como puede ser el movimiento de las nubes, la apertura de una flor, una puesta de sol, etc.

Para crear un time lapse hay que capturar varias fotografías o imágenes fijas a determinados intervalos de tiempo y unirlas en postproducción asignándoles una velocidad específica. De esta forma se logra el efecto de cámara rápida.

En base a la duración del evento, la duración deseada para el timelapse y al número de imágenes por segundo, este programa calcula el intervalo de disparo y el numero de capturas necesarias.

Los parámetros requeridos se pueden introducir a desde la línea de comandos. En su defecto, serán solicitados al usuario.

```
usage: intervalometro.py [-h] [-e EVENTO] [-v VIDEO] [-n FPS]

optional arguments:
  -h, --help            show this help message and exit
  -e EVENTO, --evento EVENTO
                        duración estimada del evento (en minutos)
  -v VIDEO, --video VIDEO
                        duración deseada para el vídeo (en segundos)
  -n FPS, --fps FPS     número de imágenes por segundo (fps)
```

## Requisitos
- Python 2.7 (módulos: os, argparse)
- GPhoto2


## Ejemplo de uso

```
./intervalometro.py -e 120 -v 20 -n 24

 >>> Duración estimada del evento  : 120 minutos
 >>> Duración deseada del timelapse: 20 segundos
 >>> Número de imágenes por segundo: 24 fps

     * Número de capturas   : 480 imágenes
     * Intervalo entre fotos: 15 segundos


De acuerdo con los parámetros indicados, iniciar el disparo del timelapse (s/N)?
```