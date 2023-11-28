import Params from './params.js';

export default class Slider extends Params {
    // ui2param is function converting from the slider value to the parameter value
    // param2ui is function converting from the parameter value to the slider value 
    // Those two function are normally inverses of each other.
    constructor(submit, id, ui2param=(x)=>x, param2ui=(x)=>x) {
        super(submit, id);
        this.ui2param = ui2param;
        this.param2ui = param2ui;
        // register callback
        this.el.addEventListener('input', ()=>this.submit(this.getParams()));
    }

    getParams() {
        return {[this.id]:this.ui2param(this.el.value)};
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
