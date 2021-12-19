export class Api {

  async getRelatoriosDisponiveis() {
    const response = await fetch(`/config/relatorios`);

    return response.json();
  }

  async getRelatoriosProcessados() {
    const response = await fetch('/relatorios/processados');

    return response.json();
  }

  async getEstados() {
    const response = await fetch(`/config/estados`);

    const responseBody = await response.json();

    const estados = responseBody.map(estadoDTO => {
      const entries = Object.entries(estadoDTO);

      return {
        sigla: entries[0][0],
        nome: entries[0][1]
      }
    });

    return estados;
  }

  async postRelatorio(tipoRelatorio, { estados, dataInicial, dataFinal, email }) {
    const enviarForm = new URL(tipoRelatorio.path, location.origin);

    const apenasAno = tipoRelatorio.id === 'CASOS_MENSAIS_POR_MUNICIPIO_POR_ESTADO'

    estados.forEach(estado => enviarForm.searchParams.append("estado", estado));

    if (apenasAno) {
      enviarForm.searchParams.append("ano_inicio", /^\d{4}/i.exec(dataInicial)[0]);
      enviarForm.searchParams.append("ano_fim", /^\d{4}/i.exec(dataFinal)[0]);
    } else {
      enviarForm.searchParams.append("data_inicio", dataInicial);
      enviarForm.searchParams.append("data_fim", dataFinal);
    }

    enviarForm.searchParams.append("email", email);
    
    const response = await fetch(enviarForm.href, { method: 'POST' });

    return response.json();
  }
}