import { Api } from "./modules/api.js";

const api = new Api();

const config = {
  tipoRelatorio: null
};

async function main() {
  await atualizarTabela();

  await listarRelatoriosDisponiveis();

  await listarEstados();

  setInterval(atualizarTabela, 10_000);

  novoPedidoForm.addEventListener('submit', processar);
}

async function listarRelatoriosDisponiveis() {
  const relatorios = await api.getRelatoriosDisponiveis();

  config.tipoRelatorio = relatorios[0];s

  relatorios.forEach(relatorio => {
    const relatorioOption = Object.assign(
      document.createElement("option"),
      {
        innerText: relatorio.nome,
        value: relatorio.id
      }
    );

    tipoRelatorio.appendChild(relatorioOption);
  })
}

async function listarEstados() {
  const estados = await api.getEstados();

  if (config.tipoRelatorio.multiplos_estados) {
    estados.unshift({sigla: "TODOS", nome: "Todos"});
  }

  for (const estado of estados) {
    const estadoOption = Object.assign(
      document.createElement("option"),
      {
        innerText: estado.nome,
        value: estado.sigla
      }
    )

    estadosSelect.appendChild(estadoOption);
  }

  estadosSelect.multiple = config.tipoRelatorio.multiplos_estados
}

async function atualizarTabela() {
  const relatorios = await api.getRelatoriosProcessados();

  linhasProcessadas.innerHTML = '';

  if (relatorios.length === 0) {
    linhasProcessadas.innerHTML = `
      <tr><td colspan="6"><strong>Nenhum relatório processado ainda!</strong></td></tr>
    `
  }

  relatorios.forEach(relatorio => {

    const dataInicial = formatarDate(relatorio.data_inicio);
    const dataFinal = formatarDate(relatorio.data_fim);

    linhasProcessadas.innerHTML += `
        <tr>
          <td class="tipoProcessado Signika--300">${relatorio.tipo}</td>
          <td class="estadoProcessado Signika--300">${relatorio.estado}</td>
          <td class="dataInicioProcessado Signika--300">${dataInicial}</td>
          <td class="dataFimProcessado Signika--300">${dataFinal}</td>
          <td class="dataFimProcessado Signika--300">${relatorio.data_processamento || '-'}</td>
          <td class="downloadProcessado Signika--300"><a href='${relatorio.uri}' target="_blank">💾 Baixar PDF</a></td>
        </tr>`;
  });
}

async function processar(event) {

  event.preventDefault()

  try {
    const responseBody = await api.postRelatorio(config.tipoRelatorio.path, {
      estados: [...estadosSelect.options].filter(o => o.selected).map(o => o.value),
      dataInicial: dataInicialInput.value,
      dataFinal: dataFinalInput.value,
      email: emailInput.value
    })

    alert(`Relatório enviado para processamento!\nCódigo: ${responseBody.id_requisicao}`);
  } catch (ex) {
    console.error(ex)
    alert('Erro ao processar relatório!');
  }

  return false;
}

function formatarDate(dateString) {

  if (dateString.length === 4) {
    return dateString;
  }

  const date = new Date(dateString);

  // Corrige timezone [https://stackoverflow.com/a/16048201]
  date.setTime(date.getTime() + date.getTimezoneOffset() * 60 * 1_000);

  return date.toLocaleDateString();
}

window.addEventListener('load', main);