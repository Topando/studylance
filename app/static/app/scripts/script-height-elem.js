class HeightElem {
    constructor(props){
        let defaultConfig = {
            idElem: 'task-container',
        }
        this.config = Object.assign(defaultConfig, props);
        this.init();
    }

    init(){
        const windowInnerHeight = document.documentElement.clientHeight;
        var Elem = document.getElementsByClassName('task-container')[0],
            stylesElem = window.getComputedStyle(Elem),
            marginTopElem = stylesElem.getPropertyValue('margin-top');
        var body = document.getElementsByTagName('body')[0],
            stylesBody = window.getComputedStyle(body),
            paddingBottomBody = stylesBody.getPropertyValue('padding-bottom');

        var heightElemCalculated = windowInnerHeight - document.getElementsByClassName('header')[0].offsetHeight - parseInt(marginTopElem, 10) - parseInt(paddingBottomBody, 10);

        console.log(heightElemCalculated);
    }

}