# BTG Energy Challenge

### Comentários

Utilizei das bibliotecas Shapely e Matplotlib, para a criação do polígono e para a criação do gráfico das precipitações acumuladas.
No início, enfrentei alguma dificuldade em confirmar se minha abordagem estava correta. Para deixar um pouco mais fácil a visualização, utilizei da biblioteca Matplotlib para conseguir observar tanto o contorno quanto os pontos dentro dele. Essa visualização, embora não integrada ao projeto final, trouxe confiança adicional à minha solução, que até então existia apenas no código.
Ainda nesse aspecto, resolvi me aventurar um pouco nos testes unitários, algo que eu nunca tinha feito em Python. Acredito que consegui abranger uma gama interessante de testes para as funções utilizadas, dando-me ainda mais confiança na finalização do projeto.

### Decisão das bibliotecas

Decidi utilizar o Shapely por conta de sua simplicidade e utilidade. Apenas com o DataFrame, que possuíamos através da função `read_contour_file`, foi possível criar o polígono. Além disso, a biblioteca oferece métodos que simplificaram um pouco a resolução do desafio. Utilizei o `Point`, que cria uma coordenada baseando-se em 2 ou 3 argumentos (x,y e as vezes z), e também o método `within`, que retorna True ou False, dependendo se o ponto está dentro do polígono ou não.
Além disso, o Shapely é extremamente eficiente, pois foi construida com base na GEOS(Geometry Engine - Open Source), uma biblioteca feita em C/C++ altamente performática para lidar com um número grande de dados.
Quanto ao Matplotlib, escolhi utilizá-lo por ser a biblioteca mais popular em Python para a criação de gráficos.

### Como rodar o código

#### Pré-requisitos

- Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo [aqui](https://www.python.org/).

#### Passos

1. Baixe o código para o seu computador. Você pode clonar este repositório usando o Git:

   ```
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```

   Ou baixe o código como um arquivo ZIP e extraia-o onde preferir.

2. Abra o terminal e navegue até o diretório onde você baixou/clonou o código.

3. Instale as dependências necessárias executando o seguinte comando:

   ```
   pip install shapely matplotlib pandas
   ```

4. Para executar o código principal, utilize o seguinte comando:

   ```
   python main.py
   ```

5. Para executar os testes unitários, utilize o seguinte comando:
   ```
   python test_main.py
   ```

## O desafio

### Introdução

Trabalhando nos sistema da mesa de Energia do banco BTG Pactual, constantemente lidamos com dados de precipitação, tanto previsto como observado.
A informação de quanto choveu ou quanto choverá em determinado lugar é dada por uma malha de coordenadas
(latitude [lat] e longitude [long]) e uma terceira variável que é a precipitação diária acumulada naquele ponto.

Na pasta `forecast_files` é possivel encontrar a previsão de precipitação do modelo meteorológico ETA, desenvolvido pelo INPE.
O nome dos arquivos seguem o seguinte padrão: ETA40_p011221a021221.dat -> ETA40_p**ddmmyy**a**ddmmyy**.dat.
Em que a primeira data é referente a quando foi feita a previsão e a segunda data diz respeito qual data está sendo prevista.

Dentro do arquivo, os dados seguem o descrito acima:

```
lat     long    data_value
-75.00  -35.00  0.0
-75.00  -34.60  0.1
-75.00  -34.20  0.0
```

Porém, estes dados não são utilizados desta forma, eles passam por um processamento. Pois, uma das perguntas que queremos
responder no nosso dia a dia é: **Quanto choveu ou choverá em determinada região do Brasil?**.

Para isso, utilizamos um **contorno**, que é um polígono consistido das coordenadas que delimitam uma região.
Assim, conseguimos "recortar" os dados que caem dentro desta região e calcular, por exemplo, a precipitação média da região.

Por exemplo (valores inventados):

```
forecast_date   forecasted_date     data_value
01/12/2021      02/12/2021          1.4
01/12/2021      03/12/2021          2.1
...             ...                 ...
01/12/2021      07/12/2021          3.2
```

### O desafio

O desafio consiste em responder a seguinte pergunta: **Qual é a previsão de precipitação ACUMULADA dada pelo modelo ETA no dia 01/12/2021 para a região de escoamento da usina Hidrelétrica Camargos (bacia do rio Grande)?**

![Contorno de Camargos [Grande]](Contour_Camargos_Grande.png "Contorno de Carmargos")

Modifique o arquivo `main.py` para fazer o "recorte" dos dados de precipitação (para **todos** os dias previstos pelo modelo) e
apresente graficamente a resposta para a pergunta.

### Resalvas

- É permitido a utilização de bibliotecas extras
- A entrega do desafio deve ser feita por GIT. Responda o email com o link do seu repositório.
