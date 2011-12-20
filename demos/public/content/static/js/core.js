
String.prototype.format = function() {
    var pattern = /\{\d+\}/g;
    var args = arguments;
    return this.replace(pattern, function(capture) { return args[capture.match(/\d+/)]; });
}
