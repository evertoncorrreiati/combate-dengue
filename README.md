# 🦟 Combate à Dengue — API + Frontend

Sistema web para registro e visualização de focos do mosquito da dengue.

---

## 🛠️ Tecnologias
- **Backend:** Python + Flask + SQLite
- **Frontend:** HTML/CSS/JS puro (sem frameworks)
- **Mapa:** OpenStreetMap via Leaflet.js
- **CEP:** API ViaCEP (gratuita)
- **Deploy:** Render.com (grátis)

---

## 🚀 Rodar LOCALMENTE

### 1. Pré-requisitos
- Python 3.9+ instalado

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Iniciar o servidor
```bash
python app.py
```

### 4. Abrir no navegador
```
http://localhost:5000
```

---

## ☁️ Deploy no Render (nuvem gratuita)

### Passo a passo:

1. **Crie uma conta** em https://render.com

2. **Suba o código no GitHub:**
   ```bash
   git init
   git add .
   git commit -m "primeiro commit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/combate-dengue.git
   git push -u origin main
   ```

3. **No Render:**
   - Clique em **New → Web Service**
   - Conecte seu repositório GitHub
   - Configure:
     - **Runtime:** Python
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
   - Clique em **Deploy**

4. **Pronto!** Seu site estará em:
   ```
   https://combate-dengue.onrender.com
   ```

---

## 📡 Rotas da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET    | `/api/focos` | Lista todos os focos |
| POST   | `/api/focos` | Registra novo foco |
| GET    | `/api/focos/:id` | Busca foco por ID |
| PATCH  | `/api/focos/:id/status` | Atualiza status |
| DELETE | `/api/focos/:id` | Exclui foco |
| GET    | `/api/stats` | Estatísticas gerais |

### Filtros na listagem:
```
GET /api/focos?status=Pendente&busca=rua
```

### Exemplo de POST:
```json
{
  "cep": "19010-080",
  "logradouro": "Rua Sete de Setembro",
  "numero": "200",
  "bairro": "Centro",
  "cidade": "Presidente Prudente",
  "uf": "SP",
  "lat": -22.1207,
  "lng": -51.3882,
  "tipos": ["💧 Água parada", "🗑️ Lixo acumulado"],
  "descricao": "Terreno com poças d'água",
  "nome": "João Silva"
}
```

### Exemplo de PATCH (atualizar status):
```json
{ "status": "Confirmado" }
```

---

## 📁 Estrutura do projeto
```
combate_dengue/
├── app.py              ← API Flask
├── requirements.txt    ← Dependências Python
├── Procfile            ← Para deploy no Render
├── render.yaml         ← Config do Render
├── dengue.db           ← Banco SQLite (criado automaticamente)
├── README.md
└── templates/
    └── index.html      ← Frontend completo
```

---

## ⚠️ Observação sobre dados no Render (plano gratuito)
O plano gratuito do Render usa um sistema de arquivos **efêmero** — o banco SQLite é apagado ao reiniciar.  
Para persistência real, use o **PostgreSQL gratuito do Render** ou o **Railway.app**.
