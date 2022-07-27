$(function() {
    function stS1() {
        $("#id_mac").attr("value", "NaN")
        $("#id_mac").hide()
        $("#id_vendor").attr("value", "NaN")
        $("#id_vendor").hide()
        $("#id_ip").show()
        $("#id_ip").attr("value", "")
        $("#id_name").attr("value", "")
        $("#id_community").show()
        $("#id_snmp_version").show()
        $("#id_model").attr("value", "NaN")
        $("#id_model").hide()
        $("#id_patrimony").attr("value", "NaN")
        $("#id_patrimony").hide()
        $("#id_location").attr("value", "NaN")
        $("#id_location").hide()
        $(".s2").css("font-size", "0.5em");
        $(".s1").css("font-size", "1em");
        $("#messages").hide()
        $("#id_disable_scan").attr("value", "0")
        $("#id_online").attr("value", "1")

    }
    /**sem gerencia */
    function stS2() {
        $("#id_mac").attr("value", "00:00:00:00:00:00")
        $("#id_mac").hide()
        $("#id_vendor").attr("value", "")
        $("#id_vendor").show()
        $("#id_ip").hide()
        $("#id_ip").attr("value", "127.0.0.1")
        $("#id_name").attr("value", "SEMGERENCIA")
        $("#id_community").hide()
        $("#id_snmp_version").hide()
        $("#id_model").show()
        $("#id_model").attr("value", "")
        $("#id_patrimony").show()
        $("#id_patrimony").attr("value", "")
        $("#id_location").show()
        $("#id_location").attr("value", "")
        $(".s1").css("font-size", "0.5em");
        $(".s2").css("font-size", "1em");
        $("#messages").hide()
        $("#id_disable_scan").attr("value", "1")
        $("#id_online").attr("value", "0")
    }

    function validaMac() {
        mac = $('#id_mac');
        var macFormat = /^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$/;
        if (mac.val().match(macFormat)) {
            mac.css("background-color", "white");
            mac.css("border-color", "green");
            mac.css("box-shadow", "0px 0px 10px green");
            return true;
        } else {
            mac.css("box-shadow", "0px 0px 10px red");
            mac.css("border-color", "red");
            return false;
        }
    }

    $('#id_mac').keyup(function() {
        mac = $('#id_mac').val().toUpperCase();
        $('#id_mac').val(mac);
        validaMac();
    });


    $('.s1').click(function() {
        $("#form_create_switch").show();
        stS1()
    });
    $('.s2').click(function() {
        $("#form_create_switch").show();
        stS2()
    });

    $("#form_create_switch").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            type: "post",
            url: "/switches_create/",
            data: form.serialize(),
            dataType: "json",
            success: function(response) {
                if (typeof(response) == 'object') {
                    $("#message").html(response.join('<br>'))
                } else {
                    $("#message").html(response)
                    document.getElementById("form_create_switch").reset();
                }
            },
            error: function(error) {
                $("#message").text(error)
            }
        });
    });
});