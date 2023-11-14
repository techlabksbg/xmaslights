import Slider from './slider.js';

window.addEventListener('load', function() {
    let currentParams = {};
    let sending = false;
    let uiElements = {
        'brightness':new Slider(sendParams, 'brightness', (x)=>x/100, (x)=>Math.floor(100*x)),
    };

    function setParams() {
        for (let key in currentParams) {
            if (key in uiElements) {
                console.log(`Setting ${key} to ${currentParams[key]}`);
                let o = {}
                o[key] = currentParams[key];
                uiElements[key].setParams(o);
            }
        }
    }

    function sendParams(pairs) {
        if (sending) return; // Do not send a request, before an old request has been answered.
        let query = [];
        for (let key in pairs) {
            query.push(encodeURI(key)+'='+encodeURI(pairs[key]));
        }
        let url = "?" + query.join("&");
        console.log(url);
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                try {
                    currentParams = JSON.parse(xmlHttp.responseText);
                    console.log(currentParams);
                    setParams();
                } catch (error) {
                    console.log(error);
                }
            }
            if (xmlHttp.readyState == 4) { // request finished, with whatever result
                sending = false;
            }
        }
        sending = true;
        xmlHttp.open("GET", url, true); // true for asynchronous 
        xmlHttp.send(null);
    }

    

    // get current params:
    sendParams({}); // empty object
});