# PiperTTS - Configuración STT para Vicidial

Sistema de Speech-to-Text (STT) para integración con Vicidial.

## 📋 Descripción

Este proyecto proporciona una solución completa de reconocimiento de voz (Speech-to-Text) integrado con Vicidial, utilizando el motor Vosk para transcripciones en español de alta calidad.

## 🚀 Características Principales

- ✅ Integración completa con Vicidial mediante scripts AGI de Asterisk
- ✅ Reconocimiento de voz en español usando Vosk
- ✅ Configuración flexible mediante archivos INI
- ✅ Sistema de logging completo
- ✅ Manejo de niveles de confianza
- ✅ Scripts de instalación automatizados
- ✅ Ejemplos de uso listos para producción

## 📚 Documentación

- [Documentación en Español](docs/README_ES.md) - Guía completa en español
- [English Documentation](docs/README_EN.md) - Complete guide in English

## ⚡ Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/sergioloragomez-wq/PiperTTS.git
cd PiperTTS

# Ejecutar instalación automática
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### Uso Básico

1. Configurar en el dialplan de Asterisk:
```
exten => _X.,1,AGI(vicidial_stt.py)
exten => _X.,n,NoOp(Texto: ${STT_TEXT})
```

2. Ver resultados en logs:
```bash
tail -f /var/log/asterisk/stt/vicidial_stt.log
```

## 📁 Estructura del Proyecto

```
PiperTTS/
├── agi/                    # Scripts AGI para Asterisk
│   └── vicidial_stt.py    # Script principal de STT
├── config/                 # Archivos de configuración
│   └── stt_config.ini     # Configuración principal
├── scripts/               # Scripts de instalación y pruebas
│   ├── install.sh        # Instalador automático
│   └── test.sh          # Script de pruebas
├── docs/                 # Documentación
│   ├── README_ES.md     # Documentación en español
│   └── README_EN.md     # Documentación en inglés
├── examples/            # Ejemplos de uso
│   └── extensions.conf # Ejemplos de dialplan
└── requirements.txt    # Dependencias de Python
```

## 🔧 Requisitos

- Ubuntu/Debian Linux
- Python 3.6+
- Asterisk 13+ con Vicidial
- 2GB RAM mínimo
- 1GB espacio en disco

## 🧪 Pruebas

```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

## 📖 Ejemplos

El directorio `examples/` contiene configuraciones de ejemplo para:
- IVR con reconocimiento de voz
- Encuestas automatizadas
- Enrutamiento de llamadas por voz

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🙏 Créditos

- [Vosk](https://alphacephei.com/vosk/) - Motor STT
- [Asterisk](https://www.asterisk.org/) - Sistema de telefonía
- [Vicidial](https://vicidial.org/) - Software de call center

## 📞 Soporte

Para preguntas o problemas, por favor abre un issue en GitHub.
