"""por qué se llama 3 veces al archivo funciones
"""

from fuciones import leer_limpiar_datos, grafico_cantidad_personas, grafico_tiempo_por_paso, hipotesis_test
from fuciones import grafico_finaliza_test, grafico_finaliza_control, hipotesis_tiempo, hipotesis_error
from fuciones import grafico_error, grafico_error_test, grafico_error_control, hipotesis_edad, crear_base_de_datos


"""no podemos ejecutar las funciones porque la ruta del archivo yaml solo permite hacerlo al administrador principal
para poder hacerlo, hemos modificado las rutas de los dataframes en el archivo yaml:

data:
  pt_1: 'data/df_final_web_data_pt_1.txt'
  pt_2: 'data/df_final_web_data_pt_2.txt'
  demo: 'data/df_final_demo.txt'
  experimet_clients:  'data/df_final_experiment_clients.txt'

También hemos modificado la línea en la que se llama el archivo yaml en la función leer_limpiar_datos:
    try:
        with open("config.yaml", 'r') as file:
            config = yaml.safe_load(file) 
    except Exception as e:
        print(f"Error reading the config file: {e}")

Ahora cualquiera que quiera ejecutar el código puede hacerlo

"""



df = leer_limpiar_datos()

grafico_cantidad_personas(df)

grafico_finaliza_test()

grafico_finaliza_control()

hipotesis_test(df)

grafico_tiempo_por_paso(df)

hipotesis_tiempo(df)

grafico_error(df)

grafico_error_test(df)

grafico_error_control(df)

hipotesis_error(df)

hipotesis_edad(df)

crear_base_de_datos(df)

""" 
las columnas de número de cuentas y dinero en cuenta eliminadas creemos que son datos interesantes para analizar el perfil
 tanto de los clientes generales como el de los que han hecho el test."""

"""
sin un análisis de los clientes generales no podemos saber o intuir si la muestra seleccionada es representativa"""
 
"""
en las funciones de hipótesis, estaría bien que se pudiera añadir como argumentos el nivel de significancia 
y la dirección de la hipótesis

También habría que añadir algo más de información en el mensaje que se imprime de la primera hipótesis, ya que por el nombre de la función
y la frase final no sabemos qué se está probando

En la última función de hipótesis por el gráfico y el mensaje que se imprime tampoco entendemos qué se está probando
"""

"""
no entendemos qué hace la función crear_base_de_datos
"""


"""
consideramos que hay poco comentario en general para entender bien el código tanto en el archivo main de producción como en el de funciones
"""