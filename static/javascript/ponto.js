var relógioAtivo = true;
var intervalId;
window.onload = function() {
    document.getElementById('nome_usuario').value = nome_usuario;
    intervalId = setInterval(atualizarRelogio, 1000);
}

function baterPonto() {
    if (relógioAtivo) {
        relógioAtivo = false;
        clearInterval(intervalId); // Para o relógio
        var horarioAtual = new Date().toLocaleTimeString();
        document.getElementById('clock').style.display = 'none'; // Oculta o relógio
        document.getElementById('mensagem').innerText = `Ponto registrado às ${horarioAtual}. Tenha um bom dia ${nome_usuario}!`;
    } else {
        document.getElementById('mensagem').innerText = `O relógio já foi parado e o ponto registrado. Recarregue a página para reiniciar.`;
    }
}

function atualizarRelogio() {
    if (relógioAtivo) {
        var horarioAtualizado = new Date().toLocaleTimeString();
        document.getElementById('clock').innerText = `Olá, ${nome_usuario}! Horário atual: ${horarioAtualizado}`;
    }
}

function enviarParaServidor(valorRelogio) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/index/ponto", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // Monta o objeto de dados a serem enviados ao servidor
    var dados = {
        nome_usuario: nome_usuario,
        valor_relogio: valorRelogio
    };

    // Converte o objeto em formato JSON
    var jsonData = JSON.stringify(dados);

    // Envia a requisição
    xhr.send(jsonData);
}