$(function() {

    $('#backup_all_st').click(function() {
        var action = 'backup_all_st'
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var command = "/index/" + action + "/"
        $.ajax({
            type: "post",
            url: command,
            data: {
                csrfmiddlewaretoken: token,
                'action': action
            },
            dataType: "json",
            success: function(response) {
                $('#gif_loading').html('<p><b>Backup concluído com sucesso!</b></p>');
                setTimeout(function() {
                    document.location.reload(true);
                }, 3000);
            },
            error: function(error) {
                $('#gif_loading').html('<p><b>Erro: corra para as montanhas!</b></p>');
                setTimeout(function() {
                    document.location.reload(true);
                }, 3000);
            }
        });
    });
    $('#scan_all_st').click(function() {
        var action = 'scan_all_st'
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var command = "/index/" + action + "/"
        $.ajax({
            type: "post",
            url: command,
            data: {
                csrfmiddlewaretoken: token,
                'action': action
            },
            dataType: "json",
            success: function(response) {
                $('#gif_loading').html('<p><b>Scan concluído com sucesso!</b></p>');
                setTimeout(function() {
                    document.location.reload(true);
                }, 3000);
            },
            error: function(error) {
                $('#gif_loading').html('<p><b>Erro: corra para as montanhas!</b></p>');
                setTimeout(function() {
                    document.location.reload(true);
                }, 3000);
            }
        });
    });

});