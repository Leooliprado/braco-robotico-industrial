#!/bin/bash
cd desktop/

source venv/bin/activate

python3 rum_app.py

# Mantém o terminal aberto após a execução
echo ""
read -p "Pressione Enter para sair..."
