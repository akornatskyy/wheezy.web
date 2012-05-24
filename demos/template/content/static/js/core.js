
String.prototype.format = function() {
    var args = arguments;
    return this.replace(/\{\d+\}/g, function(capture) {
        return args[capture.match(/\d+/)];
    });
}

function JSONForm(data, form) {
    $('input[type="password"]', form).val('');
    $(form).prev('span.error-message').remove();
    $('span.error', form).remove();
    $('.error', form).removeClass('error');
    $.each(data.errors, function(key, value) {
        if (key == '__ERROR__') {
            form.before('<span class="error-message">{0}</span>'.format(
                    value.pop()))
        }
        else {
            key = key.replace(/_/g, '-');
            $('label[for="{0}"]'.format(key), form).addClass('error')
            var field = $('#' + key, form);
            field.addClass('error');
            field.after('<span class="error">{0}</span>'.format(
                value.pop()));
        }
    });
}

function ajaxForm(selector, dataType) {
    if (!dataType) dataType = 'json'
    $(selector || 'input[type="submit"]:not(.noajax)').live('click', function(e) {
        submit = $(this);
        submit.attr('disabled', 'disabled');
        var form = submit.parents('form:first');
        var data = null;
        if (this.name) {
            data = form.serializeArray();
            data.push({name: this.name, value: ''});
            data = $.param(data);
        }
        else
            data = form.serialize();
        $.ajax({
            type: form.attr('method') || 'get',
            url: form.attr('action'),
            data: data,
            dataType: dataType,
            success: function(data, textStatus, jqXHR) {
                if (jqXHR.status == 207) {
                    window.location.replace(jqXHR.getResponseHeader('Location'));
                } else if (data.see_other) {
                    window.location.replace(data.see_other);
                } else if (dataType == 'json'){
                    submit.removeAttr('disabled');
                    JSONForm(data, form);
                }
            }
        });
        return false;
    });
}

$(document).ready(function() {
    ajaxForm();
})
