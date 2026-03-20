import sqlite3
import json
from functools import wraps
from flask import Flask, render_template, request, jsonify, url_for, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import ipaddress
import random
import math

app = Flask(__name__)

# =================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS E SEGURANÇA
# =================================================================
app.secret_key = 'telecom_pro_secreto_2026'

def init_db():
    conn = sqlite3.connect('telecom.db')
    c = conn.cursor()
    # Tabela de Usuários
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    
    # NOVA: Tabela de Projetos do CAD
    c.execute('''CREATE TABLE IF NOT EXISTS projetos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, nome TEXT, dados TEXT)''')
    
    # Cria o usuário padrão
    c.execute("SELECT * FROM usuarios WHERE username='admin'")
    if not c.fetchone():
        senha_criptografada = generate_password_hash('123')
        c.execute("INSERT INTO usuarios (username, password) VALUES ('admin', ?)", (senha_criptografada,))
    
    conn.commit()
    conn.close()

init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logado' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# =================================================================
# API DE SALVAMENTO DE PROJETOS (BANCO DE DADOS)
# =================================================================
@app.route('/api/projetos', methods=['GET'])
@login_required
def listar_projetos():
    conn = sqlite3.connect('telecom.db')
    c = conn.cursor()
    c.execute("SELECT nome FROM projetos WHERE username=?", (session['usuario'],))
    projetos = [{'nome': row[0]} for row in c.fetchall()]
    conn.close()
    return jsonify(projetos)

@app.route('/api/projetos/salvar', methods=['POST'])
@login_required
def salvar_projeto():
    dados = request.json
    nome = dados.get('nome')
    conteudo = json.dumps(dados.get('dados'))
    usuario = session['usuario']

    conn = sqlite3.connect('telecom.db')
    c = conn.cursor()
    c.execute("SELECT id FROM projetos WHERE username=? AND nome=?", (usuario, nome))
    if c.fetchone():
        c.execute("UPDATE projetos SET dados=? WHERE username=? AND nome=?", (conteudo, usuario, nome))
    else:
        c.execute("INSERT INTO projetos (username, nome, dados) VALUES (?, ?, ?)", (usuario, nome, conteudo))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

@app.route('/api/projetos/<nome>', methods=['GET'])
@login_required
def carregar_projeto(nome):
    conn = sqlite3.connect('telecom.db')
    c = conn.cursor()
    c.execute("SELECT dados FROM projetos WHERE username=? AND nome=?", (session['usuario'], nome))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(json.loads(row[0]))
    return jsonify({'erro': 'Projeto não encontrado'}), 404

@app.route('/api/projetos/<nome>', methods=['DELETE'])
@login_required
def deletar_projeto(nome):
    conn = sqlite3.connect('telecom.db')
    c = conn.cursor()
    c.execute("DELETE FROM projetos WHERE username=? AND nome=?", (session['usuario'], nome))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

# =================================================================
# BANCO DE QUESTÕES
# =================================================================
QUIZ_FTTH = {
    "q1": {"pergunta": "Qual é a cor OBRIGATÓRIA do conector em redes GPON?", "opcoes": {"A": "Azul (UPC)", "B": "Verde (APC)", "C": "Preto (PC)"}, "resposta": "B", "modulo": "FTTH"},
    "q2": {"pergunta": "Qual a faixa de sinal RX Ideal na ONU?", "opcoes": {"A": "+3 a +7 dBm", "B": "-15 a -25 dBm", "C": "-30 a -40 dBm"}, "resposta": "B", "modulo": "FTTH"},
    "q3": {"pergunta": "O que o protocolo TDMA faz na OLT?", "opcoes": {"A": "Controla a velocidade do cliente", "B": "Gerencia o tempo de envio das ONUs", "C": "Converte a luz em elétrico"}, "resposta": "B", "modulo": "FTTH"},
    "q4": {"pergunta": "Qual é o principal uso da fibra G.657A?", "opcoes": {"A": "Cabos tronco longos", "B": "Cabos Drop (baixo raio de curvatura)", "C": "Links de 10Gbps"}, "resposta": "B", "modulo": "FTTH"},
    "q5": {"pergunta": "Qual componente passivo tem a maior perda típica (atenuação) na rede FTTH?", "opcoes": {"A": "Fusão (0.05 dB)", "B": "Conector (0.5 dB)", "C": "Splitter (10.5 dB+)"}, "resposta": "C", "modulo": "FTTH"},
}

QUIZ_IP = {
    "q1": {"pergunta": "Qual protocolo é RÁPIDO, não garante entrega, e é usado para Jogos/VoIP?", "opcoes": {"A": "TCP", "B": "HTTP", "C": "UDP"}, "resposta": "C", "modulo": "IP"},
    "q2": {"pergunta": "Em uma rede /24, qual é o endereço de Broadcast?", "opcoes": {"A": "O primeiro IP", "B": "O último IP (ex: .255)", "C": "O IP do gateway"}, "resposta": "B", "modulo": "IP"},
    "q3": {"pergunta": "Qual camada do Modelo OSI é responsável pelo Endereçamento IP?", "opcoes": {"A": "Camada 2 (Enlace)", "B": "Camada 3 (Rede)", "C": "Camada 4 (Transporte)"}, "resposta": "B", "modulo": "IP"},
    "q4": {"pergunta": "Qual é o objetivo principal do PPPoE em um provedor?", "opcoes": {"A": "Garantir a qualidade de serviço (QoS)", "B": "Exigir autenticação (Login/Senha)", "C": "Apenas entregar IP automaticamente"}, "resposta": "B", "modulo": "IP"},
    "q5": {"pergunta": "O que o DNS faz?", "opcoes": {"A": "Muda o endereço MAC", "B": "Entrega IP automaticamente", "C": "Traduz domínio (nome) para IP"}, "resposta": "C", "modulo": "IP"},
}

QUIZ_RADIO = {
    "q1": {"pergunta": "Qual a porcentagem mínima da Zona de Fresnel que deve estar livre de obstáculos?", "opcoes": {"A": "50%", "B": "60%", "C": "80%"}, "resposta": "B", "modulo": "Rádio"},
    "q2": {"pergunta": "Qual frequência é preferida para Backhaul PTP em áreas rurais de longa distância?", "opcoes": {"A": "60 GHz", "B": "5.8 GHz", "C": "2.4 GHz"}, "resposta": "B", "modulo": "Rádio"},
    "q3": {"pergunta": "O que indica um alto valor de SNR (Sinal-Ruído) no enlace?", "opcoes": {"A": "Mais interferência", "B": "Sinal fraco", "C": "Maior capacidade de Modulação (Mbps)"}, "resposta": "C", "modulo": "Rádio"},
    "q4": {"pergunta": "Qual tipo de antena é usada em Torres para atender MÚLTIPLOS clientes (PTMP)?", "opcoes": {"A": "Dish (Parabólica)", "B": "Omni", "C": "Setorial (Painel)"}, "resposta": "C", "modulo": "Rádio"},
    "q5": {"pergunta": "Um cabo de rede de torre deve ser BLINDADO (STP/FTP) para proteger contra:", "opcoes": {"A": "Perda de atenuação", "B": "ESD (Descarga Eletrostática) e raios", "C": "Dobra e quebra"}, "resposta": "B", "modulo": "Rádio"},
}

QUIZ_ATENDIMENTO = {
    "q1": {"pergunta": "Qual é a primeira pergunta obrigatória na triagem de um cliente sem conexão (sinal vermelho/piscando)?", "opcoes": {"A": "Qual é a sua senha do Wi-Fi?", "B": "Qual a cor da luz LOS na ONU?", "C": "O senhor pagou a fatura?"}, "resposta": "B", "modulo": "Atendimento"},
    "q2": {"pergunta": "O que acontece se o cliente apertar o botão 'Reset' do roteador achando que vai reiniciar o aparelho?", "opcoes": {"A": "A internet fica mais rápida", "B": "Limpa o histórico de navegação", "C": "Apaga as configurações de PPPoE, exigindo visita técnica ou acesso remoto"}, "resposta": "C", "modulo": "Atendimento"},
    "q3": {"pergunta": "Se um cliente reclama que o plano de 500 Mega está batendo apenas 45 Mbps no celular pelo Wi-Fi, o diagnóstico imediato é:", "opcoes": {"A": "O teste está sendo feito na rede 2.4GHz", "B": "A fibra está dobrada na rua", "C": "O roteador está queimado"}, "resposta": "A", "modulo": "Atendimento"},
    "q4": {"pergunta": "O que a sigla MTTR mede em um provedor?", "opcoes": {"A": "O limite de banda", "B": "Tempo Médio de Reparo (rapidez da equipe de campo)", "C": "Tempo de instalação de um novo cliente"}, "resposta": "B", "modulo": "Atendimento"},
    "q5": {"pergunta": "Qual a melhor abordagem ao atender um cliente irritado com lentidão?", "opcoes": {"A": "Dizer que no sistema está tudo normal", "B": "Exigir que ele fale baixo", "C": "Demonstrar empatia ativa e verificar o status da porta PON e roteador em conjunto"}, "resposta": "C", "modulo": "Atendimento"},
}

QUIZ_VENDAS = {
    "q1": {"pergunta": "O que significa 'Churn' em Telecom?", "opcoes": {"A": "Taxa de cancelamento e perda de clientes", "B": "Sinal óptico fora do padrão", "C": "Acréscimo de velocidade"}, "resposta": "A", "modulo": "Vendas"},
    "q2": {"pergunta": "Na metodologia de Vendas PAP (Porta a Porta), o que é o 'Gatilho da Dor'?", "opcoes": {"A": "Oferecer 3 meses grátis logo na abordagem", "B": "Focar nas frustrações atuais do cliente (ex: Netflix travando à noite)", "C": "Falar as especificações da ONU"}, "resposta": "B", "modulo": "Vendas"},
    "q3": {"pergunta": "O que é 'Up-Sell' na base de assinantes?", "opcoes": {"A": "Vender o provedor para um concorrente", "B": "Entrar em contato com um cliente ativo e vender um plano de maior velocidade", "C": "Vender roteador usado"}, "resposta": "B", "modulo": "Vendas"},
    "q4": {"pergunta": "Por que o Churn precoce (cancelamento em menos de 6 meses) gera grande prejuízo?", "opcoes": {"A": "Porque o Custo de Aquisição do Cliente (CAC - ONU, Drop, Mão de Obra) ainda não se pagou", "B": "Porque a Anatel aplica multas", "C": "Porque o roteador estraga ao ser recolhido"}, "resposta": "A", "modulo": "Vendas"},
    "q5": {"pergunta": "O que é o Ticket Médio (ARPU)?", "opcoes": {"A": "A média de clientes que ligam no suporte", "B": "A Receita Média Gerada por cada Usuário no mês", "C": "O valor da multa de fidelidade"}, "resposta": "B", "modulo": "Vendas"},
}

QUIZ_GESTAO = {
    "q1": {"pergunta": "A partir de qual altura a norma NR35 exige o uso de EPI e ancoragem com Fator de Queda correto?", "opcoes": {"A": "1,5 metros", "B": "2,0 metros", "C": "4,0 metros"}, "resposta": "B", "modulo": "Normas"},
    "q2": {"pergunta": "Por que o uso de escadas de alumínio é estritamente PROIBIDO para técnicos de Telecom?", "opcoes": {"A": "Porque é pesada", "B": "Porque amassa fácil", "C": "Porque conduz eletricidade e gera risco de arco elétrico/choque (NR10)"}, "resposta": "C", "modulo": "Normas"},
    "q3": {"pergunta": "Segundo a norma conjunta ANATEL/ANEEL, qual a distância mínima da rede de telecom para a rede de Baixa Tensão?", "opcoes": {"A": "Nenhuma", "B": "50 cm a 60 cm", "C": "2 metros"}, "resposta": "B", "modulo": "Normas"},
    "q4": {"pergunta": "Como deve ser feita a ancoragem do Talabarte no poste para evitar ferimentos graves em caso de queda?", "opcoes": {"A": "Amarrar na escada", "B": "Ancorar no próprio poste e acima da cabeça (reduzindo impacto e impacto pendular)", "C": "Amarrar no mensageiro do cabo drop"}, "resposta": "B", "modulo": "Normas"},
    "q5": {"pergunta": "O que acontece se as 'raquetes' de fibra (reserva técnica) ficarem espalhadas e despencando pelo poste?", "opcoes": {"A": "Nada, é permitido", "B": "Aumenta o sinal", "C": "A Concessionária de Energia aplica multas severas e pode cortar o cabo"}, "resposta": "C", "modulo": "Normas"},
}

BANCO_MESTRE = {
    "ftth": QUIZ_FTTH,
    "ip": QUIZ_IP,
    "radio": QUIZ_RADIO,
    "atendimento": QUIZ_ATENDIMENTO,
    "vendas": QUIZ_VENDAS,
    "gestao": QUIZ_GESTAO
}

# =================================================================
# ROTAS DE AUTENTICAÇÃO E PERFIL
# =================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        
        conn = sqlite3.connect('telecom.db')
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE username=?", (usuario,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], senha):
            session['logado'] = True
            session['usuario'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        novo_usuario = request.form['novo_usuario']
        nova_senha = request.form['nova_senha']
        
        conn = sqlite3.connect('telecom.db')
        c = conn.cursor()
        
        if nova_senha:
            senha_criptografada = generate_password_hash(nova_senha)
            c.execute("UPDATE usuarios SET username=?, password=? WHERE username=?", (novo_usuario, senha_criptografada, session['usuario']))
        else:
            c.execute("UPDATE usuarios SET username=? WHERE username=?", (novo_usuario, session['usuario']))
            
        conn.commit()
        conn.close()
        
        session['usuario'] = novo_usuario
        flash('Dados de acesso atualizados com sucesso!', 'success')
        return redirect(url_for('perfil'))
        
    return render_template('perfil.html', titulo="Meu Perfil")


# =================================================================
# ROTAS DO SISTEMA
# =================================================================
@app.route('/')
@login_required
def home(): return render_template('home.html', titulo="Dashboard Principal")

@app.route('/ftth/teoria')
def ftth_teoria(): return render_template('ftth_teoria.html', titulo="FTTH: Engenharia & Arquitetura")

@app.route('/ftth/hardware')
def ftth_hardware(): return render_template('ftth_hardware.html', titulo="FTTH: Enciclopédia de Hardware")

@app.route('/ftth/calc', methods=['GET', 'POST'])
def ftth_calc(): return render_template('ftth_calc.html', titulo="FTTH: Simulador Pro")

@app.route('/ftth/simulador_avancado')
def ftth_simulador_avancado(): return render_template('ftth_simulator.html', titulo="FTTH: Simulador End-to-End")

@app.route('/ftth/simulador_campo')
def ftth_simulador_campo(): return render_template('ftth_field_simulator.html', titulo="FTTH: Simulador de Campo")

@app.route('/ftth/simulador_grafico')
def ftth_simulador_grafico(): return render_template('ftth_visual_simulator.html', titulo="FTTH: Simulador Gráfico")

@app.route('/ftth/mapa_interativo')
@login_required
def ftth_mapa_interativo(): return render_template('ftth_interactive_map.html', titulo="FTTH: Mini CAD Profissional")

@app.route('/ftth/hardware/olt')
def ftth_hw_olt(): return render_template('ftth_hw_olt.html', titulo="HW: OLT")
@app.route('/ftth/hardware/gbic')
def ftth_hw_gbic(): return render_template('ftth_hw_gbic.html', titulo="HW: GBIC/SFP")
@app.route('/ftth/hardware/fibras')
def ftth_hw_fibras(): return render_template('ftth_hw_fibras.html', titulo="HW: Fibras e Cabos")
@app.route('/ftth/hardware/splitters')
def ftth_hw_splitters(): return render_template('ftth_hw_splitters.html', titulo="HW: Splitters")
@app.route('/ftth/hardware/caixas')
def ftth_hw_caixas(): return render_template('ftth_hw_caixas.html', titulo="HW: Caixas Ópticas")
@app.route('/ftth/hardware/conectores')
def ftth_hw_conectores(): return render_template('ftth_hw_conectores.html', titulo="HW: Conectores")
@app.route('/ftth/hardware/emendas')
def ftth_hw_emendas(): return render_template('ftth_hw_emendas.html', titulo="HW: Tipos de Emenda")
@app.route('/ftth/hardware/patchcords')
def ftth_hw_patchcords(): return render_template('ftth_hw_patchcords.html', titulo="HW: Patch Cords")
@app.route('/ftth/hardware/ferragens')
def ftth_hw_ferragens(): return render_template('ftth_hw_ferragens.html', titulo="HW: Infraestrutura de Poste")
@app.route('/ftth/hardware/cpe')
def ftth_hw_cpe(): return render_template('ftth_hw_cpe.html', titulo="HW: Equipamentos CPE")
@app.route('/ftth/hardware/pto')
def ftth_hw_pto(): return render_template('ftth_hw_pto.html', titulo="HW: PTO/Roseta")

@app.route('/radio/teoria', methods=['GET', 'POST'])
def radio_teoria():
    if request.method == 'GET':
        return render_template('radio_teoria.html', titulo="Rádio: WISP Training", resultado_fresnel=None)
    if request.method == 'POST':
        try:
            distancia_km = float(request.form.get('radio_dist'))
            frequencia_ghz = float(request.form.get('radio_freq'))
            raio_100_percent = 17.32 * math.sqrt(distancia_km / (4 * frequencia_ghz))
            raio_60_percent = raio_100_percent * 0.6
            resultado = {'raio_total': f"{raio_100_percent:.2f}", 'raio_livre': f"{raio_60_percent:.2f}", 'distancia': distancia_km, 'frequencia': frequencia_ghz}
            return render_template('radio_teoria.html', titulo="Rádio: WISP Training", resultado_fresnel=resultado)
        except Exception:
            return render_template('radio_teoria.html', titulo="Rádio: WISP Training", erro_fresnel="Erro no cálculo.", resultado_fresnel=None)

@app.route('/radio/hardware')
def radio_hardware(): return render_template('radio_hardware.html', titulo="Rádio: Enciclopédia de Hardware")
@app.route('/radio/hardware/acesso')
def radio_hw_acesso(): return render_template('radio_hw_acesso.html', titulo="HW Rádio: Acesso e Backhaul")
@app.route('/radio/hardware/energia')
def radio_hw_energia(): return render_template('radio_hw_energia.html', titulo="HW Rádio: Energia e Proteção")
@app.route('/radio/hardware/infra')
def radio_hw_infra(): return render_template('radio_hw_infra.html', titulo="HW Rádio: Cabos e Infraestrutura")
@app.route('/radio/hardware/cliente')
def radio_hw_cliente(): return render_template('radio_hw_cliente.html', titulo="HW Rádio: Cliente (CPE Interior)")

@app.route('/ip/teoria')
def ip_teoria(): return render_template('ip_teoria.html', titulo="Redes IP: Protocolos")

@app.route('/ip/calc', methods=['GET', 'POST'])
def ip_calc():
    context = {'titulo': "Calculadora IP (CIDR)"}
    if request.method == 'GET': return render_template('ip_calc.html', **context)
    if request.method == 'POST':
        ip_entrada = request.form.get('ip_address')
        cidr_entrada = int(request.form.get('cidr_mask'))
        context.update({'ip_entrada': ip_entrada, 'cidr_entrada': cidr_entrada})
        try:
            network = ipaddress.ip_network(f'{ip_entrada}/{cidr_entrada}', strict=False)
            context.update({
                'resultado': True, 'net_addr': str(network.network_address), 'broadcast': str(network.broadcast_address),
                'net_mask': str(network.netmask), 'hosts': network.num_addresses - 2 if cidr_entrada < 31 else (1 if cidr_entrada == 32 else 0),
                'first_ip': str(network.network_address + 1) if cidr_entrada < 31 else "N/A", 'last_ip': str(network.broadcast_address - 1) if cidr_entrada < 31 else "N/A"
            })
            return render_template('ip_calc.html', **context)
        except ValueError:
            context['erro'] = "Endereço IP ou Máscara inválida!"
            return render_template('ip_calc.html', **context)

@app.route('/pratica')
def pratica_home(): return render_template('pratica_home.html', titulo="Prática de Campo")
@app.route('/pratica/fibra')
def pratica_fibra(): return render_template('pratica_fibra.html', titulo="Prática: Fibra Óptica")
@app.route('/pratica/radio')
def pratica_radio(): return render_template('pratica_radio.html', titulo="Prática: Instalação Rádio")
@app.route('/pratica/ceo_cto')
def pratica_ceo_cto(): return render_template('pratica_ceo_cto.html', titulo="Prática: Emendas e Caixas")

@app.route('/diag')
@login_required
def diag_home(): return render_template('diag_home.html', titulo="Central de Diagnóstico")

@app.route('/diag/quiz', methods=['GET', 'POST'])
def diag_quiz():
    modulo = request.args.get('modulo', 'ftth').lower()
    if modulo not in BANCO_MESTRE: modulo = 'ftth'
    quiz_original = BANCO_MESTRE[modulo]
    
    if request.method == 'GET':
        chaves = list(quiz_original.keys())
        chaves_aleatorias = random.sample(chaves, min(5, len(chaves)))
        return render_template('diag_quiz_server.html', titulo=f"Avaliação {modulo.upper()}", modulo=modulo, quiz={chave: quiz_original[chave] for chave in chaves_aleatorias}, resultados=None)
    
    if request.method == 'POST':
        modulo_pos = request.form.get('modulo', 'ftth')
        quiz_original = BANCO_MESTRE[modulo_pos]
        pontuacao = 0
        acertos = {}
        chaves_corrigir = []
        for key, resposta_dada in request.form.items():
            if key in quiz_original:
                chaves_corrigir.append(key)
                if resposta_dada == quiz_original[key]['resposta']:
                    pontuacao += 1
                    acertos[key] = {'correta': True, 'dada': resposta_dada}
                else:
                    acertos[key] = {'correta': False, 'dada': resposta_dada, 'esperada': quiz_original[key]['resposta']}
        return render_template('diag_quiz_server.html', titulo=f"Resultado {modulo_pos.upper()}", modulo=modulo_pos, quiz=quiz_original, resultados=acertos, pontuacao=pontuacao, total=len(chaves_corrigir), porcentagem=(pontuacao/len(chaves_corrigir))*100)

@app.route('/servers/teoria')
def servers_teoria(): return render_template('servers_teoria.html', titulo="Servidores de Provedor (AAA)")
@app.route('/core/teoria')
def core_teoria(): return render_template('core_teoria.html', titulo="Engenharia de Core (MPLS/BGP)")
@app.route('/security/teoria')
def security_teoria(): return render_template('security_teoria.html', titulo="Segurança de Redes")

@app.route('/atendimento/teoria')
def atendimento_teoria(): return render_template('atendimento_teoria.html', titulo="Suporte e Atendimento N1/N2")
@app.route('/vendas/teoria')
def vendas_teoria(): return render_template('vendas_teoria.html', titulo="Comercial e Vendas")
@app.route('/gestao/teoria')
def gestao_teoria(): return render_template('gestao_teoria.html', titulo="Normas, NR10/35 e ANATEL")
    
@app.route('/servers/mikrotik_sim')
@login_required
def mikrotik_sim(): 
    return render_template('mikrotik_simulator.html', titulo="WinBox Simulator Pro")
    
@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
