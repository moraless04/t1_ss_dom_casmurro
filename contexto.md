# AGENTS.md — Instruções para o Codex

## Contexto do projeto

Este é um trabalho acadêmico da disciplina de Segurança de Sistemas sobre:

- Cifra de Vigenère;
- criptoanálise de Vigenère;
- Índice de Coincidência;
- análise de frequência para português.

A linguagem escolhida é Python.

O arquivo `contexto.md` contém o contexto completo, requisitos do trabalho, estratégia do algoritmo e roteiro de testes. **Leia `contexto.md` antes de fazer alterações importantes.**

---

## Objetivo principal

Construir uma implementação funcional, didática e explicável que:

1. leia o arquivo `dom casmurro.txt`;
2. higienize o texto;
3. criptografe usando Vigenère;
4. descriptografe usando uma chave conhecida;
5. estime o tamanho de uma chave desconhecida usando Índice de Coincidência;
6. descubra a chave por análise estatística de frequência;
7. descriptografe o texto sem receber a chave original.

O código deve ser suficientemente robusto para receber arquivos diferentes durante a apresentação.

---

## Regra mais importante

**Não transformar o projeto em uma solução excessivamente complexa.**

Prioridades:

1. Correção
2. Clareza
3. Entendimento dos conceitos
4. Testabilidade
5. Eficiência suficiente

Não otimizar para ter o menor número possível de linhas.

O aluno precisa conseguir explicar o código durante uma apresentação individual.

---

## Desenvolvimento incremental

Trabalhe uma etapa por vez.

Ordem preferencial:

1. analisar os arquivos existentes;
2. implementar/testar higienização;
3. implementar/testar criptografia;
4. implementar/testar descriptografia;
5. implementar/testar Índice de Coincidência;
6. implementar/testar estimativa do tamanho da chave;
7. implementar/testar divisão em subtextos;
8. implementar/testar análise de frequência;
9. implementar/testar descoberta da chave;
10. integrar o ataque completo;
11. testar com diferentes textos e chaves;
12. revisar organização e documentação.

Não implemente todas as etapas de uma vez quando ainda não existe uma base funcional.

Após cada etapa importante, informe resumidamente:

- o que mudou;
- por que mudou;
- como testar;
- possíveis limitações.

---

## Antes de modificar

Sempre:

- verificar a estrutura atual do projeto;
- verificar se já existe código;
- preservar código funcional;
- evitar sobrescrever arquivos sem necessidade;
- verificar testes existentes.

Se o usuário fornecer um `.txt`, analisar esse arquivo antes de criar hipóteses sobre seu conteúdo.

---

## Cifra de Vigenère

Usar:

```text
a = 0
b = 1
...
z = 25
```

Criptografia:

```text
C = (P + K) mod 26
```

Descriptografia:

```text
P = (C - K + 26) mod 26
```

A chave deve ser repetida ciclicamente.

Não usar biblioteca que implemente Vigenère automaticamente.

---

## Higienização

A higienização deve:

- converter para minúsculas;
- remover acentos;
- remover pontuação;
- remover números;
- remover espaços;
- remover caracteres especiais;
- manter somente `a-z`.

Dar atenção especial a Unicode e caracteres portugueses como:

```text
á à â ã ä
é ê
í
ó ô õ ö
ú
ç
```

A implementação deve ser geral, não apenas substituir manualmente alguns caracteres conhecidos.

Depois da higienização, validar que o resultado contém somente:

```text
abcdefghijklmnopqrstuvwxyz
```

---

## Índice de Coincidência

Usar a fórmula:

```text
IC = Σ f_i(f_i - 1) / (N(N - 1))
```

onde:

- `f_i` é a frequência de uma letra;
- `N` é o tamanho do texto.

Ao testar possíveis tamanhos de chave, dividir o texto em subtextos de acordo com a posição da chave.

Exemplo para chave de tamanho 3:

```text
subtexto 0 = posições 0, 3, 6, 9, ...
subtexto 1 = posições 1, 4, 7, 10, ...
subtexto 2 = posições 2, 5, 8, 11, ...
```

Testar inicialmente tamanhos de 1 até 10, conforme o enunciado.

Não assumir automaticamente que o maior IC isolado sempre é a resposta. Se necessário, manter candidatos e documentar a estratégia.

---

## Criptoanálise por frequência

Depois de estimar o tamanho da chave:

1. separar o texto em subtextos;
2. analisar a frequência de cada subtexto;
3. testar os 26 deslocamentos;
4. comparar cada resultado com uma distribuição esperada do português;
5. escolher o deslocamento mais provável;
6. transformar os deslocamentos em letras da chave;
7. descriptografar.

Cada subtexto pode ser tratado como um problema semelhante a uma cifra de César.

Não utilizar uma ferramenta externa que resolva automaticamente o ataque.

---

## Frequências do português

Manter a tabela de frequências de letras do português explicitamente no projeto.

Exemplo de estrutura:

```python
FREQUENCIAS_PORTUGUES = {
    "a": ...,
    "b": ...,
    # ...
}
```

A tabela é uma aproximação estatística e não deve ser tratada como verdade absoluta para qualquer texto.

Documentar a origem ou a natureza aproximada da tabela no código/README.

---

## Organização do código

Preferir funções pequenas e com responsabilidades claras.

Funções esperadas ou equivalentes:

```python
higienizar()
criptografar()
descriptografar()
calcular_ic()
dividir_subtextos()
estimar_tamanho_chave()
calcular_frequencias()
encontrar_melhor_deslocamento()
descobrir_chave()
quebrar_vigenere()
```

Nomes devem ser claros e, preferencialmente, em português, já que isso facilita a apresentação para a disciplina.

Evitar funções gigantes.

---

## Dependências

Preferir Python padrão.

Não adicionar bibliotecas externas sem necessidade.

Se uma dependência externa for proposta:

1. explicar por que é necessária;
2. verificar se não substitui a implementação que o trabalho exige;
3. manter a parte principal da cifra e da criptoanálise implementada pelo projeto.

---

## Arquivos

Estrutura inicial preferida:

```text
seguranca-sistemas/
├── AGENTS.md
├── contexto.md
├── README.md
├── .gitignore
├── main.py
├── texto_original.txt
└── texto_cifrado.txt
```

Se o código ficar grande, pode ser separado em:

```text
vigenere.py
criptoanalise.py
estatisticas.py
```

Não separar prematuramente.

---

## Interface

Uma interface simples de terminal é suficiente.

Pode utilizar:

```text
1 - Criptografar
2 - Descriptografar
3 - Quebrar Vigenère
4 - Sair
```

ou argumentos de linha de comando.

Priorizar facilidade de demonstração.

---

## Testes

Sempre testar pelo menos:

### Higienização

Entrada com:

- maiúsculas;
- acentos;
- cedilha;
- números;
- espaços;
- pontuação;
- caracteres especiais.

### Cifra

Verificar que:

```text
descriptografar(criptografar(texto, chave), chave)
```

recupera exatamente o texto higienizado.

### Ataque

Fluxo:

```text
texto
→ criptografar
→ esquecer a chave
→ estimar tamanho
→ descobrir chave
→ descriptografar
```

Testar mais de uma chave e, quando possível, mais de um texto.

---

## Arquivos grandes

O enunciado exige suporte a arquivos grandes.

Evitar algoritmos desnecessariamente quadráticos.

Para arquivos razoáveis, `read()` pode ser utilizado por simplicidade.

Se houver evidência de que o tamanho dos arquivos exige processamento em blocos, adaptar depois.

Não sacrificar clareza por otimizações prematuras.

---

## O que NÃO fazer

Nunca:

- hardcodar a senha;
- hardcodar o tamanho da chave;
- hardcodar o texto esperado;
- adaptar o algoritmo para funcionar somente com `Dom Casmurro`;
- usar uma biblioteca pronta para quebrar Vigenère;
- esconder o algoritmo principal em uma chamada de biblioteca;
- criar código propositalmente ofuscado;
- adicionar frameworks desnecessários;
- criar arquitetura complexa apenas por "boas práticas";
- apagar código funcional sem necessidade.

---

## Explicabilidade

Sempre que implementar matemática ou criptoanálise, manter a correspondência entre teoria e código clara.

O aluno deverá conseguir explicar:

- módulo 26;
- repetição da chave;
- Índice de Coincidência;
- divisão em subtextos;
- frequência de letras;
- deslocamento de César;
- comparação estatística;
- reconstrução da chave.

Comentários devem explicar conceitos, não narrar cada linha.

Exemplo bom:

```python
# A chave é repetida ciclicamente ao longo do texto.
indice_chave = (indice_chave + 1) % len(chave)
```

Exemplo ruim:

```python
# soma 1 em indice_chave
indice_chave += 1
```

---

## Tratamento de erros

O programa deve lidar de maneira razoável com:

- arquivo inexistente;
- arquivo vazio;
- chave vazia;
- chave contendo caracteres inválidos;
- texto sem letras após higienização;
- tentativa de calcular IC em texto muito curto;
- tamanho de chave maior que o texto.

Não criar tratamento excessivamente complexo.

Mensagens de erro devem ser claras.

---

## Regra para alterações

Se o usuário pedir uma mudança:

1. entender o pedido;
2. verificar impacto no restante do projeto;
3. alterar apenas o necessário;
4. preservar comportamento já correto;
5. executar testes relevantes.

Se houver duas abordagens possíveis, explicar brevemente a diferença antes de escolher uma quando a decisão afetar a arquitetura.

---

## Quando o projeto estiver funcionando

Não encerrar simplesmente dizendo "funciona".

Fazer uma revisão final considerando:

- correção;
- legibilidade;
- nomes;
- duplicação de código;
- tratamento de erros;
- eficiência;
- testes;
- facilidade de apresentação.

Depois preparar uma lista dos principais conceitos que o aluno deve saber explicar.

---

## Regra sobre o usuário

O usuário quer usar o Codex para desenvolver o trabalho, mas pretende posteriormente analisar e entender o código.

Portanto, gerar código funcional é permitido, mas a implementação deve permanecer didática e acompanhada de explicações suficientes para que o usuário consiga estudar o que foi feito.

Quando houver uma decisão algorítmica importante, explicar o raciocínio em vez de apenas aplicar a mudança.

---

## Estado inicial esperado

No início do projeto, o próximo passo é:

1. ler `contexto.md`;
2. verificar se o `.txt` da atividade está presente;
3. analisar o texto fornecido;
4. reportar o que foi encontrado;
5. propor a primeira implementação;
6. só então começar a codificar.

Se o arquivo `.txt` ainda não estiver presente, não inventar seu conteúdo.
