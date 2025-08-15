# Deploy no Render (passo a passo rápido)

## Opção A — simples (sem disco persistente)
1) Faça push deste projeto para um repositório no GitHub/GitLab/Bitbucket.
2) No Render: New ➜ Web Service ➜ conecte o repo.
3) Render detecta Python automaticamente. Confirme:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
4) Adicione variáveis de ambiente:
   - `RENDER=true`
   - `SECRET_KEY` (opcional; se não definir, o render.yaml gera uma automaticamente)
5) Deploy.

## Opção B — com persistência de dados (SQLite não some a cada deploy)
1) Em vez de `render.yaml`, use `render-with-disk.yaml` (renomeie para `render.yaml` antes do push se preferir).
2) O serviço criará um disco e montará em `/var/data`. O app usará `/var/data/unica` via `DATA_DIR`.
3) O resto é igual à opção A.

## Acesso local
- `pip install -r requirements.txt`
- `python app.py` (usa Flask dev server). Para tunel (opcional) instale `pyngrok` e não defina `RENDER`.
