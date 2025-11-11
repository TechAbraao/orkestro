#!/bin/bash

LOGS_DIR="../source/logs"
echo "Deseja realmente apagar TODOS os arquivos .log da pasta '$LOGS_DIR'? (Y/N)"
read op

if [ "$op" = "Y" ]; then
  echo "Apagando todos os logs..."
  find "$LOGS_DIR" -maxdepth 1 -type f -name "*.log" -exec rm {} \;
  echo "Logs apagados com sucesso."
else
  echo "Nenhum log foi apagado."
fi