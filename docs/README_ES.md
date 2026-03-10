# Configuración de STT para Vicidial

Este proyecto proporciona una integración de Speech-to-Text (STT) para Vicidial usando el motor Vosk.

## Características

- ✅ Integración completa con Vicidial a través de scripts AGI
- ✅ Soporte para reconocimiento de voz en español
- ✅ Motor STT Vosk de alto rendimiento
- ✅ Configuración flexible mediante archivo INI
- ✅ Registro detallado de todas las transcripciones
- ✅ Manejo de confianza para validar transcripciones
- ✅ Compatible con Asterisk y Vicidial

## Requisitos del Sistema

- Ubuntu/Debian Linux
- Python 3.6 o superior
- Asterisk 13+ con Vicidial
- Al menos 2GB de RAM
- 1GB de espacio en disco para modelos STT

## Instalación

### Instalación Automática

```bash
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### Instalación Manual

1. **Instalar dependencias del sistema:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv wget unzip sox
```

2. **Crear entorno virtual de Python:**
```bash
python3 -m venv /opt/vicidial-stt-env
source /opt/vicidial-stt-env/bin/activate
```

3. **Instalar dependencias de Python:**
```bash
pip install --upgrade pip
pip install vosk pyst2 configparser
```

4. **Crear directorios necesarios:**
```bash
sudo mkdir -p /var/lib/asterisk/agi-bin
sudo mkdir -p /var/lib/asterisk/models
sudo mkdir -p /var/log/asterisk/stt
sudo mkdir -p /var/spool/asterisk/monitor
```

5. **Descargar modelo de STT en español:**
```bash
cd /var/lib/asterisk/models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip
```

6. **Copiar archivos:**
```bash
sudo cp agi/vicidial_stt.py /var/lib/asterisk/agi-bin/
sudo chmod +x /var/lib/asterisk/agi-bin/vicidial_stt.py
sudo mkdir -p /etc/asterisk/stt
sudo cp config/stt_config.ini /etc/asterisk/stt/
```

7. **Configurar permisos:**
```bash
sudo chown -R asterisk:asterisk /var/lib/asterisk/agi-bin
sudo chown -R asterisk:asterisk /var/log/asterisk/stt
sudo chown -R asterisk:asterisk /var/lib/asterisk/models
```

## Configuración

### Archivo de Configuración

El archivo principal de configuración está en `/etc/asterisk/stt/stt_config.ini`:

```ini
[general]
engine = vosk
model_path = /var/lib/asterisk/models/vosk-model-small-es-0.42
sample_rate = 8000
language = es-ES

[vicidial]
agi_path = /var/lib/asterisk/agi-bin
log_path = /var/log/asterisk/stt
recording_path = /var/spool/asterisk/monitor
enable_logging = true
log_level = INFO

[performance]
threads = 2
buffer_size = 4000
timeout = 30
max_recording_duration = 300

[output]
format = json
confidence_threshold = 0.5
enable_timestamps = true
```

### Integración con Vicidial

#### Opción 1: Añadir al Dialplan de Asterisk

Editar `/etc/asterisk/extensions.conf` o el archivo de extensiones de Vicidial:

```
[vicidial-stt]
exten => _X.,1,Answer()
exten => _X.,n,Wait(1)
exten => _X.,n,AGI(vicidial_stt.py)
exten => _X.,n,NoOp(Estado STT: ${STT_STATUS})
exten => _X.,n,NoOp(Texto: ${STT_TEXT})
exten => _X.,n,NoOp(Confianza: ${STT_CONFIDENCE})
exten => _X.,n,GotoIf($["${STT_STATUS}" = "SUCCESS"]?success:failed)
exten => _X.,n(success),Playback(thank-you-for-calling)
exten => _X.,n,Hangup()
exten => _X.,n(failed),Playback(sorry)
exten => _X.,n,Hangup()
```

#### Opción 2: Usar desde Campaign en Vicidial

1. Acceder al panel de administración de Vicidial
2. Ir a "Admin" > "Campaigns"
3. Seleccionar la campaña deseada
4. En "Campaign Settings", agregar en "AGI Scripts":
   ```
   vicidial_stt.py
   ```

## Uso

### Variables de Asterisk Disponibles

Después de ejecutar el script AGI, las siguientes variables estarán disponibles:

- `${STT_STATUS}` - Estado de la transcripción: SUCCESS, FAILED, LOW_CONFIDENCE, ERROR
- `${STT_TEXT}` - Texto transcrito
- `${STT_CONFIDENCE}` - Nivel de confianza (0.0 - 1.0)
- `${STT_ERROR}` - Mensaje de error (si aplica)

### Ejemplo de Uso en Dialplan

```
exten => s,1,AGI(vicidial_stt.py)
exten => s,n,GotoIf($["${STT_STATUS}" = "SUCCESS"]?process:retry)

exten => s,n(process),NoOp(Procesando: ${STT_TEXT})
exten => s,n,Set(CUSTOMER_RESPONSE=${STT_TEXT})
; Aquí puedes procesar la respuesta del cliente

exten => s,n(retry),NoOp(Error en STT: ${STT_ERROR})
; Manejo de errores
```

## Pruebas

### Ejecutar Tests Automáticos

```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

### Prueba Manual

1. **Habilitar debug de AGI en Asterisk:**
```bash
asterisk -rx 'agi set debug on'
```

2. **Realizar una llamada de prueba a una extensión configurada**

3. **Ver logs:**
```bash
tail -f /var/log/asterisk/stt/vicidial_stt.log
```

## Modelos de Idioma Disponibles

### Español
- **Pequeño** (50MB): `vosk-model-small-es-0.42`
- **Mediano** (1GB): `vosk-model-es-0.42`

### Otros Idiomas

Para usar otros idiomas, descargue el modelo apropiado desde:
https://alphacephei.com/vosk/models

Y actualice `model_path` en la configuración.

## Solución de Problemas

### El script AGI no se ejecuta
- Verificar permisos: `ls -la /var/lib/asterisk/agi-bin/vicidial_stt.py`
- Verificar que el shebang apunta al Python correcto
- Revisar logs de Asterisk: `tail -f /var/log/asterisk/full`

### Errores de importación de módulos
- Verificar que el entorno virtual está activo
- Reinstalar dependencias: `pip install vosk pyst2`

### Baja calidad de transcripción
- Usar un modelo más grande
- Ajustar `confidence_threshold` en la configuración
- Verificar calidad del audio de entrada
- Usar audio con sample rate de 8000 Hz o 16000 Hz

### El modelo no se carga
- Verificar que el path del modelo es correcto en `stt_config.ini`
- Verificar que el modelo está completamente descargado
- Verificar permisos del directorio de modelos

## Logs

Los logs se guardan en:
- Principal: `/var/log/asterisk/stt/vicidial_stt.log`
- Asterisk: `/var/log/asterisk/full`

## Rendimiento

### Recomendaciones para Optimización

1. **Usar modelos pequeños** para sistemas con recursos limitados
2. **Ajustar `buffer_size`** en la configuración según la latencia deseada
3. **Configurar `threads`** según los núcleos de CPU disponibles
4. **Habilitar `keep_recordings=false`** para ahorrar espacio en disco

### Benchmarks Aproximados

- Modelo pequeño: ~0.5x tiempo real (archivo de 10s procesa en 5s)
- Modelo mediano: ~1.0x tiempo real
- Uso de RAM: 200-500MB por proceso

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Soporte

Para problemas o preguntas:
- Abrir un issue en GitHub
- Revisar la documentación de Vosk: https://alphacephei.com/vosk/
- Revisar la documentación de Vicidial: https://vicidial.org/

## Créditos

- Motor STT: [Vosk](https://alphacephei.com/vosk/)
- Telefonía: [Asterisk](https://www.asterisk.org/)
- Call Center: [Vicidial](https://vicidial.org/)
