# PAA - Conjunto Dominante aplicado à Cobertura Wi-Fi
O projeto implementa o Problema do Conjunto Dominante Mínimo como uma forma de otimizar a distribuição de pontos de acesso Wi-Fi em ambientes físicos.


O que o projeto faz

- Modela um ambiente como um grafo, onde cada vértice representa um cômodo
- Permite que o usuário defina o tamanho do ambiente, a quantidade de cômodos e suas conexões (ainda em avaliação).
- Utiliza um algoritmo de força bruta para encontrar o menor conjunto de cômodos onde os roteadores devem ser instalados, garantindo cobertura total.
- Gera uma visualização gráfica com networkx e matplotlib, destacando os cômodos escolhidos para instalação dos roteadores.

Como funciona

- O algoritmo testa todas as combinações possíveis de instalação de roteadores.
- Retorna o conjunto dominante mínimo (solução ótima).
- Exibe um grafo colorido:
- Vermelho → cômodos onde instalar roteadores.
- Azul → cômodos cobertos pelo sinal.

🔹 Tecnologias utilizadas
- Python 3
- networkx para modelagem do grafo
- matplotlib para visualização

Saída:
Roteadores devem ser instalados em: {'SalaA', 'SalaD', 'SalaE'}


E o grafo é exibido com os roteadores destacados.


