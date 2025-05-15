#!/bin/bash
cd desktop/

source venv/bin/activate

python3 braco_robotico.py

# Mantém o terminal aberto após a execução
echo ""
read -p "Pressione Enter para sair..."
