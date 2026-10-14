#!/bin/bash

# --- CONFIGURAZIONE PERCORSI E VARIABILI ---
LOCAL_DIR="/Users/edo/Desktop/magistrale/Reti/Codice"
REMOTE_USER="edoardo.distasio"
REMOTE_HOST="login.hpc.unipr.it"
REMOTE_BASE="/hpc/home/edoardo.distasio/magistrale/Reti"
REMOTE_CODICE_DIR="$REMOTE_BASE/Codice"
REMOTE_PYTHON_SCRIPT="$REMOTE_CODICE_DIR/karate.py"

echo "=== 1. INIZIO SINCRONIZZAZIONE VERSO L'HPC ==="

# Invio della sola cartella Codice all'HPC
COPYFILE_DISABLE=1 tar czf - --exclude='.DS_Store' -C "$(dirname "$LOCAL_DIR")" "$(basename "$LOCAL_DIR")" 2>/dev/null | \
    ssh -o LogLevel=ERROR "${REMOTE_USER}@${REMOTE_HOST}" "mkdir -p '$REMOTE_BASE' && tar xzf - -C '$REMOTE_BASE'"

if [ $? -eq 0 ]; then
    echo "✓ Invio completato con successo."
else
    echo "❌ Errore durante l'invio dei file all'HPC."
    exit 1
fi

echo ""
echo "=== 2. ESECUZIONE SCRIPT PYTHON REMOTO ==="
echo "Avvio di karate.py sull'HPC..."

# Esecuzione dello script Python direttamente nella cartella Codice remota
ssh -o LogLevel=ERROR "${REMOTE_USER}@${REMOTE_HOST}" "cd '$REMOTE_CODICE_DIR' && python3 karate.py"

if [ $? -eq 0 ]; then
    echo "✓ Script Python eseguito con successo sull'HPC."
else
    echo "❌ Errore durante l'esecuzione dello script Python."
    exit 1
fi

echo ""
echo "=== 3. SCARICAMENTO FILE AGGIORNATI DALL'HPC ==="
echo "Ricezione dei file modificati dall'HPC..."

# Download della sola cartella Codice aggiornata verso il Mac
ssh -o LogLevel=ERROR "${REMOTE_USER}@${REMOTE_HOST}" "tar czf - -C '$REMOTE_BASE' Codice" 2>/dev/null | \
    tar xzf - -C "$(dirname "$LOCAL_DIR")" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Sincronizzazione di ritorno completata con successo!"
    echo "Tutti i file sono stati aggiornati in: $LOCAL_DIR"
else
    echo "❌ Errore durante il download dei file aggiornati."
    exit 1
fi

echo ""
echo "✨ Processo completato con successo!"