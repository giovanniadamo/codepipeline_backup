import boto3
import json
import os
import inquirer

# Crear una sesión de boto3
session = boto3.Session()

# Crear un cliente de CodePipeline
client = session.client('codepipeline')

# Función para listar todos los pipelines
def list_pipelines(client):
    pipelines = []
    response = client.list_pipelines()
    pipelines.extend(response['pipelines'])
    
    # Paginación si hay más de 100 pipelines
    while 'nextToken' in response:
        response = client.list_pipelines(nextToken=response['nextToken'])
        pipelines.extend(response['pipelines'])
    
    return pipelines

# Función para obtener la configuración de un pipeline y guardarlo en un archivo JSON
def get_and_save_pipeline(client, name):
    try:
        response = client.get_pipeline(name=name)
        pipeline = response['pipeline']
        
        # Crear la carpeta si no existe
        if not os.path.exists('pipelines_backup'):
            os.makedirs('pipelines_backup')
        
        # Crear un nombre de archivo válido
        filename = os.path.join('pipelines_backup', f"{name.replace(' ', '_')}.json")
        
        # Guardar la configuración del pipeline en un archivo JSON
        with open(filename, 'w') as f:
            json.dump(pipeline, f, indent=4)
        print(f"Pipeline '{name}' guardado en '{filename}'.")
    except client.exceptions.PipelineNotFoundException:
        print(f"Pipeline '{name}' no encontrado.")

def backup_all_pipelines():
    # Crear la carpeta para guardar los archivos JSON si no existe
    if not os.path.exists('pipelines_backup'):
        os.makedirs('pipelines_backup')
    
    # Listar todos los pipelines
    pipelines = list_pipelines(client)
    
    # Recorrer todos los pipelines y guardar cada uno en un archivo JSON
    for pipeline in pipelines:
        name = pipeline['name']
        get_and_save_pipeline(client, name)

def backup_individual_pipeline():
    questions = [
        inquirer.Text('name', message="Introduce el nombre del pipeline")
    ]
    answers = inquirer.prompt(questions)
    name = answers['name']
    get_and_save_pipeline(client, name)

def main():
    # Menu de opciones
    questions = [
        inquirer.List('option',
                      message="Elige una opción",
                      choices=['Respaldar todas las canalizaciones', 'Respaldar una canalización individual'],
                     ),
    ]
    answers = inquirer.prompt(questions)
    
    if answers['option'] == 'Respaldar todas las canalizaciones':
        backup_all_pipelines()
    elif answers['option'] == 'Respaldar una canalización individual':
        backup_individual_pipeline()

if __name__ == "__main__":
    main()
