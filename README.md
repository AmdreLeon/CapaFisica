# Proyecto de Redes:
El objetivo central del proyecto no es más que la de realizar una simulación de una red de computadoras interconectadas. 
## Capa física
***
Para esta parte de la simulación nos enfocamos en crear un grafo llamado network que contiene subgrafos, llamados subnetworks, que representan sus componentes conexas con el principal objetivo que en cada una de estas subnetworks se esté trasmitiendo un solo bit evitando así las colisiones. Para la simulación usamos una gran clase denominada system que es la encargada de controlar el correcto desempeño de la simulación, así como otras clases como computer y hub de cumplen la función de representar a las computadoras y hubs.
## Capa de enlace
***
En la simulación de esta capa tuvimos que realizar un cambio de paradigma. En primer lugar prescindimos de la clase subnetwork, la cual nos había servido en la capa anterior para indicar el valor que estaba sindo enviado en cada componente conexa del grafo que representaba la red. Al en esta capa existir los cables duplex y los switch, pues esta idea ya no nos era factible, por lo cual ahora cada host o switch a la hora de enviar sus datos lo realizará haciendo un recorrido DFS a través de los dispositvos conectados a él (esta idea se asemeja más a la realidad si pensamos en el recorrido que hace la electricidad por cada cable o dispositivo). Se crearon dos nuevas clases Switch y SwitchPort para representar a los switch y sus puertos.
## Cómo ejecutar el proyecto?
***
Para que el proyecto funcione correctamente se necesitará que en la carpeta raíz del mismo exista un archivo config.txt con el formato descrito en la orientación y al menos un archivo de cualquier nombre, preferiblemente "script", con el formato descrito en la orientación de tipo txt y bastará con correr la línea:
```bash
python3 system.py myScript.txt
```
Vale destacar que si no se agrega un nombre para el script el programa tomará el nombre "script.txt" por defecto.
## Instalación
***
Para su uso sólo es necesario tener el lenguaje de programación [Python](https://www.python.org/downloads) en su versión 3.9.1 o superior, que fue la usada por nosotros.
El repositorio de GitHub es este [CapaFisica](https://github.com/Andrelenin42/CapaFisica).

## Desarrollado con
***
* [VSCode](https://code.visualstudio.com)
* [GitHub](https://github.com)
* Muchas pero que muchas ganas
## Autores
***
Equipo de desarrollo:
* Manuel Antonio Vilas Valiente C-311
* Andrés Alejandro León Almaguer C-312

Equipo de apoyo:
* Rachel Lambert Correoso (Psicóloga)
* Y a todos aquellos que de alguna u otra forma brindaron su ayuda para que esto fuese posible

## A los profesores 
***
Esperamos que el proyecto sea de su agrado y sean generosos con la nota ;)\
Gracias.