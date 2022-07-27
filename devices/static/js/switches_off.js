$(function() {

    //referente ao arquivo switches_off////////////////////////////////////////////

    var table_ = document.getElementById("table_switch_off");
    var lines = table_switch_off.getElementsByTagName("tr");

    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        line.addEventListener("click", function() {
            select_line(this, false); //Selecione apenas um
        });
    }

    function select_line(line) {
        var lines = line.parentElement.getElementsByTagName("tr");
        for (var i = 0; i < lines.length; i++) {
            var line_ = lines[i];
            line_.classList.remove("selecionado");
        }
        line.classList.toggle("selecionado");
    }
    /**
   Exemplo de como capturar os dados
   **/
    var btnVisualizar = document.getElementById("delete_st");

    btnVisualizar.addEventListener("click", function() {
        var selecionados = table_switch_off.getElementsByClassName("selecionado");
        //Verificar se está selecionado
        if (selecionados.length < 1) {
            alert("Selecione um dispositivo");
            return false;
        } else {
            $('#div_modal_disable_st').show();
        }

        var ip = "";
        var nome = "";

        for (var i = 0; i < selecionados.length; i++) {
            var selecionado = selecionados[i];
            selecionado = selecionado.getElementsByTagName("td");
            ip = selecionado[0].innerHTML;
            nome = selecionado[1].innerHTML;

            $('.modal-body').text('Tem certeza que deseja excluir o dispositivo: ' + ip)
            $('.modal-body').show();
        }
    });

    $('.disable_this_st').click(function() {
        $(document).on('click', '.link-check', function(e) {
            $thatRow = $(this);
        });
        $('#btn_delete').click(function() {
            $("#div_modal_disable_st").show();
            var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        });
    });

    // botão desabilitar do modal
    $('#btn_delete').click(function() {
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var ip = $('.modal-body').text().split(':')[1].trim();

        var request = $.ajax({
            type: "post",
            url: "/switches_disable/" + ip + "/",
            dataType: "html",
            data: {
                csrfmiddlewaretoken: token
            }
        });
        request.done(function(msg) {
            $("#div_modal_disable_st").hide();
            location.reload();

        });

        request.fail(function(jqXHR, textStatus) {
            alert("Erro: " + textStatus);
        });

    });
    // botão cancelar do modal
    $('#btn_cancel').click(function() {
        $("#div_modal_disable_st").hide();
    });

    //botão menu deslizante

    $('#disabled_sts').click(function() {
        $("#sliding-menu").show();
        console.log('abrir')
        document.getElementById("sliding-menu").style.right = "0px";
    });

    $('#close-menu').click(function() {
        let largura = window.screen.width;
        document.getElementById("sliding-menu").style.right = "-" + largura + "px";
    });

});