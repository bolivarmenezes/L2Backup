$(function() {


    /**Envia imagem para a base de dados************************************** */
    function getExif(img) {
        EXIF.getData(img, function() {
            var allMetaData = EXIF.getAllTags(this);
            $("#metadata").val(JSON.stringify(allMetaData, null, "\t"))
                //var allMetaDataSpan = document.getElementById("metadata");        
                //allMetaDataSpan.innerHTML = JSON.stringify(allMetaData, null, "\t");
        });
    }

    function clearView() {
        $('#inputFilePic').change(function() {
            $('.choosePicPreview img').attr('src', '')
        })
    }


    function getMetaData() {
        try {
            getExif(document.getElementById("preview"))
        } catch (error) {
            //console.log(error)
        }
    }

    function escondeMostra() {
        $("#linkMetadata").click(function(e) {
            getMetaData()
            if (document.getElementById("metadata_textarea").style.display == "none") {
                document.getElementById("metadata_textarea").style.display = "";
            } else {
                document.getElementById("metadata_textarea").style.display = "none";
            }
        });
    }

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
                if (Object.keys(response).length == 0) {
                    line += `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash" viewBox="0 0 16 16">
                    <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"/>
                    <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"/>
                    <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"/>
                  </svg>`;
                }
                for (let name in response) {
                    line += `<a href="#" value="${response[name].fields.metadata_pic}"><img class="pic_st_base" id="${response[name].fields.name}" src="/media/${response[name].fields.st_picture}">`;
                    //console.log(name)
                }
                $('.picture_save').html(line);
            }
        });

    }
    /*********************************************************************************** */

    /**Filtra por nome do switch */

    function choose_name() {
        $('.search_a').click(function(e) {
            let name = $(this).attr('id')
            $("#id_name").val(name)
            $('#search').html('')
                /**Chama a função que busca as fotos já salvas */
            getPictureFromBase(name)
        });
    }
    /************************************************************************************ */

    $('input#id_name').keyup(function() {
        var param = $("#id_name").val()

        /** Converte para minúsculo*/
        $("#id_name").val(param.toLowerCase())

        $.ajax({
            type: "get",
            url: "/filter_switch/",
            data: {
                'param': param,
            },
            dataType: "json",
            success: function(response) {
                var line = ''

                for (let name in response) {
                    line += '<a href="#" class="search_a" id="' + response[name].fields.name + '"><div class="line_a">' + response[name].fields.name + '</div></a>';
                }
                $('#search').html(line);
                choose_name()
                if (param.length == 0) {
                    $('#search').html('');
                }
            }
        });

    });

    /**reduz a qualidade da imagem e submete o formulário */
    function compact_and_send(file) {
        document.getElementById("sendImg").addEventListener('click', (e) => {
            e.preventDefault();
            //document.getElementById('inputFilePic').addEventListener('change', (e) => {        
            var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            var name = document.getElementById('id_name').value;
            var metadata = document.getElementById('metadata').value;
            var observation = document.getElementById('observation_id').value;

            if (!file) {
                return;
            }

            new Compressor(file, {
                quality: 0.4,

                // The compression process is asynchronous,
                // which means you have to access the `result` in the `success` hook function.
                success(result) {
                    const formData = new FormData();

                    // The third parameter is required for server
                    formData.append('st_picture', result, result.name);
                    formData.append('name', name);
                    formData.append('metadata_pic', metadata);
                    formData.append('observation', observation);
                    formData.append('csrfmiddlewaretoken', token);

                    // Send the compressed image file to server with XMLHttpRequest.
                    axios.post('/switches_pictures/', formData).then(() => {
                        /**Limpa a dive com a foto recem enviada */
                        $('.choosePicPreview img').attr('src', '')

                        /**busca e mostra todas as fotos no servidor */
                        getPictureFromBase(name)

                        /** esconde o text area dos metadados */
                        document.getElementById("metadata_textarea").style.display = "none";
                    });
                },
                error(err) {
                    console.log(err.message);
                    $('#gif_loading').hide();
                    $('.modal-body').html('<p>Erro: corra para as montanhas');
                },
            });
        });
    }

    function readURL(input) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                $('#preview').attr('src', e.target.result);
                clearView()
                escondeMostra()
                setTimeout(() => {
                    getMetaData()
                }, 100);
            }

            reader.readAsDataURL(input.files[0]);
            compact_and_send(input.files[0])
        }
    }

    $("#inputFilePic").change(function() {
        readURL(this);
    });

    /**limpar formulário */

    $('#reset_form').click(function() {
        $('#formPic input').val("");
        $('.picture_save').html('')
        $('#observation_id').val('')
        $('.choosePicPreview img').attr('src', '')
    });

});