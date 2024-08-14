
# AWS CodePipeline Backup Script

Este repositorio contiene un script en Python diseñado para realizar backups automatizados de todos los pipelines de AWS CodePipeline o de un pipeline específico, según se especifique. Utilizando las capacidades de la API de AWS, este script facilita la creación de copias de seguridad de la configuración y los estados de los pipelines, permitiendo a los usuarios guardar y restaurar sus flujos de trabajo con facilidad.

## Características Principales

- **Backup de Todos los Pipelines**: Realiza un backup completo de todos los pipelines en tu cuenta de AWS.
- **Backup Selectivo**: Permite realizar un backup de un pipeline específico proporcionando su nombre.
- **Fácil Configuración**: Configurable a través de parámetros sencillos y fácil de integrar en flujos de trabajo existentes.
- **Compatibilidad**: Compatible con cualquier entorno que soporte Python y la AWS CLI.
- **Seguridad**: Las credenciales y configuraciones sensibles se manejan de manera segura mediante variables de entorno o perfiles de AWS configurados.

## Requisitos

- Python 3.7 o superior
- AWS CLI configurado
- Paquetes de Python requeridos (ver `requirements.txt`)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/giovanniadamo/codepipeline_backup.git
   cd codepipeline_backup


2. Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt

4. Configura tus credenciales de AWS si aún no lo has hecho:
    ```bash
    aws configure
