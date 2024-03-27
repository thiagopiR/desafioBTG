import pandas as pd
import tempfile
import unittest
import os
from shapely.geometry import Polygon, Point
from unittest.mock import patch, mock_open
from main import (
    read_data_file,
    read_contour_file,
    apply_contour,
    calc_precipitacao_acumulada,
)

class TestMain(unittest.TestCase):
  @patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="-75.00 -35.00   0.0\n-75.00 -34.60   0.1\n",
  )
  def test_read_data_file(self, mock_open):
    # DataFrame esperado ao ler o arquivo mock
    expected_df = pd.DataFrame(
        {
            "lat": [-75.00, -75.00],
            "long": [-35.00, -34.60],
            "data_value": [0.0, 0.1],
        }
    )
    df = read_data_file("mock")

    # Verifica se a função retorna um DataFrame
    self.assertIsInstance(df, pd.DataFrame)

    # Verifica se os DataFrames são iguais
    self.assertEqual(df.values.tolist(), expected_df.values.tolist())


  @patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="3,0\n-44.60181259796872,-22.27254676426213\n-44.59956701592149,-22.27108034847117\n-44.59233941813173,-22.27056786161309\n",
  )
  def test_read_contour_file(self, mock_open):
    # Data Frame esperado ao ler o arquivo mock
    expected_df = pd.DataFrame(
        {
            "lat": [-44.60181259796872, -44.59956701592149, -44.59233941813173],
            "long": [-22.27254676426213, -22.27108034847117, -22.27056786161309],
        }
    )
    df = read_contour_file("mock")

    # Verifica se a função retorna um DataFrame
    self.assertIsInstance(df, pd.DataFrame)

    # Verifica se os DataFrames são iguais
    self.assertEqual(df.values.tolist(), expected_df.values.tolist())


  def test_apply_contour(self):
    # Define o contorno do polígono
    contour_df = pd.DataFrame({'lat': [0, 0, 1, 1], 'long': [0, 1, 1, 0]})
    
    # Criar pontos de teste (alguns dentro do polígono e outros fora)
    data_df = pd.DataFrame({'lat': [0.5, 0.5, 0.2, 1.5],
                            'long': [0.5, 1.5, 0.2, 1.5]})

    # Chamar a função apply_contour, que define os pontos que estão dentro do contorno
    data_inside_contour = apply_contour(contour_df, data_df)

    # Verificar se os pontos retornados estão dentro do polígono
    for index, row in data_inside_contour.iterrows():
      point = Point(row['lat'], row['long'])
      self.assertTrue(point.within(Polygon(contour_df[["lat", "long"]].values)))


  def test_apply_contour_outside_points(self):
    # Define o contorno do polígono
    contour_df = pd.DataFrame({"lat": [0, 0, 10, 10], "long": [0, 10, 10, 0]})

    # Criar pontos de teste, todos fora do polígono
    data_df = pd.DataFrame({"lat": [15, 20, 25], "long": [15, 20, 25]})

    # Chama a função apply_contour, que define os pontos que estão dentro do contorno
    result_df = apply_contour(contour_df, data_df)

    # Verifica se os pontos fora do contorno estão fora do polígono definido
    for index, row in result_df.iterrows():
      point = Point(row["lat"], row["long"])
      self.assertFalse(point.within(Polygon(contour_df[["lat", "long"]].values)))


  def test_calc_precipitacao_acumulada(self):
    # Criar um mock para o DataFrame de contorno
    contour_df_mock = pd.DataFrame(
        {"lat": [-45, -45, -35, -35, -45], "long": [-75, -70, -70, -75, -75]}
    )

    # Criar uma estrutura temporária de diretórios e arquivos
    with tempfile.TemporaryDirectory() as temp_dir:
      # Criar arquivos .dat na pasta temporária
      file_paths = []
      for i, content in enumerate(
          [
              "-44.00 -74.50   0.3\n-43.80 -74.80   0.1\n-43.60 -74.90   0.1\n",
              "-44.00 -72.50   0.3\n-41.80 -76.80   1.0\n-39.60 -71.90   0.1\n",
              "-44.10 -70.50   0.3\n-43.80 -72.80   0.0\n-43.60 -73.90   0.1\n",
          ]
      ):
          file_path = os.path.join(temp_dir, f"arquivo{i + 1}.dat")
          with open(file_path, "w") as f:
              f.write(content)
          file_paths.append(file_path)

      # Chamar a função calc_precipitacao_acumulada com os arquivos mocks
      precipitacao_acumulada_por_arquivo = calc_precipitacao_acumulada(contour_df_mock, temp_dir)

      # Verificar os resultados da precipitação acumulada para cada arquivo
      self.assertEqual(precipitacao_acumulada_por_arquivo[0], 0.5) 
      self.assertEqual(precipitacao_acumulada_por_arquivo[1], 0.4)
      self.assertEqual(precipitacao_acumulada_por_arquivo[2], 0.4)


if __name__ == "__main__":
    unittest.main()
