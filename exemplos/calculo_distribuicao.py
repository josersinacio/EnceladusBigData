
from random import randint
import pandas as pd 

max_por_mes = 6000
max_por_item = 400
meses = 12
quant_itens = 20

output_matrix = []


for i in range(quant_itens):
    print(f'Item {i+1}')

    output_matrix.append([])

    restante = max_por_mes

    for j in range(meses):
        quant_item = randint(1, max_por_item);
        print(f"No mês {j+1} será vendido {quant_item}.")
        output_matrix[i].append(quant_item)

    print()

print(output_matrix)

pd.DataFrame(output_matrix).to_csv('./vendas.csv')

