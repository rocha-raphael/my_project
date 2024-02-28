var nome_usuario = "{{ nome_usuario }}"; // Defina o nome do usuário conforme necessário
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