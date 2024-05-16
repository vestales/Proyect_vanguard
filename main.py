from fuciones import leer_limpiar_datos, grafico_cantidad_personas, grafico_tiempo_por_paso, hipotesis_test
from fuciones import grafico_finaliza_test, grafico_finaliza_control, hipotesis_tiempo, hipotesis_error
from fuciones import grafico_error, grafico_error_test, grafico_error_control, hipotesis_edad, crear_base_de_datos

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