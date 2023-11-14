
// Abstract class to talk to ui-Elements

export default class Params {

    // Pass a function to be called, when the ui-Element changes
    constructor(submit) {
        this.submit = submit;
    }

    // Set the UI Element to the current values
    setParams(params) {
    }

    // Get the Params from the UI Element
    getParams() {
        return {};
    }

}

