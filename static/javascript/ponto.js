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

function obterLocalizacao() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(enviarLocalizacao, mostrarErro);
  } else { 
    alert("Geolocalização não é suportada por este navegador.");
  }
}

function enviarLocalizacao(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;

  // Aqui você pode enviar os dados para o servidor Django
  fetch('/caminho-para-sua-view/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Inclua isso se estiver usando CSRF tokens em suas forms Django
      'X-CSRFToken': getCookie('csrftoken'), 
    },
    body: JSON.stringify({latitude: latitude, longitude: longitude})
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch((error) => console.error('Erro:', error));
}

function mostrarErro(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      alert("Usuário negou a solicitação de Geolocalização.");
      break;
    case error.POSITION_UNAVAILABLE:
      alert("Informação de localização indisponível.");
      break;
    case error.TIMEOUT:
      alert("A solicitação para obter a localização do usuário expirou.");
      break;
    case error.UNKNOWN_ERROR:
      alert("Ocorreu um erro desconhecido.");
      break;
  }
}

// Função para obter o valor do cookie, útil para CSRFToken
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}