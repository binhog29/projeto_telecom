# 📡 Telecom Pro System

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-black)
![Deploy](https://img.shields.io/badge/Deploy-Vercel-black)

### 🔗 Link para o Projeto Ao Vivo: [https://projeto-telecom.vercel.app/](https://projeto-telecom.vercel.app/)

---

## 🎯 Sobre o Projeto

O **Telecom Pro System** é uma plataforma de EAD (Ensino a Distância) e ferramenta de apoio (Toolbox) focada na capacitação profissional para provedores de internet (ISPs). 

Este projeto foi criado para resolver um problema real do setor: a falta de material de estudo centralizado, interativo e em português para técnicos de Nível 1 e Nível 2. Ele serve como um portfólio profissional que demonstra a união de duas áreas: **Engenharia de Telecomunicações** e **Desenvolvimento de Software (Python/Flask)**.

## ✨ Funcionalidades (Módulos)

O sistema é 100% responsivo (PWA) e dividido em 6 módulos de conhecimento principais:

1.  **Módulo FTTH (Fibra Óptica):**
    * Teoria de Arquitetura e Engenharia (CLI).
    * **Enciclopédia de Hardware** (OLTs, SFPs, Caixas, Ferragens, etc).
    * **Calculadora Profissional** de Orçamento de Potência.

2.  **Módulo Wireless (Rádio):**
    * Engenharia WISP (PTP, PTMP).
    * Conceitos de RF (5.8GHz, 2.4GHz) e Infra de Torres.
    * **Calculadora Interativa** de Zona de Fresnel.

3.  **Módulo Redes IP (Lógico):**
    * Teoria avançada (Modelo OSI, TCP/UDP, VLANs).
    * **Calculadora CIDR** (Sub-redes IPv4) com análise binária.

4.  **Módulo Servidores (AAA):**
    * O coração do provedor: Explica o fluxo de autenticação.
    * PPPoE (PADI, PADO, etc.).
    * RADIUS (Authentication, Authorization, Accounting).
    * DNS Cache (Unbound/Bind9).

5.  **Módulo Core (MPLS/BGP):**
    * Engenharia de Core e Backbone (miolo da rede).
    * MPLS (L2VPN, L3VPN) para serviços corporativos.
    * BGP (iBGP vs eBGP) e Roteamento Avançado.

6.  **Módulo Diagnóstico (Troubleshooting):**
    * **Fluxograma Interativo** para guiar o técnico na resolução de problemas.
    * **Terminal Simulado** (`ping`, `traceroute`) para treinar comandos.

## 💻 Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (ES6+)
* **PWA:** Web App Manifest (`manifest.json`)
* **Infra/Deploy:** Git, GitHub, Vercel

## 🚀 Como Rodar Localmente

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/binhog29/projeto_telecom.git](https://github.com/binhog29/projeto_telecom.git)
    cd projeto_telecom
    ```
2.  (Opcional) Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Rode o servidor Flask:
    ```bash
    python app.py
    ```
5.  Acesse `http://127.0.0.1:5000` no seu navegador.

## 🧑‍💻 Desenvolvedor

* **Fábio (binhog29)**
* **GitHub:** [github.com/binhog29](https://github.com/binhog29/projeto_telecom.git)
* **Link Vercel:** [https://projeto-telecom.vercel.app/](https://projeto-telecom.vercel.app/)
