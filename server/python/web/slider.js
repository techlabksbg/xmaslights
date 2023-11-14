import Params from './params.js';

export default class Slider extends Params {
    // ui2param is function converting from the slider value to the parameter value
    // param2ui is function converting from the parameter value to the slider value 
    // Those two function are normally inverses of each other.
    constructor(submit, id, ui2param=(x)=>x, param2ui=(x)=>x) {
        super(submit);
        this.ui2param = ui2param;
        this.param2ui = param2ui;
        this.id = id;
        this.el = document.getElementById(this.id);
        if (!this.el) {
            throw "No Element with id "+this.id;
        }
        this.el.addEventListener('change', ()=>this.submit(this.getParams()));
    }

    getParams() {
        let o = {};
        o[this.id] = this.ui2param(this.el.value);
        return o;
    }

    setParams(params) {
        if (this.id in params) {
            //console.log(`param2ui(${params[this.id]}) = ${this.param2ui(params[this.id])}`);
            this.el.value = this.param2ui(params[this.id]);
        } else {
            console.log(`setParams called but key ${this.id} does not exist.`)
            console.log(params);
        }
    }

}