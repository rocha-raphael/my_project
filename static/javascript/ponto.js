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



function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else { 
        document.getElementById("location").innerHTML = "Geolocalização não é suportada por este navegador.";
    }
}

function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    document.getElementById("location").innerHTML = "Latitude: " + latitude + 
    "<br>Longitude: " + longitude;
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("location").innerHTML = "Usuário negou a solicitação de Geolocalização."
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("location").innerHTML = "Informação de localização indisponível."
            break;
        case error.TIMEOUT:
            document.getElementById("location").innerHTML = "A solicitação para obter a localização do usuário expirou."
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("location").innerHTML = "Ocorreu um erro desconhecido."
            break;
    }
}
function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    
    // Aqui você pode enviar a latitude e longitude para o servidor
    $.ajax({
        url: '/index/ponto/',
        type: 'POST',
        data: {
            'latitude': latitude,
            'longitude': longitude
        },
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.error(error);
        }
    });
}
