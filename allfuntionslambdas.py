import boto3
import csv

def export_lambda_info_to_csv(region='us-east-1', output_file='lambda_functions.csv'):
    # Crear un cliente de Lambda
    lambda_client = boto3.client('lambda', region_name=region)

    try:
        # Obtener todas las funciones Lambda
        response = lambda_client.list_functions()
        functions = response.get('Functions', [])

        if not functions:
            print("No se encontraron funciones Lambda.")
            return

        # Crear el archivo CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Escribir el encabezado
            csvwriter.writerow(['Nombre de la función', 'Total de versiones', 'Tamaño total usado (MB)'])

            for function in functions:
                function_name = function['FunctionName']

                # Obtener versiones de la función
                versions = lambda_client.list_versions_by_function(FunctionName=function_name)
                version_list = versions.get('Versions', [])

                # Calcular el almacenamiento total usado por las versiones
                total_storage = sum(version.get('CodeSize', 0) for version in version_list)

                # Escribir la información en el archivo CSV
                csvwriter.writerow([function_name, len(version_list), total_storage / (1024 * 1024)])

        print(f"Información exportada correctamente a {output_file}")

    except Exception as e:
        print(f"Error al obtener la información de las Lambdas: {e}")

# Llamar a la función
export_lambda_info_to_csv()
