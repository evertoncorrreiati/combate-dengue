from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3, os, json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

DB = 'dengue.db'

# ── Banco de dados ────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS focos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            cep         TEXT,
            logradouro  TEXT NOT NULL,
            numero      TEXT,
            complemento TEXT,
            bairro      TEXT,
            cidade      TEXT NOT NULL,
            uf          TEXT,
            lat         REAL,
            lng         REAL,
            tipos       TEXT NOT NULL,
            descricao   TEXT,
            nome        TEXT,
            telefone    TEXT,
            status      TEXT DEFAULT 'Pendente',
            criado_em   TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')
    conn.commit()
    conn.close()

# ── Servir o frontend ─────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# ── ROTAS DA API ──────────────────────────────────────────────

# Listar todos os focos
@app.route('/api/focos', methods=['GET'])
def listar_focos():
    status = request.args.get('status')
    busca  = request.args.get('busca', '')
    conn = get_db()
    query = 'SELECT * FROM focos WHERE 1=1'
    params = []
    if status:
        query += ' AND status = ?'
        params.append(status)
    if busca:
        query += ' AND (logradouro LIKE ? OR bairro LIKE ? OR cidade LIKE ? OR tipos LIKE ?)'
        params += [f'%{busca}%'] * 4
    query += ' ORDER BY id DESC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d['tipos'] = json.loads(d['tipos'])
        result.append(d)
    return jsonify(result)

# Criar foco
@app.route('/api/focos', methods=['POST'])
def criar_foco():
    data = request.get_json()
    required = ['logradouro', 'cidade', 'tipos']
    for f in required:
        if not data.get(f):
            return jsonify({'erro': f'Campo obrigatório: {f}'}), 400
    conn = get_db()
    cur = conn.execute('''
        INSERT INTO focos (cep,logradouro,numero,complemento,bairro,cidade,uf,lat,lng,tipos,descricao,nome,telefone)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        data.get('cep',''),
        data['logradouro'],
        data.get('numero',''),
        data.get('complemento',''),
        data.get('bairro',''),
        data['cidade'],
        data.get('uf',''),
        data.get('lat'),
        data.get('lng'),
        json.dumps(data['tipos'], ensure_ascii=False),
        data.get('descricao',''),
        data.get('nome',''),
        data.get('telefone',''),
    ))
    conn.commit()
    novo_id = cur.lastrowid
    conn.close()
    return jsonify({'mensagem': 'Foco registrado com sucesso!', 'id': novo_id}), 201

# Buscar foco por ID
@app.route('/api/focos/<int:foco_id>', methods=['GET'])
def buscar_foco(foco_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM focos WHERE id = ?', (foco_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'erro': 'Foco não encontrado'}), 404
    d = dict(row)
    d['tipos'] = json.loads(d['tipos'])
    return jsonify(d)

# Atualizar status
@app.route('/api/focos/<int:foco_id>/status', methods=['PATCH'])
def atualizar_status(foco_id):
    data   = request.get_json()
    novo   = data.get('status')
    validos = ['Pendente', 'Confirmado', 'Resolvido']
    if novo not in validos:
        return jsonify({'erro': f'Status inválido. Use: {validos}'}), 400
    conn = get_db()
    conn.execute('UPDATE focos SET status = ? WHERE id = ?', (novo, foco_id))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': f'Status atualizado para {novo}'})

# Deletar foco
@app.route('/api/focos/<int:foco_id>', methods=['DELETE'])
def deletar_foco(foco_id):
    conn = get_db()
    row = conn.execute('SELECT id FROM focos WHERE id = ?', (foco_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({'erro': 'Foco não encontrado'}), 404
    conn.execute('DELETE FROM focos WHERE id = ?', (foco_id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Foco excluído com sucesso'})

# Estatísticas para o dashboard
@app.route('/api/stats', methods=['GET'])
def stats():
    conn = get_db()
    total      = conn.execute('SELECT COUNT(*) FROM focos').fetchone()[0]
    pendentes  = conn.execute("SELECT COUNT(*) FROM focos WHERE status='Pendente'").fetchone()[0]
    confirmados= conn.execute("SELECT COUNT(*) FROM focos WHERE status='Confirmado'").fetchone()[0]
    resolvidos = conn.execute("SELECT COUNT(*) FROM focos WHERE status='Resolvido'").fetchone()[0]
    conn.close()
    return jsonify({'total': total, 'pendentes': pendentes,
                    'confirmados': confirmados, 'resolvidos': resolvidos})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
