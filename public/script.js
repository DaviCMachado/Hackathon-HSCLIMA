//console.log('Site estático carregado com sucesso!');
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script>
	var map = L.map('map',{scrollWheelZoom: false}).setView([-29, -51], 7);

	var planetLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);

	planetLayer.addTo(map)


	for(let i=0;i<1000;i++){
		let lat = -51 + 0.005 *i
		var marker1 = L.marker([-29, lat]).addTo(map)
	}

</script>