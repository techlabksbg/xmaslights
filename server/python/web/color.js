import Params from './params.js';

export default class Color extends Params {
    constructor(submit, id) {
        super(submit, id);
        this.el.addEventListener('change', ()=>this.submit(this.getParams()));
    }

    getParams() {
        return {[this.id]: this.el.value.substring(1)};
    }

    setParams(params) {
        console.log(params);
        console.log(this.id);
        this.el.value = "#"+params[this.id].map(e=>e.toString(16).padStart(2,'0')).join("");
    }
    
}

