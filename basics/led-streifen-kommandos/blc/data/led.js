// Globale Variablen ist schlechte Praxis
// Dafür kann man die Funktionen direkt in den HTML-Elementen eintragen.

state = "off";
pwm = 0.25;
rateLimit = false;

function setPWMLabel() {
    let pwmlabel = document.getElementById('pwmlabel');
    pwmlabel.innerText = Math.round(pwm*1000)/10 + " %";
}

// Ruft die gleich URL mit den Parametern im
// Hintergrund auf. Die Seite im Browser wird nicht
// neu geladen. Allerdings wird hier als Antwort die
// ganze Seite gesendet, was überflüssig ist.
// Auf dem ESP würde es sich lohnen, eine zweite URL
// «ledcontrol» zu machen, die nur "OK" oder eine 
// Fehlermeldung liefert.

function makeGetRequest(url=null) {
    if (rateLimit) return;  // Keine parallelen Zugriffe erlauben
    rateLimit = true;
    // URL bauen (alles davor wird von der aktuellen URL übernommen)
    url = url ? url : `/cmd?state=${state}&pwm=${pwm}`;
    // Zugriff vorbereiten
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    // Callback wenn Zugriff fertig
    xhr.onload = () => { // callback, wenn Antwort da
        if (xhr.readyState == 4 && xhr.status == 200) {
            //console.log(xhr.response);
            console.log(`loaded ${url}`);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
        rateLimit = false; // Erste jetzt wieder sind Zugriffe erlaubt.
    };
    // Zugriff starten
    xhr.send();

}

function setState(newstate) {
    state=newstate;
    makeGetRequest();
}

function setPWM(newpwm) {
    pwm = newpwm;
    setPWMLabel();
    makeGetRequest();
}

function setLED(led) {
    makeGetRequest(`/cmd?led=${led}`);
}

// Erst wenn die Seite vollständig geladen ist, kann auf
// die einzelnen Elemente zugegriffen werden. 
window.addEventListener('load', function() {
    this.document.getElementById('pwm').value=pwm;
    setPWMLabel();
});