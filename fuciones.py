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

