$(function() {
    $('.scan_st').click(function () {
        $('.modal-backdrop').show();
        var ip = $(this).attr('id');
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            type: "post",
            url: "/update_switch/" + ip + "/",
            data: {
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                setTimeout(function() {
                  $('#exampleModal').modal('hide');
                }, 300);
                document.location.reload(true);
            },
            error: function (error){
                $('#gif_loading').hide();
                $('.modal-body').html('<p>Erro: verifique a <br>conectividade do switch</p>');
                setTimeout(function() {
                    $('#exampleModal').modal('hide');
                }, 3000);
            }

        });

    });

    $('#mac_to_vendor').click(function () {
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var ip = $('#ipSt').text()
        $.ajax({
            type: "post",
            url: "/mac_to_vendor/" + ip + "/",
            data: {
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                var line = '<tr><th>Marca</th><th>MAC</th></tr>'
                for (let vendor in response) {
                    line += '<tr><td>' + vendor + '</td><td>' + response[vendor] + '</td></tr>';
                }
                $('#gif_loading2').hide()
                $('#tbody_mac_to_vendor').html(line)


            }
        });

    });
});