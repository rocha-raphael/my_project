
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
        document.getElementById('mensagem').innerText = `Ponto registrado às ${horarioAtual}. Tenha um bom dia, ${nome_usuario}!`;
        document.getElementById('clock').innerText = ``;
    } else {
        document.getElementById('mensagem').innerText = `O relógio já foi parado e o ponto registrado. Recarregue a página para reiniciar.`;
        document.getElementById('clock').innerText = ``;
    }
}

function atualizarRelogio() {
    if (relógioAtivo) {
        var horarioAtualizado = new Date().toLocaleTimeString();
        document.getElementById('clock').innerText = `Olá, ${nome_usuario}! Horário atual: ${horarioAtualizado}`;
    } else {
        document.getElementById('clock').innerText = ``;
    }
}