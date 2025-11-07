from flask import Flask, render_template, request
import ipaddress
import random

app = Flask(__name__)

# =================================================================
# BANCO DE QUESTÕES (Mantido no topo)
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

BANCO_MESTRE = {
    "ftth": QUIZ_FTTH,
    "ip": QUIZ_IP,
    "radio": QUIZ_RADIO
}
# =================================================================

app = Flask(__name__)

# --- ROTA PRINCIPAL (DASHBOARD) ---
@app.route('/')
def home():
    return render_template('home.html', titulo="Dashboard Principal")

# --- MÓDULO FTTH (FIBRA) ---
@app.route('/ftth/teoria')
def ftth_teoria():
    return render_template('ftth_teoria.html', titulo="FTTH: Engenharia & Arquitetura")

@app.route('/ftth/hardware')
def ftth_hardware():
    return render_template('ftth_hardware.html', titulo="FTTH: Enciclopédia de Hardware")

@app.route('/ftth/calc', methods=['GET', 'POST'])
def ftth_calc():
    if request.method == 'GET':
        return render_template('ftth_calc.html', titulo="FTTH: Simulador Pro")
    return render_template('ftth_calc.html', titulo="FTTH: Simulador Pro")

# --- SUB-ROTAS FTTH (Mantidas) ---
# ... (suas 11 sub-rotas de hardware FTTH aqui) ...
# @app.route('/ftth/hardware/olt') ...

# --- MÓDULO RÁDIO (WIRELESS) ---
@app.route('/radio/teoria')
def radio_teoria():
    return render_template('radio_teoria.html', titulo="Rádio: WISP Training")

@app.route('/radio/hardware')
def radio_hardware():
    return render_template('radio_hardware.html', titulo="Rádio: Enciclopédia de Hardware")

# --- NOVAS SUB-ROTAS RÁDIO (HARDWARE) ---
@app.route('/radio/hardware/acesso')
def radio_hw_acesso():
    return render_template('radio_hw_acesso.html', titulo="HW Rádio: Acesso e Backhaul")

@app.route('/radio/hardware/energia')
def radio_hw_energia():
    return render_template('radio_hw_energia.html', titulo="HW Rádio: Energia e Proteção")

@app.route('/radio/hardware/infra')
def radio_hw_infra():
    return render_template('radio_hw_infra.html', titulo="HW Rádio: Cabos e Infraestrutura")

@app.route('/radio/hardware/cliente')
def radio_hw_cliente():
    return render_template('radio_hw_cliente.html', titulo="HW Rádio: Cliente (CPE Interior)")


# --- MÓDULO IP (REDES LÓGICAS) ---
@app.route('/ip/teoria')
def ip_teoria():
    return render_template('ip_teoria.html', titulo="Redes IP: Protocolos")

@app.route('/ip/calc', methods=['GET', 'POST'])
def ip_calc():
    # ... (Sua lógica de cálculo IP em Python - Mantida por brevidade) ...
    pass # Remova este 'pass' se você estiver usando a lógica de cálculo IP


# --- ROTA DE DIAGNÓSTICO E QUIZ ---
@app.route('/diag')
def diag_home():
    return render_template('diag_home.html', titulo="Central de Diagnóstico")


@app.route('/diag/quiz', methods=['GET', 'POST'])
def diag_quiz():
    # ... (Sua lógica de Quiz Python - Mantida por brevidade) ...
    pass # Remova este 'pass' se você estiver usando a lógica de Quiz


# --- MÓDULO SERVIDORES & CORE & SEGURANÇA ---
@app.route('/servers/teoria')
def servers_teoria():
    return render_template('servers_teoria.html', titulo="Servidores de Provedor (AAA)")

@app.route('/core/teoria')
def core_teoria():
    return render_template('core_teoria.html', titulo="Engenharia de Core (MPLS/BGP)")

@app.route('/security/teoria')
def security_teoria():
    return render_template('security_teoria.html', titulo="Segurança de Redes (Zero Trust)")


if __name__ == '__main__':
    app.run(debug=True)
