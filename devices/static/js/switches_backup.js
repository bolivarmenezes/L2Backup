$(function() {
    $('.bacukp_st').click(function() {
        $('.modal-backdrop').show();
        var ip = $(this).attr('id');
        var action = 'backup_st'
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var command = "/backup_switch/" + ip + "/" + action + "/"
        console.log(command);
        $.ajax({
            type: "post",
            url: command,
            data: {
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            success: function(response) {
                $('#exampleModal').modal('hide');
                console.log(response);
                document.location.reload(true);
            },
            error: function(error) {
                console.log(error);
                $('#gif_loading').hide();
                $('.modal-body').html('<p>Erro: verifique a <br>conectividade do switch</p>');
                setTimeout(function() {
                    $('#exampleModal').modal('hide');
                }, 3000);
            }
        });
    });

    $('.download_bacukp_st').click(function() {
        $('.modal-backdrop').show();
        var name = $(this).attr('id');
        var action = 'download_backup_st'
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            type: "post",
            url: "/backup_switch/" + name + "/" + action + "/",
            data: {
                csrfmiddlewaretoken: token,
                'action': action
            },
            dataType: "json",
            success: function(response) {
                $('#name_switch').text(name.replace('download_', ''));
                var line = ''
                if (typeof(response) == 'object') {
                    var path_url = '';
                    var date = '';
                    var id = '';
                    var array_url = [];
                    response.forEach(element => {
                        path_url = '/static/' + element["path"];
                        date = element["date_bkp"];
                        id = "id_" + date;
                        line += "<a id='" + id + "' href='" + path_url + "'> Data do backup: " + element["date_bkp"] + "</a><br>";
                    });
                    $('.modal-long-body').html(line);
                } else {
                    $('.modal-long-body').html(response);
                }
            },
            error: function(error) {
                $('#gif_loading').hide();
                $('.modal-long-body').html('<p>Erro: Algo errado não está certo</p>');
                setTimeout(function() {
                    $('#exampleModal').modal('hide');
                }, 3000);
            }
        });
    });

    $('#btn_all_backups').click(function() {
        $("#col1").hide();
        $("#col3").show();
        $("#col4").hide();
        $("#btn_all_backups").hide();
        $("#btn_overview_backups").show();
        $("#btn_backups_strategy").show();
    });

    $('#btn_backups_strategy').click(function() {
        $("#col1").hide();
        $("#col3").hide();
        $("#col4").show();
        $("#btn_all_backups").show();
        $("#btn_overview_backups").show();
        $("#btn_backups_strategy").hide();
    });

    $('#btn_overview_backups').click(function() {
        $("#col3").hide();
        $("#col4").hide();
        $("#col1").show();
        $("#btn_backups_strategy").show();
        $("#btn_all_backups").show();
        $("#btn_overview_backups").hide();
    });

    /**Busca, se hover, fotos do switche na base de dados *************************/
    function getPictureFromBase(param) {
        $.ajax({
            type: "get",
            url: "/get_picture_switch/",
            data: {
                'param': param
            },
            dataType: "json",
            success: function(response) {
                var line = ''
                console.log(response)
                if (Object.keys(response).length == 0) {
                    line += `<br><br><a href="/switches_pictures/"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash" viewBox="0 0 16 16">
                    <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"/>
                    <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"/>
                    <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"/>
                  </svg></a><br><br>`;
                }
                for (let name in response) {
                    line += `
                    <img class="pic_st_base" id="${response[name].fields.name}" src="/media/${response[name].fields.st_picture}">
                    `;
                }
                $('.modal-long-body').html(line);
            }
        });

    }

    /**clica em chama a função de buscar foto */
    $('.pictures_st').click(function(e) {
        e.preventDefault();
        let param = $(this).attr('id').split('_')[1]
        console.log(param)
        $('#name_switch_picture').text(param)
        getPictureFromBase(param)
    });

});