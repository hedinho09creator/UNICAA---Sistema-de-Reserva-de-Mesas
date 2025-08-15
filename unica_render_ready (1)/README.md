# UNICAA - Sistema de Reserva de Mesas

Este sistema permite reservar mesas em salas específicas.  
Compatível com execução **local** (com Pyngrok) e no **Render** (sem Pyngrok).

## Executar Localmente
```bash
pip install -r requirements.txt
python app.py
```

## Executar no Render
- Faça o deploy do repositório no Render como **Web Service**.
- Configure a variável de ambiente `RENDER=true`.
- Adicione `SECRET_KEY` se quiser definir manualmente.

## Estrutura
- `app.py` → Código principal
- `qrcode_registros/` → Banco de dados SQLite
- `static/unica_logo.png` → Logo do sistema
