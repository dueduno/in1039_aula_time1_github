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
    data: new Date("2023-05-10") // Exemplo: Ontem
  }
];

// Função para renderizar o histórico no accordion
function renderizarHistorico(filtro = null) {
  const accordion = document.getElementById('accordionVagas');
  accordion.innerHTML = ''; // Limpar o histórico atual
  
  let locaisFiltrados = locais;
  
  if (filtro) {
    locaisFiltrados = locais.filter(local => {
      switch (filtro) {
        case "hoje":
          return local.data.toDateString() === new Date().toDateString();
        case "ontem":
          const ontem = new Date();
          ontem.setDate(ontem.getDate() - 1);
          return local.data.toDateString() === ontem.toDateString();
        default:
          return true;
      }
    });
  }

  if (locaisFiltrados.length === 0) {
    document.getElementById("mensagem-vazia").classList.remove("d-none");
  } else {
    document.getElementById("mensagem-vazia").classList.add("d-none");
  }

  locaisFiltrados.forEach((local, index) => {
    const accordionItem = document.createElement('div');
    accordionItem.classList.add('accordion-item');
    accordionItem.innerHTML = `
      <h2 class="accordion-header" id="heading${index}">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}" aria-expanded="true" aria-controls="collapse${index}">
          ${local.nome} - ${local.tipo}
        </button>
      </h2>
      <div id="collapse${index}" class="accordion-collapse collapse" aria-labelledby="heading${index}" data-bs-parent="#accordionVagas">
        <div class="accordion-body">
          <p><strong>Tempo de vaga:</strong> ${local.tempoVaga}</p>
          <p><strong>Entrada:</strong> ${local.entrada}</p>
          <p><strong>Localização:</strong> ${local.localizacao}</p>
          <button class="btn-excluir" onclick="excluirItem(${index})">🗑️</button>
        </div>
      </div>
    `;
    accordion.appendChild(accordionItem);
  });
}

// Função para excluir item do histórico
function excluirItem(index) {
  // Mostrar modal de confirmação
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmarExclusao'));
  modal.show();

  document.getElementById('confirmarExclusao').onclick = function() {
    locais.splice(index, 1); // Excluir o item
    renderizarHistorico(); // Re-renderizar o histórico
    modal.hide(); // Fechar o modal
  };
}

// Função para limpar filtro
document.getElementById('btnLimparFiltro').addEventListener('click', () => {
  renderizarHistorico();
});

// Inicializar o histórico
renderizarHistorico();
