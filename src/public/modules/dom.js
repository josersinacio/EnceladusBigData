

export function criarElementEstado({ sigla, nome }) {
  const label = Object.assign(document.createElement('label'), {
    className: 'novoPedido--label Signika--300'
  });

  const input = Object.assign(document.createElement('input'), {
    type: 'checkbox',
    name: 'estado',
    value: sigla
  })

  const span = Object.assign(document.createElement('span'), {
    innerText: nome,
  })

  label.appendChild(input);
  label.appendChild(span);

  return label;
}

export function selecionarTodosEstados(event) {
  const todosChecked = event.target.checked;

  document.getElementsByName('estado').forEach(ec => {
    if (ec.value !== 'TODOS') {
      ec.checked = todosChecked;
      ec.disabled = todosChecked
    }
  })
}

export function selecionarEstado(event) {
  const estadoCheckbox =  event.target;

  if (!estadoCheckbox.checked) {
    return;
  }

  if (estadosFieldset.getAttribute('selecao') === 'unica' && estadoCheckbox.value !== 'TODOS') {
    document.getElementsByName('estado').forEach(ec => {
      if (ec !== estadoCheckbox) {
        ec.checked = false;
      }
    })
  } 
}

export function configurarEstadosSelecaoUnica() {
  estadosFieldset.setAttribute('selecao', 'unica');

  document.getElementsByName('estado').forEach(ec => {
    ec.checked = false;

    if (ec.value === 'TODOS') {
      ec.disabled = true;
    }
  })
}

export function configurarEstadosSelecaoMultipla() {
  estadosFieldset.setAttribute('selecao', 'multipla');

  document.getElementsByName('estado').forEach(ec => {
    if (ec.value !== 'TODOS') {
      ec.disabled = false;
    }
  })
}

export function setUpDates() {
  flatpickr('.datePicker', {
    mode: 'range',
    dateFormat: 'd/m/Y',
    minDate: '01/01/2013',
    maxDate: '31/12/2019',
    defaultDate: ['01/03/2018', "31/02/2019"],
    locale: 'pt',
    conjunction: 'à'
  });
}