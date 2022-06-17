//gtts
const gTTS = require('gtts');

function speakGtts(textoGtts){
  var gtts = new gTTS(textoGtts, 'es');
}

// R E C O N O C I M I E N T O    D E     V O Z
const btnStartRecord = document.getElementById('btnStartRecord');
const texto = document.getElementById("textInput");
//const btnplayText = document.getElementById('playText');
//const textoLeer = document.getElementById("mensaje");

let recognition = new webkitSpeechRecognition();
recognition.lang = 'es-ES';
recognition.continuous = false;
recognition.interimResults = false;

recognition.onresult = (event) => {
    const results = event.results;
    const frase = results[results.length - 1][0].transcript;
    texto.value += frase;
    console.log(texto.value);
}
recognition.onerror = (event) => {
    console.log(event.error);
}
recognition.onend = (event) => {
    console.log('Micro deja de grabar')
}
btnStartRecord.addEventListener('click',()=>{
    recognition.start();
    texto.focus();
});
/*
btnStopRecorbtnStopRecord.addEventListener('click',()=>{
    recognition.abort();
});d.addEventListener('click',()=>{
    recognition.abort();
});
btnplayText.addEventListener('click',()=>{
    const texto = document.getElementById('botText');
    leerTexto(texto.value);
});
*/
// R E S P U E S T A    C H A T B O T
function getBotResponse() {
  var rawText = $("#textInput").val();
  var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
  $("#textInput").val("");
  $("#chatbox").append(userHtml);
  document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });
  $.get("/get", { msg: rawText }).done(function(data) {
    var botHtml = '<div id="msg-read" class="botText">' + data + "</div>";
    $("#chatbox").append(botHtml);
    document
      .getElementById("userInput")
      .scrollIntoView({ block: "start", behavior: "smooth" });
  });
}
$("#textInput").keypress(function(e) {
  if (e.which == 13) {
    getBotResponse();
  }
});


//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

const IDIOMAS_PREFERIDOS = ["es-MX", "es-US", "es-ES", "es_US", "es_ES"];

// Esperar a que el que DOM cargue
document.addEventListener("DOMContentLoaded", () => {
  const $voces = document.querySelector("#voces"),
    $boton = document.querySelector("#btnEscuchar"),
    $botonStop = document.querySelector("#btnStop"),
    $mensaje = document.querySelector("#mensaje");
  let posibleIndice = 0, vocesDisponibles = [];

  // Función que pone las voces dentro del select
  const cargarVoces = () => {
    if (vocesDisponibles.length > 0) {
      console.log("No se cargan las voces porque ya existen: ", vocesDisponibles);
      return;
    }
    vocesDisponibles = speechSynthesis.getVoices();
    console.log({ vocesDisponibles })
    posibleIndice = vocesDisponibles.findIndex(voz => IDIOMAS_PREFERIDOS.includes(voz.lang));
    // if (posibleIndice === -1) posibleIndice = 0;
    // vocesDisponibles.forEach((voz, indice) => {
    //   const opcion = document.createElement("option");
    //   opcion.value = indice;
    //   opcion.innerHTML = voz.name;
    //   opcion.selected = indice === posibleIndice;
    //   $voces.appendChild(opcion);
    // });
  };

  // Si no existe la API, lo indicamos
  //if (!'speechSynthesis' in window) return alert("Lo siento, tu navegador no soporta esta tecnología");

  // No preguntes por qué pongo esto que se ejecuta dos veces
  // en determinados casos, solo así funciona en algunos casos
  cargarVoces();
  // Si hay evento, entonces lo esperamos
  if ('onvoiceschanged' in speechSynthesis) {
    speechSynthesis.onvoiceschanged = function () {
      cargarVoces();
    };
  }
  // El click del botón. Aquí sucede la magia
  $boton.addEventListener("click", () => {
    var x = document.getElementsByClassName("botText").length;
    let textoAEscuchar = document.getElementsByTagName("div")[x+1].textContent;
    //let textoAEscuchar = document.getElementById("msg-read").textContent;
    //let textoAEscuchar = $mensaje.value;
    //if (!textoAEscuchar) return alert("Escribe el texto");
    let mensaje = new SpeechSynthesisUtterance();
    //console.log($voces.value)
    mensaje.voice = vocesDisponibles[79];
    mensaje.volume = 1;
    mensaje.rate = 1;
    mensaje.text = textoAEscuchar;
    mensaje.pitch = 1;
    // ¡Parla!
    speechSynthesis.speak(mensaje);
  });

  $botonStop.addEventListener("click", () => {
    speechSynthesis.cancel();
  });
});

