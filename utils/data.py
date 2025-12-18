import requests
from typing import Optional, Dict, List
import pandas as pd

class OpenFoodFactsAPI:
    """Classe pour interagir avec l'API OpenFoodFacts"""
    
    BASE_URL = "https://world.openfoodfacts.org"
    
    @staticmethod
    def search_products(query: str, page_size: int = 20) -> List[Dict]:
        """Recherche des produits par nom"""
        url = f"{OpenFoodFactsAPI.BASE_URL}/cgi/search.pl"
        params = {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": page_size,
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("products", [])
        except Exception as e:
            print(f"Erreur recherche: {e}")
            return []
    
    @staticmethod
    def get_product(barcode: str) -> Optional[Dict]:
        """Récupère un produit par son code-barres"""
        url = f"{OpenFoodFactsAPI.BASE_URL}/api/v0/product/{barcode}.json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 1:
                return data.get("product")
            return None
        except Exception as e:
            print(f"Erreur produit: {e}")
            return None
    
    @staticmethod
    def extract_product_info(product: Dict) -> Dict:
        """Extrait les infos clés d'un produit"""
        return {
            "name": product.get("product_name", "Produit sans nom"),
            "brands": product.get("brands", "Marque inconnue"),
            "nutriscore": product.get("nutriscore_grade", "N/A").upper(),
            "nova_group": product.get("nova_group", "N/A"),
            "image_url": product.get("image_url", ""),
            "ingredients": product.get("ingredients_text", "Non disponible"),
            "allergens": product.get("allergens", "Non spécifié"),
            "nutriments": product.get("nutriments", {}),
            "categories": product.get("categories", ""),
            "code": product.get("code", ""),
        }