$(function() {
    var predios = ["2-ITSM",
        "4-CRECHE",
        "6-IMPRENSA",
        "7-CT",
        "8-INPE",
        "9B-CT",
        "9D-CT",
        "9E-CT",
        "9F-CAU",
        "10-CTLAB",
        "13-CCNE",
        "13A-CCNE",
        "13B-CCNE",
        "14-NTE",
        "15-NAPO",
        "16-CE",
        "19-BASE",
        "20-BASE",
        "21-BASE",
        "26-CCS",
        "26D-TO",
        "26E-FONO",
        "26F-ODONTO",
        "28-CCS",
        "30-BC",
        "31-RU1",
        "31-UNIAO",
        "31A-RU2",
        "32-CEU2",
        "40-CAL",
        "40A-CAL",
        "40B-CAL",
        "40C-CAL",
        "42-CCR ",
        "44-CCR",
        "44C-CCR",
        "44E-NTA",
        "44F-NESAF",
        "44G-LARP",
        "44J- LABGEO",
        "46-NIDAL",
        "47-ADM",
        "48A-CPD",
        "48B-COPERVES",
        "48C-CQVS",
        "48D-PROGRAD",
        "48D-PRAE",
        "51-CEFD",
        "61H-AGITTEC",
        "62B-COMUNICA",
        "62E-MULTIUSO",
        "63-CCR",
        "64A-ALMOX",
        "67-ANIMA",
        "68-IRRIGA",
        "70A-POLITEC",
        "70G-POLITEC",
        "74A-CCSH",
        "74D-CCSH",
        "76-VIVEIRO",
        "77-CCR",
        "78-CCR",
        "97-HVU"
    ];

    var numberOfFloors = 11;
    var numberOfRacks = 15;

    var predio = ""
    var andar = ""
    var rack_nome = ""
    var salaCorredor = ""
    var numero_sala = ""

    /** *************************/
    var optionsBuild = "<option marked>PRÉDIO/CENTRO</option>"
    predios.forEach(element => {
        /**adiciona os options no dropdown */
        optionsBuild += `<option value="${element}">${element}</option>`
    });
    $("#id_building").html(optionsBuild)

    /** *************************/
    var optionsFloor = "<option marked>ANDAR</option>"
    optionsFloor += `<option value="0">Andar 0 (subsolo)</option>`
    optionsFloor += `<option value="0">Andar 1 (térreo)</option>`
    for (let index = 2; index < numberOfFloors; index++) {
        optionsFloor += `<option value="${index}">Andar ${index}</option>`
    }
    $("#id_floor").html(optionsFloor)

    /** *************************/

    var optionsRack = "<option marked>RACK</option>"
    for (let index = 1; index < numberOfRacks; index++) {
        optionsRack += `<option value="${index}">Rack ${index}</option>`
    }
    /** *************************/
    $("#id_rack").html(optionsRack)
    $("#location_generate").submit(function(e) {
        e.preventDefault();
        predio = $("#id_building").val()
        andar = $("#id_floor").val()
        rack_nome = $("#id_rack").val()
        salaCorredor = document.querySelector('input[name="sala_corredor"]:checked').value;
        numero_sala = $("#number_room").val()
        $("#id_location").attr('value', `${predio}_R${andar}${rack_nome}_${salaCorredor}${numero_sala}`)

    });
    /** *************************/
    $("#id_rack").html(optionsRack)

});