# Quick Start Guide - STT para Vicidial

## Instalación en 3 Pasos

### 1. Clonar el Repositorio
```bash
git clone https://github.com/sergioloragomez-wq/PiperTTS.git
cd PiperTTS
```

### 2. Instalar (requiere root)
```bash
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### 3. Configurar Dialplan de Asterisk

Editar `/etc/asterisk/extensions.conf` y añadir:

```ini
[my-stt-context]
exten => _X.,1,Answer()
exten => _X.,n,AGI(vicidial_stt.py)
exten => _X.,n,NoOp(Texto: ${STT_TEXT})
exten => _X.,n,NoOp(Confianza: ${STT_CONFIDENCE})
exten => _X.,n,Hangup()
```

## Verificar Instalación

```bash
# Verificar archivos
./scripts/test.sh

# Verificar configuración
python3 scripts/test_config.py

# Ver logs en tiempo real
tail -f /var/log/asterisk/stt/vicidial_stt.log
```

## Variables Disponibles

Después de ejecutar el script AGI, estas variables estarán disponibles en Asterisk:

- `${STT_STATUS}` → SUCCESS, FAILED, LOW_CONFIDENCE, ERROR
- `${STT_TEXT}` → Texto transcrito
- `${STT_CONFIDENCE}` → Nivel de confianza (0.0 - 1.0)
- `${STT_ERROR}` → Mensaje de error (si hay)

## Configuración

Archivo principal: `/etc/asterisk/stt/stt_config.ini`

```ini
[general]
engine = vosk
model_path = /var/lib/asterisk/models/vosk-model-small-es-0.42
language = es-ES

[output]
confidence_threshold = 0.5  # Ajustar según necesidad
```

## Ejemplos de Uso

Ver archivo `examples/extensions.conf` para:
- IVR con reconocimiento de voz
- Encuestas automatizadas
- Enrutamiento por voz

## Solución de Problemas

### El script no se ejecuta
```bash
# Verificar permisos
ls -la /var/lib/asterisk/agi-bin/vicidial_stt.py

# Verificar logs
tail -f /var/log/asterisk/full
```

### Baja calidad de transcripción
- Ajustar `confidence_threshold` en `/etc/asterisk/stt/stt_config.ini`
- Usar modelo más grande (ver documentación completa)
- Verificar calidad del audio

## Documentación Completa

- **Español**: `docs/README_ES.md`
- **English**: `docs/README_EN.md`

## Soporte

- GitHub Issues: https://github.com/sergioloragomez-wq/PiperTTS/issues
- Documentación Vosk: https://alphacephei.com/vosk/
- Documentación Vicidial: https://vicidial.org/

---

**Versión**: 1.0.0  
**Licencia**: MIT  
**Idioma**: Español (configurable)
