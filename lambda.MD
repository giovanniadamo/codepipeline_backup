# AWS Lambda Functions Export Tool

## Descripción del Proyecto

Este proyecto contiene una herramienta en Python diseñada para exportar información detallada de todas las funciones AWS Lambda de una cuenta específica a un archivo CSV. La herramienta proporciona un análisis completo del uso de almacenamiento y versiones de las funciones Lambda, facilitando la gestión y monitoreo de recursos.

## Funcionalidad Principal

El script `allfuntionslambdas.py` realiza las siguientes operaciones:

### 1. Conexión a AWS Lambda
- Establece una conexión con el servicio AWS Lambda utilizando el SDK de boto3
- Permite especificar la región de AWS (por defecto: `us-east-1`)
- Utiliza las credenciales configuradas en el entorno local

### 2. Recopilación de Información
- **Lista todas las funciones Lambda** disponibles en la cuenta
- **Obtiene todas las versiones** de cada función Lambda
- **Calcula el tamaño total** de almacenamiento utilizado por cada función (incluyendo todas sus versiones)

### 3. Exportación de Datos
Genera un archivo CSV con la siguiente información para cada función:
- **Nombre de la función**: Identificador único de la función Lambda
- **Total de versiones**: Número total de versiones existentes de la función
- **Tamaño total usado (MB)**: Espacio de almacenamiento total consumido por todas las versiones

## Estructura del Código

### Función Principal: `export_lambda_info_to_csv()`

```python
def export_lambda_info_to_csv(region='us-east-1', output_file='lambda_functions.csv')
```

**Parámetros:**
- `region` (opcional): Región de AWS donde buscar las funciones Lambda (default: 'us-east-1')
- `output_file` (opcional): Nombre del archivo CSV de salida (default: 'lambda_functions.csv')

### Proceso de Ejecución

1. **Inicialización**: Crea un cliente de AWS Lambda para la región especificada
2. **Listado de funciones**: Obtiene todas las funciones Lambda usando `list_functions()`
3. **Análisis por función**: Para cada función encontrada:
   - Obtiene todas sus versiones con `list_versions_by_function()`
   - Calcula el tamaño total sumando el `CodeSize` de cada versión
   - Convierte el tamaño de bytes a megabytes
4. **Exportación**: Escribe los datos en formato CSV con codificación UTF-8

## Requisitos del Sistema

### Dependencias de Python
- `boto3`: SDK de AWS para Python
- `csv`: Biblioteca estándar para manejo de archivos CSV (incluida en Python)

### Configuración de AWS
- **Credenciales AWS**: Configuradas mediante AWS CLI, variables de entorno, o roles IAM
- **Permisos necesarios**:
  - `lambda:ListFunctions`
  - `lambda:ListVersionsByFunction`

## Casos de Uso

### 1. Auditoría de Recursos
- Identificar funciones Lambda que consumen más almacenamiento
- Analizar el número de versiones por función para optimización

### 2. Gestión de Costos
- Monitorear el uso de almacenamiento para control de costos
- Identificar funciones con versiones excesivas que pueden generar costos innecesarios

### 3. Limpieza y Mantenimiento
- Detectar funciones con múltiples versiones para posible limpieza
- Generar reportes periódicos del estado de las funciones Lambda

### 4. Compliance y Documentación
- Crear inventarios detallados de funciones Lambda
- Generar reportes para auditorías internas o externas

## Formato de Salida

El archivo CSV generado contiene las siguientes columnas:

| Nombre de la función | Total de versiones | Tamaño total usado (MB) |
|---------------------|-------------------|------------------------|
| mi-funcion-lambda-1 | 5                 | 15.25                  |
| mi-funcion-lambda-2 | 3                 | 8.75                   |

## Manejo de Errores

El script incluye manejo robusto de errores:
- **Funciones no encontradas**: Informa si no hay funciones Lambda en la región
- **Errores de conexión**: Captura y reporta problemas de conectividad con AWS
- **Errores de permisos**: Maneja casos donde faltan permisos necesarios
- **Errores de escritura**: Gestiona problemas al crear o escribir el archivo CSV

## Ejecución

Para ejecutar el script:

```bash
python allfuntionslambdas.py
```

El script generará automáticamente un archivo `lambda_functions.csv` en el directorio actual con toda la información recopilada.

## Personalización

El script puede ser personalizado modificando los parámetros de la función:

```python
# Ejemplo: Exportar funciones de una región específica
export_lambda_info_to_csv(region='eu-west-1', output_file='lambda_eu_functions.csv')
```

## Consideraciones de Rendimiento

- El tiempo de ejecución depende del número de funciones Lambda y sus versiones
- Para cuentas con muchas funciones, el proceso puede tomar varios minutos
- Se recomienda ejecutar durante horarios de baja actividad para evitar límites de API

## Seguridad

- El script no almacena credenciales en el código
- Utiliza las credenciales configuradas en el entorno AWS local
- No expone información sensible en los logs o archivos de salida