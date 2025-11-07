from flask import Flask, render_template, request
import ipaddress
import random
import math

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

# --- SUB-ROTAS: DETALHES DE HARDWARE FTTH (Mantidas) ---
# [Rotas omitidas aqui por brevidade, mas devem estar no seu arquivo]
# ...

# --- MÓDULO RÁDIO (WIRELESS) ---
@app.route('/radio/teoria', methods=['GET', 'POST'])
def radio_teoria():
    # Bloco GET: Apenas mostra a página
    if request.method == 'GET':
        return render_template('radio_teoria.html', titulo="Rádio: WISP Training", resultado_fresnel=None)
    
    # Bloco POST: Processa o cálculo de Fresnel (AGORA FUNCIONAL)
    if request.method == 'POST':
        try:
            distancia_km = float(request.form.get('radio_dist'))
            frequencia_ghz = float(request.form.get('radio_freq'))
            
            if distancia_km <= 0 or frequencia_ghz <= 0:
                raise ValueError("Valores devem ser positivos.")

            # FÓRMULA DE FRESNEL
            raio_100_percent = 17.32 * math.sqrt(distancia_km / (4 * frequencia_ghz))
            raio_60_percent = raio_100_percent * 0.6
            
            resultado = {
                'raio_total': f"{raio_100_percent:.2f}",
                'raio_livre': f"{raio_60_percent:.2f}",
                'distancia': distancia_km,
                'frequencia': frequencia_ghz
            }

            return render_template('radio_teoria.html', 
                                   titulo="Rádio: WISP Training", 
                                   resultado_fresnel=resultado)

        except Exception as e:
            return render_template('radio_teoria.html', 
                                   titulo="Rádio: WISP Training", 
                                   erro_fresnel="Erro no cálculo: Verifique se Distância e Frequência são números válidos.",
                                   resultado_fresnel=None)


@app.route('/radio/hardware')
def radio_hardware():
    return render_template('radio_hardware.html', titulo="Rádio: Enciclopédia de Hardware")

# --- SUB-ROTAS: DETALHES DE HARDWARE RÁDIO (ADICIONADAS AQUI NOVAMENTE) ---
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
    context = {'titulo': "Calculadora IP (CIDR)"}

    if request.method == 'GET':
        return render_template('ip_calc.html', **context)
    
    if request.method == 'POST':
        ip_entrada = request.form.get('ip_address')
        cidr_entrada = int(request.form.get('cidr_mask'))
        
        context.update({
            'ip_entrada': ip_entrada,
            'cidr_entrada': cidr_entrada
        })

        try:
            # Lógica de cálculo (Mantida para brevidade)
            network = ipaddress.ip_network(f'{ip_entrada}/{cidr_entrada}', strict=False)
            
            network_address = str(network.network_address)
            netmask = str(network.netmask)
            broadcast_address = str(network.broadcast_address)
            
            if cidr_entrada == 32:
                total_hosts = 1
                first_usable = ip_entrada
                last_usable = ip_entrada
            elif cidr_entrada == 31:
                total_hosts = 0
                first_usable = "N/A"
                last_usable = "N/A"
            else:
                total_hosts = network.num_addresses - 2
                first_usable = str(network.network_address + 1)
                last_usable = str(network.broadcast_address - 1)
            
            context.update({
                'resultado': True,
                'net_addr': network_address,
                'broadcast': broadcast_address,
                'net_mask': netmask,
                'first_ip': first_usable,
                'last_ip': last_usable,
                'hosts': total_hosts
            })

            return render_template('ip_calc.html', **context)

        except ValueError:
            context['erro'] = "Endereço IP ou Máscara inválida! Verifique a sintaxe."
            return render_template('ip_calc.html', **context)

# --- NOVOS MÓDULOS: PRÁTICA DE CAMPO ---
@app.route('/pratica')
def pratica_home():
    return render_template('pratica_home.html', titulo="Prática de Campo")

@app.route('/pratica/fibra')
def pratica_fibra():
    return render_template('pratica_fibra.html', titulo="Prática: Fibra Óptica")

@app.route('/pratica/radio')
def pratica_radio():
    return render_template('pratica_radio.html', titulo="Prática: Instalação Rádio")

@app.route('/pratica/ceo_cto')
def pratica_ceo_cto():
    return render_template('pratica_ceo_cto.html', titulo="Prática: Emendas e Caixas")


# --- MÓDULO DIAGNÓSTICO E QUIZ ---
@app.route('/diag')
def diag_home():
    return render_template('diag_home.html', titulo="Central de Diagnóstico")


@app.route('/diag/quiz', methods=['GET', 'POST'])
def diag_quiz():
    
    # Lógica do Quiz (Mantida para brevidade)
    modulo = request.args.get('modulo', 'ftth')
    modulo = modulo.lower()
    
    if modulo not in BANCO_MESTRE:
        modulo = 'ftth'

    quiz_original = BANCO_MESTRE[modulo]
    
    # 2. SELEÇÃO ALEATÓRIA (Lógica de GET)
    chaves = list(quiz_original.keys())
    num_questoes = 5
    chaves_aleatorias = random.sample(chaves, min(num_questoes, len(chaves)))
    quiz_a_exibir = {chave: quiz_original[chave] for chave in chaves_aleatorias}


    if request.method == 'GET':
        return render_template('diag_quiz_server.html', 
                               titulo=f"Avaliação {modulo.upper()}", 
                               modulo=modulo,
                               quiz=quiz_a_exibir, 
                               resultados=None)
    
    
    if request.method == 'POST':
        # ... (Resto da lógica de correção do Quiz) ...
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
