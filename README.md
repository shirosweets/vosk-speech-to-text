[![Vosk](https://img.shields.io/pypi/v/vosk.svg)](https://pypi.org/project/vosk/) [![Vosk](https://img.shields.io/pypi/v/yt2mp3.svg)](https://pypi.org/project/vosk/) [![PyPi Python Versions](<https://img.shields.io/pypi/pyversions/vosk.svg>)](<https://pypi.org/project/vosk/>)

# Descripción
Este repositorio es para recibir señales, realizar transcripción de video/sonido a texto para enviarlo por elastic para realizar búsquedas de texto.</p>
> Importante: el desarrollo de este feature solo funciona correctamente para sistemas x64

# Contenido
- [Feature](#feature)
- [Instalación](#instalación)
  - [Correr local](#cómo-correrlo-local)
  - [Testeos particulares](#cómo-correr-testeos-particulares)
    - [Desactivación del virtualenv](#desactivación-del-virtualenv)
- [¿Cómo desarrollar este feature?](#¿cómo-desarrollar-este-feature?)
  - [Flujo vosk-speech-to-text](#flujo-welo-speech-to-text)
  - [Documentos del feature](#documentos-del-feature)
  - [Formatos admitidos para correr la transcripción](#formatos-admitidos-para-correr-la-transcripción)
  - [¿En dónde se puede dejar corriendo el feature?](#¿en-dónde-se-puede-dejar-corriendo-el-feature?)
  - [¿Dónde está en Elastic?](#¿dónde-está-en-elastic?)
    - [Mapeo de Elastic](#mapeo-de-elastic)
    - [Cerebro](#cerebro)
  - [Grafana (para futuro)](#grafana-(para-futuro))
  - [Uso de Pubsub](#uso-de-pubsub)
- [Versión de Python](#versión-de-Python-utilizada-para-crearlo)
- [Directorios](#directorios)
- [Configuración](#configuración)
  - [Comandos](#comandos)
- [Acerca de VOSK](#acerca-de-vosk)
  - [¿Qué es VOSK?](#¿qué-es-vosk?)
  - [¿Cómo añadir nuevos idiomas al feature?](#¿cómo-añadir-nuevos-idiomas-al-feature?)
  - [Normas ISO 639 1](#normas-ISO-639-1)
  - [Idiomas soportados por VOSK](#idiomas-soportados-por-VOSK)
  - [Idiomas configurados actualmente para este feature](#idiomas-configurados-actualmente-para-este-feature)
- [Ejemplo Actions Github](#ejemplo-actions-github)
- [Ejemplo Gitlab CI/CD](#ejemplo-gitlab-CI/CD)
- [En el futuro: NLP](#en-el-futuro:-NLP)
- [Extra](#extra)

# Feature
Te permite recibir mensajes de señales de streaming a través de Pubsub
- Formatear mensajes con esta estructura de mensaje
- Descarga archivos (.ts, .mp4, .mp3, .mkv, .wav) de los mensajes</p>

Te permite correr la librería de reconocimiento de voz
- Librería ya configurada para ser corrida en Inglés y Español con modelos livianos
- Toma el archivo descargado, le corre el speech-to-text y guarda los datos necesarios
- Prepara los mensajes para ser enviados por Elastic</p>

En Elastic:
- Mandar mensajes a Elastic (index)</p>
# Instalación

## Cómo correrlo local:
`git clone https://github.com/shirosweets/vosk-speech-to-text.git`     
`python3 -m venv speech_venv` (por única vez)  
`source speech_venv/bin/activate`  
`sudo apt-get update -y` (por única vez)   
`sudo apt-get install -y libportaudio2` (por única vez)   
`sudo apt-get install -y portaudio19-dev` (por única vez)   
`pip install --upgrade pip`   
`pip install -r requirements.txt`   
`python3 main_run.py` 

## Cómo correr testeos particulares:
`git clone https://github.com/shirosweets/vosk-speech-to-text.git`     
`python3 -m venv speech_venv` (por única vez)  
`source speech_venv/bin/activate`  
`sudo apt-get update -y` (por única vez)   
`sudo apt-get install libportaudio2` (por única vez)   
`sudo apt-get install -y portaudio19-dev` (por única vez)   
`pip install --upgrade pip`   
`pip install -r requirements.txt`   
`python3 main_local_test.py` 

1) Cada opción es una parte del desarrollo. Seleccionar qué se quiere probar en particular.
2) Si se desea realizar más pruebas particular modificar el archivo con una nueva opción ingresada por input.
3) En el archivo `src/test` se encuentran videos y audios para realizar pruebas (esto para reducir el tiempo de los testeos).

### Desactivación del virtualenv
`deactivate`

# ¿Cómo desarrollar este feature?
El desarrollo debe realizarse mediante leer mensajes de Pubsub de la señal de streaming, filtrar y procesar esos mensajes, parsearlos y mandarlos por elastic.</p>

## Flujo vosk-speech-to-text
<p align="center">
  <img src="images/flujo_ speech_to_text_y_search.png" width="" title="Flujo welo-speech-to-text">
</p>

## Formatos admitidos para correr la transcripción
- mp3
- mp4
- avi
- mkv
- ts
- wav

## ¿En dónde se puede dejar corriendo el feature?
**Recomendable y deseable**: VM de GCP</p>
**Configuración necesaria**: Kubernetes</p>
No recomendable: local

Configuración necesaria para GCP:</p>
Se debe modificar/reemplazar el archivo `config_speech/service_account.json`
```json
{
  "type": "service_account",
  "project_id": "name-proyect",
  "private_key_id": "key",
  "private_key": "key",
  "client_email": "email@example.com",
  "client_id": "id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "url"
}
```

## ¿Dónde está en Elastic?
Elastic es la herramienta principal para poder realizar las búsquedas de texto.
Todos los mensajes enviados se encuentran en el index qque se configure en `INDEX_DSL` del archivo `config_speech/elasticsearch-dsl_config.py` (recordar que uno debe tener ya creado el servidor en Elasticsearch para poder acceder al index)</p>
Si se desea cambiar la configuración del mapeo se debe borrar el index, inicializarlo nuevamente con el documento modificado.
### Mapeo de Elastic
```python
{ - 
  "parse-speech": { - 
    "mappings": { - 
      "properties": { - 
        "channel_id": { - 
          "type": "integer"
        },
        "channel_name": { - 
          "type": "text",
          "fields": { - 
            "raw": { - 
              "type": "keyword"
            }
          },
          "analyzer": "snowball"
        },
        "end_time": { - 
          "type": "date"
        },
        "end_word": { - 
          "type": "text",
          "fields": { - 
            "raw": { - 
              "type": "keyword"
            }
          },
          "analyzer": "snowball"
        },
        "first_time": { - 
          "type": "date"
        },
        "first_word": { - 
          "type": "text",
          "fields": { - 
            "raw": { - 
              "type": "keyword"
            }
          },
          "analyzer": "snowball"
        },
        "sentence": { - 
          "type": "text",
          "fields": { - 
            "raw": { - 
              "type": "keyword"
            }
          },
          "analyzer": "snowball"
        }
      }
    }
  }
}
```

### Cerebro
Esta herramienta nos sirve para poder visualizar los indexs, mapeos, cantidad de espacio utilizado, y cantidad de documentos de elastic. </p>
La forma más sencilla de correrlo es con su propio [docker](https://hub.docker.com/r/lmenezes/cerebro/)</p>

`docker run -e CEREBRO_PORT=8092 -p 8092:8092 lmenezes/cerebro`</p>

Ir al puerto levantado:</p>

[http://localhost:8092/#/connect](http://localhost:8092/#/connect)</p>

Luego ingresar el servidor de elastic en el Node address.

## Grafana (para futuro)
Permite mandar alertas, crear queries para visualizar en gráficos y realizar consultas.

## Uso de Pubsub
Recibe las señales de chunks en streaming por mensajes de los cuales se deben filtrar los canales que queremos y "preparar" dichos mensajes.</p>
Actualmente se encuentra escuchando la suscripción [projects/welo-feeds/subscriptions/chunks_to_speech](https://console.cloud.google.com/cloudpubsub/subscription/detail/chunks_to_speech?project=welo-feeds) con el tópico [projects/welo-feeds/topics/chunk_processed](https://console.cloud.google.com/cloudpubsub/topic/detail/chunk_processed?project=welo-feeds)

## Versión de Python utilizada para crearlo
`Python 3.8.5`

# Directorios
- **`config`**: archivos de configuración

  - **`config.env`**: archivo con las variables de entorno
  - **`vosk_config`**: modelos de configuración de Vosk

- **`images`**: imágenes del README del repositorio 

- **`files`**: archivos que se van descargando para aplicarle Vosk

  - **`global_test`**: chunks del canal `GLOBAL TEST`

- **`logs`**: configuración de los logs

  - **`parse_logs`**: logs de los parse

- **`src`**: código
  
  - **`test`**: archivos para utilizar en los test
  - **`examples`**: archivos para tener en cuenta

# Configuración
Esto cambiará en un futuro, pero actualmente se debe hacer en el mismo repositorio:

1) Se debe configurar los canales que pueden acceder a esta funcionalidad en: `config/channel_config.py`
- Añadir un nuevo canal: agregarlo al diccionario `CHANNELS`.
- Eliminar un nuevo canal: eliminarlo del diccionario `CHANNELS`.
2) Configurar idiomas del speech en: `config/vosk_config` cada archivo `model_` es un idioma añadido y configurado. Si se desea añadir un nuevo idioma se debe establecer la lógica para detectarlo.
3) Cada modelo tiene una manera diferente de realizar el output del speech, por lo tanto se debe tener en cuenta esto para poder procesar los mensajes, parsearlos y mandarlos a elastic. 
4) Los modelos pueden ser añadidos directamente o descargados.

## Comandos
Ver los procesos corriendo en background:   
`fg`    
Estilo del código (PEP8):   
`pycodestyle . --exclude=ignore_*,config_speech/channel_config.py`  
Eliminar todos los modelos:   
`python3 clear_models.py`
1) type: `y`

# Acerca de VOSK
## ¿Qué es VOSK?
VOSK es una librería que se puede utilizar para realizar transcripciones de voz/audio a texto de manera offline. Funciona a través de modelos los cuáles uno puede definir, crear y utilizar pero existen modelos comunitarios (libres) en los cuáles ya están definidos los idiomas y esquemas a utilizar.

### Links de VOSK
[Documentación general de la librería](https://alphacephei.com/vosk/)    
[Librería en Python](https://github.com/alphacep/vosk-api/tree/master/python)   
[Modelos de VOSK](https://alphacephei.com/vosk/models)

## ¿Cómo añadir nuevos idiomas al feature?
Debido a que VOSK trabaja con modelos y estos deben ser definidos, configurados y entrenados, dependiendo el modelo es el formato del output del mismo, por lo cual depende qué tan diferentes estén definidos los formatos para realizar el parseo y posterior envío por elastic.

## Normas ISO 639 1
La identificación de cada modelo de idioma es tomado por las siglas de las normas [**ISO 639-1**](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

## Idiomas soportados por VOSK
Este es el listado de todos los idiomas que puede expandirse este fetuare:
- English, 
- Indian English, 
- German, 
- French, 
- Spanish, 
- Portuguese, 
- Chinese, 
- Russian, 
- Turkish, 
- Vietnamese, 
- Italian, 
- Dutch, 
- Catalan, 
- Arabic, 
- Greek, 
- Farsi, 
- Filipino.

## Idiomas configurados actualmente para este feature
- Spanish,
- English

# En el futuro: NLP
La idea es poder crear nuestros propios modelos de VOSK para cada idioma añadiendole redes neuronales las cuales serían entrenadas con [NLP](https://www.nltk.org/). Esto supone una enorme expansión de esta funcionalidad para el futuro.

# Ejemplo Actions Github
Añadí un ejemplo básico de actions con el archivo `check_codestyle.yml` con su `requirements_tci.txt`
# Ejemplo Gitlab CI/CD
Añadí un ejemplo básico de `.gitlab-ci.yml` con su `requirements_tci.txt`

# Extra
https://shields.io/</p>
https://pypi.org/project/python-dotenv/

# Autor
Github: [shirosweets](https://github.com/shirosweets)</p>
Email de contacto: vsv.dev.soft@gmail.com
> Valentina Vispo ≧◠ᴥ◠≦
