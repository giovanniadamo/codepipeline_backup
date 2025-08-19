import boto3
import csv

def list_lambda_versions_and_generate_csv(output_file='lambda_versions.csv', region='us-east-1'):
    # Crear cliente de AWS Lambda
    lambda_client = boto3.client('lambda', region_name=region)

    try:
        # Obtener todas las funciones Lambda
        response = lambda_client.list_functions()
        functions = response.get('Functions', [])

        if not functions:
            print("No se encontraron funciones Lambda.")
            return
        
        print(f"Se encontraron {len(functions)} funciones Lambda.\n")

        # Crear el archivo CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Function Name', 'Total Versions', 'Total Size (Bytes)'])

            for function in functions:
                function_name = function['FunctionName']
                print(f"Procesando función: {function_name}")

                # Obtener las versiones de la función
                versions = lambda_client.list_versions_by_function(FunctionName=function_name)
                version_list = versions.get('Versions', [])

                # Calcular el tamaño total de las versiones
                total_size = sum(v.get('CodeSize', 0) for v in version_list)

                # Escribir en el CSV
                csvwriter.writerow([function_name, len(version_list), total_size])

        print(f"\nCSV generado exitosamente: {output_file}")

    except Exception as e:
        print(f"Error al listar funciones Lambda: {e}")

def delete_old_versions_of_function(function_name, keep_last=5, region='us-east-1'):
    # Crear cliente de AWS Lambda
    lambda_client = boto3.client('lambda', region_name=region)

    try:
        # Obtener versiones de la función
        versions = lambda_client.list_versions_by_function(FunctionName=function_name)
        version_list = versions.get('Versions', [])

        # Ordenar versiones por `LastModified` (fecha de creación) en orden descendente
        sorted_versions = sorted(version_list, key=lambda v: v['LastModified'], reverse=True)

        # Obtener las versiones a eliminar
        versions_to_delete = sorted_versions[keep_last:]

        if len(versions_to_delete) == 0:
            print(f"No hay versiones antiguas para eliminar en la función {function_name}.")
            return

        for version in versions_to_delete:
            # Excluir `$LATEST`, ya que no puede ser eliminado
            if version['Version'] != '$LATEST':
                try:
                    lambda_client.delete_function(FunctionName=function_name, Qualifier=version['Version'])
                    print(f"Eliminada versión: {version['Version']}")
                except Exception as e:
                    print(f"Error al eliminar versión {version['Version']}: {e}")

        print(f"\nLimpieza de versiones antiguas completada para la función {function_name}.")

    except Exception as e:
        print(f"Error al eliminar versiones de la función {function_name}: {e}")

# Main
if __name__ == "__main__":
    """ print("Generando CSV con información de funciones Lambda...")
    list_lambda_versions_and_generate_csv() """

    # Pedir al usuario el nombre de la función para eliminar versiones antiguas
    function_name = input("\nIngrese el nombre de la función Lambda para eliminar versiones antiguas: ").strip()
    if function_name:
        print(f"Eliminando versiones antiguas para la función: {function_name}")
        delete_old_versions_of_function(function_name)
    else:
        print("No se proporcionó un nombre de función.")
