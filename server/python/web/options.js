import Params from './params.js';

export default class Options extends Params {
    constructor(submit, id) {
        super(submit, id);
        // register callback
        this.el.addEventListener('change', ()=>this.submit(this.getParams()));
    }

    setParams(params, controls=null) {
        if (this.id in params) {
            this.el.value = params[this.id];
            if (controls) {
                // Toggle control elements
                if (!controls.includes('prg')) controls.push('prg');
                document.querySelectorAll(".parameter").forEach((el)=>{
                    if (controls.includes(el.id)) {
                        el.parentNode.style.display = null;
                    } else {
                        el.parentNode.style.display = "none";
                    }
                });
            }
        } else {
            console.log(`setParams called but key ${this.id} does not exist.`)
            console.log(params);
        }
    }

}

