# Guía de Uso - STT para Vicidial

Esta guía proporciona ejemplos prácticos de cómo usar el sistema STT con Vicidial.

## Escenarios de Uso Comunes

### 1. Transcripción de Llamadas Entrantes

**Objetivo**: Transcribir automáticamente todas las llamadas entrantes.

**Configuración en extensions.conf**:
```asterisk
[incoming-with-stt]
exten => _X.,1,Answer()
    same => n,Set(CALLDATE=${STRFTIME(${EPOCH},,%Y%m%d-%H%M%S)})
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/${CALLDATE}-${CALLERID(num)}-${UNIQUEID}.wav)
    ; Grabar la llamada
    same => n,MixMonitor(${RECORDING_FILE})
    ; Continuar con el flujo normal de Vicidial
    same => n,Goto(vicidial-auto,${EXTEN},1)
    
; Al finalizar la llamada, transcribir
exten => h,1,NoOp(Llamada finalizada, iniciando transcripción)
    same => n,AGI(stt_recognition.py)
    same => n,NoOp(Transcripción: ${STT_RESULT})
```

### 2. Encuesta de Satisfacción Post-Llamada

**Objetivo**: Realizar encuesta con respuestas de voz y transcribirlas.

**Script de ejemplo**:
```asterisk
[post-call-survey]
exten => s,1,Answer()
    same => n,Wait(1)
    same => n,Playback(custom/survey-welcome)
    
    ; Pregunta 1: ¿Cómo calificaría el servicio?
    same => n,Playback(custom/question-service)
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/survey-q1-${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},3,15,k)
    same => n,AGI(stt_recognition.py)
    same => n,Set(SURVEY_Q1=${STT_RESULT})
    same => n,NoOp(Respuesta Q1: ${SURVEY_Q1})
    
    ; Pregunta 2: ¿Recomendaría nuestro servicio?
    same => n,Playback(custom/question-recommend)
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/survey-q2-${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},3,15,k)
    same => n,AGI(stt_recognition.py)
    same => n,Set(SURVEY_Q2=${STT_RESULT})
    same => n,NoOp(Respuesta Q2: ${SURVEY_Q2})
    
    ; Pregunta 3: Comentarios adicionales
    same => n,Playback(custom/question-comments)
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/survey-q3-${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},5,30,k)
    same => n,AGI(stt_recognition.py)
    same => n,Set(SURVEY_Q3=${STT_RESULT})
    same => n,NoOp(Respuesta Q3: ${SURVEY_Q3})
    
    same => n,Playback(custom/survey-thanks)
    same => n,Hangup()
```

### 3. IVR con Reconocimiento de Voz

**Objetivo**: Menú IVR que acepta comandos de voz.

```asterisk
[voice-ivr]
exten => s,1,Answer()
    same => n,Wait(1)
    same => n,Set(ATTEMPTS=0)
    same => n(start),Playback(custom/ivr-menu)
    ; "Diga 'ventas', 'soporte' o 'información'"
    
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/ivr-${UNIQUEID}-${ATTEMPTS}.wav)
    same => n,Record(${RECORDING_FILE},3,10,k)
    same => n,AGI(stt_recognition.py)
    same => n,NoOp(Cliente dijo: ${STT_RESULT})
    
    ; Procesar respuesta
    same => n,Set(LOWER_RESULT=${TOLOWER(${STT_RESULT})})
    same => n,GotoIf($["${LOWER_RESULT}" =~ "venta"]?sales)
    same => n,GotoIf($["${LOWER_RESULT}" =~ "soporte"]?support)
    same => n,GotoIf($["${LOWER_RESULT}" =~ "informacion"]?info)
    same => n,GotoIf($["${LOWER_RESULT}" =~ "información"]?info)
    
    ; No se entendió la opción
    same => n,Set(ATTEMPTS=$[${ATTEMPTS}+1])
    same => n,GotoIf($[${ATTEMPTS} < 3]?retry:operator)
    
    same => n(retry),Playback(custom/ivr-not-understood)
    same => n,Goto(start)
    
    same => n(operator),Playback(custom/transfer-operator)
    same => n,Goto(default,100,1)
    
    same => n(sales),Playback(custom/transferring-sales)
    same => n,Goto(sales-queue,s,1)
    
    same => n(support),Playback(custom/transferring-support)
    same => n,Goto(support-queue,s,1)
    
    same => n(info),Playback(custom/transferring-info)
    same => n,Goto(info-queue,s,1)
```

### 4. Transcripción de Buzón de Voz

**Objetivo**: Convertir mensajes de voz en texto.

```asterisk
[voicemail-transcription]
exten => _*98XX,1,Answer()
    same => n,Set(VMBOX=${EXTEN:3})
    same => n,Wait(1)
    same => n,Playback(vm-intro)
    
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/voicemail/default/${VMBOX}/tmp/${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},5,120,k)
    
    ; Transcribir el mensaje
    same => n,AGI(stt_recognition.py)
    same => n,Set(VM_TRANSCRIPTION=${STT_RESULT})
    
    ; Guardar transcripción en archivo de texto
    same => n,Set(TXT_FILE=/var/spool/asterisk/voicemail/default/${VMBOX}/tmp/${UNIQUEID}.txt)
    same => n,System(echo "${VM_TRANSCRIPTION}" > ${TXT_FILE})
    
    ; Opcional: enviar por email
    same => n,System(/usr/local/bin/send-vm-email.sh ${VMBOX} "${VM_TRANSCRIPTION}")
    
    same => n,Playback(vm-goodbye)
    same => n,Hangup()
```

### 5. Verificación de Datos con Voz

**Objetivo**: Verificar información del cliente mediante comandos de voz.

```asterisk
[voice-verification]
exten => s,1,Answer()
    same => n,Wait(1)
    same => n,Set(VERIFY_ATTEMPTS=0)
    
    same => n(ask_phone),Playback(custom/say-phone-number)
    same => n,Set(RECORDING_FILE=/var/spool/asterisk/monitor/verify-phone-${UNIQUEID}.wav)
    same => n,Record(${RECORDING_FILE},3,15,k)
    same => n,AGI(stt_recognition.py)
    same => n,Set(SPOKEN_PHONE=${STT_RESULT})
    
    ; Remover espacios y caracteres no numéricos
    same => n,Set(SPOKEN_PHONE=${FILTER(0-9,${SPOKEN_PHONE})})
    same => n,NoOp(Teléfono reconocido: ${SPOKEN_PHONE})
    
    ; Comparar con base de datos
    same => n,Set(DB_PHONE=${ODBC_CUSTOMER_PHONE(${CALLERID(num)})})
    same => n,GotoIf($["${SPOKEN_PHONE}" = "${DB_PHONE}"]?verified:retry)
    
    same => n(retry),Set(VERIFY_ATTEMPTS=$[${VERIFY_ATTEMPTS}+1])
    same => n,GotoIf($[${VERIFY_ATTEMPTS} < 3]?ask_phone:failed)
    
    same => n(failed),Playback(custom/verification-failed)
    same => n,Goto(security-queue,s,1)
    
    same => n(verified),Playback(custom/verification-success)
    same => n,Goto(main-menu,s,1)
```

## Consultas a la Base de Datos

### Consultar Transcripciones

```sql
-- Obtener todas las transcripciones de hoy
SELECT 
    call_id,
    audio_file,
    transcription,
    created_at
FROM stt_transcriptions
WHERE DATE(created_at) = CURDATE()
ORDER BY created_at DESC;

-- Buscar por palabras clave
SELECT 
    call_id,
    transcription,
    created_at
FROM stt_transcriptions
WHERE transcription LIKE '%queja%'
   OR transcription LIKE '%problema%'
   OR transcription LIKE '%insatisfecho%'
ORDER BY created_at DESC;

-- Estadísticas de transcripciones por día
SELECT 
    DATE(created_at) as fecha,
    COUNT(*) as total_transcripciones,
    COUNT(DISTINCT call_id) as llamadas_unicas
FROM stt_transcriptions
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY fecha DESC;

-- Análisis de sentimiento simple (palabras positivas/negativas)
SELECT 
    call_id,
    transcription,
    CASE 
        WHEN transcription REGEXP 'excelente|gracias|bueno|satisfecho|contento'
        THEN 'Positivo'
        WHEN transcription REGEXP 'malo|problema|queja|insatisfecho|molesto'
        THEN 'Negativo'
        ELSE 'Neutral'
    END as sentimiento
FROM stt_transcriptions
WHERE DATE(created_at) = CURDATE();
```

## Scripts de Utilidad

### Script para Procesamiento Batch

```bash
#!/bin/bash
# batch_transcribe.sh - Transcribir múltiples archivos de audio

AUDIO_DIR="/var/spool/asterisk/monitor"
LOG_FILE="/var/log/asterisk/batch_transcribe.log"

echo "Iniciando transcripción batch: $(date)" >> $LOG_FILE

# Procesar archivos .wav no transcritos
find $AUDIO_DIR -name "*.wav" -mtime -1 | while read audio_file; do
    # Verificar si ya fue transcrito
    if [ ! -f "${audio_file}.txt" ]; then
        echo "Procesando: $audio_file" >> $LOG_FILE
        
        # Ejecutar transcripción (adaptado para standalone)
        python3 /var/lib/asterisk/agi-bin/batch_stt.py "$audio_file"
        
        if [ $? -eq 0 ]; then
            echo "  ✓ Completado" >> $LOG_FILE
        else
            echo "  ✗ Error" >> $LOG_FILE
        fi
    fi
done

echo "Transcripción batch finalizada: $(date)" >> $LOG_FILE
```

### Monitoreo de Calidad

```bash
#!/bin/bash
# monitor_stt_quality.sh - Monitorear calidad de transcripciones

MYSQL_CMD="mysql -u cron -p1234 asterisk"

# Obtener estadísticas del día
echo "=== Estadísticas STT - $(date +%Y-%m-%d) ==="

TOTAL=$($MYSQL_CMD -sN -e "SELECT COUNT(*) FROM stt_transcriptions WHERE DATE(created_at) = CURDATE()")
echo "Total transcripciones: $TOTAL"

ERRORS=$($MYSQL_CMD -sN -e "SELECT COUNT(*) FROM stt_transcriptions WHERE DATE(created_at) = CURDATE() AND transcription LIKE '%error%'")
echo "Errores: $ERRORS"

if [ $TOTAL -gt 0 ]; then
    ERROR_RATE=$(echo "scale=2; $ERRORS * 100 / $TOTAL" | bc)
    echo "Tasa de error: ${ERROR_RATE}%"
    
    # Alertar si tasa de error es alta
    if (( $(echo "$ERROR_RATE > 10" | bc -l) )); then
        echo "⚠️  ALERTA: Tasa de error superior al 10%"
        # Enviar notificación
        # mail -s "STT Error Alert" admin@example.com <<< "Error rate: ${ERROR_RATE}%"
    fi
fi
```

## Mejores Prácticas

1. **Calidad de Audio**
   - Usar sample rate de 8000 Hz para telefonía
   - Formato mono (1 canal)
   - Codec: PCM/WAV para mejor calidad

2. **Rendimiento**
   - Procesar transcripciones en batch durante horas de bajo tráfico
   - Usar Whisper "tiny" o "base" para respuesta en tiempo real
   - Usar Google Cloud para mejor precisión en producción

3. **Seguridad**
   - Encriptar transcripciones sensibles en la base de datos
   - Usar políticas de retención de datos
   - Limitar acceso a credenciales de API

4. **Mantenimiento**
   - Limpiar archivos de audio antiguos regularmente
   - Monitorear uso de espacio en disco
   - Revisar logs de errores diariamente

5. **Testing**
   - Probar con diferentes acentos y dialectos
   - Validar con muestras de audio reales
   - Comparar precisión entre diferentes motores

## Solución de Problemas Comunes

### Problema: Baja precisión en el reconocimiento

**Soluciones**:
- Verificar calidad de audio
- Ajustar sample_rate en configuración
- Cambiar a un motor más preciso (Google Cloud)
- Entrenar modelos personalizados para terminología específica

### Problema: Transcripciones lentas

**Soluciones**:
- Usar modelo Whisper más pequeño (tiny/base)
- Procesar en batch en lugar de tiempo real
- Aumentar recursos del servidor
- Usar caché para frases comunes

### Problema: Caracteres especiales o acentos incorrectos

**Soluciones**:
- Verificar configuración de idioma (es-ES vs es-MX)
- Usar UTF-8 en base de datos
- Ajustar post-procesamiento de texto

## Recursos Adicionales

- [Documentación Asterisk](https://wiki.asterisk.org)
- [Vicidial Wiki](http://www.vicidial.org/docs)
- [Google Cloud Speech API](https://cloud.google.com/speech-to-text/docs)
- [OpenAI Whisper](https://github.com/openai/whisper)
