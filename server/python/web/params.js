
// Abstract class to talk to ui-Elements

export default class Params {

    // Pass a function to be called, when the ui-Element changes
    constructor(submit, id) {
        this.submit = submit;
        this.id = id;
        this.el = document.getElementById(this.id);
        if (!this.el) {
            throw "No Element with id "+this.id;
        }
    }


    // Get the Params from the UI Element
    getParams() {
        return {[this.id]: this.el.value};
    }

    // Set the UI Element to the current values
    setParams(params) {
        if (this.id in params) {
            this.el.value = params[this.id];
        } else {
            console.log(`setParams called but key ${this.id} does not exist.`)
            console.log(params);
        }
    }

}

