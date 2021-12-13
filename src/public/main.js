import { Api } from "./modules/api.js";
import { criarElementEstado, selecionarTodosEstados, configurarEstadosSelecaoUnica, configurarEstadosSelecaoMultipla, selecionarEstado, setUpDates } from "./modules/dom.js";

const api = new Api();

const config = {
  tipoRelatorioAtual: null,
  tiposRelatorio: []
};

async function main() {
  await atualizarTabela();

  await listarRelatoriosDisponiveis();

  await listarEstados();

  setInterval(atualizarTabela, 10_000);

  novoPedidoForm.addEventListener('submit', processar);
  todosEstadosCheckbox.addEventListener('change', selecionarTodosEstados);
  document.getElementsByName('estado').forEach(ec => ec.addEventListener('change', selecionarEstado));
  tipoRelatorio.addEventListener('change', onTipoRelatorioChange);

  setUpDates();
}

async function listarRelatoriosDisponiveis() {
  const relatorios = await api.getRelatoriosDisponiveis();

  config.tipoRelatorioAtual = relatorios[0];
  config.tiposRelatorio = relatorios;

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

  if (config.tipoRelatorioAtual.multiplos_estados) {
    configurarEstadosSelecaoMultipla()
  } else {
    configurarEstadosSelecaoUnica()
  }

  for (const estado of estados) {
    const elemento = criarElementEstado(estado);

    estadosFieldset.appendChild(elemento);
  }

  //  estadosSelect.multiple = config.tipoRelatorio.multiplos_estados
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
    const estados = [...document.getElementsByName('estado')]
      .filter(e => e.checked)
      .map(e => e.value);

    const responseBody = await api.postRelatorio(config.tipoRelatorioAtual.path, {
      estados: estados,
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

function onTipoRelatorioChange(event) {
  config.tipoRelatorioAtual = config.tiposRelatorio.find(tp => tp.id === event.target.value);

  if (config.tipoRelatorioAtual.multiplos_estados) {
    configurarEstadosSelecaoMultipla()
  } else {
    configurarEstadosSelecaoUnica()
  }
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