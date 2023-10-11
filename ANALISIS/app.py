import click
import os
from dotenv import load_dotenv
import psycopg2

def conectar_a_postgresql():
  load_dotenv()
  try:
    connection = psycopg2.connect (
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      dbname = os.getenv("DB_NAME"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD")
    )
    cursor = connection.cursor()
    return connection, cursor
  except psycopg2.Error as error:
    print("\nError al conectarse a la base de datos:", error)
    return None, None

def ejecutar_consulta(connection, cursor, consulta):
  try:
    cursor.execute(consulta)
    connection.commit()
    print("\nConsulta ejecutada con éxito.")
  except psycopg2.Error as error:
    connection.rollback()
    print("\nError al ejecutar la consulta:", error)

def cerrar_conexion(connection, cursor):
  if cursor:
    cursor.close()
  if connection:
    connection.close()

@click.group()
def cli():
  pass


@cli.command(name="Update")
def Update():
  connection, cursor =  conectar_a_postgresql();
  if connection and cursor:
    consulta = """
      COPY logs(log_timestamp, log_level, module_name, api,func_name, log_message, elapsed_time_ms)
      FROM '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana09/Tarea/POKE_API/app.csv' DELIMITER ';';
    """
    route = '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana09/Tarea/POKE_API/app.csv'
    ejecutar_consulta(connection, cursor, consulta)
    with open(route, 'w') as archivo:
      archivo.write('')


@cli.command(name="CheckAvailability")
@click.option('--module_name', required=True, help="module's name")
@click.pass_context
def CheckAvailability(ctx, module_name, last_days):
  if not module_name:
    ctx.fail('Se necesita el nombre de un módulo')
  else:
    if last_days:
      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT log_level,
        COUNT(*) AS cantidad
        FROM logs
        GROUP BY log_level
      """
      ejecutar_consulta(connection, cursor, consulta)
      resultados = cursor.fetchall()
      
      # Crear un diccionario para almacenar los resultados
      resultados_dict = {}
      
      # Iterar a través de los resultados y agregarlos al diccionario
      for fila in resultados:
        fecha, log_level, cantidad = fila
        if fecha not in resultados_dict:
          resultados_dict[fecha] = {}
        resultados_dict[fecha][log_level] = cantidad
      
      # Imprimir el diccionario de resultados
      # System availability = uptime / (uptime + downtime) * 100
      print("\n------------------------------\n")
      for fecha, valores in resultados_dict.items():
        print(f"{fecha}", end=": ")
        if(len(valores.items()) == 1):
          if 'WARNING' in valores:
            print("0%")
          else:
            print("100%")
        else:
          availability = (valores['INFO'] / (valores['INFO'] + valores['WARNING'])) * 100
          print(round(availability,2), end="%")
      print("\n------------------------------\n")
