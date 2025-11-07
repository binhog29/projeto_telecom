// =================================================================
// 🧠 ARQUIVO: diag.js - CÉREBRO DO DIAGNÓSTICO
// =================================================================

// --- PARTE 1: LÓGICA DO FLUXOGRAMA (ASSISTENTE DE TROUBLESHOOTING) ---
const fluxos = {
    // =================================================================
    // FLUXO 1: SEM CONEXÃO
    // =================================================================
    sem_conexao: {
        pergunta: "Qual o status dos LEDs na ONU do cliente?",
        opcoes: [
            { texto: "LED 'PON' piscando ou 'LOS' vermelho aceso", proximo: "rompimento_fibra" },
            { texto: "LEDs 'PON' e 'LAN' verdes fixos", proximo: "problema_logico" },
            { texto: "Nenhum LED acende (ONU apagada)", proximo: "problema_eletrico" }
        ]
    },
    rompimento_fibra: { 
        pergunta: "DIAGNÓSTICO: Problema Físico na Fibra (LOS).", 
        solucao: "Possível rompimento do cabo Drop ou atenuação altíssima (> -30dBm). Enviar técnico para verificar a potência na Roseta Óptica e no CTO.", 
        final: true 
    },
    problema_eletrico: { 
        pergunta: "DIAGNÓSTICO: Falha Elétrica.", 
        solucao: "Pedir para o cliente verificar a tomada, a fonte da ONU ou se houve queda de energia no bairro. Se não resolver, trocar a fonte/ONU.", 
        final: true 
    },
    problema_logico: {
        pergunta: "A fibra parece OK (PON fixo). O cliente navega se ligar o cabo direto no PC?",
        opcoes: [
            { texto: "Sim, navega normal no cabo", proximo: "problema_wifi" },
            { texto: "Não, continua sem navegar", proximo: "verificar_auth" }
        ]
    },
    problema_wifi: { 
        pergunta: "DIAGNÓSTICO: Problema no Roteador Wi-Fi.", 
        solucao: "O link chega até a casa, mas o Wi-Fi travou. Reiniciar roteador, verificar canal e interferência.", 
        final: true 
    },
    verificar_auth: {
        pergunta: "Verifique o servidor PPPoE. O cliente está autenticado?",
        opcoes: [
            { texto: "Não, erro de autenticação (falha de login)", proximo: "erro_senha" },
            { texto: "Sim, está logado mas não navega", proximo: "bloqueio_financeiro" }
        ]
    },
    erro_senha: { 
        pergunta: "DIAGNÓSTICO: Falha de Autenticação PPPoE.", 
        solucao: "Roteador pode ter sido resetado e perdeu a configuração. Reconfigurar usuário/senha do PPPoE no equipamento do cliente.", 
        final: true 
    },
    bloqueio_financeiro: { 
        pergunta: "DIAGNÓSTICO: Bloqueio Lógico/Financeiro.", 
        solucao: "Cliente autenticado, mas o servidor RADIUS/Billing não liberou banda. Verificar se há faturas em atraso ou se o plano está suspenso.", 
        final: true 
    },

    // =================================================================
    // FLUXO 2: LENTIDÃO
    // =================================================================
    lentidao: {
        pergunta: "A lentidão ocorre em todos os dispositivos ou só em um (ex: celular específico)?",
        opcoes: [
            { texto: "Só em um dispositivo específico", proximo: "lentidao_dispositivo" },
            { texto: "Em todos (TV, Celular, PC)", proximo: "teste_cabo" }
        ]
    },
    lentidao_dispositivo: { 
        pergunta: "DIAGNÓSTICO: Gargalo no Dispositivo do Cliente.", 
        solucao: "Problema não é a rede. O dispositivo pode estar antigo, com vírus, ou longe demais do roteador Wi-Fi.", 
        final: true 
    },
    teste_cabo: {
        pergunta: "Peça um teste de velocidade via CABO DE REDE (RJ45). O resultado bateu o plano contratado?",
        opcoes: [
            { texto: "Sim, no cabo a velocidade chega normal", proximo: "lentidao_wifi" },
            { texto: "Não, mesmo no cabo fica lento", proximo: "verificar_sinal_optico" }
        ]
    },
    lentidao_wifi: {
        pergunta: "DIAGNÓSTICO: Interferência Wi-Fi (Gargalo Clássico).",
        solucao: "O Wi-Fi 2.4GHz está saturado. Migrar cliente para 5GHz ou trocar canal.",
        final: true
    },
    verificar_sinal_optico: {
        pergunta: "Verifique o sinal óptico (dBm) na OLT. Ele está próximo do limite de sensibilidade (pior que -27dBm)?",
        opcoes: [
            { texto: "Sim, sinal muito fraco (-28, -30dBm...)", proximo: "atenuacao_alta" },
            { texto: "Não, sinal está ótimo (-15 a -25dBm)", proximo: "gargalo_rede" }
        ]
    },
    atenuacao_alta: {
        pergunta: "DIAGNÓSTICO: Atenuação Óptica Alta.",
        solucao: "Fibra pode estar 'estrangulada' (dobrada) ou conector sujo. Enviar técnico para corrigir.",
        final: true
    },
    gargalo_rede: {
        pergunta: "DIAGNÓSTICO: Gargalo de Uplink/Concentrador.",
        solucao: "Problema no seu Backbone: Link de saída saturado (horário de pico) ou OLT sobrecarregada. Verificar gráficos de tráfego.",
        final: true
    },

    // =================================================================
    // FLUXO 3: QUEDAS INTERMITENTES
    // =================================================================
    quedas: {
        pergunta: "As quedas têm um padrão de horário? (ex: todo dia às 18h)",
        opcoes: [
            { texto: "Sim, sempre no mesmo horário", proximo: "padrao_quedas" },
            { texto: "Não, é aleatório o dia todo", proximo: "verificar_logs_olt" }
        ]
    },
    padrao_quedas: {
        pergunta: "DIAGNÓSTICO: Interferência Externa ou Sobrecarga.",
        solucao: "Pode ser interferência elétrica (poste de luz que liga a noite) ou saturação de banda no horário de pico. Investigar ambiente.",
        final: true
    },
    verificar_logs_olt: {
        pergunta: "Verifique os logs da OLT. A ONU está desconectando por 'Dying Gasp' (falta de energia)?",
        opcoes: [
            { texto: "Sim, log mostra 'Dying Gasp'", proximo: "energia_instavel" },
            { texto: "Não, log mostra 'LOS' intermitente", proximo: "fibra_instavel" }
        ]
    },
    energia_instavel: {
        pergunta: "DIAGNÓSTICO: Energia Elétrica Instável.",
        solucao: "A rede elétrica do cliente está oscilando ou a fonte da ONU está com defeito. Testar com outra fonte/nobreak.",
        final: true
    },
    fibra_instavel: {
        pergunta: "DIAGNÓSTICO: Conexão Óptica Intermitente.",
        solucao: "Provável mau contato em conector ou fusão mal feita que falha com variação de temperatura (sol/chuva). Refazer conexões da CTO até o cliente.",
        final: true
    }
};

function iniciarFluxo(tipo) {
    mostrarEtapa(fluxos[tipo]);
}

function mostrarEtapa(etapa) {
    const container = document.getElementById('fluxoContainer');
    
    // Animação simples para suavizar a troca de perguntas
    container.style.opacity = 0;
    setTimeout(() => {
        let html = `<h4 class="card-title mb-4 fw-bold text-dark">${etapa.pergunta}</h4>`;

        if (etapa.final) {
            // Se for a etapa final (Solução)
            html += `
                <div class="alert alert-success border-success shadow-sm">
                    <h5><i class="bi bi-check-circle-fill text-success"></i> SOLUÇÃO SUGERIDA:</h5>
                    <p class="mb-0 fs-5">${etapa.solucao}</p>
                </div>
                <button class="btn btn-secondary mt-3 fw-bold px-4 py-2" onclick="location.reload()">
                    <i class="bi bi-arrow-counterclockwise"></i> Reiniciar Diagnóstico
                </button>
            `;
        } else {
            // Se for uma pergunta com opções
            html += `<div class="d-grid gap-3 col-md-10 mx-auto">`;
            etapa.opcoes.forEach(opcao => {
                let btnClass = "btn-outline-dark";
                if (opcao.texto.includes("vermelho") || opcao.texto.includes("Não")) btnClass = "btn-outline-danger";
                if (opcao.texto.includes("verde") || opcao.texto.includes("Sim")) btnClass = "btn-outline-success";

                html += `
                    <button class="btn ${btnClass} text-start p-3 fs-5 shadow-sm" onclick="mostrarEtapa(fluxos['${opcao.proximo}'])">
                        <i class="bi bi-arrow-right-circle-fill me-2"></i> ${opcao.texto}
                    </button>
                `;
            });
            html += `</div>`;
        }
        container.innerHTML = html;
        container.style.opacity = 1;
    }, 200); // Pequeno delay para a animação
}

// --- PARTE 2: SIMULADOR DE TERMINAL ---
const terminalInput = document.getElementById('terminalInput');
const terminalOutput = document.getElementById('terminalOutput');

if (terminalInput) {
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
    if (cmd === 'help') {
        printLine("Comandos disponíveis:");
        printLine("- ping [destino]: Testa conectividade ICMP.");
        printLine("- traceroute [destino]: Mostra a rota até o destino.");
        printLine("- clear: Limpa a tela.");
    } else if (cmd === 'clear') {
        terminalOutput.innerHTML = '';
    } else if (cmd.startsWith('ping ')) {
        const destino = cmd.split(' ')[1];
        if (!destino) { printLine("Uso: ping [ip_ou_dominio]"); return; }
        
        printLine(`PING ${destino} (simulado): 56 data bytes`);
        let count = 0;
        const interval = setInterval(() => {
            count++;
            if (count <= 4) {
                if (Math.random() > 0.1) {
                    const time = (Math.random() * 20 + 10).toFixed(1);
                    printLine(`64 bytes from ${destino}: icmp_seq=${count} ttl=54 time=${time} ms`);
                } else {
                    printLine(`Request timeout for icmp_seq=${count}`);
                }
            } else {
                clearInterval(interval);
                printLine(`--- ${destino} ping statistics ---`);
                printLine("4 packets transmitted, simulação finalizada.");
            }
        }, 1000);

    } else if (cmd.startsWith('traceroute ')) {
        printLine(`traceroute to ${cmd.split(' ')[1]} (simulado), 30 hops max, 60 byte packets`);
        setTimeout(() => { printLine(" 1  192.168.1.1 (Gateway Local)  2.1 ms  1.9 ms  2.0 ms"); }, 1000);
        setTimeout(() => { printLine(" 2  100.64.20.1 (CGNAT Provedor)  5.4 ms  5.2 ms  6.1 ms"); }, 2000);
        setTimeout(() => { printLine(" 3  200.200.200.1 (Borda ASN)  7.8 ms  7.5 ms  8.0 ms"); }, 3000);
        setTimeout(() => { printLine(" 4  * * * (Salto com bloqueio de ICMP)"); }, 4000);
        setTimeout(() => { printLine(" 5  8.8.8.8 (Destino)  15.2 ms  14.9 ms  15.5 ms"); }, 5000);
    } else {
        printLine(`Comando não reconhecido: ${cmd}. Digite 'help' para ajuda.`);
    }
}
