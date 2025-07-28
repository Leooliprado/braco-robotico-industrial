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
    } else {
        botao.classList.remove('parar')
        botao.classList.add('gravar')
        botao.innerHTML = 'GRAVAR'
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
        document.querySelector('.historicoAcoes').classList.remove('active')
        document.querySelector('.camera-box').classList.add('active')
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
    }

}