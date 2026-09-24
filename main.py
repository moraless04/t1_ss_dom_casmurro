"""Cifra de Vigenere: higienizacao, criptografia e descriptografia."""

from pathlib import Path
import unicodedata


PASTA_PROJETO = Path(__file__).parent
ARQUIVO_ORIGINAL = PASTA_PROJETO / "texto_original.txt"
ARQUIVO_CIFRADO = PASTA_PROJETO / "texto_cifrado.txt"
ARQUIVO_DECIFRADO = PASTA_PROJETO / "texto_decifrado.txt"
ALFABETO = "abcdefghijklmnopqrstuvwxyz"
MAX_TAMANHO_CHAVE = 10
MINIMO_LETRAS_POR_SUBTEXTO = 20

# Percentuais aproximados de letras em português, publicados a partir do
# corpus jornalístico CTEMPúblico (mais de 180 milhões de palavras):
# https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/
FREQUENCIAS_PORTUGUES = {
    "a": 13.9, "b": 1.0, "c": 4.4, "d": 5.4, "e": 12.2,
    "f": 1.0, "g": 1.2, "h": 0.8, "i": 6.9, "j": 0.4,
    "k": 0.1, "l": 2.8, "m": 4.2, "n": 5.3, "o": 10.8,
    "p": 2.9, "q": 0.9, "r": 6.9, "s": 7.9, "t": 4.9,
    "u": 4.0, "v": 1.3, "w": 0.0, "x": 0.3, "y": 0.0,
    "z": 0.4,
}


def higienizar(texto):
    """Converte para minusculas, remove acentos e mantem somente a-z."""
    texto = unicodedata.normalize("NFD", texto.lower())
    sem_acentos = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return "".join(letra for letra in sem_acentos if "a" <= letra <= "z")


def transformar_vigenere(texto, chave, decifrar=False):
    """Aplica Vigenere; decifrar=True usa a operacao inversa."""
    texto = higienizar(texto)
    chave = higienizar(chave)
    if not chave:
        raise ValueError("A chave precisa conter pelo menos uma letra de a a z.")

    resultado = []
    for indice, letra in enumerate(texto):
        valor_texto = ord(letra) - ord("a")
        valor_chave = ord(chave[indice % len(chave)]) - ord("a")
        if decifrar:
            valor_novo = (valor_texto - valor_chave) % 26
        else:
            valor_novo = (valor_texto + valor_chave) % 26
        resultado.append(chr(valor_novo + ord("a")))

    return "".join(resultado)


def calcular_ic(texto):
    """Calcula o Indice de Coincidencia de um texto higienizado."""
    texto = higienizar(texto)
    tamanho = len(texto)
    if tamanho < 2:
        raise ValueError("O texto precisa ter ao menos duas letras para calcular o IC.")

    frequencias = [0] * 26
    for letra in texto:
        indice_letra = ord(letra) - ord("a")
        frequencias[indice_letra] += 1

    pares_iguais = sum(
        frequencia * (frequencia - 1)
        for frequencia in frequencias
    )
    total_de_pares = tamanho * (tamanho - 1)
    return pares_iguais / total_de_pares


def dividir_subtextos(texto, tamanho_chave):
    """Agrupa letras pelas posicoes que usariam a mesma letra da chave."""
    if tamanho_chave < 1:
        raise ValueError("O tamanho da chave deve ser maior que zero.")

    texto = higienizar(texto)
    if tamanho_chave > len(texto):
        raise ValueError("O tamanho da chave nao pode superar o numero de letras.")
    return [texto[posicao::tamanho_chave] for posicao in range(tamanho_chave)]


def estimar_tamanho_chave(texto, max_tamanho=MAX_TAMANHO_CHAVE):
    """Calcula o IC medio dos subtextos para cada tamanho candidato."""
    texto = higienizar(texto)
    if len(texto) < 2:
        raise ValueError("O texto precisa ter ao menos duas letras para estimar a chave.")
    if max_tamanho < 1:
        raise ValueError("O tamanho maximo da chave deve ser maior que zero.")

    # Cada subtexto precisa ter pelo menos duas letras para que seu IC exista.
    limite_teste = min(max_tamanho, len(texto) // 2)
    indices_medios = {}

    for tamanho_chave in range(1, limite_teste + 1):
        subtextos = dividir_subtextos(texto, tamanho_chave)
        ic_medio = sum(calcular_ic(subtexto) for subtexto in subtextos)
        ic_medio /= len(subtextos)
        indices_medios[tamanho_chave] = ic_medio

    return indices_medios


def calcular_frequencias(texto):
    """Conta quantas vezes cada letra de a-z aparece no texto."""
    texto = higienizar(texto)
    if not texto:
        raise ValueError("O subtexto precisa conter letras para analisar frequencias.")

    frequencias = {letra: 0 for letra in ALFABETO}
    for letra in texto:
        frequencias[letra] += 1
    return frequencias


def encontrar_melhor_deslocamento(subtexto):
    """Retorna o deslocamento cuja distribuicao mais se aproxima do portugues."""
    subtexto = higienizar(subtexto)
    if not subtexto:
        raise ValueError("O subtexto precisa conter letras para analisar deslocamentos.")

    soma_frequencias_esperadas = sum(FREQUENCIAS_PORTUGUES.values())
    menor_distancia = float("inf")
    melhor_deslocamento = 0

    # Cada deslocamento e uma hipotese para a letra correspondente da chave.
    for deslocamento in range(26):
        texto_candidato = "".join(
            chr((ord(letra) - ord("a") - deslocamento) % 26 + ord("a"))
            for letra in subtexto
        )
        frequencias_observadas = calcular_frequencias(texto_candidato)

        # Soma das diferencas absolutas entre proporcoes observadas e esperadas.
        # Uma distancia menor indica uma distribuicao mais parecida.
        distancia = 0.0
        for letra in ALFABETO:
            proporcao_observada = frequencias_observadas[letra] / len(texto_candidato)
            proporcao_esperada = (
                FREQUENCIAS_PORTUGUES[letra] / soma_frequencias_esperadas
            )
            distancia += abs(proporcao_observada - proporcao_esperada)

        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_deslocamento = deslocamento

    return melhor_deslocamento, menor_distancia


def descobrir_chave(texto_cifrado, tamanho_chave):
    """Combina as letras estimadas para todos os subtextos."""
    subtextos = dividir_subtextos(texto_cifrado, tamanho_chave)
    letras_chave = []

    for subtexto in subtextos:
        deslocamento, _ = encontrar_melhor_deslocamento(subtexto)
        letras_chave.append(chr(deslocamento + ord("a")))

    return "".join(letras_chave)


def quebrar_vigenere(texto_cifrado, max_tamanho=MAX_TAMANHO_CHAVE):
    """Estima o tamanho e a chave, depois descriptografa o texto."""
    indices_medios = estimar_tamanho_chave(texto_cifrado, max_tamanho)
    tamanho_chave = max(indices_medios, key=indices_medios.get)
    quantidade_letras = len(higienizar(texto_cifrado))
    letras_por_subtexto = quantidade_letras / tamanho_chave
    if letras_por_subtexto < MINIMO_LETRAS_POR_SUBTEXTO:
        raise ValueError(
            "O tamanho estimado deixa poucos dados para a analise de frequencia: "
            f"{letras_por_subtexto:.1f} letras por subtexto. Use um texto maior "
            f"ou uma chave menor; o recomendado e ao menos "
            f"{MINIMO_LETRAS_POR_SUBTEXTO} letras por subtexto."
        )
    chave_estimada = descobrir_chave(texto_cifrado, tamanho_chave)
    texto_decifrado = transformar_vigenere(
        texto_cifrado,
        chave_estimada,
        decifrar=True,
    )
    return tamanho_chave, chave_estimada, texto_decifrado, indices_medios


def validar_chave_para_criptoanalise(texto, chave):
    """Garante amostras suficientes para o ataque por frequencia."""
    texto_higienizado = higienizar(texto)
    chave_higienizada = higienizar(chave)
    tamanho_maximo_pelo_texto = len(texto_higienizado) // MINIMO_LETRAS_POR_SUBTEXTO
    tamanho_maximo = min(MAX_TAMANHO_CHAVE, tamanho_maximo_pelo_texto)

    if len(chave_higienizada) > tamanho_maximo:
        raise ValueError(
            "A chave tem "
            f"{len(chave_higienizada)} letras, mas este texto permite no maximo "
            f"{tamanho_maximo} para a criptoanalise por frequencia. O programa "
            f"testa chaves de ate {MAX_TAMANHO_CHAVE} letras. "
            f"Use uma chave menor ou um texto com pelo menos "
            f"{len(chave_higienizada) * MINIMO_LETRAS_POR_SUBTEXTO} letras higienizadas."
        )


def ler_arquivo(caminho):
    return caminho.read_text(encoding="utf-8")


def criptografar_arquivo(chave):
    texto_original = ler_arquivo(ARQUIVO_ORIGINAL)
    validar_chave_para_criptoanalise(texto_original, chave)
    texto_cifrado = transformar_vigenere(texto_original, chave)
    ARQUIVO_CIFRADO.write_text(texto_cifrado, encoding="utf-8")
    print(f"Texto cifrado salvo em: {ARQUIVO_CIFRADO.name}")


def descriptografar_arquivo(chave):
    texto_cifrado = ler_arquivo(ARQUIVO_CIFRADO)
    texto_decifrado = transformar_vigenere(texto_cifrado, chave, decifrar=True)
    ARQUIVO_DECIFRADO.write_text(texto_decifrado, encoding="utf-8")
    print(f"Texto descriptografado salvo em: {ARQUIVO_DECIFRADO.name}")


def mostrar_ic_arquivo():
    texto_cifrado = ler_arquivo(ARQUIVO_CIFRADO)
    indice = calcular_ic(texto_cifrado)
    indices_medios = estimar_tamanho_chave(texto_cifrado)
    media_de_todos_ics = sum(indices_medios.values()) / len(indices_medios)

    print(f"Indice de Coincidencia do texto cifrado: {indice:.6f}")
    print(
        "Media dos ICs medios para os tamanhos de chave de 1 a "
        f"{MAX_TAMANHO_CHAVE}: {media_de_todos_ics:.6f}"
    )


def mostrar_estimativa_tamanho_chave(max_tamanho=MAX_TAMANHO_CHAVE):
    texto_cifrado = ler_arquivo(ARQUIVO_CIFRADO)
    indices_medios = estimar_tamanho_chave(texto_cifrado, max_tamanho)
    tamanho_mais_provavel = max(indices_medios, key=indices_medios.get)
    melhores_candidatos = sorted(
        indices_medios.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:3]

    print("Tamanho da chave | IC medio dos subtextos")
    for tamanho, indice in indices_medios.items():
        print(f"{tamanho:16} | {indice:.6f}")

    print(f"\nMelhor candidato pelo IC: {tamanho_mais_provavel}")
    candidatos = ", ".join(str(tamanho) for tamanho, _ in melhores_candidatos)
    print(f"Os três candidatos com IC mais alto: {candidatos}")
    print("A estimativa e provisoria; multiplos do tamanho real tambem podem pontuar alto.")


def mostrar_analise_deslocamento():
    texto_cifrado = ler_arquivo(ARQUIVO_CIFRADO)
    tamanho_chave = int(input("Tamanho candidato da chave: "))
    subtextos = dividir_subtextos(texto_cifrado, tamanho_chave)
    posicao = int(input(f"Posicao do subtexto (0 a {tamanho_chave - 1}): "))
    if not 0 <= posicao < len(subtextos):
        raise ValueError("A posicao precisa estar dentro do tamanho da chave.")

    deslocamento, distancia = encontrar_melhor_deslocamento(subtextos[posicao])
    letra_chave = chr(deslocamento + ord("a"))
    print(f"Deslocamento mais provavel: {deslocamento} (letra {letra_chave})")
    print(f"Distancia em relacao ao portugues: {distancia:.6f} (menor e melhor)")


def mostrar_quebra_automatica(max_tamanho=MAX_TAMANHO_CHAVE):
    texto_cifrado = ler_arquivo(ARQUIVO_CIFRADO)
    tamanho, chave, texto_decifrado, indices_medios = quebrar_vigenere(
        texto_cifrado,
        max_tamanho,
    )

    print("Tamanho da chave | IC medio dos subtextos")
    for tamanho_teste, indice in indices_medios.items():
        print(f"{tamanho_teste:16} | {indice:.6f}")

    melhores_candidatos = sorted(
        indices_medios.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:3]
    candidatos = ", ".join(str(tamanho_teste) for tamanho_teste, _ in melhores_candidatos)
    print(f"\nTamanho estimado: {tamanho}")
    print(f"Tamanhos candidatos com IC mais alto: {candidatos}")
    print(f"Chave estimada: {chave}")
    print("Multiplos do tamanho real tambem podem pontuar alto.")
    print("A estimativa e estatistica; textos curtos podem produzir uma chave incorreta.")

    ARQUIVO_DECIFRADO.write_text(texto_decifrado, encoding="utf-8")
    print(f"Texto decifrado salvo em: {ARQUIVO_DECIFRADO.name}")
    print("Previa do texto decifrado:")
    print(texto_decifrado[:500])


def main():
    print("=== SEGURANCA DE SISTEMAS: VIGENERE ===")
    print("1 - Criptografar texto_original.txt")
    print("2 - Descriptografar texto_cifrado.txt")
    print("3 - Calcular Média do Indice de Coincidencia")
    print("4 - Estimar tamanho da chave")
    print("5 - Quebrar Vigenere automaticamente")
    print("6 - Sair")

    opcao = input("Opcao: ").strip()
    if opcao == "1":
        try:
            criptografar_arquivo(input("Chave: "))
        except ValueError as erro:
            print(erro)
    elif opcao == "2":
        try:
            descriptografar_arquivo(input("Chave: "))
        except ValueError as erro:
            print(erro)
    elif opcao == "3":
        try:
            mostrar_ic_arquivo()
        except ValueError as erro:
            print(erro)
    elif opcao == "4":
        try:
            mostrar_estimativa_tamanho_chave()
        except ValueError as erro:
            print(erro)
    elif opcao == "5":
        try:
            mostrar_quebra_automatica()
        except ValueError as erro:
            print(erro)
    elif opcao == "6":
        print("Encerrado.")
    else:
        print("Opcao invalida.")
    # elif opcao == "5":
    #     try:
    #         mostrar_analise_deslocamento()
    #     except ValueError as erro:
    #         print(erro)


if __name__ == "__main__":
    main()
