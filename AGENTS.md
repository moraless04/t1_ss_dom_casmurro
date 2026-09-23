# CONTEXTO — Trabalho de Segurança de Sistemas
## Criptografia e Criptoanálise com Cifra de Vigenère

Este arquivo serve como contexto principal para o Codex no VS Code. Leia este documento antes de modificar o projeto.

---

# 1. Objetivo do trabalho

O trabalho da disciplina de Segurança de Sistemas exige a implementação de dois algoritmos:

1. Um algoritmo de criptografia utilizando a Cifra de Vigenère.
2. Um algoritmo de criptoanálise capaz de quebrar a cifra sem conhecer a senha.

A implementação pode ser feita em Java, Python ou C++. A linguagem escolhida para este projeto é **Python**, priorizando:

- código curto e legível;
- facilidade de entendimento;
- facilidade de explicação na apresentação;
- manipulação simples de arquivos e strings;
- implementação clara dos conceitos matemáticos;
- funcionamento adequado com arquivos grandes.

A avaliação será prática e pode utilizar arquivos diferentes dos usados durante o desenvolvimento. Portanto, não criar uma solução que funcione apenas para um texto específico.

A apresentação é individual. Todos os integrantes precisam conseguir explicar:

- funcionamento da Cifra de Vigenère;
- funcionamento do ataque;
- código implementado.

O professor pode fazer perguntas para qualquer integrante.

---

# 2. Requisitos obrigatórios do enunciado

## Parte 1 — Criptografia

Entrada:

- arquivo `.txt` contendo o texto original;
- senha/chave fornecida pelo usuário.

Saída:

- arquivo contendo o texto criptografado.

### Higienização obrigatória

Antes da criptografia:

1. converter todo o texto para minúsculas;
2. remover acentos;
3. remover pontuação;
4. remover números;
5. remover espaços;
6. remover caracteres especiais;
7. manter somente letras de `a` a `z`.

Exemplos:

- `á` → `a`
- `ç` → `c`
- `ã` → `a`

Depois da higienização, o texto deve conter somente caracteres entre `a` e `z`.

### Criptografia

A senha deve ser repetida ciclicamente ao longo do texto.

A Cifra de Vigenère utiliza operações modulares no alfabeto de 26 letras.

Representação:

```text
a = 0
b = 1
c = 2
...
z = 25
```

Fórmula de criptografia:

C_i = (P_i + K_i) mod 26

Onde:

- P_i = valor da letra do texto original;
- K_i = valor da letra da chave;
- C_i = valor da letra cifrada.

---

# 3. Descriptografia

Embora a proposta destaque principalmente a criptografia e a criptoanálise, implementar também uma função de descriptografia é recomendado para validar a implementação.

Fórmula:

P_i = (C_i - K_i + 26) mod 26

A descriptografia deve ser capaz de recuperar exatamente o texto higienizado quando a chave correta é fornecida.

Teste fundamental:

```text
texto original
    ↓
higienização
    ↓
criptografia
    ↓
texto cifrado
    ↓
descriptografia com a mesma chave
    ↓
texto higienizado original
```

---

# 4. Parte 2 — Criptoanálise

O programa deve tentar recuperar o texto original sem conhecer a senha, assumindo que o idioma é português.

O ataque deve ser dividido em duas etapas principais.

## Etapa 1 — Descoberta do tamanho da senha

Calcular o Índice de Coincidência (IC) para diferentes tamanhos possíveis de chave.

O enunciado sugere, por exemplo, testar tamanhos de 1 até 10.

Para cada tamanho:

1. dividir o texto cifrado em subtextos de acordo com as posições da chave;
2. calcular o IC dos subtextos;
3. obter uma medida representativa para aquele tamanho;
4. comparar os resultados;
5. identificar os tamanhos mais prováveis.

Não assumir cegamente que o maior valor isolado sempre é a resposta. O algoritmo deve ser explicado e, se necessário, considerar candidatos próximos/múltiplos.

---

# 5. Índice de Coincidência

Para um texto com N caracteres e frequências f_i para cada uma das 26 letras:

IC = [Σ f_i(f_i - 1)] / [N(N - 1)]

O cálculo deve considerar as letras `a` a `z`.

Para cada tamanho de chave K:

```text
subtexto 0 = posições 0, K, 2K, 3K, ...
subtexto 1 = posições 1, K+1, 2K+1, ...
subtexto 2 = posições 2, K+2, 2K+2, ...
...
```

Depois calcular o IC de cada subtexto e obter uma medida agregada, como a média.

Criar uma saída de diagnóstico semelhante a:

```text
Tamanho da chave | IC médio
1                | 0.xxxx
2                | 0.xxxx
3                | 0.xxxx
...
10               | 0.xxxx
```

Isso será útil durante a apresentação.

---

# 6. Etapa 2 — Análise de frequência

Depois de estimar o tamanho da chave:

1. dividir o texto cifrado em um subtexto para cada posição da chave;
2. calcular a frequência das letras de cada subtexto;
3. comparar com a distribuição típica das letras do português;
4. inferir o deslocamento correspondente a cada posição da chave;
5. aplicar o deslocamento inverso;
6. reconstruir o texto original.

A ideia importante para entender:

Cada posição da chave da Vigenère funciona como um deslocamento de César sobre o respectivo subtexto.

Exemplo conceitual:

```text
chave = ABCD

posição 0 → deslocamento A
posição 1 → deslocamento B
posição 2 → deslocamento C
posição 3 → deslocamento D
```

Assim, depois de descobrir o tamanho da chave, cada subtexto pode ser analisado como um problema de encontrar um deslocamento entre 0 e 25.

---

# 7. Método de análise de frequência

Para cada subtexto, testar os 26 deslocamentos possíveis:

```text
0
1
2
...
25
```

Para cada deslocamento:

1. aplicar o deslocamento inverso;
2. calcular a distribuição resultante;
3. comparar essa distribuição com a distribuição esperada para o português;
4. atribuir uma pontuação;
5. selecionar o deslocamento com melhor correspondência.

A comparação deve ser baseada em um método estatístico simples e explicável.

Uma abordagem recomendada é utilizar uma métrica de distância entre a frequência observada e a frequência esperada do português.

Não utilizar uma biblioteca pronta que simplesmente "quebre Vigenère".

O algoritmo precisa ser implementado pelo projeto e ser compreensível durante a apresentação.

---

# 8. Frequência do português

Precisamos utilizar uma tabela de frequências esperadas das letras do português.

Essa tabela deve ficar claramente identificada no código, por exemplo:

```python
FREQUENCIAS_PORTUGUES = {
    "a": ...,
    "b": ...,
    ...
    "z": ...
}
```

Não esconder essa informação dentro de uma biblioteca.

Se for necessário escolher uma tabela de frequências, documentar no código que ela representa uma distribuição aproximada do português e manter a fonte/justificativa em comentário ou no README.

Não assumir que uma única tabela funciona perfeitamente para qualquer tipo de texto. Textos muito curtos ou com vocabulário muito específico podem gerar resultados menos confiáveis.

---

# 9. Estrutura inicial recomendada

Começar simples.

Estrutura:

```text
seguranca-sistemas/
│
├── main.py
├── texto_original.txt
├── texto_cifrado.txt
└── contexto.md
```

Inicialmente, pode ser utilizado um único `main.py`.

Se o arquivo crescer demais, separar posteriormente em módulos:

```text
seguranca-sistemas/
│
├── main.py
├── vigenere.py
├── criptoanalise.py
├── estatisticas.py
├── texto_original.txt
├── texto_cifrado.txt
└── contexto.md
```

Não criar arquitetura excessivamente complexa sem necessidade.

---

# 10. Funções esperadas

A implementação deve, preferencialmente, ser organizada em funções pequenas e explicáveis.

Funções sugeridas:

```python
def higienizar(texto):
    ...

def criptografar(texto, chave):
    ...

def descriptografar(texto_cifrado, chave):
    ...

def calcular_ic(texto):
    ...

def dividir_subtextos(texto, tamanho_chave):
    ...

def estimar_tamanho_chave(texto, max_tamanho=10):
    ...

def calcular_frequencias(texto):
    ...

def encontrar_melhor_deslocamento(subtexto):
    ...

def descobrir_chave(texto_cifrado, tamanho_chave):
    ...

def quebrar_vigenere(texto_cifrado):
    ...
```

Os nomes podem ser ajustados se houver uma razão clara.

---

# 11. Interface

A interface pode ser simples de linha de comando.

Uma opção:

```text
1 - Criptografar arquivo
2 - Descriptografar arquivo
3 - Quebrar cifra
4 - Sair
```

Ou argumentos de linha de comando, se isso tornar o projeto mais simples.

Priorizar a solução que seja fácil de demonstrar.

---

# 12. Fluxo da criptografia

O fluxo esperado:

```text
arquivo .txt
     ↓
leitura
     ↓
higienização
     ↓
chave fornecida
     ↓
Vigenère
     ↓
texto_cifrado.txt
```

---

# 13. Fluxo da criptoanálise

O fluxo esperado:

```text
texto_cifrado.txt
       ↓
estimar tamanho da chave
       ↓
dividir em subtextos
       ↓
calcular frequências
       ↓
testar deslocamentos 0..25
       ↓
comparar com português
       ↓
obter uma letra da chave para cada posição
       ↓
montar chave estimada
       ↓
descriptografar
       ↓
texto legível
```

---

# 14. Testes obrigatórios/recomendados

## Teste 1 — Higienização

Usar uma frase com:

- letras maiúsculas;
- letras minúsculas;
- acentos;
- cedilha;
- espaços;
- pontuação;
- números;
- caracteres especiais.

Exemplo:

```text
Olá, Mundo! 123 Çãção.
```

Esperar algo equivalente a:

```text
olamundocacao
```

Verificar cuidadosamente a remoção de acentos.

---

## Teste 2 — Criptografia conhecida

Usar a chave sugerida no enunciado:

```text
segredo
```

Usar `Dom Casmurro` ou outro texto fornecido.

---

## Teste 3 — Criptografia + descriptografia

Garantir:

```text
higienizado == descriptografar(criptografar(higienizado, chave), chave)
```

---

## Teste 4 — Ataque

1. escolher um texto razoavelmente grande em português;
2. escolher uma chave;
3. criptografar;
4. apagar/ignorar a chave;
5. executar o ataque;
6. verificar o tamanho estimado;
7. verificar a chave estimada;
8. verificar se o texto recuperado é legível.

---

# 15. Textos curtos

O ataque estatístico pode falhar ou ficar instável em textos muito curtos.

Não esconder esse fato.

Se o resultado for ruim, investigar:

- tamanho do texto;
- tamanho da chave;
- qualidade da estimativa do IC;
- distribuição das letras;
- escolha da métrica de frequência.

O programa não deve ser artificialmente ajustado para um único texto.

---

# 16. Arquivos grandes

O enunciado exige funcionamento com arquivos grandes.

Evitar:

- loops desnecessários;
- recalcular frequências repetidamente quando não for necessário;
- estruturas de dados excessivamente pesadas;
- bibliotecas externas sem necessidade.

Para os testes iniciais, `read()` é aceitável se os arquivos forem razoáveis.

Se forem encontrados arquivos realmente grandes, considerar processamento por blocos.

Não sacrificar clareza prematuramente por uma otimização que não é necessária.

---

# 17. Regras importantes para o desenvolvimento

O objetivo não é apenas gerar um código que funcione.

O código precisa ser:

- legível;
- didático;
- comentado onde o conceito não for óbvio;
- modular;
- fácil de apresentar;
- fácil de testar;
- independente de um texto específico.

Evitar:

- código excessivamente compacto;
- funções gigantes;
- "mágica" de bibliotecas;
- algoritmos prontos de criptoanálise;
- hardcode da chave;
- hardcode do tamanho da chave;
- hardcode de respostas;
- soluções específicas para `Dom Casmurro`;
- esconder etapas importantes dentro de uma única expressão.

---

# 18. Como o Codex deve trabalhar

IMPORTANTE:

Não substituir todo o projeto de uma vez sem necessidade.

Trabalhar incrementalmente.

Ordem recomendada:

1. analisar o estado atual do projeto;
2. verificar quais arquivos existem;
3. implementar a higienização;
4. testar;
5. implementar Vigenère;
6. testar;
7. implementar descriptografia;
8. testar;
9. implementar IC;
10. testar;
11. implementar estimativa do tamanho da chave;
12. testar;
13. implementar análise de frequência;
14. testar;
15. implementar descoberta da chave;
16. integrar o ataque;
17. testar com diferentes textos e chaves;
18. melhorar organização somente depois que a lógica estiver funcionando.

Depois de cada etapa, informar:

- o que foi alterado;
- por que foi alterado;
- como testar;
- quais limitações ainda existem.

Não avançar silenciosamente por várias etapas se uma etapa intermediária estiver falhando.

---

# 19. Regra sobre explicações

Sempre que implementar uma parte importante, explicar o conceito correspondente em linguagem simples.

Exemplo:

Antes de implementar:

```python
def calcular_ic(texto):
```

explicar:

- o que é o Índice de Coincidência;
- por que ele ajuda a estimar o tamanho da chave;
- qual fórmula será usada;
- como a implementação corresponde à fórmula.

Depois mostrar o código.

O mesmo vale para:

- Vigenère;
- módulo 26;
- repetição da chave;
- subtextos;
- frequência de letras;
- deslocamento de César;
- comparação estatística.

---

# 20. Regra sobre dependências

Preferir Python padrão.

Não instalar bibliotecas externas sem necessidade.

Se uma biblioteca externa for realmente útil:

1. explicar por que ela é necessária;
2. verificar se ela é permitida/adequada para o trabalho;
3. evitar que ela faça a parte principal da atividade automaticamente.

A implementação da cifra e da criptoanálise deve ser nossa.

---

# 21. Qualidade do código

Usar nomes de variáveis claros.

Preferir:

```python
tamanho_chave
frequencia_observada
frequencia_esperada
melhor_deslocamento
```

em vez de:

```python
x
y
z
a
b
```

Comentários devem explicar conceitos, não repetir literalmente o código.

Ruim:

```python
# incrementa i
i += 1
```

Bom:

```python
# A chave é repetida ciclicamente ao longo do texto.
indice_chave = (indice_chave + 1) % len(chave)
```

---

# 22. Segurança acadêmica

Não transformar o projeto em uma implementação de criptografia moderna.

Vigenère é uma cifra clássica e o objetivo é acadêmico.

Não usar AES, RSA ou bibliotecas de criptografia como substitutos da implementação pedida.

O foco é demonstrar:

- cifra clássica;
- análise estatística;
- criptoanálise;
- recuperação da chave;
- recuperação do texto.

---

# 23. Critérios de avaliação que devem orientar o projeto

O enunciado avalia:

- correção funcional dos algoritmos;
- qualidade da higienização;
- eficiência do ataque;
- organização do código;
- clareza da apresentação;
- domínio individual do conteúdo.

Portanto, não otimizar somente para "passar no teste".

O projeto precisa ser defensável durante uma apresentação oral.

---

# 24. Preparação para apresentação

Depois da implementação, preparar uma explicação capaz de responder:

### Vigenère

- O que é Vigenère?
- Por que usamos módulo 26?
- Como transformamos uma letra em número?
- Como a chave é repetida?
- Como ocorre a criptografia?
- Como ocorre a descriptografia?

### Higienização

- Por que remover acentos?
- Por que remover espaços?
- Por que manter apenas `a-z`?
- Como tratar caracteres Unicode?

### Índice de Coincidência

- O que é IC?
- Qual a fórmula?
- Por que ele ajuda a encontrar o tamanho da chave?
- Por que dividimos o texto em subtextos?

### Frequência

- Por que frequência de letras ajuda?
- Por que cada subtexto pode ser analisado como César?
- Como escolhemos o deslocamento?
- Como a distribuição do português é utilizada?

### Ataque

- O que acontece se a chave estimada estiver errada?
- O ataque funciona melhor com textos longos?
- Quais são as limitações?
- Como o programa reconstrói a chave?
- Como o texto é finalmente descriptografado?

---

# 25. Resultado final esperado

O projeto deverá permitir algo equivalente a:

```text
=== SEGURANÇA DE SISTEMAS ===

1 - Criptografar
2 - Descriptografar
3 - Quebrar Vigenère
4 - Sair

Opção: 1

Arquivo: texto_original.txt
Chave: segredo

Texto criptografado salvo em:
texto_cifrado.txt
```

E no ataque:

```text
=== CRIPTOANÁLISE ===

Arquivo: texto_cifrado.txt

Analisando possíveis tamanhos de chave...

Tamanho 1: IC = ...
Tamanho 2: IC = ...
Tamanho 3: IC = ...
...

Tamanho provável da chave: 7

Analisando frequência...

Chave estimada: segredo

Texto decifrado:
...
```

Os números acima são apenas exemplos de formato. Não hardcodar esses resultados.

---

# 26. Importante: primeiro analisar o .txt fornecido pelo usuário

O usuário ainda fornecerá um arquivo `.txt` para ser utilizado no desenvolvimento.

Quando ele for disponibilizado:

1. ler o conteúdo;
2. verificar tamanho;
3. verificar codificação;
4. verificar presença de acentos;
5. verificar caracteres especiais;
6. verificar se é texto em português;
7. verificar tamanho adequado para os testes;
8. usar o arquivo para testar a implementação.

Não assumir previamente o conteúdo do arquivo.

---

# 27. Estado atual

Até este momento:

- linguagem escolhida: Python;
- foco: simplicidade + entendimento + eficiência suficiente;
- trabalho: Vigenère + criptoanálise;
- próximo passo: receber/analisar o `.txt` do usuário;
- depois disso: iniciar a implementação incremental.

Não começar inventando dados de teste se o arquivo fornecido pelo usuário ainda não estiver disponível. Podemos criar pequenos testes unitários próprios para validar funções, mas o arquivo fornecido pelo usuário deve ser usado assim que estiver disponível.

---

# 28. Princípio final

Prioridade:

```text
CORREÇÃO
   ↓
ENTENDIMENTO
   ↓
TESTABILIDADE
   ↓
CLAREZA
   ↓
EFICIÊNCIA
```

Não buscar a menor quantidade possível de linhas a qualquer custo.

A meta é um código relativamente curto, mas que o aluno consiga explicar linha por linha e defender durante a apresentação.
