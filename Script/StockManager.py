import pandas as pd
import logging
import os

class StockManager:
    def __init__(self):
        self.data = pd.DataFrame()
        logging.basicConfig(level=logging.INFO)  # Configuration de base du logger
        self.logger = logging.getLogger(__name__)  # Création d'un logger

    def load_files(self, folder_path):
        try:
            all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
            dataframes = [pd.read_csv(file) for file in all_files]
            self.data = pd.concat(dataframes, ignore_index=True)
            print("Tous les fichiers ont été consolidés avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement des fichiers : {e}")

    def search(self, column, value):
        try:
            results = self.data[self.data[column].astype(str).str.contains(value, case=False, na=False)]
            self.logger.info(f"Résultats trouvés : \n{results}")
            return results  # Retourne les résultats
        except KeyError:
            self.logger.error(f"La colonne '{column}' n'existe pas dans les données.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche : {e}")
        return None  # Retourne None en cas d'erreur

    def generate_report(self, output_path):
        try:
            summary = self.data.groupby('Catégorie').agg({
                'Quantité': 'sum',
                'Prix Unitaire': 'mean'
            }).reset_index()
            summary.to_csv(output_path, index=False)
            print(f"Rapport généré : {output_path}")
        except Exception as e:
            print(f"Erreur lors de la génération du rapport : {e}")
