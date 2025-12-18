"""Tests unitaires pour utils/data.py"""

import pytest
from unittest.mock import patch, Mock
from utils.data import OpenFoodFactsAPI


class TestOpenFoodFactsAPI:
    """Tests pour la classe OpenFoodFactsAPI"""

    @patch('utils.data.requests.get')
    def test_search_products_success(self, mock_get):
        """Test recherche de produits - succès"""
        # Mock de la réponse API
        mock_response = Mock()
        mock_response.json.return_value = {
            "products": [
                {
                    "product_name": "Nutella",
                    "brands": "Ferrero",
                    "nutriscore_grade": "e"
                },
                {
                    "product_name": "Nocciolata",
                    "brands": "Rigoni di Asiago",
                    "nutriscore_grade": "b"
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Test
        api = OpenFoodFactsAPI()
        results = api.search_products("nutella", page_size=2)

        # Assertions
        assert len(results) == 2
        assert results[0]["product_name"] == "Nutella"
        assert results[1]["brands"] == "Rigoni di Asiago"
        
        # Vérifier l'appel API
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "nutella" in str(call_args)

    @patch('utils.data.requests.get')
    def test_search_products_no_results(self, mock_get):
        """Test recherche sans résultats"""
        mock_response = Mock()
        mock_response.json.return_value = {"products": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenFoodFactsAPI()
        results = api.search_products("produitinexistant123456")

        assert results == []

    @patch('utils.data.requests.get')
    def test_search_products_api_error(self, mock_get):
        """Test gestion d'erreur API"""
        mock_get.side_effect = Exception("API Error")

        api = OpenFoodFactsAPI()
        results = api.search_products("nutella")

        assert results == []

    @patch('utils.data.requests.get')
    def test_get_product_success(self, mock_get):
        """Test récupération produit par code-barres - succès"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": 1,
            "product": {
                "code": "3017620422003",
                "product_name": "Nutella",
                "brands": "Ferrero",
                "nutriscore_grade": "e",
                "nova_group": 4
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenFoodFactsAPI()
        product = api.get_product("3017620422003")

        assert product is not None
        assert product["product_name"] == "Nutella"
        assert product["nova_group"] == 4

    @patch('utils.data.requests.get')
    def test_get_product_not_found(self, mock_get):
        """Test produit non trouvé"""
        mock_response = Mock()
        mock_response.json.return_value = {"status": 0}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenFoodFactsAPI()
        product = api.get_product("0000000000000")

        assert product is None

    @patch('utils.data.requests.get')
    def test_get_product_api_error(self, mock_get):
        """Test gestion erreur lors de la récupération"""
        mock_get.side_effect = Exception("Network Error")

        api = OpenFoodFactsAPI()
        product = api.get_product("3017620422003")

        assert product is None

    def test_extract_product_info_complete(self):
        """Test extraction d'infos avec toutes les données"""
        raw_product = {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "nutriscore_grade": "e",
            "nova_group": 4,
            "image_url": "https://example.com/image.jpg",
            "ingredients_text": "Sucre, huile de palme, noisettes...",
            "allergens": "fruits à coque",
            "nutriments": {
                "proteins_100g": 6.3,
                "carbohydrates_100g": 57.5,
                "fat_100g": 30.9
            },
            "categories": "Pâtes à tartiner",
            "code": "3017620422003"
        }

        api = OpenFoodFactsAPI()
        info = api.extract_product_info(raw_product)

        assert info["name"] == "Nutella"
        assert info["brands"] == "Ferrero"
        assert info["nutriscore"] == "E"
        assert info["nova_group"] == 4
        assert info["image_url"] == "https://example.com/image.jpg"
        assert "noisettes" in info["ingredients"]
        assert info["allergens"] == "fruits à coque"
        assert info["nutriments"]["proteins_100g"] == 6.3
        assert info["categories"] == "Pâtes à tartiner"
        assert info["code"] == "3017620422003"

    def test_extract_product_info_missing_fields(self):
        """Test extraction avec champs manquants"""
        raw_product = {
            # Produit avec données minimales
        }

        api = OpenFoodFactsAPI()
        info = api.extract_product_info(raw_product)

        # Vérifier valeurs par défaut
        assert info["name"] == "Produit sans nom"
        assert info["brands"] == "Marque inconnue"
        assert info["nutriscore"] == "N/A"
        assert info["nova_group"] == "N/A"
        assert info["image_url"] == ""
        assert info["ingredients"] == "Non disponible"
        assert info["allergens"] == "Non spécifié"
        assert info["nutriments"] == {}
        assert info["categories"] == ""
        assert info["code"] == ""

    def test_extract_product_info_nutriscore_uppercase(self):
        """Test conversion Nutri-Score en majuscule"""
        raw_product = {
            "nutriscore_grade": "a"  # minuscule
        }

        api = OpenFoodFactsAPI()
        info = api.extract_product_info(raw_product)

        assert info["nutriscore"] == "A"  # doit être majuscule

    @patch('utils.data.requests.get')
    def test_search_products_custom_page_size(self, mock_get):
        """Test avec page_size personnalisé"""
        mock_response = Mock()
        mock_response.json.return_value = {"products": [{"product_name": f"Produit {i}"} for i in range(50)]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenFoodFactsAPI()
        results = api.search_products("test", page_size=50)

        # Vérifier que page_size est passé dans les params
        call_args = mock_get.call_args
        assert call_args[1]["params"]["page_size"] == 50
        assert len(results) == 50

    @patch('utils.data.requests.get')
    def test_base_url_correct(self, mock_get):
        """Test que l'URL de base est correcte"""
        mock_response = Mock()
        mock_response.json.return_value = {"products": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenFoodFactsAPI()
        api.search_products("test")

        # Vérifier que l'URL contient le bon domaine
        call_args = mock_get.call_args
        assert "world.openfoodfacts.org" in call_args[0][0]


# Tests d'intégration (optionnels, décommenter pour tester avec la vraie API)
"""
class TestOpenFoodFactsAPIIntegration:
    '''Tests d'intégration avec la vraie API (nécessite connexion internet)'''

    @pytest.mark.integration
    def test_real_api_search(self):
        '''Test recherche réelle'''
        api = OpenFoodFactsAPI()
        results = api.search_products("nutella", page_size=5)
        
        assert len(results) > 0
        assert any("nutella" in p.get("product_name", "").lower() for p in results)

    @pytest.mark.integration
    def test_real_api_get_product(self):
        '''Test récupération produit réel'''
        api = OpenFoodFactsAPI()
        product = api.get_product("3017620422003")  # Nutella
        
        assert product is not None
        assert "nutella" in product.get("product_name", "").lower()
"""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])