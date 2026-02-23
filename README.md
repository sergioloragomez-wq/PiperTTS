# PiperTTS - Configuración STT para Vicidial

Sistema de Speech-to-Text (STT) para integración con Vicidial/Asterisk.

## 🚀 Inicio Rápido

```bash
# Instalar
sudo bash install.sh

# Configurar
sudo nano /etc/asterisk/stt/stt_config.conf

# Probar
python3 test_stt_config.py
```

## 📋 Características

- ✅ Múltiples motores STT (Google, Whisper, Sphinx)
- ✅ Soporte para español y múltiples idiomas
- ✅ Integración con Vicidial/Asterisk
- ✅ Almacenamiento de transcripciones en MySQL
- ✅ Scripts AGI listos para usar

## 📚 Documentación

Ver [DOCUMENTACION.md](DOCUMENTACION.md) para instrucciones completas.

## 🔧 Requisitos

- Asterisk 13+
- Python 3.7+
- MySQL/MariaDB 5.7+

## 📞 Uso Básico

```asterisk
exten => 1000,1,Answer()
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},5,30,k)
    same => n,AGI(stt_recognition.py)
    same => n,NoOp(Resultado: ${STT_RESULT})
    same => n,Hangup()
```

## 📄 Licencia

MIT License
