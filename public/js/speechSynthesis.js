import * as buttonBehavior from "./buttonBehavior.js";
const synthetizer = window.speechSynthesis;
let voices = [];
let pitch = 1.0;
let rate = 1.0;
export let selected_voice;
let selected_language="es"
document.body.onload = () =>{
    voices = synthetizer.getVoices();
    if (voices.length < 1) {
        console.log("Tu navegador no tiene voces disponibles.");
        return -1;
    } else {
        // Seleccionar la voz adecuada según el idioma
        if (selected_language === "es") {
            console.log("Voz en español");
            selected_voice = voices.find(voice => voice.lang.includes("es-US"));
        } else if (selected_language === "ja") {
            console.log("Voz en japonés");
            selected_voice = voices.find(voice => voice.lang.includes("ja"));
        }
        if (!selected_voice) {
            console.log("No se encontró una voz para el idioma seleccionado.");
            return -1;
        }
    }
}
/*
let temporal_voices = synthetizer.getVoices();
    for(let voice of temporal_voices){
        if(voice.lang.includes("es")>0){
            voices.push(voice);
        }
    }

    
    if(voices.length<1){
        console.log("Tu navegador no tiene voces en español.");
        return -1;
    }
    else if(voices.length==1){
        selected_voice = voices[0];
    }
    else{
        for(let voice of voices){
            if(voice.lang.includes("US")){
                selected_voice = voice;
            }
        }
        if(!selected_voice){
            selected_voice = voices[0]
        }
    }
*/

let onendSynthetizer = console.log;

export const set_onEnd_synthetizer = (callback) =>{
    onendSynthetizer = callback
}

export const say = (text) =>{
    const current_utterance = new SpeechSynthesisUtterance(text);
    //current_utterance.lang = selected_voice.lang;
    current_utterance.voice = selected_voice;
    current_utterance.pitch = pitch;
    current_utterance.rate = rate;
    current_utterance.onend = (e)=> {
            onendSynthetizer()
    };  
    current_utterance.onerror = (e) => {
        console.error("SpeechSynthesisUtterance.onerror",e);
      };
  
    synthetizer.speak(current_utterance);
}

export const change_pitch = (value) => {
    if(Number(value)==NaN){
        console.log("El pitch tiene que ser numerico")
        return -1;
    }
    else if(value<0){
        console.log("El pitch no puede ser negativo, asignando 0.1");
        pitch = 0.1;
    }else if(value>2.0){
        console.log("El pitch no puede ser mayor de 2.0, asignando 2.0")
        pitch = 2.0
    } else{
        pitch = value;
    }
}

export const change_rate = (value) => {
    if(Number(value)==NaN){
        console.log("El rate tiene que ser numerico")
        return -1;
    }
    else if(value<0){
        console.log("El rate no puede ser negativo, asignando 0.1");
        rate = 0.1;
    }else if(value>2.0){
        console.log("El rate no puede ser mayor de 2.0, asignando 2.0")
        rate = 2.0
    }else{
        rate = value;
    }
}

// Event listener para el cambio en el combo box
document.getElementById("combo-lang").addEventListener("change", function() {
    if (this.value === "1") {
        console.log("Español");
        selected_language = "es";
        configurarVoz();
    } else if (this.value === "2") {
        console.log("Japonés");
        selected_language = "ja";
        configurarVoz();
    }
    
});

function cargarVoces() {
    voices = synthetizer.getVoices();
    if (voices.length < 1) {
        console.log("Tu navegador no tiene voces disponibles.");
        return -1;
    } else {
        // Seleccionar la voz adecuada según el idioma
        if (selected_language === "es") {
            selected_voice = voices.find(voice => voice.lang.includes("US"));
        } else if (selected_language === "ja") {
            selected_voice = voices.find(voice => voice.lang.includes("JA"));
        }
        if (!selected_voice) {
            console.log("No se encontró una voz para el idioma seleccionado.");
            return -1;
        }
    }
}

function configurarVoz() {
    cargarVoces();
    if (!selected_voice) {
        console.log("No se pudo configurar la voz.");
        return -1;
    }
}


export default voices;

