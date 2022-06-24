function autogrow(textarea){
    textarea.style.boxSizing = 'border-box';
    var offset = textarea.offsetHeight - textarea.clientHeight;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + offset + 'px';

    textarea.addEventListener('input', function (event) {
        event.target.style.height = 'auto';
        event.target.style.height = event.target.scrollHeight + offset + 'px';
    });
    textarea.addEventListener('focus', function (event) {
        event.target.style.height = 'auto';
        event.target.style.height = event.target.scrollHeight + offset + 'px';
    });
}

document.querySelectorAll('textarea').forEach(function (element) {
    autogrow(element);
});
