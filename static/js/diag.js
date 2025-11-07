// =================================================================
// 🧠 ARQUIVO: diag.js - CÉREBRO DO DIAGNÓSTICO E AVALIAÇÃO
// =================================================================

// --- PARTE 1: LÓGICA DO FLUXOGRAMA (Mantido e Reorganizado) ---
const fluxos = {
    // ... (Seu array de fluxos longos: sem_conexao, lentidao, quedas) ...
    // Para fins de brevidade neste código, vamos manter a estrutura e assumir que os fluxos já estão no seu arquivo.
    sem_conexao: {
        pergunta: "Qual o status dos LEDs na ONU do cliente?",
        opcoes: [
            { texto: "LED 'PON' piscando ou 'LOS' vermelho aceso", proximo: "rompimento_fibra" },
            { texto: "LEDs 'PON' e 'LAN' verdes fixos", proximo: "problema_logico" },
            { texto: "Nenhum LED acende (ONU apagada)", proximo: "problema_eletrico" }
        ]
    },
    rompimento_fibra: { pergunta: "DIAGNÓSTICO: Problema Físico na Fibra (LOS).", solucao: "Possível rompimento do cabo Drop ou atenuação altíssima. Medir potência na Roseta.", final: true },
    problema_eletrico: { pergunta: "DIAGNÓSTICO: Falha Elétrica.", solucao: "Verificar tomada, fonte da ONU ou queda de energia no bairro.", final: true },
    problema_logico: {
        pergunta: "A fibra parece OK. O cliente navega se ligar o cabo direto no PC?",
        opcoes: [
            { texto: "Sim, navega normal no cabo", proximo: "problema_wifi" },
            { texto: "Não, continua sem navegar", proximo: "verificar_auth" }
        ]
    },
    problema_wifi: { pergunta: "DIAGNÓSTICO: Problema no Roteador Wi-Fi.", solucao: "Reiniciar roteador, verificar canal e interferência.", final: true },
    verificar_auth: {
        pergunta: "Verifique o servidor PPPoE. O cliente está autenticado?",
        opcoes: [
            { texto: "Não, erro de autenticação", proximo: "erro_senha" },
            { texto: "Sim, está logado mas não navega", proximo: "bloqueio_financeiro" }
        ]
    },
    erro_senha: { pergunta: "DIAGNÓSTICO: Falha de Autenticação PPPoE.", solucao: "Reconfigurar usuário/senha do PPPoE.", final: true },
    bloqueio_financeiro: { pergunta: "DIAGNÓSTICO: Bloqueio Lógico/Financeiro.", solucao: "Cliente autenticado, mas sem acesso. Verificar status de pagamento/fatura.", final: true },
    // ... (Adicione aqui as chaves para lentidao e quedas)
};

function iniciarFluxo(tipo) {
    mostrarEtapa(fluxos[tipo]);
}

function mostrarEtapa(etapa) {
    const container = document.getElementById('fluxoContainer');
    container.style.opacity = 0;
    setTimeout(() => {
        let html = `<h4 class="card-title mb-4 fw-bold text-dark">${etapa.pergunta}</h4>`;

        if (etapa.final) {
            html += `<div class="alert alert-success border-success shadow-sm"><h5><i class="bi bi-check-circle-fill text-success"></i> SOLUÇÃO SUGERIDA:</h5><p class="mb-0 fs-5">${etapa.solucao}</p></div>`;
            html += `<button class="btn btn-secondary mt-3 fw-bold px-4 py-2" onclick="location.reload()"><i class="bi bi-arrow-counterclockwise"></i> Reiniciar Diagnóstico</button>`;
        } else {
            html += `<div class="d-grid gap-3 col-md-10 mx-auto">`;
            etapa.opcoes.forEach(opcao => {
                let btnClass = "btn-outline-dark";
                if (opcao.texto.includes("vermelho") || opcao.texto.includes("Não")) btnClass = "btn-outline-danger";
                if (opcao.texto.includes("verde") || opcao.texto.includes("Sim")) btnClass = "btn-outline-success";

                html += `<button class="btn ${btnClass} text-start p-3 fs-5 shadow-sm" onclick="mostrarEtapa(fluxos['${opcao.proximo}'])"><i class="bi bi-arrow-right-circle-fill me-2"></i> ${opcao.texto}</button>`;
            });
            html += `</div>`;
        }
        container.innerHTML = html;
        container.style.opacity = 1;
    }, 200);
}

// --- PARTE 2: SIMULADOR DE TERMINAL (Mantido) ---
const terminalInput = document.getElementById('terminalInput');
const terminalOutput = document.getElementById('terminalOutput');

if (terminalInput) { // Se o terminal existir na página
    terminalInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            const comando = this.value.trim().toLowerCase();
            this.value = '';
            printLine(`<span class="text-warning">$ ${comando}</span>`);
            processarComando(comando);
        }
    });
}

function printLine(html) {
    if (terminalOutput) {
        terminalOutput.innerHTML += `<div>${html}</div>`;
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
}

function processarComando(cmd) {
    // ... (Sua lógica de terminal simulado: ping, traceroute, clear)
}

// =================================================================
// 🏆 PARTE 3: LÓGICA DO QUIZ (AVALIAÇÃO TÉCNICA)
// =================================================================

const bancoDePerguntas = {
    ftth: [
        { pergunta: "Qual é o valor MÁXIMO aceitável de atenuação na ONU para um link ser considerado viável?",
          opcoes: ["-10 dBm", "-20 dBm", "-27 dBm", "-35 dBm"], resposta: "-27 dBm" },
        { pergunta: "Qual cor de conector é OBRIGATÓRIA em redes GPON por conta da reflexão?",
          opcoes: ["Azul (UPC)", "Verde (APC)", "Preto (PC)", "Amarelo (SC)"], resposta: "Verde (APC)" },
        { pergunta: "Qual componente passivo tem a maior perda de sinal na rede?",
          opcoes: ["Fusão (Emenda)", "Splitter", "Conector", "Fibra por KM"], resposta: "Splitter" },
        { pergunta: "A função primária da OLT é:",
          opcoes: ["Autenticar PPPoE", "Distribuir Wi-Fi", "Gerenciar o tempo de fala das ONUs (TDMA)", "Fazer o NAT de clientes"], resposta: "Gerenciar o tempo de fala das ONUs (TDMA)" },
    ],
    ip: [
        { pergunta: "Qual protocolo é RÁPIDO, não garante entrega, e é usado para Jogos/VoIP?",
          opcoes: ["TCP", "HTTP", "ICMP", "UDP"], resposta: "UDP" },
        { pergunta: "Em uma rede 192.168.1.0/24, quantos IPs úteis existem?",
          opcoes: ["256", "255", "254", "2"], resposta: "254" },
        { pergunta: "Qual camada do Modelo OSI é responsável pelo Endereçamento IP e Roteamento?",
          opcoes: ["Camada 2 (Enlace)", "Camada 3 (Rede)", "Camada 4 (Transporte)", "Camada 7 (Aplicação)"], resposta: "Camada 3 (Rede)" },
    ],
    radio: [
        { pergunta: "Qual a porcentagem mínima da Zona de Fresnel que deve estar livre de obstáculos?",
          opcoes: ["50%", "60%", "80%", "100%"], resposta: "60%" },
        { pergunta: "A banda 5.8 GHz é preferida por provedores por qual motivo?",
          opcoes: ["Melhor penetração em árvores", "Maior alcance", "Mais canais disponíveis (espectro maior)", "Equipamento mais barato"], resposta: "Mais canais disponíveis (espectro maior)" },
    ],
};

function iniciarQuiz(modulo) {
    const quizArea = document.getElementById('quizArea');
    quizArea.classList.remove('d-none');
    
    const perguntas = bancoDePerguntas[modulo];
    let html = `<form id="quizForm" onsubmit="return false;">`;

    perguntas.forEach((p, index) => {
        html += `<div class="card mb-4 shadow-sm"><div class="card-body">`;
        html += `<p class="fw-bold fs-5">${index + 1}. ${p.pergunta}</p>`;

        p.opcoes.forEach((opcao, opIndex) => {
            // Cria um ID único para o input radio
            const inputId = `${modulo}_q${index}_o${opIndex}`;
            html += `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="pergunta${index}" id="${inputId}" value="${opcao}" required>
                    <label class="form-check-label" for="${inputId}">
                        ${opcao}
                    </label>
                </div>
            `;
        });
        html += `</div></div>`;
    });

    html += `<div class="d-grid mt-4">
                <button type="submit" class="btn btn-info btn-lg fw-bold text-white" onclick="corrigirQuiz('${modulo}')">
                    <i class="bi bi-check-circle-fill"></i> FINALIZAR E CORRIGIR
                </button>
             </div>`;
    html += `</form>`;
    
    quizArea.innerHTML = html;
}

function corrigirQuiz(modulo) {
    const form = document.getElementById('quizForm');
    const perguntas = bancoDePerguntas[modulo];
    let pontuacao = 0;
    
    // 1. Percorrer todas as perguntas e checar as respostas
    perguntas.forEach((p, index) => {
        const respostaCorreta = p.resposta;
        const nomePergunta = `pergunta${index}`;
        const respostaSelecionada = form.elements[nomePergunta].value;

        const cardBody = document.querySelector(`input[name="${nomePergunta}"]`).closest('.card-body');
        
        // Limpa classes anteriores
        cardBody.classList.remove('bg-danger', 'bg-success', 'text-white');

        if (respostaSelecionada === respostaCorreta) {
            pontuacao++;
            cardBody.classList.add('bg-success', 'text-white');
        } else {
            cardBody.classList.add('bg-danger', 'text-white');
            // Opcional: Mostrar a resposta correta
            const labelCorreta = document.querySelector(`label[for="${modulo}_q${index}_o${perguntas[index].opcoes.indexOf(respostaCorreta)}"]`);
            if (labelCorreta) {
                 labelCorreta.innerHTML += ` <span class="badge bg-white text-success fw-bold ms-2">CORRETA</span>`;
            }
        }
    });

    // 2. Mostrar o resultado final
    const totalPerguntas = perguntas.length;
    const porcentagem = (pontuacao / totalPerguntas) * 100;
    
    let resultadoHTML = `
        <div class="alert mt-5 p-4 text-center ${porcentagem >= 70 ? 'alert-success' : 'alert-danger'} shadow-lg">
            <h3 class="fw-bold">${modulo.toUpperCase()} - RESULTADO FINAL</h3>
            <h1 class="display-3">${pontuacao}/${totalPerguntas}</h1>
            <p class="fs-4">Aproveitamento: ${porcentagem.toFixed(0)}%</p>
            <p class="small">${porcentagem >= 70 ? 'Parabéns! Você demonstrou conhecimento sólido no módulo.' : 'Abaixo do esperado. Revise a seção e tente novamente.'}</p>
            <button class="btn btn-secondary mt-3" onclick="location.reload()">Sair da Avaliação</button>
        </div>
    `;
    
    document.getElementById('quizContainer').innerHTML += resultadoHTML;
    document.getElementById('quizForm').querySelector('button[type="submit"]').style.display = 'none'; // Esconde o botão após a correção
}
