import Params from './params.js';

export default class Vector extends Params {
    constructor(submit, id) {
        super(submit,id);
        this.coords = ['x', 'y', 'z'].map((c)=>document.getElementById(this.id+"_"+c));
        if (!this.coords.every((e)=>e!==undefined)) throw "coordinate elements not found!";
        // register callback
        this.coords.forEach((el)=>el.addEventListener('change', ()=>this.submit(this.getParams())));
    }

    getParams() {
        return {[this.id]: this.coords.map((c)=>c.value).join(",")};
    }

    setParams(params) {
        if (this.id in params) {
            for (let i=0; i<3; i++) {
                this.coords[i].value = Number(params[this.id][i]);
            }
        } else {
            console.log(`setParams called but key ${this.id} does not exist.`)
            console.log(params);
        }
    }

}

