import Params from './params.js';

export default class Text extends Params {
    constructor(submit, id) {
        super(submit, id);
        this.el.addEventListener('change', ()=>this.submit(this.getParams()));
    }
}

