var mapa = L.map('mapa').setView([-15.7942, -47.8822], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data © OpenStreetMap contributors'
}).addTo(mapa);

function distanciaKm(lat1, lon1, lat2, lon2) {
  function toRad(x) { return x * Math.PI / 180; }
  var R = 6371;
  var dLat = toRad(lat2 - lat1);
  var dLon = toRad(lon2 - lon1);
  var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = {
    categoria: document.querySelectorAll('.filtro-categoria'),
    tipo: document.querySelectorAll('.filtro-tipo'),
    cobranca: document.querySelectorAll('.filtro-cobranca'),
    horario: document.querySelectorAll('.filtro-horario'),
    dias: document.querySelectorAll('.filtro-dias')
  };
  const vagas = document.querySelectorAll('.vaga');
  const slider = document.getElementById('slider-distancia');
  const distanciaValor = document.getElementById('distancia-valor');

  let pontoReferencia = null;
  let marcadorReferencia = null;

  // Criação do slider
  noUiSlider.create(slider, {
    start: [10],
    connect: 'lower',
    step: 1,
    range: { min: 1, max: 100 },
    format: {
      to: value => Math.round(value),
      from: value => Number(value)
    }
  });

  distanciaValor.textContent = slider.noUiSlider.get();

  // Função para aplicar os filtros
  function aplicarFiltros() {
    const filtros = {
      categoria: Array.from(checkboxes.categoria).filter(cb => cb.checked).map(cb => cb.value),
      tipo: Array.from(checkboxes.tipo).filter(cb => cb.checked).map(cb => cb.value),
      cobranca: Array.from(checkboxes.cobranca).filter(cb => cb.checked).map(cb => cb.value),
      horario: Array.from(checkboxes.horario).filter(cb => cb.checked).map(cb => cb.value),
      dias: Array.from(checkboxes.dias).filter(cb => cb.checked).map(cb => cb.value)
    };

    const distanciaMax = Number(slider.noUiSlider.get());

    vagas.forEach(vaga => {
      const okFiltros =
        filtros.categoria.includes(vaga.dataset.categoria) &&
        filtros.tipo.includes(vaga.dataset.tipo) &&
        filtros.cobranca.includes(vaga.dataset.cobranca) &&
        filtros.horario.includes(vaga.dataset.horario) &&
        filtros.dias.includes(vaga.dataset.dias);

      if (!pontoReferencia) {
        // Se não tem ponto de referência, mostra todos que passam os outros filtros
        vaga.style.display = okFiltros ? 'block' : 'none';
        return;
      }

      const lat = parseFloat(vaga.dataset.lat);
      const lng = parseFloat(vaga.dataset.lng);
      const dist = distanciaKm(pontoReferencia.lat, pontoReferencia.lng, lat, lng);

      vaga.style.display = (okFiltros && dist <= distanciaMax) ? 'block' : 'none';
    });
  }

  // Adicionando eventos de mudança nos filtros
  Object.values(checkboxes).forEach(grupo => {
    grupo.forEach(cb => cb.addEventListener('change', aplicarFiltros));
  });

  // Atualizando o valor do slider e aplicando filtros
  slider.noUiSlider.on('update', (values) => {
    distanciaValor.textContent = values[0];
    aplicarFiltros();
  });

  // Evento de clique no mapa para definir o ponto de referência
  mapa.on('click', e => {
    pontoReferencia = e.latlng;
    if (marcadorReferencia) {
      mapa.removeLayer(marcadorReferencia);
    }
    marcadorReferencia = L.marker(pontoReferencia).addTo(mapa).bindPopup('Ponto de referência').openPopup();
    aplicarFiltros();
  });

  // Aplicando os filtros ao carregar a página
  aplicarFiltros();
});
