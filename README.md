# ROS-Autonomous-Vehicle
ROS-Autonomous-Vehicle: AI-powered project using ROS for image recognition, control, and line following. Explore the world of autonomous driving

REPORTE ESCRITO DEL PROYECTO DE

ROBOTICA´ INTELIGENTE

Equipo 4:

Ariadna Minerva Sol´ıs Naranjo A01639943 , Barbara Nicole Vidal Sandoval A01635233 , Luis Paulo Flores Arzate A01275194 , and

Manuel Eduardo Ochoa Obezo A00227718

Tecnol´ogico de Monterrey Campus Guadalajara

Abstract. Dentro de ´esta unidad de formaci´on se asign´o un reto en donde el objetivo principal es controlar el movimiento y traslado de un robot diferencial proporcionado por Manchester Robotics. El robot con- tiene piezas tales como una Jetson Nano y una hackerboard, en las cuales se implement´o visi´on computacional y una red neuronal en Yolov5 para la detecci´on de senales˜ de tr´ansito as´ı como un seguidor de l´ıneas. Igual- mente se le implement´o control al robot para regular la velocidad a la que se traslada. Para probar el correcto funcionamiento del robot, se re- aliz´o exitosamente un recorrido de la pista proporcionada, mientras se realizaba la detecci´on de senales˜ para modificar el comportamiento del robot acorde a ellas.

Keywords: Robot diferencial · Jetson Nano · Control · Yolov5· De- tecci´on de senales˜ · Visi´on computacional · Manchester Robotics.

1  Introducci´on

Aunque se piensa que los veh´ıculos aut´onomos son una tecnolog´ıa novedosa que empez´o desde hace poco tiempo, la realidad es que las ra´ıces de los veh´ıculos aut´onomos tienen casi 100 anos˜ . En 1925, Francis Houdina asombr´o a las calles de Nueva York al poner en marcha un veh´ıculo sin ningun´ pasajeros a bordo, en su lugar hab´ıa tubos, bater´ıas, cables y radios. Pese a no ser un veh´ıculo comple- tamente aut´onomo, ya que era controlado a distancia por radio control, es uno de los primeros en desarrollar un concepto cercano al veh´ıculo aut´onomo [10]. En la d´ecada de 1980, en un proyecto patrocinado por la Universidad Bundeswehr de Munich, Ernst Dickmanns logr´o que el veh´ıculo recorriera las calles vac´ıas a 63 km/h sin otra ayuda m´as que una computadora integrada [11].

Posteriormente, en 1994 el proyecto PROMETHEUS-EUREKA logr´o que un Mercedes-Benz viajara desde Munich hasta Copenhague con una conducci´on aut´onoma que lograba hacer un seguimiento de carriles y de otros veh´ıculos [7].

9

Se puede observar que el camino de la rob´otica inteligente y los veh´ıculos aut´onomos est´an estrechamente relacionados entre s´ı, ya que uno de los princi- pales objetivos de la rob´otica inteligente es crear un sistema o m´aquina que sea capaz de percibir tanto su ambiente como lo que pasa en el interior de este (ya sea mediante sensores y/o actuadores) y tomar decisiones con base a esa refer- encia. Si bien, es todo un reto hacer la teor´ıa detr´as de un veh´ıculo aut´onomo tambi´en hay que tomar en cuenta los problemas ´eticos y los dilemas morales a los que se enfrenta el desarrollo de esta tecnolog´ıa.

Es importante considerar la parte de sostenibilidad de cada proyecto, y medi- ante eso podemos observar a cu´ales Objetivos de Desarrollo Sostenible podemos apoyar y aportar de manera considerable mediante la creaci´on y la utilizaci´on de nuestro proyecto. Analizando el impacto de nuestro proyecto en la sociedad, las ODS que se ver´ıan involucradas ser´ıan:

- ODS 9. Industria, Innovaci´on e Infraestructura: Fomentar la innovaci´on me- diante la implementaci´on de la tecnolog´ıa en ´areas industriales. [15]
- ODS 11. Ciudades y Comunidades Sostenibles: Mediante la tecnolog´ıa y la innovaci´on lograr aportar a la creaci´on de ciudades inteligentes y seguras.[15]

Asimismo, es fundamental contemplar los dilemas ´eticos que pueden llegar a ex- istir dentro de la planeaci´on y creaci´on de nuestro proyecto. Dentro de nuestro m´odulo se observaron ejemplos que podr´ıan estar dentro de los casos que nuestro robot puede llegar a tener, un ejemplo de ´estos ser´ıa el dilema del tranv´ıa, que consta de la responsabilidad de elegir no hacer nada, o reaccionar en casos ex- tremos c´omo lo que dice ´este ejemplo, un tranv´ıa se dirige hacia cuatro personas, en caso de desviarse tomar´ıa una v´ıa en hacia una sola persona.

El dilema se encuentra en la posibilidad de elegir dejar al tranv´ıa seguir su camino hac´ıa las cuatro personas o reaccionar y accionar un bot´on para que cambie su ruta hacia una uni´ ca persona. Se consider´o que ´este dilema se ase- meja a casos en los que posiblemente un mecanismo aut´onomo se puede llegar a encontrar como al momento de llegar a encontrarse con seres vivos en caminos,

- elegir entre peatones y nuestro usuario.

En otros t´erminos, dentro de ´este reporte se muestra el desarrollo y soluci´on de un sistema vehicular aut´onomo en donde el principal objetivo la detecci´on de senalamien˜ tos y sem´aforos al igual que el seguimiento de una trayectoria en donde el robot actua´ sin la participaci´on humana.

2  Marco te´orico

Para llegar a la resoluci´on del problema se requieren de algunos conceptos claves que ayudar´an a comprender m´as a fondo el entorno en el que se est´a desarrol- lando el sistema. Por una parte se pueden encontrar definiciones y uso de los componentes f´ısicos del sistema, por otra parte, existen definiciones que ayu- dar´an a comprender de mejor manera ´ambitos t´ecnicos.

- Circuito en lazo abierto: Conjunto de elementos electr´onicos en el cual la salida no se retroalimenta a la entrada y por lo tanto no existe ninguna ref- erencia del sistema en base a tiempo anterior.[1]
- Circuito en lazo cerrado: Se trata de un conjunto el´ectrico en el cual la senal˜ de salida se retroalimenta a la entrada de dicho sistema comport´andose como una referencia al mecanismo el´ectrico.[1]
- Puzzle bot: Kit electr´onico proporcionado por la empresa de Manchester Robotics, que cuenta con una Jetson nano de Nvidia, una hackerboard, c´amara tipo Raspberry Pi, entre otros componentes y piezas.[14]
- Jetson nano: Es una placa creada por la empresa de tecnolog´ıa Nvidia es- pec´ıficamente para el desarrollo de inteligencia artificial en sistemas embe- bidos.[8]
- Hackerboard: M´odulo de control creado por Manchester Robotics, el m´odulo contiene multiples´ entradas y salidas para los diferentes sensores y actu- adores, as´ı como capacidades de procesamiento en tiempo real. [15]
- Red neuronal: Es un sistema o modelo computacional interconectado por neuronas artificiales principalmente empleado para el aprendizaje y fun- cionamiento similar al de un cerebro humano.[4]
- Gazebo: Simulador utilizado para la recreaci´on de robots, modelos f´ısicos e inteligencia artificial en tercera dimensi´on.[2]
- ROS: Es un conjunto de librer´ıas el cual ayuda a facilitar el desarrollo de software para la creaci´on de m´aquinas inteligentes.[9]
- Visi´on computacional: Ayuda al analisis, procesamiento, e interpretaci´on de im´agenes y videos para la extracci´on de caracter´ısticas y atributos de cada figura o im´agen.[6]
- Control: Se trata del manejo y regularizaci´on de sistemas din´amicos medi- ante la manipulaci´on de componentes controladores para el ajuste del hard- ware.[13]
- M´aquina de estados: Es un m´etodo de organizaci´on que ayuda a ordenar el comportamiento de un sistema conforme las variables cambian con e tiempo
- estados.[5]
- Navegaci´on aut´onoma: Es la habilidad de un sistema para el movimiento dentro de un ambiente sin interacci´on humana.[12]
- Hardware: Es la parte f´ısica de un sistema el´ectrico, compuesto por elemen- tos electr´onicos que son capaces de ser manipulados.[3]
- Software: Se trata de las aplicaciones y/o programaci´on que ayuda a realizar ciertas tareas y controlar el hardware del sistema.[3]
3  Metodolog´ıa
1. Explicaci´on de Reto

Inicialmente se introdujo como situaci´on problema el impacto que tiene la rob´otica inteligente en la conducci´on aut´onoma y, a su vez, de los veh´ıculos aut´onomos. El problema a solucionar consiste en llevar un prototipo de veh´ıculo aut´onomo de un punto a otro de un recorrido lleno de obst´aculos. M´as tarde Manchester Robotics, el socio formador de la materia, aterriz´o el problema a solucionar en una autopista a escala adaptada para el puzzlebot.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.001.png)

Fig.1: Autopista escala para puzzlebot

Las senales˜ que se utilizaran en la pista ser´an las mostradas en la siguiente imagen.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.002.jpeg)

Fig.2: Senales˜ utilizadas en la autopista

Para cumplir exitosamente con la soluci´on problema, el puzzlebot deber´a com- pletar la pista siguiendo la l´ınea negra que existe en medio de la autopista e identificar y realizar las acciones correspondientes a cada una de las senales.˜

Inicialmente se introdujo como situaci´on problema el impacto que tiene la rob´otica inteligente en la conducci´on aut´onoma y, a su vez, de los veh´ıculos aut´onomos. El problema a solucionar consiste en llevar un prototipo de veh´ıculo aut´onomo de un punto a otro de un recorrido lleno de obst´aculos. M´as tarde Manchester Robotics, el socio formador de la materia, aterriz´o el problema a solucionar en una pista.

2. Procedimiento para la resoluci´on de la problematica

Para facilitar el entendimiento de la soluci´on del problema se decidi´o dividir el proceso en 2 partes principales: por una parte el control, y por otra la red neuronal y la visi´on.

Control

Para llevar a cabo todo de manera correcta se comenz´o a trabajar con el control en lazo abierto mediante simulaciones en gazebo y realizando pruebas se obtuvieron resultados buenos. Asimismo, se prob´o en el puzzlebot y realizaba de manera correcta la trayector´ıa tanto en la simulaci´on de Gazebo como en f´ısico, ya que realizaba el cuadro completo. Despu´es, se continu´o con la construcci´on del control en lazo cerrado, el cual solo pudimos probar en simulador debido a que nuestro hardware se encontraba en mal estado e inservible.

Visi´on y red neuronal

Para llevar a cabo la detecci´on de senales˜ y colores de sem´aforos, se utiliz´o la implementaci´on de red neuronal para que el sistema tenga la capacidad de saber que tipo de senal˜ es mediante entrenamiento con im´agenes previas y de acuerdo al conocimiento adquirido mandarle senales˜ de ajuste de velocidad al control a manera de mensaje en ROS.

Para poder hacer que el puzzlebot detectar´a las senales˜ fue necesario primero tener un dataset de las diferentes senales˜ de la pista. Dichas senales˜ fueron tomadas desde la c´amara que hay en el puzzlebot para tener una mayor ex- actitud de lo que podr´ıa percibir en el momento de encontrarse en la autopista a escala. Al tener un aproximado de 500 im´agenes por senal,˜ se procedi´o a etique- tar manualmente cada una de las im´agenes para entrenar el modelo y pasarlo a Yolov5 (modelo de detecci´on de objetos en tiempo real). Tras pasar el modelo pre-entrenado a Yolov5 con formato ONNX con los pesos de nuestro modelo, se define el formato correspondiente el cual tiene las im´agenes de entrada al modelo para poder mandar a llamarlo y sacar las predicciones correspondientes. Despu´es solo se implementaron los marcos de las predicciones y se filtraron las detecciones de bajo nivel de confianza para evitar que se tuviera un doble marco.

Asimismo, se utiliz´o visi´on para la creaci´on de nuestro seguidor de l´ıneas, el cual mediante la c´amara capta un video y por cada im´agen capturada se realiza un procesamiento de im´agenes y se calcula el error en base al centro de la l´ınea a seguir.

Para que nuestro sistema pudiera comunicarse correctamente en ROS se hizo una organizaci´on con diferentes nodos. Dicho sistema consiste en comenzar con un nodo que se encarga de abrir la c´amara del robot, a continuaci´on manda a manera de mensaje cam a los nodos de detecci´on de senales˜ y el seguidor de l´ıneas y depende de lo que se detecte en cada nodo, se env´ıan los mensajes de la senal˜ y del error respectivamente al controlador y eseu´ltimo nodo se encarga de env´ıar el mensaje de cmd vel a la hackerboard.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.003.png)

Fig.3: Sistema y organizaci´on de nodos y mensajes

Para la m´aquina de estados se creo una organizaci´on similar a la del sistema de nodos, incluyendo algunas variables como las velocidades y la variable de la senal.˜ Se comienza con un estado idle que se refiere a un estado de fabricaci´on en donde las variables se encuentran en reposo, el siguiente estado es start que se trata del inicio del sistema con la c´amara encendida y las velocidades iniciadas en el m´aximo valor, el siguiente estado es el del sigue lineas en donde sigue la c´amara encendida, la velocidad lineal igualmente en su m´aximo valor, pero la velocidad angular siendo variable dependiendo del ajuste que se obtenga al detectar el error, a continuaci´on se sigue con la detecci´on de senales˜ y sem´aforos en donde las variables anteriores se mantienen de igual manera, pero se inluye una nueva variable en donde se detecta de qu´e senal˜ se trata y por ultimo´ se pasa a un estado de t´ermino.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.004.png)

Fig.4: Diseno˜ de m´aquina de estados

4  Experimentos

Uno de los primeros experimentos realizados fue revisar el estado de nuestros encoders en el osciloscopio, ya que anteriormente se not´o que al implementar el control en los motores no se obten´ıa un resultado ´optimo. Lo primero que hicimos fue revisar en nuestros t´opicos de ros la velocidad que sal´ıa, y al detectar que la senal˜ no estaba llegando correctamente, el equipo decidi´o ir a comprobar si el error registrado se deb´ıa a un fallo en los motores, en los encoder o simplemente un fallo en el c´odigo. Al revisar los motores y encoders descubrimos que el fallo se encontraba en los encoders, en ambos encoders fallaba una fase.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.005.png)

Fig.5: Revisi´on de encoders

La segunda prueba realizada fue comprobar que la c´amara del Puzzlebot fun- cionar´a correctamente.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.006.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.007.png)

(a) Conexi´on del puzzlebot (b) Vista de c´amara desde el monitor

Fig.6: Pruebas de la c´amara

Posteriormente, se tomaron las im´agenes de las diferentes senales˜ y colores de sem´aforos con la c´amara del Puzzlebot para entrenar nuestra red neuronal.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.008.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.009.png)

(a) Conexi´on del puzzlebot y vista a sena˜ l (b) Vista de dataset en el monitor

Fig.7: Creaci´on del dataset

Una vez obtenido el dataset de todas las senales˜ y colores de sem´aforos, se entren´o la red neuronal y se incorpor´o a la jetson para que desde la c´amara del puzzlebot se detectara, por medio de visi´on, las diferentes senales˜ como: stop, give way, right, forward, left, working, round y los colores de los sem´aforos como se muestran en las im´agenes a continuaci´on.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.010.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.011.png)

(a) Detecci´on de la senal˜ “give way” (b) Detecci´on de la senal˜ “forward”

Fig.8: Correcta detecci´on de las senal˜ es

Asimismo, se comprob´o el rango en el cual se detectaban las senales˜ y cu´antas de ellas se percib´ıan al mismo tiempo. El prop´osito de esta prueba era verificar que nuestra red neuronal era capaz de detectar dos senales˜ simult´aneas, ya que en nuestra pista se tendr´ıa que detectar dos senales˜ al mismo tiempo: el sem´aforo y las diferentes vueltas.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.012.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.013.png)

(a) Detecci´on de las senales˜ en el puzzlebot (b) Vista del puzzlebot y las senales˜ Fig.9: Detecci´on de varias sen˜ales al mismo tiempo

Por otra parte, se tuvo un problema con la hackerboard. No se supo exactamente cu´al o a qu´e se deb´ıa el problema con la misma, pero tras algunas pruebas con otra hackerboard se pudo implementar la parte relacionada con los motores correctamente.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.014.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.015.png)

(a) Vista de las diferentes hackerboards (b) Pruebas de la hackerboard nueva Fig.10: Pruebas con diferentes Hackerboards

A continuaci´on, se trabaj´o en la creaci´on de un sigue lineas para obtener el error conforme a la detecci´on de la l´ınea del camino desde la c´amara del robot.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.016.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.017.png)

(a) Vista de las diferentes hackerboards (b) Pruebas de la hackerboard nueva Fig.11: Seguidor de l´ıneas en diferentes tramos de la autopista

Posteriormente, incorporamos el sigue l´ıneas en la jetson para que la imple- mentaci´on del error sea desde el puzzlebot.

11

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.018.png)

1) Implementaci´on del sigue l´ıneas en robot

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.019.png)

2) Implementaci´on del sigue l´ıneas en robot con pista

15

Fig.12: Sigue l´ıneas en el puzzlebot

En seguida, se prob´o el seguidor de l´ınea en la pista completa y se observ´o un correcto funcionamiento.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.020.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.021.png)

(a) Seguidor de l´ınea recorrido recto (b) Seguidor de linea recorrido en vuelta

Fig.13: Seguidor de lineas en la autopista

M´as adelante, se combin´o el sigue l´ıneas con visi´on, la cual es la detecci´on de senales.˜ Logrando que el robot avance mediante el seguimiento de la l´ınea adem´as de imprimir a terminal el numero´ de id de la sen˜al que ve en el trayecto.

![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.022.png) ![](Aspose.Words.d739c641-0d41-4bde-b20a-66617666774a.023.png)

(a) Detecci´on de senal˜ desde el robot (b) Detecci´on de senales˜ y publicaci´on de id

Fig.14: Detecci´on de l´ıneas en la pista

5  Resultados obtenidos

Despu´es de realizar todos los experimentos anteriores, finalmente se obtuvo el objetivo final del reto; lograr crear un sistema aut´onomo de conducci´on el cual siga una l´ınea e identifique mediante visi´on computacional las senales˜ y sem´aforos dentro de una pista proporcionada. A continuaci´on, se presentan los resultados en forma de videos demostrativos y codificaci´on realizada.

Exito´ en la soluci´on final. ⋆ ⋆ ⋆ ⋆ ⋆

5\.1 Recursos adicionales Link a c´odigos

C´odigo desarrollado para la implementaci´on , se puede consultar en: https://drive.google.com/drive/folders/1HobdaGZhqcq2381vUu6SjBN\_eLAoy7VG? usp=sharing

Link a videos

Video de Manchester Robotics, se puede consultar en: https://youtu.be/hO4i0kJHNz0

Video de la trayectoria final del puzzlebot, se puede consultar en: https://youtu.be/RpoSmSxaNiI

Video de la presentaci´on final, se puede consultar en: https://youtu.be/yPJffV-CdpI

6  Conclusi´on

Al realizar este proyecto se tuvo la oportunidad de observar la utilidad que tiene tanto la visi´on como las redes neuronales, el control y el hardware dentro de un robot, para realizar una autonom´ıa y funcionalidad correcta. Durante el proceso se encontraron algunos problemas sobre todo con el hardware por lo que se em- ple´o una gran parte del tiempo en resolver dichas cuestiones y debido a eso el tiempo destinado para avanzar y completar el reto se redujo, ya que, se obtu- vieron los componentes necesarios para tener un prototipo funcial en la semana de la entrega final. Sin embargo, se trabaj´o el tema de visi´on y la red neuronal, as´ı como el seguidor de l´ıneas para el momento en el que el hardware estuviera completamente funcional.

7  Reflexi´on Etica´

Finalmente pero no menos importante, es fundamental tener en cuenta los avances que prometen los veh´ıculos aut´onomos tanto en el campo de la industria e inno- vaci´on como en el desarrollo de ciudades sostenibles, ya que al tener un avance e implementaci´on de esta tecnolog´ıa se podr´ıa reducir las cantidades de accidentes automovil´ısticos causados por el ser humano tales como: el conducir en estado de ebriedad, saltarse los altos en los sem´aforos, ignorar senalamien˜ tos viales e ignorar al peat´on; y mejorar la vialidad al tener un correcto seguimiento de las leyes viales.

Sin embargo, el tener un veh´ıculo totalmente aut´onomo se encuentran difer- entes dificultades y nuevos retos como lo son los dilemas ´etico-morales alrededor de ellos, c´omo evitar accidentes en los veh´ıculos y en caso de tenerlos lo que se deber´ıa de priorizar primero: la seguridad de los pasajeros dentro del veh´ıculo

- de las personas que pasan por la calle. De la misma manera, se encuentra el mismo dilema que corre entorno a los robots inteligentes, generaci´on tanto de desempleos en ciertas ´areas tanto de nuevos empleos en ´areas diferentes y nuevas.

Este proyecto nos hizo comprender y reflexionar c´omo no s´olo la tecnolog´ıa est´a involucrada en la creaci´on de una m´aquina y/o sistema aut´onomo, sino que tambi´en hay cuestiones ´eticas y morales que tomar en cuenta para que el proyecto pueda desarrollarse en las mejores condiciones y tenga un impacto pos- itivo para la sociedad.

8  Contribuci´on de los autores

Barbara ⋆ ⋆ ⋆ ⋆ ⋆:

Para la creaci´on y desarrollo del reto, contribuy´o en la creaci´on de la red neuronal para la detecci´on de senales˜ y sem´aforos, tomando las im´agenes y eti- quetando cada una en la plataforma de Roboflow. Asimismo, aport´o con investi- gaci´on para el desarrollo correcto del reto. Tambi´en, ayud´o a la documentaci´on de cada parte que se conclu´ıa as´ı como de los problemas con los que se en- frentaba. Despu´es, contribuy´o en la realizaci´on de las pruebas con el puzzlebot en la pista con las diferentes senales˜ y sem´aforos y tambi´en con pruebas del sigue l´ıneas. Porulti´ mo, particip´o en los borradores de la documentaci´on, creaci´on del reporte escrito as´ı como el video final del reto, y posteriores revisiones de ´estos.

Manuel ⋆ ⋆ ⋆ ⋆ ⋆:

Se contribuy´o en la configuraci´on, desarrollo y pruebas del robot. Hizo las configuraciones necesarias para que el robot pudiera funcionar correctamente y se pudiera leer los datos arrojados por los componentes de este. Desarrollo el software del robot, en lo que incluimos el c´odigo que se us´o para la lectura de la c´amara, para el seguidor de lineas y para el control que el robot ejecutar´a depen- diendo de la senal,˜ adem´as de a la adaptaci´on de estos c´odigos para que puedan ser usados en ROS y puedan comunicarse unos con otros, adem´as de tambi´en adaptar el c´odigo de la detecci´on de senales˜ para que pudiera comunicarse con los demas codigos. Tambi´en contribuy´o en el etiquetado de las im´agenes para el entrenamiento del modelo de detecci´on de senales,˜ marcando aproximadamente 1400 im´agenes. Adem´as de que al momento de hacer las pruebas necesarias para hacer que todo funcionara correctamente fue la persona m´as pro-activa, haciendo continuamente pruebas, cambios y modificaciones para que todo pudiera inte- grarse de la mejor manera y la manera m´as robusta.

Luis ⋆ ⋆ ⋆ ⋆ ⋆:

Se desarroll´o un c´odigo para la toma de im´agenes desde la c´amara del Puzzle- Bot, en donde un video tomado por la c´amara se divide en frames que se guardan como im´agenes dentro de una carpeta previamente creada dentro de la jetson. Tambi´en se cre´o un proyecto en la herramienta de Roboflow donde se subieron un total de 4998 im´agenes de las senales˜ que formar´ıan parte de los datos con los que se entrenar´ıa nuestra red neuronal. Despu´es se administr´o dicho proyecto, repartiendo las im´agenes entre los miembros del equipo para la segmentaci´on de cada una de ellas, por mi parte se etiquetaron aproximadamente 1700 im´agenes en total. Luego se enviaron los datos a un companero˜ que ten´ıa una computa- dora m´as poderosa para el entrenamiento de la red. Una vez recibido el modelo entrenado, se hizo un c´odigo de yolo dentro de la jetson, donde se carg´o el mod- elo y pude realizar las pruebas de detecci´on de senales˜ desde casa. Importante mencionar que antes de poder realizar la carga del modelo a la jetson, tuve que realizar la instalaci´on de opencv dentro de la jetson, proceso que dur´o alrededor de 15 horas, pues hubo algunos errores que surgieron durante la instalaci´on, pero que fueron corregidos en ese lapso de tiempo. Finalmente, participaci´on activa en la recta final del proyecto, donde se adaptaron los c´odigos funcionales de cada parte del robot (vision y seguidor de l´ıneas, donde yo me involucr´e m´as en la primera) a que fueran nodos dentro de ROS; tambi´en se realizaron las pruebas de estos dos nodos funcionando ya en el PuzzleBot, y finalmente se trabaj´o en algunos puntos (cabe aclarar que no todos) de la realizaci´on del nodo contro- lador donde se integraban los dos nodos anteriores y se ajustaban los detalles del movimiento del robot segun´ cada senal˜ detectada. Vale la pena incluir la participaci´on durante la mayor´ıa de las pruebas que se llevaron a cabo durante todo el desarrollo del proyecto.

Ariadna ⋆ ⋆ ⋆ ⋆ ⋆:

En el desarrollo y resoluci´on de este reto, se contribuy´o con la participaci´on de la mayor´ıa de las pruebas de los componentes del puzzlebot, as´ı como con la toma de las fotograf´ıas que posteriormente se incluir´ıan a Roboflow como parte de nuestro dataset. Se hizo la anotaci´on de un aproximado de 1,050 im´agenes

que se incluir´ıan en el modelo de la red neuronal. Posteriormente se realiz´o

la investigaci´on y documentaci´on relacionada con el proyecto, se incluyen las diferentes revisiones y borradores del reporte final. Tambi´en, se hizo parte del gui´on del video entregado a Manchester Robotics, como la edici´on del mismo. Asimismo, se hizo el video y parte del gui´on del v´ıdeo final. En las ultimas´

pruebas realizadas con el puzzlebot en la pista.

References

1. Castano˜ , S. https://controlautomaticoeducacion.com/control-realimentado/ lazo-abierto-y-lazo-cerrado/.
1. Cuevas, C. https://hemeroteca.unad.edu.co/index.php/ publicaciones-e-investigacion/article/view/1593/1940.
1. GCFGlobal. https://edu.gcfglobal.org/es/informatica-basica/ que-es-hardware-y-software/1/.
1. IBM. https://www.ibm.com/mx-es/topics/neural-networks.
1. IBM. https://www.ibm.com/docs/es/bpm/8.6.0?topic=types-state-machines. (2021)
1. LAC BLOG. https://blog-es.lac.tdsynnex.com/ que-es-la-vision-computacional. (2017)
1. Li, Y. D´ıaz, M. Morantes, S. Dorati, Y. Veh´ıculos aut´onomos: Innovaci´on en la log´ıstica urbana. https://revistas.utp.ac.pa/index.php/ric/article/view/ 1864/2812.
1. Naylamp Mechatronics. https://naylampmechatronics.com/ sbc-placa-computadora/720-nvidia-jetson-nano-developer-kit.html
1. Ortego, D. https://openwebinars.net/blog/que-es-ros/. (2017)
1. Rodriguez, A. https://www.redalyc.org/journal/924/92469371015/html/. (2021)
1. Veh´ıculos aut´onomos. https://www.bbva.ch/noticia/ la-historia-de-los-vehiculos-autonomos-como-han-evolucionado-desde-los-primeros-prototipos/. (2021)
1. UNNOBA.https://sitio.unnoba.edu.ar/posgrado/estudiantes/cursos/ fundamentos-de-navegacion-autonoma-de-robots/.
1. UNNOBA. http://www.portaleso.com/web\_robot\_3/robot\_indice.html
1. Manchester Robotics. https://manchester-robotics.com/puzzlebot/
15. Manchester Robotics. https://manchester-robotics.com/puzzlebot/ hacker-board/
15. Naciones Unidas. https://www.un.org/sustainabledevelopment/es/ objetivos-de-desarrollo-sostenible/
