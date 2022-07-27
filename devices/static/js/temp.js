$(function() {
    function clearView() {
        $('#inputFilePic').change(function() {
            $('.choosePicPreview img').remove()
        })
    }

    function readImage() {

        $('#inputFilePic').change(function() {
            let allFiles = $(this)[0].files
            let line = '';
            for (let i = 0; i < allFiles.length; i++) {
                const fileReader = new FileReader()
                fileReader.onloadend = function() {
                    line = `<img class="preview" src="${fileReader.result}"></img>`
                    $('.choosePicPreview').append(line);
                }
                fileReader.readAsDataURL(allFiles[i])
            }
            clearView()

        })
    }

    // Evento Submit do formulário
    $('#formPic').submit(function() {
        $('#gif_loading').show();
        // Captura os dados do formulário
        var formulario = document.getElementById('formPic');
        // Instância o FormData passando como parâmetro o formulário
        var formData = new FormData(formulario);
        // Envia O FormData através da requisição AJAX
        $.ajax({
            url: "src/DB/DBInterfaceInsert.php",
            type: "POST",
            data: formData,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function(retorno) {
                console.log(retorno['response'])
            },
            error: function(err) {
                console.log(err)
            }
        });
        return false;
    });

    $("#pictiure-for").click(function() {
        $('#gif_loading').hide();
        readImage()
    })


});