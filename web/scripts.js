// Variável para armazenar o último conteúdo
let ultimoConteudo = null;

async function buscarComando() {
    try {
        console.log("Buscando comando...");
        // Usando cache-busting com timestamp
        const url = 'comando.json?' + new Date().getTime();
        const res = await fetch(url);

        if (!res.ok) throw new Error(`Erro ${res.status}: ${res.statusText}`);

        const comando = await res.json();
        console.log("Dados recebidos:", comando);

        document.getElementById('ultimaAtualizacao').textContent = new Date().toLocaleString();

        const conteudoAtual = JSON.stringify(comando, null, 2);

        if (conteudoAtual !== ultimoConteudo) {
            document.getElementById('comando').textContent = conteudoAtual;
            ultimoConteudo = conteudoAtual;
            console.log("Conteúdo atualizado!");
        }

    } catch (error) {
        console.error("Erro na requisição:", error);
        document.getElementById('comando').textContent = 'Erro: ' + error.message;
    } finally {
        setTimeout(buscarComando, 1000);
    }
}



function mudaBotaoGravar() {
    const botao = document.getElementById('toggleGravar')
    if (botao.getAttribute('class').includes('gravar')) {
        botao.classList.remove('gravar')
        botao.classList.add('parar')
        botao.innerHTML = 'PARAR'
        gravarComando();
    } else {
        botao.classList.remove('parar')
        botao.classList.add('gravar')
        botao.innerHTML = 'GRAVAR';
        salvarComando();
    }
}
function verHistorico() {
    if (document.querySelector('.camera-box').getAttribute('class').includes('active')) {
        document.querySelector('.historicoAcoes').style.display = '';
        document.querySelector('.camera-box').style.display = 'none';
        document.querySelector('.historicoAcoes').classList.add('active')
        document.querySelector('.camera-box').classList.remove('active')
    } else {
        document.querySelector('.historicoAcoes').style.display = 'none';
        document.querySelector('.camera-box').style.display = '';
        document.querySelector('.historicoAcoes').classList.remove('active');
        document.querySelector('.camera-box').classList.add('active');
    }

    const botao = document.getElementById('verHistorico')
    if (botao.getAttribute('class').includes('historico')) {
        botao.classList.remove('historico');
        botao.classList.add('camera');
        botao.innerHTML = 'CÂMERA';
    } else {
        botao.classList.remove('camera');
        botao.classList.add('historico');
        botao.innerHTML = 'HISTÓRICO';
        getHistoricoComandos();
    }

}

function listaHistoricoComandos(dados, quantidade) {
    const lista = document.querySelector('#listaHistorico');
    document.querySelector('#quantidadeHistorico').innerHTML = quantidade;
    lista.innerHTML = ''; // limpa o conteúdo antes de preencher

    for (let dado of dados) {
    lista.innerHTML += `
        <div id="${dado}" class="comandoSelecionar">
            ${formatarNomeArquivo(dado)}
            <br>
            <div class="linhaIcones">
                <div class="cardIcone Play"><i class="fa-solid fa-circle-play" onclick="executaComandoGravado(this)"></i></div>
                <div class="cardIcone Edit"><i class="fa-regular fa-pen-to-square" onclick="renomeiaComandoGravado(this)"></i></div>
                <div class="cardIcone Delete"><i class="fa-regular fa-trash-can" onclick="deletaComandoGravado(this)"></i></div>
            </div>
        </div>
    `;
}
}





function formatarNomeArquivo(nomeArquivo) {
    // Remove a extensão .json
    const base = nomeArquivo.replace('.json', '');

    // Extrai partes do nome
    const [prefixo, dataStr, horaStr] = base.split('_');

    // Formata data
    const ano = dataStr.slice(0, 4);
    const mes = dataStr.slice(4, 6);
    const dia = dataStr.slice(6, 8);
    const dataFormatada = `${dia}/${mes}/${ano}`;

    // Formata hora
    const hora = horaStr.slice(0, 2);
    const minuto = horaStr.slice(2, 4);
    const segundo = horaStr.slice(4, 6);
    const horaFormatada = `${hora}:${minuto}:${segundo}`;

    return `${prefixo}: ${dataFormatada} ${horaFormatada}`;
}
/////////////////////// SERVER /////////////////////////////////
function executaComandoGravado(comando) {
    fetch('http://localhost:5000/executar_comandos_gravados/' + comando.id)
        .then(response => response.json())
        .then(data => {
            console.log("[EXECUTAR COMANDO]", data);
        })
        .catch(error => console.error("[ERRO] ao executar comando gravado:", error));
}
function renomeiaComandoGravado(comando) {
    // fetch('http://localhost:5000/executar_comandos_gravados/' + comando.id)
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log("[EXECUTAR COMANDO]", data);
    //     })
    //     .catch(error => console.error("[ERRO] ao executar comando gravado:", error));
}
function deletaComandoGravado(comando) {
    // fetch('http://localhost:5000/executar_comandos_gravados/' + comando.id)
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log("[EXECUTAR COMANDO]", data);
    //     })
    //     .catch(error => console.error("[ERRO] ao executar comando gravado:", error));
}

function getHistoricoComandos() {
    // fetch('http://localhost:5000/listar_comandos_gravados')
    //     .then(response => response.json())
    //     .then(data => listaHistoricoComandos(data.arquivos, data.quantidade))
    //     .catch(error => console.error('Erro ao buscar histórico:', error));

    //TESTE ABAIXO

    const data = {
        "arquivos": [
            "comando_20250729_140003.json",
            "comando_20250729_134930.json",
            "comando_20250729_134149.json",
            "comando_20250729_133602.json",
            "comando_20250729_133310.json",
            "comando_20250729_131609.json",
            "comando_20250728_144314.json",
            "comando_20250728_142835.json",
            "comando_20250728_142635.json",
            "comando_20250728_142547.json",
            "comando_20250728_142002.json",
            "comando_20250728_141540.json",
            "comando_20250728_141335.json",
            "comando_20250728_141228.json",
            "comando_20250729_140003.json",
            "comando_20250729_134930.json",
            "comando_20250729_134149.json",
            "comando_20250729_133602.json",
            "comando_20250729_133310.json",
            "comando_20250729_131609.json",
            "comando_20250728_144314.json",
            "comando_20250728_142835.json",
            "comando_20250728_142635.json",
            "comando_20250728_142547.json",
            "comando_20250728_142002.json",
            "comando_20250728_141540.json",
            "comando_20250728_141335.json",
            "comando_20250728_141228.json",
            "comando_20250728_141205.json"
        ],
        "quantidade": 15,
        "status": "sucesso"
    };
    listaHistoricoComandos(data.arquivos, data.quantidade);
}

function gravarComando() {
    fetch('http://localhost:5000/gravar_data_comando')
        .then(response => response.json())
        .then(data => {
            console.log("[GRAVAR COMANDO]", data);
        })
        .catch(error => console.error("Erro ao gravar comando:", error));
}

function salvarComando() {
    fetch('http://localhost:5000/salvar_comando')
        .then(response => response.json())
        .then(data => {
            console.log("[SALVAR COMANDO]", data);
        })
        .catch(error => console.error("Erro ao salvar comando:", error));
}
