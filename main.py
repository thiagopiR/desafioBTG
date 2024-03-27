import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from functools import wraps


def read_data_file(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as f:
        raw_file = f.readlines()

    list_dados = [line.split() for line in raw_file]
    float_raw_lines = [list(map(float, raw_line)) for raw_line in list_dados]
    return pd.DataFrame(float_raw_lines, columns=['lat', 'long', 'data_value'])


def read_contour_file(file_path: str) -> pd.DataFrame:
    line_split_comp = re.compile(r'\s*,')

    with open(file_path, 'r') as f:
        raw_file = f.readlines()

    l_raw_lines = [line_split_comp.split(raw_file_line.strip()) for raw_file_line in raw_file]
    l_raw_lines = list(filter(lambda item: bool(item[0]), l_raw_lines))
    float_raw_lines = [list(map(float, raw_line))[:2] for raw_line in l_raw_lines]
    header_line = float_raw_lines.pop(0)
    assert len(float_raw_lines) == int(header_line[0])
    return pd.DataFrame(float_raw_lines, columns=['lat', 'long'])


def apply_contour(contour_df: pd.DataFrame, data_df: pd.DataFrame) -> pd.DataFrame:
    # Criar um polígono utilizando o countour_df como base
    contour_polygon = Polygon(contour_df[['lat', 'long']].values)

    """ Para cada linha do Data Frame, aplica uma função lambda que recebe a linha do Data Frame como entrada.
    Na linha do DF, um objeto Point é criado, utilizando latitude e longitude como parâmetro.
    A função within verifica se esse ponto existe dentro do polígono definido anteriormente, e retorna True ou False """
    inside_contour_mask = data_df.apply(lambda row: Point(row['lat'], row['long']).within(contour_polygon), axis=1)

    # Filtra os dados de data_df para obter apenas os que estão dentro do polígono e os retorna
    data_inside_contour = data_df[inside_contour_mask]
    return data_inside_contour


def calc_precipitacao_acumulada(contour_df: pd.DataFrame, forecast_dir: str) -> list:
    # Lista todos os arquivos na pasta de previsões que terminam com .dat
    arquivos_forecast = [arquivo for arquivo in os.listdir(forecast_dir) if arquivo.endswith('.dat')]
    
    # Lista para armazenar a precipitação acumulada para cada arquivo
    precipitacao_acumulada_por_arquivo = []
    
    for arquivo in arquivos_forecast:
        # Constrói o caminho completo do arquivo e realiza a leitura do mesmo
        caminho_arquivo = os.path.join(forecast_dir, arquivo)
        data_df = read_data_file(caminho_arquivo)

        # Aplica o contorno aos dados para obter apenas os pontos dentro da região de interesse
        data_inside_contour = apply_contour(contour_df=contour_df, data_df=data_df)

        # Calcula a precipitação acumulada para a região e a adiciona à lista
        precipitacao_acumulada_por_arquivo.append(data_inside_contour['data_value'].sum())
    return precipitacao_acumulada_por_arquivo


def make_graph(arquivos_forecast: list, precipitacao_acumulada_por_arquivo: list) -> None:
    # Cria um novo gráfico de barras
    plt.figure(figsize=(10, 6))
    
    # Plota as barras no gráfico
    plt.bar(arquivos_forecast, precipitacao_acumulada_por_arquivo)

    # Modificação visual no gráfico, para mostrar apenas a data da previsão no eixo X, e não o nome do arquivo todo
    datas_previsao = [f"{arquivo[-10:-8]}/{arquivo[-8:-6]}" for arquivo in arquivos_forecast]
    plt.xticks(range(len(arquivos_forecast)), datas_previsao) 

    # Adiciona rótulos aos eixos e título ao gráfico
    plt.xlabel('2021')
    plt.ylabel('Precipitação acumulada (em mm)')
    plt.title('Previsão de precipitação acumulada (modelo ETA 01/12/21) para a região da usina Hidrelétrica Camargos')
    plt.show()


def main() -> None:
    contour_df: pd.DataFrame = read_contour_file('PSATCMG_CAMARGOS.bln')
    forecast_dir = 'forecast_files'
    precipitacao_acumulada_por_arquivo = calc_precipitacao_acumulada(contour_df, forecast_dir)
    arquivos_forecast = [arquivo for arquivo in os.listdir(forecast_dir) if arquivo.endswith('.dat')]
    make_graph(arquivos_forecast, precipitacao_acumulada_por_arquivo)


if __name__ == '__main__':
    main()
