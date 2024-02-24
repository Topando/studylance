const windowInnerWidth = document.documentElement.clientWidth;

if (windowInnerWidth <= 767) {
    var header = `
        <div class = 'header-logo'>
                <a href = '{% url "home" %}'>SL</a>
            </div>
            <div class = 'header-nav'>
                <a href = ''>
                    <img src = "{% static 'main/img/menu-icon.svg' %}">
                </a>
            </div>
    `;
    document.getElementsByClassName('header-main')[0].innerHTML = header;
}

