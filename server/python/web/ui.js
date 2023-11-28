import Slider from './slider.js';
import Options from './options.js';
import Text from './options.js';
import Vector from './vector.js';

window.addEventListener('load', function() {
    let currentParams = {};
    let sending = false;
    let uiElements = {
        'brightness':new Slider(sendParams, 'brightness', (x)=>(x*x/10000), (x)=>Math.floor(100*Math.sqrt(x))),
        'saturation':new Slider(sendParams, 'saturation', (x)=>x/100, (x)=>Math.floor(100*x)),
        'scale':new Slider(sendParams, 'scale', (x)=>5*Math.pow(100,x/100), (x)=>Math.floor(Math.log(x/5)/Math.log(100)*100)),
        'period':new Slider(sendParams, 'period', (x)=>(x*x/10000)*20+1, (x)=>Math.floor(Math.sqrt((x-1)/20)*100)),
        'prg':new Options(sendParams, 'prg'),
        'text':new Text(sendParams, 'text'),
        'dir':new Vector(sendParams, 'dir'),
        'umdrehungen':new Slider(sendParams, 'umdrehungen', (x)=>x/5, (x)=>Math.floor(5*x)),    
    };

    function setParams() {
        console.log(currentParams);
        if ('webconfig' in currentParams) {
            let selection = document.getElementById('prg');
            selection.innerHTML="";
            let html = "";
            for (let prg in currentParams['webconfig']) {
                html += `<option value="${prg}">${prg}</option>\n`;
            }
            selection.innerHTML = html;
        }
        for (let key in currentParams) {
            if (key in uiElements) {
                //console.log(`Setting ${key} to ${currentParams[key]}`);
                if (key=='prg') {
                    uiElements[key].setParams({[key] : currentParams[key]}, currentParams['webconfig'][currentParams['prg']]);
                } else {
                    uiElements[key].setParams({[key] : currentParams[key]});
                }
            }
        }
    }

    function sendParams(pairs) {
        if (sending) return; // Do not send a request, before an old request has been answered.
        let query = [];
        for (let key in pairs) {
            query.push(encodeURIComponent(key)+'='+encodeURIComponent(pairs[key]));
        }
        let url = "?" + query.join("&");
        console.log(url);
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                try {
                    currentParams = JSON.parse(xmlHttp.responseText);
                    //console.log(currentParams);
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