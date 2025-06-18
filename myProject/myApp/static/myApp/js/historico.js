// Inicialização do mapa Leaflet
const mapa = L.map('mapa').setView([-23.55052, -46.633308], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(mapa);

let marcador = null;

// Dados dos estacionamentos
let locais = [
  {
    nome: "Av. Paulista, São Paulo",
    coords: [-23.561684, -46.655981],
    tempoVaga: "1h 20min",
    tipo: "Carro",
    tempoPrevisto: "2h",
    entrada: "10:15h",
    localizacao: "A1",
    data: new Date() // Hoje
  },
  {
    nome: "Rua Siqueira Campos, Rio de Janeiro",
    coords: [-22.968432, -43.185172],
    tempoVaga: "45min",
    tipo: "Moto",
    tempoPrevisto: "1h 30min",
    entrada: "11:00h",
    localizacao: "B2",
    data: new Date(new Date().setDate(new Date().getDate() - 1)) // Ontem
  },
  {
    nome: "Estacionamento Centro", 
    coords: [-23.55052, -46.633308],
    tempoVaga: "2h",
    tipo: "Carro",
    tempoPrevisto: "3h",
    entrada: "09:00h",
    localizacao: "C3",
    data: new Date(new Date().setDate(new Date().getDate() - 3)) // Esta semana
  },
  {
    nome: "Estacionamento Shopping", 
    coords: [-23.564, -46.647],
    tempoVaga: "30min",
    tipo: "Carro",
    tempoPrevisto: "1h",
    entrada: "14:30h",
    localizacao: "D4",
    data: new Date(new Date().setDate(new Date().getDate() - 20)) // Este mês
  },
  {
    nome: "Estacionamento Antigo", 
    coords: [-23.555, -46.640],
    tempoVaga: "3h",
    tipo: "Carro",
    tempoPrevisto: "4h",
    entrada: "08:00h",
    localizacao: "E5",
    data: new Date(new Date().setMonth(new Date().getMonth() - 5)) // 5 meses atrás
  },
  {
    nome: "Estacionamento Velho", 
    coords: [-23.560, -46.635],
    tempoVaga: "1h",
    tipo: "Carro",
    tempoPrevisto: "2h",
    entrada: "10:00h",
    localizacao: "F6",
    data: new Date(new Date().setMonth(new Date().getMonth() - 7)) // 7 meses atrás
  }
];

let itensExibidos = [...locais];
let indiceParaExcluir = null;

const accordionVagas = document.getElementById("accordionVagas");
const mensagemVazia = document.getElementById("mensagem-vazia");
const modalExclusao = new bootstrap.Modal(document.getElementById('modalConfirmarExclusao'));
const btnConfirmarExclusao = document.getElementById('confirmarExclusao');

// Formata data
function formatarData(data) {
  const opcoes = { year: 'numeric', month: '2-digit', day: '2-digit' };
  return data.toLocaleDateString('pt-BR', opcoes);
}

// Filtro por tempo
function filtrarPorTempo(tipoFiltro) {
  const agora = new Date();
  return locais.filter(item => {
    const dataItem = new Date(item.data);
    switch (tipoFiltro) {
      case 'hoje':
        return dataItem.toDateString() === agora.toDateString();
      case 'ontem':
        const ontem = new Date();
        ontem.setDate(agora.getDate() - 1);
        return dataItem.toDateString() === ontem.toDateString();
      case 'estaSemana':
        const primeiroDiaSemana = new Date(agora);
        primeiroDiaSemana.setDate(agora.getDate() - agora.getDay() + 1);
        const ultimoDiaSemana = new Date(primeiroDiaSemana);
        ultimoDiaSemana.setDate(primeiroDiaSemana.getDate() + 6);
        return dataItem >= primeiroDiaSemana && dataItem <= ultimoDiaSemana;
      case 'esteMes':
        return dataItem.getMonth() === agora.getMonth() && dataItem.getFullYear() === agora.getFullYear();
      case 'ultimos6Meses':
        const seisMesesAtras = new Date();
        seisMesesAtras.setMonth(agora.getMonth() - 6);
        return dataItem >= seisMesesAtras && dataItem <= agora;
      case 'mais6Meses':
        const seisMesesAtrasMais = new Date();
        seisMesesAtrasMais.setMonth(agora.getMonth() - 6);
        return dataItem < seisMesesAtrasMais;
      default:
        return true;
    }
  });
}

// Limpa filtro
function limparFiltro() {
  itensExibidos = [...locais];
  atualizarLista();
  desmarcarFiltros();
}

// Atualiza o HTML
function atualizarLista() {
  accordionVagas.innerHTML = "";
  if (itensExibidos.length === 0) {
    mensagemVazia.classList.remove("d-none");
  } else {
    mensagemVazia.classList.add("d-none");

    itensExibidos.forEach((item, index) => {
      const idAccordion = `vagaAccordion${index}`;
      const idCollapse = `collapse${index}`;
      const itemHTML = document.createElement("div");
      itemHTML.classList.add("accordion-item");
      itemHTML.style.position = "relative";

      const btnExcluir = document.createElement("button");
      btnExcluir.textContent = "×";
      btnExcluir.title = "Excluir item";
      btnExcluir.classList.add("btn-excluir");
      btnExcluir.onclick = e => {
        e.stopPropagation();
        indiceParaExcluir = locais.indexOf(item);
        modalExclusao.show();
      };

      itemHTML.innerHTML = `
        <h2 class="accordion-header" id="heading${index}">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${idCollapse}" aria-expanded="false" aria-controls="${idCollapse}">
            ${item.nome} - ${formatarData(item.data)}
          </button>
        </h2>
        <div id="${idCollapse}" class="accordion-collapse collapse" aria-labelledby="heading${index}" data-bs-parent="#accordionVagas">
          <div class="accordion-body">
            <div><b>Tempo de vaga:</b> ${item.tempoVaga}</div>
            <div><b>Tipo:</b> ${item.tipo}</div>
            <div><b>Tempo previsto:</b> ${item.tempoPrevisto}</div>
            <div><b>Entrada:</b> ${item.entrada}</div>
            <div><b>Localização:</b> ${item.localizacao}</div>
          </div>
        </div>
      `;

      itemHTML.appendChild(btnExcluir);
      accordionVagas.appendChild(itemHTML);

      const collapseEl = itemHTML.querySelector(`#${idCollapse}`);
      collapseEl.addEventListener('show.bs.collapse', () => {
        if (marcador) mapa.removeLayer(marcador);
        marcador = L.marker(item.coords).addTo(mapa);
        mapa.setView(item.coords, 15);
      });
      collapseEl.addEventListener('hide.bs.collapse', () => {
        if (marcador) {
          mapa.removeLayer(marcador);
          marcador = null;
        }
      });
    });
  }
}

// Botão confirmar exclusão
btnConfirmarExclusao.addEventListener("click", () => {
  if (indiceParaExcluir !== null && indiceParaExcluir >= 0) {
    locais.splice(indiceParaExcluir, 1);
    itensExibidos = itensExibidos.filter(item => locais.includes(item));
    atualizarLista();
    modalExclusao.hide();
    indiceParaExcluir = null;
  }
});

// Filtros de tempo
const filtroTempoContainer = document.getElementById("filtro-tempo");
filtroTempoContainer.addEventListener("click", e => {
  if (e.target.classList.contains("btn")) {
    [...filtroTempoContainer.children].forEach(btn => btn.classList.remove("active"));
    e.target.classList.add("active");

    const filtroSelecionado = e.target.dataset.filter;
    itensExibidos = filtrarPorTempo(filtroSelecionado);
    atualizarLista();
  }
});

// Botão limpar filtro
const btnLimparFiltro = document.getElementById("btnLimparFiltro");
btnLimparFiltro.addEventListener("click", () => {
  limparFiltro();
});

// Desmarcar filtros
function desmarcarFiltros() {
  [...filtroTempoContainer.children].forEach(btn => btn.classList.remove("active"));
}

// Inicializa
atualizarLista();
