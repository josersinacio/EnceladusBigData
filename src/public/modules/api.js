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

  async postRelatorio(relatorioPath, { estado, estados, dataInicial, dataFinal, email }) {
    const enviarForm = new URL(relatorioPath, location.origin);

    estados.forEach(estado => enviarForm.searchParams.append("estado", estado));
    enviarForm.searchParams.append("data_inicio", dataInicial);
    enviarForm.searchParams.append("data_fim", dataFinal);
    enviarForm.searchParams.append("email", email);
    
    const response = await fetch(enviarForm.href, { method: 'POST' });

    return response.json();
  }
}