# tema_1.py - matriculas duplicadas
# PAA - trabalho pratico - tema 1
# rodar com: python tema_1.py

import math
import random
from trabalho_base import (mergesort, teste_do_dobro, salvar_csv,
                           matriculas, distintos, ordenado)


# ------------------------------------------------------------
# versao ingenua: compara cada matricula com as seguintes
# devolve (uma repetida ou None, comparacoes)
# ------------------------------------------------------------
def ing(v):
    c = 0
    n = len(v)
    for i in range(n):
        for j in range(i + 1, n):
            c += 1                      # compara v[i] com v[j]
            if v[i] == v[j]:
                return v[i], c
    return None, c


# ------------------------------------------------------------
# versao esperta: ordena com o mergesort e olha so os vizinhos
# esp_f devolve as fases separadas: (resultado, c_ord, c_var)
# ------------------------------------------------------------
def esp_f(v):
    w, c_ord = mergesort(v)
    c_var = 0
    for i in range(1, len(w)):
        c_var += 1                      # compara w[i-1] com w[i]
        if w[i - 1] == w[i]:
            return w[i], c_ord, c_var
    return None, c_ord, c_var


# esp junta as duas fases, no mesmo formato da ing
def esp(v):
    r, a, b = esp_f(v)
    return r, a + b


# ------------------------------------------------------------
# entradas de melhor e pior caso
# ------------------------------------------------------------
def ing_pior(n):
    # sem nenhuma repetida: tem que comparar todos os pares
    return distintos(n)


def ing_melhor(n):
    # as duas primeiras iguais: acha na 1a comparacao
    v = distintos(n)
    if n > 1:
        v[1] = v[0]
    return v


def mistura(l):
    # monta uma lista que faz o mergesort gastar o maximo
    # (cada intercalacao fica alternando esquerda/direita)
    if len(l) <= 1:
        return l
    return mistura(l[1::2]) + mistura(l[0::2])


def esp_pior(n):
    # sem repetidas e na ordem ruim pro mergesort
    return mistura(list(range(n)))


def esp_melhor(n):
    # ja ordenada (mergesort gasta pouco) e repetida no comeco
    v = ordenado(n)
    if n > 1:
        v[1] = v[0]
    return v


# ------------------------------------------------------------
# caso medio: 30 entradas aleatorias, so a media
# hipotese: n matriculas distintas e depois 1 copia (repetidas=1).
# as vezes a copia cai na mesma posicao e nao repete nada
# ------------------------------------------------------------
def medio(f, n, k=30):
    t = 0
    for s in range(k):
        v = matriculas(n, semente=s, repetidas=1)
        t += f(v)[1]
    return t / k


# ------------------------------------------------------------
# testes de correcao (set e count so aqui, como oraculo)
# ------------------------------------------------------------
def testa():
    r = random.Random(1)
    casos = [[], [7], [7, 7], [1, 2, 3], [5, 5, 5, 5], [1, 2, 1], [3, 1, 2, 3]]
    for _ in range(1000):               # aleatorias com muito repetido
        n = r.randint(0, 30)
        casos.append([r.randint(0, 20) for _ in range(n)])
    for _ in range(100):                # sem nenhum repetido
        casos.append(distintos(r.randint(0, 30), r.randint(1, 999)))
    for _ in range(100):                # gerador de matriculas
        casos.append(matriculas(r.randint(1, 50), r.randint(1, 999), r.randint(0, 3)))
    for v in casos:
        copia = list(v)
        a = ing(v)[0]
        b = esp(v)[0]
        assert v == copia               # nao pode mudar a lista
        tem = len(set(v)) < len(v)
        assert (a is not None) == tem
        assert (b is not None) == tem
        if tem:
            assert v.count(a) >= 2
            assert v.count(b) >= 2
    print("testes ok:", len(casos), "casos")


# ------------------------------------------------------------
# confronto: medido x formula feita a mao
# ------------------------------------------------------------
def conf():
    print("\nconfronto medido x formula")
    print(f"{'n':>6} {'o que':<22} {'medido':>9} {'formula':>9}")
    for n in (100, 400, 1600):
        print(f"{n:>6} {'ing pior':<22} {ing(ing_pior(n))[1]:>9} {n * (n - 1) // 2:>9}")
    for n in (128, 256, 1024):
        lg = int(math.log2(n))
        o = esp_f(esp_pior(n))
        print(f"{n:>6} {'esp pior (ordenar)':<22} {o[1]:>9} {n * lg - n + 1:>9}")
        print(f"{n:>6} {'esp pior (varrer)':<22} {o[2]:>9} {n - 1:>9}")
        m = esp_f(esp_melhor(n))
        print(f"{n:>6} {'esp melhor (ordenar)':<22} {m[1]:>9} {n // 2 * lg:>9}")
    for n in (100, 1600):               # n que nao e potencia de 2
        t = math.ceil(math.log2(n))
        print(f"{n:>6} {'esp pior (ordenar)':<22} {esp_f(esp_pior(n))[1]:>9} "
              f"{n * t - 2 ** t + 1:>9}")


if __name__ == "__main__":
    testa()
    dados = []
    pq = (100, 200, 400, 800, 1600)
    gr = (12500, 25000, 50000, 100000)

    print("\n===== INGENUA =====")
    teste_do_dobro("ing - pior caso (sem repetidas), comparacoes",
                   lambda n: ing(ing_pior(n))[1], pq, "ing_pior", dados)
    teste_do_dobro("ing - melhor caso (1as iguais), comparacoes",
                   lambda n: ing(ing_melhor(n))[1], pq, "ing_melhor", dados)
    teste_do_dobro("ing - caso medio (media de 30), comparacoes",
                   lambda n: medio(ing, n), pq, "ing_medio", dados)

    print("\n===== ESPERTA =====")
    teste_do_dobro("esp - pior caso, fase ordenacao",
                   lambda n: esp_f(esp_pior(n))[1], pq, "esp_pior_ord", dados)
    teste_do_dobro("esp - pior caso, fase varredura",
                   lambda n: esp_f(esp_pior(n))[2], pq, "esp_pior_var", dados)
    teste_do_dobro("esp - pior caso, total",
                   lambda n: esp(esp_pior(n))[1], pq, "esp_pior_total", dados)
    teste_do_dobro("esp - melhor caso, total",
                   lambda n: esp(esp_melhor(n))[1], pq, "esp_melhor_total", dados)
    teste_do_dobro("esp - caso medio (media de 30), total",
                   lambda n: medio(esp, n), pq, "esp_medio", dados)

    print("\n===== ESPERTA, SERIE MAIOR =====")
    teste_do_dobro("esp - pior caso, fase ordenacao (maior)",
                   lambda n: esp_f(esp_pior(n))[1], gr, "esp_pior_ord_gr", dados)
    teste_do_dobro("esp - pior caso, fase varredura (maior)",
                   lambda n: esp_f(esp_pior(n))[2], gr, "esp_pior_var_gr", dados)
    teste_do_dobro("esp - pior caso, total (maior)",
                   lambda n: esp(esp_pior(n))[1], gr, "esp_pior_total_gr", dados)

    conf()
    salvar_csv(dados, "medicoes.csv")
