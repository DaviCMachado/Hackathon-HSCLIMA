/*/////////// SCRIPT MAP //////////////////////////*/
import require
const http = require('http')

// Inicializa o mapa
var map = L.map('map').setView([-29, -51], 13);

// Adiciona a camada do OpenStreetMap
var planetLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
testeMarker()
mysqlTeste()

function mysqlTeste(){

    var mysql = require('mysql');

    var con = mysql.createConnection({
      host: "localhost",
      user: "root",
      password: "root",
    });
    console.log("MIGUEL");
    con.connect(function(err) {
      if (err) throw err;
      console.log("Connected!");
    });
}

function testeMarker(){
// Exemplo de adição de marcadores para visualização inicial
    let qtd = 0;
    for (let i = 0; i < 100; i++) {
        let lat = -51 + 0.5 * i;
        var marker = L.marker([-29, lat]);
        qtd = qtd + 1;
        var popup = marker.bindPopup(qtd.toString()); // COLOCAR REFERENCIA PARA DADOS DO BANCO de dados
        marker.addTo(map);
    }
}


function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
			if (Array.isArray(data)) {
                data.forEach(item => {
					let marker = L.marker([-29 + item.codRegiao * 0.01, -51]);
                    marker.bindPopup(`Produto: ${item.codProduto}, Quantidade: ${item.quantidade}`);
                    marker.addTo(map);
                });
            } else {
				console.error('Erro: Os dados não são um array', data);
            }
        })
        .catch(error => console.error('Erro ao buscar dados:', error));
}
// Fetch data every 10 seconds
fetchData();
setInterval(fetchData, 10000);
/*/////// END MAP //////////*/
