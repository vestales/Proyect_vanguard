def leer_limpiar_datos():
    import yaml
    import pandas as pd

    try:
        with open(r"C:\Users\germa\Documents\GitHub\Proyect_vanguard\config.yaml", 'r') as file:
            config = yaml.safe_load(file) 
    except Exception as e:
        print(f"Error reading the config file: {e}")

    #leemos la base de datos
    df1 = pd.read_csv(config['data']['demo'])
    df2 = pd.read_csv(config['data']['experimet_clients'])
    df3 = pd.read_csv(config['data']['pt_1'])
    df4 = pd.read_csv(config['data']['pt_2'])

    #eliminamos los usuarios que no participan en el test
    df2 = df2.dropna(subset = ["Variation"])

    #juntamos la tabla de los datos de los usuarios con la tabla de los usuarios que participan en el test
    df_clientes = pd.merge(df2, df1, on='client_id')

    #ponemos que los floats sean de dos decimales
    pd.set_option('display.float_format', '{:.2f}'.format)

    #eliminamos las columnas "clnt_tenure_mnth", "num_accts", "bal"
    columnas_eliminar = ["clnt_tenure_mnth", "num_accts", "bal"]

    df_clientes = df_clientes.drop(columns=columnas_eliminar)

    #cambiamos el genero X por U para que este todo igual (los dos generos significan que no han querido decir cual era el suyo) y eliminamos datos nulos
    df_clientes["gendr"] = df_clientes["gendr"].replace({"X":"U"})
    df_clientes = df_clientes.dropna()

    #unimos las tablas de los resultado de control y test
    df_pruebas = pd.concat([df3, df4], axis=0)
    df_pruebas = df_pruebas.reset_index(drop=True)
    
    #aqui unimos todas las tablas en una y las ordenamos por cliente, fecha y codigo de sesion
    df_pruebas_con_clientes = pd.merge(df_clientes, df_pruebas, on='client_id', how='left')
    df_test = df_pruebas_con_clientes.sort_values(by=["client_id", "visit_id", "date_time"])

    #lista de los pasos que queremos analizar
    list_okey = ['start_step_1', 'step_1_step_2', 'step_2_step_3',
       'step_3_confirm','step_3_step_1',
       'step_2_step_1', 'step_3_step_2',
       'step_1_start', 'step_3_start', 'step_2_start']
    
    #guardamos la fecha de la ultima fecha y paso
    df_test["last_date_time"] = df_test.groupby(["client_id", "visit_id"])["date_time"].shift(1)

    df_test["last_step"] = df_test.groupby(["client_id", "visit_id"])["process_step"].shift(1)
    
    df_test["step"] = df_test["last_step"] + "_" + df_test["process_step"]
    df_test = df_test[(df_test["step"].isin(list_okey))]

    #pasamos date_time a tipo fecha
    df_test["date_time"] = pd.to_datetime(df_test["date_time"])
    
    df_test["last_date_time"] = pd.to_datetime(df_test["last_date_time"])

    #guardamos la diferencia de tiempo y lo convertimos a segundos
    df_test["diference_time"] = df_test["date_time"] - df_test["last_date_time"]
    df_test["total_segons"] = df_test["diference_time"].dt.total_seconds()
    

    return df_test


def grafico_cantidad_personas(df):
    import plotly.express as px

    df_total_clientes = df.groupby(by=["process_step", "Variation", "client_id"]).count()["calls_6_mnth"].reset_index()
    

    order = ["step_1", "step_2", "step_3", "confirm"]

    df_total_clientes = df_total_clientes[(df_total_clientes["process_step"].isin(order))]


    fig = px.histogram(df_total_clientes, x="process_step", color="Variation", barmode="group")
    fig.update_layout(xaxis=dict(categoryorder='array', categoryarray=order))
    fig.show()
    return None



def grafico_finaliza_test():
    import plotly.graph_objects as go
    start_test = 26672000
    finish_test = 18682000

    tasa_fin_test = finish_test/start_test * 100

    tasa_fin_test

    labels = ['Finalizado','No Finalizado']
    values = [tasa_fin_test, 100 - tasa_fin_test]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()
    return None



def grafico_finaliza_control():
    import plotly.graph_objects as go
    start_control = 23391000
    finish_control = 15428000

    tasa_fin_control = finish_control/start_control * 100

    tasa_fin_control

    labels = ['Finalizado','No Finalizado']
    values = [tasa_fin_control, 100 - tasa_fin_control]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()
    return None


def grafico_tiempo_por_paso(df):
    import plotly.express as px

    df_algo = df.groupby(["step", "Variation"])["total_segons"].mean().reset_index()


    fig = px.bar(df_algo, x="step", y="total_segons", color="Variation", barmode="group")
    fig.show()
    return None


def hipotesis_test(df):
    import scipy.stats as st

    #Set the hypothesis

    #H0: df_test = df_control
    #H1: df_test > df_control

    #significance level = 0.05

    df_test = df[(df["Variation"].isin("Test"))]
    df_control = df[(df["Variation"].isin("Control"))]
    statistic, pvalue = st.ttest_ind(df_test, df_control, equal_var=False,alternative="greater")

    if pvalue > 0.05:
        print("No hay evidencia suficiente para saber si el nuevo sitio web fue mejor.")
    else:
        print("El nuevo sitio web dio unos resultamos mucho mejores ques el del viejo.")


def hipotesis_tiempo(df):
    import scipy.stats as st

    #Set the hypothesis

    #H0: df_test = df_control
    #H1: df_test > df_control

    #significance level = 0.05

    list_rute_okey = ['start_step_1', 'step_1_step_2', 'step_2_step_3','step_3_confirm']

    df_test = df[(df["step"].isin(list_rute_okey)) & (df["Variation"] == "Test")]

    df_control = df[(df["step"].isin(list_rute_okey)) & (df["Variation"] == "Control")]
    statistic, pvalue = st.ttest_ind(df_test["total_segons"], df_control["total_segons"], equal_var=False,alternative="greater")

    if pvalue > 0.05:
        print("No hay evidencia suficiente para saber si la gente del nuevo sitio web fue mas rapida que la del viejo.")
    else:
        print("La gente en el nuevo sitio web tardo menos tiempo ques el del viejo.")


def hipotesis_error(df):
    import scipy.stats as st

    list_rute_reves = ['step_3_step_1',
       'step_2_step_1', 'step_3_step_2',
       'step_1_start', 'step_3_start', 'step_2_start']
    
    list_error_test = df[(df["step"].isin(list_rute_reves)) & (df["Variation"] == "Test")].groupby("client_id").count()["gendr"]
    list_error_control = df[(df["step"].isin(list_rute_reves)) & (df["Variation"] == "Control")].groupby("client_id").count()["gendr"]
    #Set the hypothesis

    #H0: df_test = df_control
    #H1: df_test > df_control

    #significance level = 0.05

    
    statistic, pvalue = st.ttest_ind(list_error_control, list_error_test, equal_var=False,alternative="greater")

    if pvalue > 0.05:
        print("No hay evidencia suficiente para saber si la gente del nuevo sitio web tiene mas errores que la del viejo.")
    else:
        print("La gente en el nuevo sitio web tiene mas errores ques la del viejo.")


def grafico_error(df):
    import plotly.express as px

    list_rute_reves = ['step_3_step_1',
       'step_2_step_1', 'step_3_step_2',
       'step_1_start', 'step_3_start', 'step_2_start']

    df_error = df[(df["step"].isin(list_rute_reves))].groupby("step").count()["client_id"].reset_index()
    fig = px.pie(df_error, values='client_id', names='Variation', title='Porcentaje de errores')
    fig.show()

    return None


def grafico_error_test(df):
    import plotly.express as px

    list_rute_reves = ['step_3_step_1',
       'step_2_step_1', 'step_3_step_2',
       'step_1_start', 'step_3_start', 'step_2_start']

    df_error = df[(df["step"].isin(list_rute_reves)) & (df["Variation"] == "Test")].groupby("step").count()["client_id"].reset_index()
    fig = px.pie(df_error, values='client_id', names='Variation', title='Porcentaje de errores')
    fig.show()

    return None


def grafico_error_control(df):
    import plotly.express as px

    list_rute_reves = ['step_3_step_1',
       'step_2_step_1', 'step_3_step_2',
       'step_1_start', 'step_3_start', 'step_2_start']

    df_error = df[(df["step"].isin(list_rute_reves)) & (df["Variation"] == "Control")].groupby("step").count()["client_id"].reset_index()
    fig = px.pie(df_error, values='client_id', names='Variation', title='Porcentaje de errores')
    fig.show()

    return None


def hipotesis_edad(df):
    import plotly.express as px
    import scipy.stats as st

    df_edad = df[(df["process_step"] == "confirm")].groupby(["client_id", "clnt_age", "Variation"]).count()["visit_id"].reset_index()
    
    df_edad_sum = df_edad.groupby(["clnt_age", "Variation"])["visit_id"].count().reset_index()

    fig = px.histogram(df_edad_sum, x="clnt_age", y="visit_id" ,color="Variation", nbins=80, marginal="box")
    fig.show()

    #Set the hypothesis


    #H0: df_edad_sum_test = df_edad_sum_control
    #H1: df_edad_sum_test != df_edad_sum_control

    #significance level = 0.05

    #En este caso no podemos rechazar la hipotesis ya que son muy similares.
    #No hay evidencia para decir que las edades son diferentes.

    df_edad_sum_test = df_edad_sum[df_edad_sum["Variation"] == "Test"]
    df_edad_sum_control = df_edad_sum[df_edad_sum["Variation"] == "Control"]

    statistic, pvalue = st.ttest_ind(df_edad_sum_test['visit_id'].values, df_edad_sum_control['visit_id'].values, equal_var=False)

    if pvalue > 0.05:
        print("No hay evidencia para decir que las edades son diferentes.")
    else:
        print("Las edades no estan repartidas de forma uniforme.")



def crear_base_de_datos(df):
    df.to_csv("lectura_datos.csv", sep=",", index=False, encoding="utf-8")

