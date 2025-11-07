from flask import Flask, render_template

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

@app.route('/ftth/calc')
def ftth_calc():
    return render_template('ftth_calc.html', titulo="FTTH: Simulador Pro")

# --- SUB-ROTAS: DETALHE HARDWARE FTTH ---
@app.route('/ftth/hardware/olt')
def ftth_hw_olt():
    return render_template('ftth_hw_olt.html', titulo="HW: OLT")

@app.route('/ftth/hardware/gbic')
def ftth_hw_gbic():
    return render_template('ftth_hw_gbic.html', titulo="HW: GBIC/SFP")

@app.route('/ftth/hardware/fibras')
def ftth_hw_fibras():
    return render_template('ftth_hw_fibras.html', titulo="HW: Fibras e Cabos")

@app.route('/ftth/hardware/splitters')
def ftth_hw_splitters():
    return render_template('ftth_hw_splitters.html', titulo="HW: Splitters")

@app.route('/ftth/hardware/caixas')
def ftth_hw_caixas():
    return render_template('ftth_hw_caixas.html', titulo="HW: Caixas Ópticas")

@app.route('/ftth/hardware/conectores')
def ftth_hw_conectores():
    return render_template('ftth_hw_conectores.html', titulo="HW: Conectores")

@app.route('/ftth/hardware/emendas')
def ftth_hw_emendas():
    return render_template('ftth_hw_emendas.html', titulo="HW: Tipos de Emenda")

@app.route('/ftth/hardware/patchcords')
def ftth_hw_patchcords():
    return render_template('ftth_hw_patchcords.html', titulo="HW: Patch Cords")

@app.route('/ftth/hardware/ferragens')
def ftth_hw_ferragens():
    return render_template('ftth_hw_ferragens.html', titulo="HW: Infraestrutura de Poste")

@app.route('/ftth/hardware/cpe')
def ftth_hw_cpe():
    return render_template('ftth_hw_cpe.html', titulo="HW: Equipamentos CPE")

@app.route('/ftth/hardware/pto')
def ftth_hw_pto():
    return render_template('ftth_hw_pto.html', titulo="HW: PTO/Roseta")

# --- MÓDULO RÁDIO (WIRELESS) ---
@app.route('/radio/teoria')
def radio_teoria():
    return render_template('radio_teoria.html', titulo="Rádio: WISP Training")

# --- MÓDULO IP (REDES LÓGICAS) ---
@app.route('/ip/teoria')
def ip_teoria():
    return render_template('ip_teoria.html', titulo="Redes IP: Protocolos")

@app.route('/ip/calc')
def ip_calc():
    return render_template('ip_calc.html', titulo="Calculadora IP (CIDR)")

# --- MÓDULO SERVIDORES & CORE ---
@app.route('/servers/teoria')
def servers_teoria():
    return render_template('servers_teoria.html', titulo="Servidores de Provedor (AAA)")

@app.route('/core/teoria')  # <--- NOVA ROTA AVANÇADA
def core_teoria():
    return render_template('core_teoria.html', titulo="Engenharia de Core (MPLS/BGP)")

# --- MÓDULO DIAGNÓSTICO ---
@app.route('/diag')
def diag_home():
    return render_template('diag_home.html', titulo="Central de Diagnóstico")

if __name__ == '__main__':
    app.run(debug=True)
