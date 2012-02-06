
/* Screens */

function signin() {
    $(this)
    .f1("#username[type='text']", "demo")
    .f2("#username[type='text']", "test")
    .f("#password", "P@ssw0rd")
    .s("input[name='logon']");
}

function signup() {
    $(this)
    .f("#username[type='text']", nextWord())
    .f("#display-name[type='text']", nextWord())
    .f("#email[type='text']", nextMail())
    .f("#date-of-birth[type='text']", nextDate(1941, 2000))
    .f("#password", "P@ssw0rd")
    .f("#confirm-password", "P@ssw0rd")
    .f("#answer", nextInt(1, 9))
    .s("input[name='register']");
}


/* Foundation */

document.onkeydown = function(event) {
    if (window.event) event = window.event;
    if (event.ctrlKey && event.keyCode != 17 /* Ctrl */
        || event.altKey && event.keyCode != 18 /* Alt */) {
        jQuery.fn.f = doIgnore;
        jQuery.fn.f1 = doIgnore;
        jQuery.fn.f2 = doIgnore;
        jQuery.fn.f3 = doIgnore;
        jQuery.fn.f4 = doIgnore;
        jQuery.fn.f5 = doIgnore;
        jQuery.fn.s = doIgnore;
        var autoFill = true;
        switch (event.keyCode ? event.keyCode : event.which ? event.which : null) {
            case 45: /* Insert */
                jQuery.fn.f = doReplace;
                break;
            case 46: /* Delete */
                jQuery.fn.f = doClear;
                break;
            case 49: /* 1 */
                jQuery.fn.f = doReplace;
                jQuery.fn.f1 = doReplace;
                break;
            case 50: /* 2 */
                jQuery.fn.f = doReplace;
                jQuery.fn.f2 = doReplace;
                break;
            case 51: /* 3 */
                jQuery.fn.f = doReplace;
                jQuery.fn.f3 = doReplace;
                break;
            case 52: /* 4 */
                jQuery.fn.f = doReplace;
                jQuery.fn.f4 = doReplace;
                break;
            case 53: /* 5 */
                jQuery.fn.f = doReplace;
                jQuery.fn.f5 = doReplace;
                break;
            case 33: /* PageUp */
            case 34: /* PageDown */
                jQuery.fn.f = doReplace;
                break;
            case 10: /* Enter */
            case 13:
                jQuery.fn.s = doSubmit;
                break;
            default:
                autoFill = false;
                break;
        }

        if (autoFill) autoFillScreen();
    }

    return true;
}

function autoFillScreen() {
    var container = $("#placeholder>div");
    var id = container.attr("id");
    if (!isFunction(id)) {
        if ($("form", container).length > 0)
            alert("Screen '{0}' is not available for auto complete yet.".format(id));
        else
            alert("Screen '{0}' has no form thus not applicable for auto complete.".format(id));
        return;
    }

    var screen = eval(id);
    $(screen);
}

function isFunction(name) {
    var type = eval("typeof(" + name + ")");
    return type == 'function';
}

function doReplace(selector, value) {
    var elements = $(selector+":not(:hidden)", this);
    if (elements.length == 0) return this;
    var element = elements[0];
    if (element.type == "checkbox" | element.type == "radio") {
        element.checked = value;
        elements.trigger('click');
        element.checked = value;
    }
    else {
        element.value = value;
        if (element.tagName == 'SELECT') {
            elements.trigger('click');
        }
    }

    return this;
}

function doClear(selector) {
    var elements = $(selector+":not(:hidden)", this);
    if (elements.length == 0) return this;
    var element = elements[0];
    if (element.type == "checkbox") {
        element.checked = false;
        elements.trigger('click');
        element.checked = false;
    }
    else {
        element.val("");
        if (element.tagName == 'SELECT') {
            elements.trigger('click');
        }
    }

    return this;
}

function doSubmit(selector) {
    $(selector != null ? selector : "input[type='submit']", this).click();
}

function doIgnore() {
    return this;
}

/* Random */

function nextBool() {
    return Math.random() < 0.5;
}

function nextWord(words) {
    words = words != null ? words : g_words;
    return words[nextInt(0, words.length - 1)];
}

function nextSentence(wordsNumber) {
    var sentence = nextWord();
    for (i = 1; i < wordsNumber; i++) {
        sentence += " " + nextWord();
    }

    return sentence;
}

function nextInt(min, max) {
    if (min == max) return min;
    if (min > max) return nextInt(max, min);
    return min + Math.floor(Math.random() * (max - min + 1));
}

function nextDate(min, max) {
    month = nextInt(1, 12)
    day = nextInt(1, 28)
    year = nextInt(min, max)
    return year + "/" + month + "/" + day
}

function nextOption(id, all) {
    if (all) start = 0; else start = 1;
    var options = $(id + " option");
    var count = options.length;
    if (count == 0)
        return 0;
    return options[nextInt(start, count-1)].value;
}

function nextMail() {
    return "{0}@{1}.com".format(nextWord(), nextWord());
}

var g_words = new Array("lorem", "ipsum", "dolor", "sit", "amet",
    "consetetur", "sadipscing", "elitr", "sed", "diam",
    "nonumy", "eirmod", "tempor", "invidunt", "ut", "labore", "et",
    "dolore", "magna", "aliquyam", "erat", "sed", "diam", "voluptua",
    "at", "vero", "eos", "accusam", "et", "justo", "duo", "dolores",
    "et", "ea", "rebum", "stet", "clita", "kasd", "gubergren", "no",
    "sea", "takimata", "sanctus", "est", "minim", "exercitation",
    "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "officia", "deserunt", "mollit");
