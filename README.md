<h1>L2Backup</h1>

Em redes onde o conjunto de ativos é constituído por uma gama de equipamentos de marcas e modelos distintos, a automatização de rotinas precisa levar em consideração as diversas interfaces e formas de acesso. 

Nesse cenário, a L2Backup é proposta com o objetivo principal de automatizar o backup, a recuperação e a manutenção de configuração de switches. Além de resolver a demanda inicial (backup de configuração), também foi pensada para servir como base para automações futuras, como por exemplo, a automatização da execução de comandos, em conjuntos de equipamentos, independente das diferentes CLI.


Na página inicial são apresentadas informações sumarizadas a respeito da quantidade de equipamentos cadastrados, bem como a quantidade de backups e switches offlines. Alguns dos equipamentos cadastrados não são gerenciáveis. São cadastrados no L2Backup por conta de outra funcionalidades (fotos e localização).

Os Botões a direita, de Busca completa SNMP e Backup completo, são utilizados para executar a mesma rotina que já é executada automaticamente, no entanto, utilizando os botões, as rotinas são utilizadas sob demanda.

![1](https://user-images.githubusercontent.com/24876583/181395140-ea43b1e5-b2c8-4804-9ccb-e14ec0586f97.png)



<h3>Atualização das Informaçõe via SNMP</h3>

Utilizando o protocolo SNMP, o L2Backup mantém atualizado as informações que identificam o equipamento (sysName, sysLocation, sysContact, MAC, Marca/Modelo). Dessa forma, sempre que alguma dessas configurações é alterada no equipamento, ou o switch é substituído, desde que o IP se mantenha igual, a configuração é automaticamente alterada na aplicação. 

Os backups são realizados automaticamente uma vez por dia (a frequência pode ser alterada), ou sob demanda, por meio de uma interface WEB.

Uma vez que o switch é adicionado, as seguintes informações são apresentadas: 

![2](https://user-images.githubusercontent.com/24876583/181395270-073bb9db-812a-435f-9871-4b7f02c35464.png)


<b>Endereço IP, Nome (rasurado por questão de privacidade), Marca/Modelo, Localização (conforme configurada no SNMP), Marca/Modelo</b>

![3](https://user-images.githubusercontent.com/24876583/181395401-d905d9c4-26c3-4a96-b7bf-f1f7bf4f010c.png)

<b>Na imagem acima</b>, da esquerda para direita, os ícones apresentados servem para mostrar as fotos registradas do switch (se não tiver fotos, é apresentado a opção de adicionar novas), um ícone de atualização (que realiza um backup do equipamento, sob demanda) e um ícone de download (que apresenta os últimos 30 backups do switch).  Ao clicar nos ícones, ocorre as seguintes ações: 


Quando não existe foto cadastrada (ao clicar no ícone, é redirecionado para uma página de registro de foto): 

![4](https://user-images.githubusercontent.com/24876583/181395426-bf8e2e91-a651-4cae-832c-49fec4cedf4a.png)



<h3>Quando existe foto cadastrada</h3>

![5](https://user-images.githubusercontent.com/24876583/181395452-4901144e-9cc1-47f9-91e3-cc91961204fc.png)


O registro de fotos é feito utilizando metadados de localização, para que futuramente esses equipamentos sejam marcados em mapa, de forma automática, via API.



<h3>Backup sob demanda</h3>


![6](https://user-images.githubusercontent.com/24876583/181395473-a6d3eb19-a049-4c6a-9a27-aef4498784df.png)



<h3>Últimos 30 backups realizados</h3>


![7](https://user-images.githubusercontent.com/24876583/181395496-befca1dc-7b1b-4ee9-acbf-0a31cb2f3885.png)


Na parte de upload de imagem, é dada a opção de tirar uma foto e enviar para o L2Backup, com os metadados, conforme imagem abaixo.

![8](https://user-images.githubusercontent.com/24876583/181395512-d93a6563-e14a-41f7-b38f-e47391060bfa.png)

Além de registrada a(s) foto(s) da instalação do equipamento, é possível vincular ao switch, aos metadados e a alguma observação que for pertinente em cada caso.



<h3>Cadastro de switches com gerência</h3>


![9](https://user-images.githubusercontent.com/24876583/181395558-9e27212e-bc78-4a48-bc42-671881628769.png)



<h3>Cadastro de switches sem gerência</h3>


![10](https://user-images.githubusercontent.com/24876583/181395587-1aa9df7f-aa86-40f1-8d47-f0d428089246.png)


<h3>Gerador de configurações</h3>

Utilizado para auxiliar na configuração via CLI de novos equipamentos. Ao fornecer os parâmetros e clicar no botão gerar, é apresentada a configuração apropriada, de acordo com a marca e modelo. Obviamente que para casos específicos, serão necessárias configurações específicas adicionais.

![11](https://user-images.githubusercontent.com/24876583/181395618-0720a93a-69d1-461f-a333-ceeb19e5e54a.png)


O sistema atualmente está instalado e operando a mais de um ano. Nesse período de tempo, fui adicionando funcionalidades e melhorando adaptando as existentes, de forma a entregar uma melhor experiência aos utilizadores. 

As tecnologias e linguagens utilizadas foram escolhidas por dois motivos principais. O primeiro é  por que atendiam a necessidade da aplicação que eu havia idealizado. O segundo, é porque gostaria de aprender e/ou desenvolver novas habilidades. Devido ao segundo motivo, como pode ser observado no código e principalmente em sua organização, existem diversos pontos a melhorar. 

Além de adicionar novas funcionalidades e melhorar as existentes, como projeto em andamento, eu pretendo reestruturar de maneira adequada e disponibilizar a aplicação para a comunidade. Principalmente visando facilitar o deploy.



<h3>Segue as informações de algumas tecnologias utilizadas:</h3>

Front-end em Django, JavaScript (CSS, HTML)
Back-end em Python
Base de dados Mongo
Servidor HTTP Nginx


