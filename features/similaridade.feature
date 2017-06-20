#language: pt

Funcionalidade:Calculo de Similaridade

Esquema do Cenário: Calcular similaridade entre usuarios 

Dado que possuo <lista_classificacao_usuario_1> e <lista_classificacao_usuario_2> 
Quando realizo o calculo de similaridade 
Então deverá ser igual ao <resultado> 

Exemplos:

| lista_classificacao_usuario_1 | lista_classificacao_usuario_2 | resultado |
| {5,3,4,4}                     | {3,1,2,3}                     |  0.85     |
