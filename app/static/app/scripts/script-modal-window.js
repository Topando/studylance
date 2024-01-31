class HystModal{

    constructor(props){
        let defaultConfig = {
            linkAttributeName: 'data-hystmodal',
        }
        this.config = Object.assign(defaultConfig, props);
        this.init();
    }

    init(){

        this.isOpened = false; // открыто ли окно
        this.openedWindow = false; //ссылка на открытый .hystmodal
        this._modalBlock = false; //ссылка на открытый .hystmodal__window
        //не нужно
        this.starter = false, //ссылка на элемент "открыватель" текущего окна
        this._nextWindows = false; //ссылка на .hystmodal который нужно открыть
        this._scrollPosition = 0; //текущая прокрутка (см. выше)

        //Обработчик событий
        this.eventsFeeler();
    }

    eventsFeeler(){
        document.addEventListener("click", function (e) {
            if (!this.openedWindow.id) {
                return;
            }
            let containingElement = document.querySelector("#" + this.openedWindow.id);
            if(!containingElement.contains(e.target) ) {
                e.preventDefault();
                this.close();
            }

        }.bind(this));

        document.addEventListener("click", function (e) {
            const clickedlink = e.target.closest("[" + this.config.linkAttributeName + "]");

            if (clickedlink) {
                e.preventDefault();
                this.starter = clickedlink;
                let targetSelector = this.starter.getAttribute(this.config.linkAttributeName);
                this._nextWindows = document.querySelector(targetSelector);
                this.open();
                return;
            }

            if (e.target.closest('[data-hystclose]')) {
                this.close();
                return;
            }
        }.bind(this));

        //клавиша escape
        window.addEventListener("keydown", function (e) {
            if (e.which == 27 && this.isOpened) {
                e.preventDefault();
                this.close();
                return;
            }

        }.bind(this));

    }

    open(selector){
        this.openedWindow = this._nextWindows;
        this._modalBlock = this.openedWindow.querySelector('.hystmodal__window');

        this._bodyScrollControl();
        this.openedWindow.classList.add("hystmodal--active");
        this.openedWindow.setAttribute('aria-hidden', 'false');

        this.isOpened = true;
    }

    close(){
        if (!this.isOpened) {
            return;
        }
        this.openedWindow.classList.remove("hystmodal--active");
        this.openedWindow.setAttribute('aria-hidden', 'true');

        //возвращаем скролл
        this._bodyScrollControl();
        this.isOpened = false;
    }

    _bodyScrollControl(){
        let html = document.documentElement;
        if (this.isOpened === true) {
            //разблокировка страницы
            html.classList.remove("hystmodal__opened");
            html.style.marginRight = "";
            window.scrollTo(0, this._scrollPosition);
            html.style.top = "";
            return;
        }
        //блокировка страницы
        this._scrollPosition = window.pageYOffset;
        html.style.top = -this._scrollPosition + "px";
        html.classList.add("hystmodal__opened");
    }

}

const myModal = new HystModal({
    linkAttributeName: 'data-hystmodal',
});