import re
aaaaaa
bbbbbb
class Analise:
    def le_assinatura(self):
        print("\nInforme os traços linguísticos que deseja fazer a comparação:\n")

        t_mediopalavra = float(input("Digite o tamanho médio de palavra:"))
        rel_typetoken = float(input("Digite a relação Type-Token:"))
        raz_hapaxlegomana = float(input("Digite a razão Hapax Legomana:"))
        t_mediosentenca = float(input("Digite o tamanho médio de sentença:"))
        complex_sentenca = float(input("Digite a complexidade média da sentença:"))
        t_mediofrase = float(input("Digite o tamanho medio de frase:"))

        return [t_mediopalavra, rel_typetoken, raz_hapaxlegomana, t_mediosentenca, complex_sentenca, t_mediofrase]

    def le_textos(self):
        i = 1
        textos = []
        texto = input("\nDigite o texto " + str(i) +" (aperte enter para sair):")
        while texto:
            textos.append(texto)
            i = i + 1
            texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")

        return textos

    def separa_sentencas(self, texto):
        sentencas = re.split(r'[.!?]+', texto)
        if sentencas[-1] == '':
            del sentencas[-1]
        return sentencas

    def separa_frases(self, sentenca):
        return re.split(r'[,:;]+', sentenca)

    def separa_palavras(self, frase):
        return frase.split()

    def n_palavras_unicas(self, lista_palavras):
        freq = dict()
        unicas = 0
        for palavra in lista_palavras:
            p = palavra.lower()
            if p in freq:
                if freq[p] == 1:
                    unicas -= 1
                freq[p] += 1
            else:
                freq[p] = 1
                unicas += 1

        return unicas

    def n_palavras_diferentes(self, lista_palavras):
        freq = dict()
        for palavra in lista_palavras:
            p = palavra.lower()
            if p in freq:
                freq[p] += 1
            else:
                freq[p] = 1

        return len(freq)

    def tamanho_medio_de_sentenca(self, sentencas):
        caracteres_sentenca = 0
        for sentenca in sentencas:
            caracteres_sentenca = caracteres_sentenca + len(sentenca)
        return caracteres_sentenca / len(sentencas)

    def tamanho_medio_de_frase(self, frases):
        caracteres_frase = 0
        for frase in frases:
            caracteres_frase = caracteres_frase + len(frase)
        return caracteres_frase / len(frases)

    def lista_frases(self, texto):
        lista = []
        for i in self.separa_sentencas(texto):
            lista.extend(self.separa_frases(i))
        return lista

    def lista_palavras(self, texto):
        lista = []
        for i in self.lista_frases(texto):
            lista.extend(self.separa_palavras(i))
        return lista

    def total_caracteres(self, texto):
        soma = 0
        for i in self.lista_palavras(texto):
            soma = soma + len(i)
        return soma

    def calcula_assinatura(self, texto, devolver_formatada):
        t_mediopalavra =  self.total_caracteres(texto) / len(self.lista_palavras(texto))
        rel_typetoken = self.n_palavras_diferentes(self.lista_palavras(texto)) / len(self.lista_palavras(texto))
        raz_hapaxlegomana = self.n_palavras_unicas(self.lista_palavras(texto)) / len(self.lista_palavras(texto))

        sentencas = self.separa_sentencas(texto)
        t_mediosentenca = self.tamanho_medio_de_sentenca(sentencas)

        complex_sentenca = len(self.lista_frases(texto)) / len(self.separa_sentencas(texto))

        frase = self.lista_frases(texto)
        t_mediofrase = self.tamanho_medio_de_frase(frase)

        assinatura = [t_mediopalavra, rel_typetoken, raz_hapaxlegomana, t_mediosentenca, complex_sentenca, t_mediofrase] 

        if devolver_formatada:
            assinatura_formatada = (
                f"Tamanho médio de palavra: {assinatura[0]}\n"
                f"Relação Type-Token: {assinatura[1]}\n"
                f"Razão Hapax Legomana: {assinatura[2]}\n"
                f"Tamanho médio de sentença: {assinatura[3]}\n"
                f"Complexidade média da sentença: {assinatura[4]}\n"
                f"Tamanho médio de frase: {assinatura[5]}"
            )
            return assinatura_formatada

        return assinatura 

    def compara_assinatura(self, as_a, as_b):
        soma_diferencas = 0.0
        for i in range(len(as_a)):
            diferenca_absoluta = abs(as_a[i] - as_b[i])
            soma_diferencas = soma_diferencas + diferenca_absoluta
        similaridade = soma_diferencas / len(as_a)
        return similaridade

    def avalia_textos(self, textos, ass_cp):
        lista_assinatura_textos = []
        for i in textos:
            lista_assinatura_textos.append(self.calcula_assinatura(i, False))

        lista_similaridades = []
        for i in lista_assinatura_textos:
            similaridade = self.compara_assinatura(ass_cp, i)
            lista_similaridades.append(similaridade)

        menor_similaridade = lista_similaridades[0]
        mais_suspeito = 1

        for i in lista_similaridades:
            if i < menor_similaridade:
                menor_similaridade = i
                mais_suspeito = lista_similaridades.index(i) + 1

        return mais_suspeito

def main():
    analise = Analise()
    print("Bem-vindo ao detector automático de Plágio Acadêmico!")

    while True:
        try:
            print("\nEscolha uma das opções:")
            print("---> Calcular a assinatura de determinado texto (Digite 1)")
            print("---> Verificar plágio com base na assinatura de um texto principal (Digite 2)")
            print("---> Sair do sistema (Digite 3)\n")
            escolha = int(input("Digite o número de sua escolha: "))

            if escolha == 1:
                print("\nVocê escolheu calcular a assinatura de determinado texto!\n")
                texto = input("Copie e cole o texto que você deseja saber a assinatura: ")
                print("\nO conjunto da assinatura deste texto é:")
                print("\n" + str(analise.calcula_assinatura(texto, True)) + "\n") 
            
            elif escolha == 2:
                assinatura_principal = analise.le_assinatura()
                textos = analise.le_textos()
                resposta_final = analise.avalia_textos(textos, assinatura_principal)
                
                print("\nBaseado em cálculos de similaridade entre os traços linguísticos fornecidos e os retirados dos textos:")
                print(f"O texto {resposta_final} é o mais suspeito de plágio acadêmico.\n")
            
            elif escolha == 3: 
                print("Você saiu do sistema!")
                break

            else:
                print("\nOoops! Parece que você digitou um valor inválido...\n")

        except ValueError: 
            print("\nOoops! Parece que você digitou um valor inválido...")

if __name__ == "__main__":
    main()
