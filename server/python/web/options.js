import Params from './params.js';

export default class Options extends Params {
    // ui2param is function converting from the slider value to the parameter value
    // param2ui is function converting from the parameter value to the slider value 
    // Those two function are normally inverses of each other.
    constructor(submit, id) {
        super(submit);
        this.id = id;
        this.el = document.getElementById(this.id);
        if (!this.el) {
            throw "No Element with id "+this.id;
        }
        this.el.addEventListener('change', ()=>this.submit(this.getParams()));
    }

    getParams() {
        return {[this.id]: this.el.value};
    }

    setParams(params) {
        if (this.id in params) {
            this.el.value = params[this.id];
        } else {
            console.log(`setParams called but key ${this.id} does not exist.`)
            console.log(params);
        }
    }

}

