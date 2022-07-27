{ % extends 'base.html' % } { % load static % } { % block content % } <
link rel = "stylesheet"
href = "{% static 'css/switches_create.css' %}" >
    <
    link rel = "stylesheet"
href = "{% static 'css/location.css' %}" >
    <
    div class = "container" >
    <
    div class = "change_type" >
    <
    a href = "#" >
    <
    div class = "s1" > Com Gerência < /div> < /
    a > <
    a href = "#" >
    <
    div class = "s2" > Sem Gerência < /div> < /
    a > <
    /div> <
div class = "change_form" >
    <
    form method = "post"
id = "form_create_switch"
style = "display:none ;" > { % csrf_token % } <
    tr >
    <
    td > < input type = "text"
name = "ip"
placeholder = "Endereço IP"
maxlength = "50"
id = "id_ip" > < /td> < /
    tr > <
    tr >
    <
    td > < input type = "text"
name = "mac"
placeholder = "Endereço MAC"
maxlength = "50"
id = "id_mac" > < /td> < /
    tr > <
    tr >
    <
    td > < input type = "text"
name = "name"
placeholder = "Hostname"
maxlength = "50"
id = "id_name" > < /td> < /
    tr > <
    tr >
    <
    td > < input type = "text"
name = "vendor"
placeholder = "Marca"
maxlength = "50"
id = "id_vendor" > < /td> < /
    tr > <
    tr >
    <
    td > < input type = "text"
name = "model"
placeholder = "Modelo"
maxlength = "50"
id = "id_model" > < /td> < /
    tr > <
    tr >
    <
    td >
    <
    select name = "community"
id = "id_community" >
    <
    option value = "public"
selected > public < /option> <
option value = "public" > public < /option> <
option value = "UFSMcomunidade" > UFSMcomunidade < /option> <
option value = "UFSM2002n" > UFSM2002n < /option> < /
    select > <
    /td> < /
    tr > <
    tr >
    <
    select name = "snmp_version"
id = "id_snmp_version" >
    <
    option value = "1" > SNMP v1 < /option> <
option value = "2"
selected > SNMP v2c < /option> <
option value = "3" > SNMP v3 < /option> < /
    select > <
    /tr> <
tr >
    <
    td > < input type = "text"
name = "patrimony"
placeholder = "Patrimônio"
maxlength = "50"
id = "id_patrimony" > < /td> < /
    tr > <
    tr >
    <
    td > < input type = "text"
name = "location"
placeholder = "Localização"
maxlength = "100"
id = "id_location"
data - bs - toggle = "modal"
data - bs - target = "#doLocation" >
    <
    /td> < /
    tr > <
    input type = "text"
name = "disable_scan"
id = "id_disable_scan"
hidden >
    <
    input type = "text"
name = "online"
id = "id_online"
hidden >
    <
    input type = "submit"
id = "createSt"
autocomplete = "off"
value = "Cadastrar"
data - bs - toggle = "modal"
data - bs - target = "#doCreate" >
    <
    /form> < /
    div > <
    /div>

<!-- Modal Mensagens-->
<
div class = "modal fade"
id = "doCreate"
tabindex = "-1"
role = "dialog"
aria - labelledby = "exampleModalLabel"
aria - hidden = "true" >
    <
    div class = "modal-dialog"
role = "document" >
    <
    div class = "modal-content" >
    <
    div class = "modal-body" >
    <
    p id = "message" >
    <
    /p> < /
    div > <
    /div> < /
    div > <
    /div> < /
    div >

    <!-- Modal gerar localização-->
    <
    div class = "modal fade"
id = "doLocation"
tabindex = "-1"
role = "dialog"
aria - labelledby = "exampleModalLongTitle"
aria - hidden = "true" >
    <
    div class = "modal-dialog"
role = "document" >
    <
    div class = "modal-content" >
    <
    div class = "modal-header" >
    <
    h5 class = "modal-title" > Gera localização < /h5> <
button type = "button"
class = "btn-close"
data - bs - dismiss = "modal"
aria - label = "Close" >
    <
    /button> < /
    div > <
    div class = "modal-long-body" >
    <
    form id = "location_generate" >
    <
    select type = "text"
name = "building"
id = "id_building" >
    <
    /select> <
select type = "text"
name = "floor"
id = "id_floor" >
    <
    /select> <
select type = "text"
name = "rack"
id = "id_rack" >
    <
    /select> <
div class = "sala_corredor" >
    <
    label
for = "sala" > Sala < /label> <
input class = "sc"
value = "S"
type = "radio"
name = "sala_corredor"
checked >
    <
    label
for = "corredor" > Corredor < /label> <
input class = "sc"
value = "C"
type = "radio"
name = "sala_corredor" >
    <
    /div> <
input type = "text"
placeholder = "Número de SALA próxima"
id = "number_room" >
    <
    button type = "submit"
data - bs - dismiss = "modal"
class = "btn btn-info" > Gerar Localização < /button> <
div class = "result" >
    <
    /div> < /
    form > <
    /div> < /
    div > <
    /div> < /
    div >

    <
    script src = "{% static 'js/jquery-3.6.0.min.js' %}" > < /script> <
script src = "{% static 'js/switches_create.js' %}" > < /script> <
script src = "{% static 'js/location.js' %}" > < /script>

{ % endblock % }
terface GigabitEthernet0 / 0 / 16 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 17 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 18 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 19 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 20 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 21 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 22 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 23 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 24 < br >
    dhcp snooping enable < br >
    dhcp snooping trusted < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    interface XGigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    quit < br >
    user - interface vty 0 4 < br >
    authentication - mode aaa < br >
    protocol inbound all < br >
    quit < br >
    aaa < br >
    local - user admin privilege level 15 < br >
    local - user admin service - type ssh telnet http terminal < br >
    quit < br >
    ssh user admin authentication - type password < br >
    stelnet server enable < br >
    telnet server enable < br >
    ssh user admin service - type stelnet < br >
    quit < br >
    save config.cfg < br >
    save < br >
    `;
        var commands_huawei48 = `
system - view < br >
    sysname $ { name } < br >
    ip route - static 0.0 .0 .0 0.0 .0 .0 $ { gateway }
permanent < br >
    snmp - agent < br >
    snmp - agent sys - info version v2c < br >
    snmp - agent community read cipher $ { community } < br >
    snmp - agent sys - info contact $ { patrimony } < br >
    snmp - agent sys - info location $ { location } < br >
    snmp - agent mib - view included iso - view iso < br >
    snmp - agent community read public mib - view iso - view < br >
    snmp - agent sys - info version all < br >
    y < br >
    dhcp enable < br >
    dhcp snooping enable < br >
    lldp enable < br >
    aaa < br >
    undo user - password complexity - check < br >
    <
    br >
    quit < br >
    <
    br >
    interface Vlanif1 < br >
    ip address $ { ip }
$ { netmask } < br >
    quit < br >
    <
    br >
    clock timezone Brasilia minus 03: 00: 00 < br >
    ntp - service server disable < br >
    ntp - service ipv6 server disable < br >
    ntp - service unicast - server 127.0 .0 .1 < br >
    interface GigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 5 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 6 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 7 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 8 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 9 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 10 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 11 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 12 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 13 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 14 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 15 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 16 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 17 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 18 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 19 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 20 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 21 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 22 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 23 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 24 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 25 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 26 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 27 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 28 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 29 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 30 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 31 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 32 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 33 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 34 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 35 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 36 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 37 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 38 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 39 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 40 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 41 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 42 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 43 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 44 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 45 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 46 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 47 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 48 < br >
    dhcp snooping enable < br >
    dhcp snooping trusted < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    interface XGigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    quit < br >
    user - interface vty 0 4 < br >
    authentication - mode aaa < br >
    protocol inbound all < br >
    quit < br >
    aaa < br >
    local - user admin privilege level 15 < br >
    local - user admin service - type ssh telnet http terminal < br >
    quit < br >
    ssh user admin authentication - type password < br >
    stelnet server enable < br >
    telnet server enable < br >
    ssh user admin service - type stelnet < br >
    quit < br >
    save config.cfg < br >
    save < br >
    `;
        var commands_huawei_poe = `
system - view < br >
    sysname $ { name } < br >
    ip route - static 0.0 .0 .0 0.0 .0 .0 $ { gateway }
permanent < br >
    snmp - agent < br >
    snmp - agent sys - info version v2c < br >
    snmp - agent community read cipher $ { community } < br >
    snmp - agent sys - info contact $ { patrimony } < br >
    snmp - agent sys - info location $ { location } < br >
    snmp - agent mib - view included iso - view iso < br >
    snmp - agent community read public mib - view iso - view < br >
    snmp - agent sys - info version all < br >
    y < br >
    dhcp enable < br >
    dhcp snooping enable < br >
    lldp enable < br >
    aaa < br >
    undo user - password complexity - check < br >
    <
    br >
    quit < br >
    vlan 99 < br >
    name WIFImgmt < br >
    quit < br >
    vlan 195 < br >
    name eduroam < br >
    quit < br >
    vlan 199 < br >
    name WIFI - UFSM < br >
    quit < br >
    vlan 198 < br >
    name WIFI - guest < br >
    <
    br >
    interface Vlanif1 < br >
    ip address $ { ip }
$ { netmask } < br >
    quit < br >
    ntp - service server disable < br >
    ntp - service ipv6 server disable < br >
    ntp - service unicast - server 127.0 .0 .1 < br >
    interface GigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 5 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 6 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 7 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 8 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 9 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 10 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 11 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 12 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 13 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 14 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 15 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 16 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 17 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 18 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 19 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 20 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 21 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 22 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 23 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 24 < br >
    dhcp snooping enable < br >
    dhcp snooping trusted < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    interface XGigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    quit < br >
    user - interface vty 0 4 < br >
    authentication - mode aaa < br >
    protocol inbound all < br >
    quit < br >
    aaa < br >
    local - user admin privilege level 15 < br >
    local - user admin service - type ssh telnet http terminal < br >
    quit < br >
    ssh user admin authentication - type password < br >
    stelnet server enable < br >
    telnet server enable < br >
    ssh user admin service - type stelnet < br >
    quit < br >
    save config.cfg < br >
    save < br >
    `;

        var commands_huawei248 = `
system - view < br >
    sysname $ { name } < br >
    ip route - static 0.0 .0 .0 0.0 .0 .0 $ { gateway }
permanent < br >
    <
    br >
    snmp - agent < br >
    snmp - agent protocol source - status all - interface < br >
    snmp - agent sys - info version v2c < br >
    snmp - agent community read cipher $ { community } < br >
    snmp - agent sys - info contact $ { patrimony } < br >
    snmp - agent sys - info location $ { location } < br >
    snmp - agent mib - view included iso - view iso < br >
    snmp - agent community read public mib - view iso - view < br >
    snmp - agent sys - info version all < br >
    y < br >
    dhcp enable < br >
    dhcp snooping enable < br >
    lldp enable < br >
    <
    br >
    aaa < br >
    undo user - password complexity - check < br >
    quit < br >
    clock timezone Brasilia minus 03: 00: 00 < br >
    ntp - service server disable < br >
    ntp - service ipv6 server disable < br >
    ntp - service unicast - server 127.0 .0 .1 < br >
    interface Vlanif1 < br > ip address $ { ip }
$ { netmask } < br >
    quit < br >
    <
    br >
    telnet server - source - i Vlanif1 < br >
    y < br >
    ssh server - source - i Vlanif1 < br >
    y < br >
    http server - source - i Vlanif1 < br >
    y < br >
    <
    br >
    interface GigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 5 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 6 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 7 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 8 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 9 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 10 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 11 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 12 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 13 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 14 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 15 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 16 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 17 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 18 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 19 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 20 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 21 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 22 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 23 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 24 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 25 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 26 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 27 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 28 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 29 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 30 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 31 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 32 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 33 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 34 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 35 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 36 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 37 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 38 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 39 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 40 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 41 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 42 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 43 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 44 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 45 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 46 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 47 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 48 < br >
    dhcp snooping enable < br >
    dhcp snooping trusted < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    interface XGigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    quit < br >
    <
    br >
    user - interface vty 0 4 < br >
    authentication - mode aaa < br >
    protocol inbound all < br >
    quit < br >
    aaa < br >
    <
    br >
    local - user admin password irreversible - cipher $ { password } < br >
    local - user admin privilege level 15 < br >
    local - user admin service - type ssh telnet http terminal < br >
    local - aaa - user password policy administrator < br >
    undo password alert original < br >
    quit < br >
    ssh user admin authentication - type password < br >
    stelnet server enable < br >
    telnet server enable < br >
    ssh user admin service - type stelnet < br >
    quit < br >
    save config.cfg < br >
    save < br >
    `;

        var commands_huawei2 = `
system - view < br >
    sysname $ { name } < br >
    ip route - static 0.0 .0 .0 0.0 .0 .0 $ { gateway }
permanent < br >
    <
    br >
    snmp - agent < br >
    snmp - agent protocol source - status all - interface < br >
    snmp - agent sys - info version v2c < br >
    snmp - agent community read cipher $ { community } < br >
    snmp - agent sys - info contact $ { patrimony } < br >
    snmp - agent sys - info location $ { location } < br >
    snmp - agent mib - view included iso - view iso < br >
    snmp - agent community read public mib - view iso - view < br >
    snmp - agent sys - info version all < br >
    y < br >
    dhcp enable < br >
    dhcp snooping enable < br >
    lldp enable < br >
    <
    br >
    aaa < br >
    undo user - password complexity - check < br >
    quit < br >
    clock timezone Brasilia minus 03: 00: 00 < br >
    ntp - service server disable < br >
    ntp - service ipv6 server disable < br >
    ntp - service unicast - server 127.0 .0 .1 < br >
    interface Vlanif1 < br > ip address $ { ip }
$ { netmask } < br >
    quit < br >
    <
    br >
    telnet server - source - i Vlanif1 < br >
    y < br >
    ssh server - source - i Vlanif1 < br >
    y < br >
    http server - source - i Vlanif1 < br >
    y < br >
    <
    br >
    interface GigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 5 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 6 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 7 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 8 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 9 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 10 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 11 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 12 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 13 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 14 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 15 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 16 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 17 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 18 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 19 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 20 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 21 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 22 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 23 < br >
    dhcp snooping enable < br >
    interface GigabitEthernet0 / 0 / 24 < br >
    dhcp snooping enable < br >
    dhcp snooping trusted < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    interface XGigabitEthernet0 / 0 / 1 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 2 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 3 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    interface XGigabitEthernet0 / 0 / 4 < br >
    dhcp snooping enable < br >
    port link - type trunk < br >
    port trunk allow - pass vlan all < br >
    dhcp snooping trusted < br >
    quit < br >
    <
    br >
    user - interface vty 0 4 < br >
    authentication - mode aaa < br >
    protocol inbound all < br >
    quit < br >
    aaa < br >
    <
    br >
    local - user admin password irreversible - cipher $ { password } < br >
    local - user admin privilege level 15 < br >
    local - user admin service - type ssh telnet http terminal < br >
    local - aaa - user password policy administrator < br >
    undo password alert original < br >
    quit < br >
    ssh user admin authentication - type password < br >
    stelnet server enable < br >
    telnet server enable < br >
    ssh user admin service - type stelnet < br >
    quit < br >
    save config.cfg < br >
    save < br >
    `;

        //console.log(type);
        var commands = '';
        if (vendor == 'huawei') {
            if (type == 'normal') {
                commands = commands_huawei;
            } else if (type == 'normal48') {
                commands = commands_huawei48;
            } else if (type == 'poewifi') {
                commands = commands_huawei_poe;
            }
        } else if (vendor == 'huawei2') {
            if (type == 'normal') {
                commands = commands_huawei2;
            } else if (type == 'normal48') {
                commands = commands_huawei248;
            }
        } else if (vendor == 'dell') {
            if (type == 'normal') {
                commands = "enable<br>configure<br>hostname " + name + "<br>interface vlan 1<br>ip address " + ip + " " + netmask + "<br>exit <br>ip route default " + gateway + "<br>ip route 0.0.0.0 0.0.0.0 " + gateway + "<br>username admin password " + password + " privilege 15<br>crypto key generate dsa<br>crypto key generate rsa<br>ip ssh server<br>crypto certificate 1 generate<br>key-generate<br>exit<br>ip http secure-server<br>snmp-server community " + community + "<br>snmp-server contact " + patrimony + "<br>snmp-server location " + location + "<br>ip dhcp snooping vlan 1-4093<br>interface gigabitethernet 1/0/24<br>ip dhcp snooping trust<br>exit<br>exit<br>wr<br>";
            } else if (type == 'normal48') {
                commands = "Não temos Switches 48 portas da Dell, aí fiquei com prequiça de implementar (por enquanto) :D";
            } else if (type == 'poewifi') {
                commands = "enable<br>configure<br>hostname " + name + "<br>interface vlan 1<br>ip address " + ip + " " + netmask + "<br>exit <br>ip route default " + gateway + "<br>ip route 0.0.0.0 0.0.0.0 " + gateway + "<br>username admin password " + password + " privilege 15<br>crypto key generate dsa<br>crypto key generate rsa<br>ip ssh server<br>crypto certificate 1 generate<br>key-generate<br>exit<br>ip http secure-server<br>snmp-server community " + community + "<br>snmp-server contact " + patrimony + "<br>snmp-server location " + location + "<br>ip dhcp snooping vlan 1-4093<br>interface gigabitethernet 1/0/24<br>ip dhcp snooping trust<br>exit<br>wr<br>";
                var poe = '<br>#OBS: NÃO EXISTE SWITCH DELL COM POE<br>';
                commands = commands + poe;
            }

        }

        $('#response').html(commands);

    });

});