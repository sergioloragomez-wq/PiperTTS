# Configuración de STT para Vicidial

## Descripción

Este repositorio contiene la configuración completa para integrar Speech-to-Text (STT) con Vicidial/Asterisk. Permite transcribir automáticamente llamadas, grabar respuestas de clientes y almacenar transcripciones en la base de datos.

## Características

- 🎤 **Múltiples motores STT**: Google Cloud Speech, OpenAI Whisper, CMU Sphinx
- 🌐 **Soporte multiidioma**: Español, Inglés, Portugués y más
- 💾 **Almacenamiento en BD**: Transcripciones guardadas en MySQL/MariaDB
- 📊 **Integración Vicidial**: Scripts AGI listos para usar
- 🔧 **Configuración flexible**: Archivo de configuración centralizado

## Requisitos

### Software Requerido

- Asterisk 13+ o superior
- Python 3.7 o superior
- MySQL/MariaDB 5.7+
- Vicidial (opcional, pero recomendado)

### Dependencias Python

- speechrecognition
- pydub
- google-cloud-speech
- openai-whisper
- pymysql

## Instalación

### 1. Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/sergioloragomez-wq/PiperTTS.git
cd PiperTTS

# Ejecutar instalación (requiere permisos root)
sudo bash install.sh
```

### 2. Instalación Manual

```bash
# Crear directorios
sudo mkdir -p /etc/asterisk/stt
sudo mkdir -p /var/lib/asterisk/agi-bin
sudo mkdir -p /var/log/asterisk

# Copiar archivos de configuración
sudo cp stt_config.conf /etc/asterisk/stt/

# Copiar script AGI
sudo cp asterisk/agi/stt_recognition.py /var/lib/asterisk/agi-bin/
sudo chmod +x /var/lib/asterisk/agi-bin/stt_recognition.py

# Instalar dependencias Python
sudo pip3 install speechrecognition pydub google-cloud-speech openai-whisper pymysql

# Configurar permisos
sudo chown -R asterisk:asterisk /var/lib/asterisk/agi-bin
sudo chown -R asterisk:asterisk /etc/asterisk/stt
```

## Configuración

### 1. Motor STT

Editar `/etc/asterisk/stt/stt_config.conf`:

```ini
[general]
engine=google          # Opciones: google, whisper, sphinx
language=es-ES         # Idioma de reconocimiento
```

### 2. Google Cloud Speech API

Si usa Google Cloud Speech:

```bash
# Descargar credenciales desde Google Cloud Console
# Guardar en /etc/asterisk/google-credentials.json
sudo nano /etc/asterisk/google-credentials.json
```

### 3. OpenAI Whisper

Para usar Whisper localmente:

```ini
[whisper]
model=base             # Opciones: tiny, base, small, medium, large
model_path=/var/lib/asterisk/whisper/models
```

### 4. Base de Datos

Configurar conexión a MySQL:

```ini
[vicidial]
db_host=localhost
db_port=3306
db_name=asterisk
db_user=cron
# ⚠️ IMPORTANTE: Cambie esta contraseña por una segura en producción
db_pass=1234
```

**NOTA DE SEGURIDAD**: La contraseña por defecto (1234) es solo para propósitos de ejemplo. En un entorno de producción, debe usar una contraseña fuerte y segura.

La tabla `stt_transcriptions` se crea automáticamente.

### 5. Dialplan de Asterisk

Agregar a `/etc/asterisk/extensions.conf`:

```asterisk
#include extensions_stt.conf
```

O copiar los ejemplos manualmente desde `asterisk/extensions_stt.conf`.

## Uso

### Ejemplo Básico en Dialplan

```asterisk
exten => 1000,1,Answer()
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},5,30,k)
    same => n,AGI(stt_recognition.py)
    same => n,NoOp(Transcripción: ${STT_RESULT})
    same => n,Hangup()
```

### Variables Disponibles

Después de ejecutar el AGI:

- `${STT_RESULT}` - Texto transcrito
- `${STT_SUCCESS}` - "1" si exitoso, "0" si error

### Integración con Vicidial

1. **Grabación de llamadas entrantes**:
   - Las grabaciones se transcriben automáticamente
   - Se almacenan en la tabla `stt_transcriptions`

2. **Encuestas post-llamada**:
   - Usar contexto `[vicidial-stt-survey]`
   - Cada pregunta se transcribe individualmente

3. **Análisis de sentimiento**:
   - Las transcripciones pueden procesarse posteriormente
   - Integrar con herramientas de análisis

## Pruebas

Ejecutar script de prueba:

```bash
python3 test_stt_config.py
```

Esto verificará:
- ✓ Dependencias Python instaladas
- ✓ Archivos de configuración
- ✓ Permisos y directorios
- ✓ Script AGI instalado

## Estructura del Proyecto

```
PiperTTS/
├── README.md                          # Este archivo
├── DOCUMENTACION.md                   # Documentación detallada
├── stt_config.conf                    # Configuración principal
├── install.sh                         # Script de instalación
├── test_stt_config.py                 # Script de pruebas
└── asterisk/
    ├── agi/
    │   └── stt_recognition.py         # Script AGI principal
    └── extensions_stt.conf            # Ejemplos de dialplan
```

## Solución de Problemas

### Error: "speech_recognition module not installed"

```bash
sudo pip3 install speechrecognition
```

### Error: "Could not understand audio"

- Verificar calidad del audio
- Ajustar `sample_rate` en configuración
- Probar con otro motor STT

### Error de conexión a base de datos

```bash
# Verificar credenciales en stt_config.conf
# Verificar que MySQL esté corriendo
sudo systemctl status mysql
```

### Permisos denegados

```bash
sudo chown -R asterisk:asterisk /var/lib/asterisk/agi-bin
sudo chown -R asterisk:asterisk /etc/asterisk/stt
```

## Motores STT Disponibles

### 1. Google Cloud Speech API
- **Pros**: Muy preciso, múltiples idiomas
- **Contras**: Requiere API key, costo por uso
- **Mejor para**: Producción, alta calidad

### 2. OpenAI Whisper
- **Pros**: Gratuito, funciona offline, muy preciso
- **Contras**: Requiere más recursos, más lento
- **Mejor para**: Procesamiento offline, privacidad

### 3. CMU Sphinx
- **Pros**: Completamente offline, gratuito
- **Contras**: Menor precisión
- **Mejor para**: Desarrollo, pruebas

## Idiomas Soportados

- Español (es-ES, es-MX, es-AR)
- Inglés (en-US, en-GB)
- Portugués (pt-BR, pt-PT)
- Y muchos más según el motor STT

## Rendimiento

### Tiempos de Procesamiento (aproximados)

- Google Cloud: 1-2 segundos
- Whisper (base): 3-5 segundos
- Whisper (large): 10-15 segundos
- Sphinx: 2-3 segundos

### Recursos del Sistema

- RAM mínima: 2GB
- RAM recomendada: 4GB (Whisper large: 8GB)
- CPU: 2+ cores recomendado

## Seguridad

- Mantener credenciales de API seguras
- Usar conexiones encriptadas para API
- Revisar permisos de archivos regularmente
- Considerar cifrado de transcripciones en BD

## Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Cree una rama para su feature
3. Commit sus cambios
4. Push a la rama
5. Abra un Pull Request

## Soporte

Para reportar problemas o solicitar características:
- Abrir un issue en GitHub
- Proporcionar logs relevantes
- Describir pasos para reproducir

## Autor

Sergio Lora Gómez

## Agradecimientos

- Proyecto Asterisk
- Vicidial Community
- OpenAI Whisper
- Google Cloud Speech API
