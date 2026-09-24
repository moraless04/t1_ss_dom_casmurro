# Trabalho de Segurança de Sistemas — Vigenère

Implementação acadêmica de:

- Cifra de Vigenère;
- descriptografia;
- Índice de Coincidência;
- estimativa do tamanho da chave;
- criptoanálise por frequência;
- recuperação da chave;
- recuperação do texto original.

## Linguagem

Python.

## Documentação principal

Leia primeiro:

- `contexto.md` — requisitos completos e estratégia do trabalho;
- `AGENTS.md` — instruções que devem orientar o Codex durante o desenvolvimento.

## Estrutura

```text
seguranca-sistemas/
├── AGENTS.md
├── contexto.md
├── README.md
├── .gitignore
├── main.py
├── dom casmurro.txt
├── texto_original.txt
├── texto_cifrado.txt
└── texto_decifrado.txt
```

Os arquivos de código podem ser separados em módulos posteriormente caso isso melhore a organização.

## Objetivo

O programa deve ser capaz de:

1. higienizar um texto;
2. criptografar com Vigenère;
3. descriptografar com chave conhecida;
4. estimar o tamanho de uma chave desconhecida;
5. descobrir a chave por análise de frequência;
6. descriptografar o texto sem receber a chave original.

## Execução

Para executar o menu:

```bash
python main.py
```

`texto_original.txt` é a cópia de trabalho do arquivo `dom casmurro.txt` fornecido. O programa permite higienizar, criptografar, descriptografar, calcular o Índice de Coincidência, estimar tamanhos candidatos, analisar um subtexto e executar o ataque automático para estimar a chave e salvar o texto recuperado em `texto_decifrado.txt`.

A análise de frequência usa uma distribuição aproximada publicada a partir do corpus jornalístico CTEMPúblico, com mais de 180 milhões de palavras. Como a tabela tem percentuais arredondados e representa um corpus específico, ela é normalizada no cálculo e pode não descrever perfeitamente todo texto em português. A comparação soma as diferenças absolutas entre as frequências observadas e esperadas; o menor resultado indica o deslocamento mais próximo.

Fonte: [Tabelas de frequências na língua portuguesa — Rogério Reis](https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/).

O ataque automático é estatístico: textos curtos, distribuição incomum de letras ou estimativa incorreta do tamanho da chave podem levar a uma chave incorreta. O programa mostra os principais tamanhos candidatos para facilitar a análise.

O ataque testa tamanhos de chave de 1 a 10, conforme o enunciado. Na opção de criptografia, o programa aceita chaves de no máximo 10 letras e exige pelo menos 20 letras por posição da chave. Assim, ele impede uma chave longa demais para o texto escolhido, pois ela impediria a recuperação estatística durante a criptoanálise.

## Observação acadêmica

Este projeto implementa uma cifra clássica para fins didáticos. Não deve ser utilizado como substituto de algoritmos criptográficos modernos.
