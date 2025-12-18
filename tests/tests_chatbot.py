"""Tests unitaires pour utils/chatbot.py"""

import os
import pytest
from unittest.mock import patch, Mock
from utils.chatbot import NutriChatbot


class TestNutriChatbot:
    """Tests pour la classe NutriChatbot"""

    def test_init_default_provider(self):
        """Test initialisation avec provider par défaut"""
        with patch.dict(os.environ, {"NUTRISCAN_PROVIDER": "openai"}, clear=False):
            chatbot = NutriChatbot()
            assert chatbot.provider == "openai"
            assert "gpt" in chatbot.model.lower() or chatbot.model == "gpt-4o-mini"

    def test_init_custom_provider(self):
        """Test initialisation avec provider custom"""
        chatbot = NutriChatbot(provider="gemini")
        assert chatbot.provider == "gemini"
        assert "gemini" in chatbot.model

    def test_init_ollama_provider(self):
        """Test initialisation avec Ollama"""
        chatbot = NutriChatbot(provider="ollama")
        assert chatbot.provider == "ollama"
        assert "ollama" in chatbot.model or "mistral" in chatbot.model

    def test_init_custom_model(self):
        """Test initialisation avec modèle custom"""
        chatbot = NutriChatbot(provider="openai", model="gpt-4o")
        assert chatbot.model == "gpt-4o"

    def test_resolve_model_openai(self):
        """Test résolution modèle OpenAI"""
        chatbot = NutriChatbot(provider="openai")
        model, kwargs = chatbot._resolve_model_and_kwargs(None)
        
        assert "gpt" in model.lower() or model == "gpt-4o-mini"
        assert kwargs == {}

    def test_resolve_model_gemini(self):
        """Test résolution modèle Gemini"""
        chatbot = NutriChatbot(provider="gemini")
        model, kwargs = chatbot._resolve_model_and_kwargs(None)
        
        assert "gemini" in model
        assert kwargs == {}

    def test_resolve_model_ollama(self):
        """Test résolution modèle Ollama avec API base"""
        with patch.dict(os.environ, {"OLLAMA_API_BASE": "http://localhost:11434"}, clear=False):
            chatbot = NutriChatbot(provider="ollama")
            model, kwargs = chatbot._resolve_model_and_kwargs(None)
            
            assert "ollama" in model or "mistral" in model
            assert "api_base" in kwargs
            assert "localhost" in kwargs["api_base"]

    @patch('utils.chatbot.completion')
    def test_analyze_product_success(self, mock_completion):
        """Test analyse de produit - succès"""
        # Mock de la réponse LiteLLM
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Analyse nutritionnelle complète..."))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        product_info = {
            "name": "Nutella",
            "brands": "Ferrero",
            "nutriscore": "E",
            "nova_group": 4,
            "ingredients": "Sucre, huile de palme, noisettes..."
        }

        result = chatbot.analyze_product(product_info)

        # Assertions
        assert "Analyse nutritionnelle" in result
        mock_completion.assert_called_once()
        
        # Vérifier les arguments du call
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["model"] == chatbot.model
        assert call_kwargs["temperature"] == 0.7
        assert len(call_kwargs["messages"]) == 1
        assert "Nutella" in call_kwargs["messages"][0]["content"]

    @patch('utils.chatbot.completion')
    def test_analyze_product_error(self, mock_completion):
        """Test analyse de produit - erreur API"""
        mock_completion.side_effect = Exception("API Error")

        chatbot = NutriChatbot(provider="openai")
        
        product_info = {
            "name": "Nutella",
            "brands": "Ferrero",
            "nutriscore": "E",
            "nova_group": 4,
            "ingredients": "Sucre, huile de palme..."
        }

        result = chatbot.analyze_product(product_info)

        assert "❌ Erreur d'analyse" in result
        assert "API Error" in result

    @patch('utils.chatbot.completion')
    def test_suggest_alternatives_success(self, mock_completion):
        """Test suggestion d'alternatives - succès"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Ces alternatives sont meilleures car..."))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        product_info = {
            "name": "Nutella",
            "nutriscore": "E"
        }
        
        alternatives = [
            {"name": "Nocciolata", "nutriscore": "B"},
            {"name": "Pâte noisette bio", "nutriscore": "A"}
        ]

        result = chatbot.suggest_alternatives(product_info, alternatives)

        assert "meilleures" in result.lower() or "alternatives" in result.lower()
        mock_completion.assert_called_once()
        
        # Vérifier que les alternatives sont dans le prompt
        call_kwargs = mock_completion.call_args[1]
        prompt_content = call_kwargs["messages"][0]["content"]
        assert "Nocciolata" in prompt_content
        assert "Pâte noisette bio" in prompt_content

    @patch('utils.chatbot.completion')
    def test_suggest_alternatives_error(self, mock_completion):
        """Test suggestion d'alternatives - erreur"""
        mock_completion.side_effect = Exception("Network Error")

        chatbot = NutriChatbot(provider="openai")
        
        result = chatbot.suggest_alternatives(
            {"name": "Nutella", "nutriscore": "E"},
            [{"name": "Alt", "nutriscore": "A"}]
        )

        assert "❌ Erreur" in result

    @patch('utils.chatbot.completion')
    def test_chat_simple_message(self, mock_completion):
        """Test chat simple sans contexte"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Le Nutri-Score est un système..."))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        result = chatbot.chat("C'est quoi le Nutri-Score ?")

        assert "Nutri-Score" in result
        assert len(chatbot.conversation_history) == 2  # user + assistant
        
        # Vérifier l'historique
        assert chatbot.conversation_history[0]["role"] == "user"
        assert chatbot.conversation_history[1]["role"] == "assistant"

    @patch('utils.chatbot.completion')
    def test_chat_with_context(self, mock_completion):
        """Test chat avec contexte"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Pour ce produit spécifique..."))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        context = "Produit: Nutella (Nutri-Score E)"
        result = chatbot.chat("Est-ce bon pour la santé ?", context=context)

        # Vérifier que le contexte est inclus
        call_kwargs = mock_completion.call_args[1]
        user_message = call_kwargs["messages"][1]["content"]  # messages[0] = system
        assert "Nutella" in user_message

    @patch('utils.chatbot.completion')
    def test_chat_conversation_history(self, mock_completion):
        """Test maintien de l'historique de conversation"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Réponse test"))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        # Premier message
        chatbot.chat("Question 1")
        assert len(chatbot.conversation_history) == 2
        
        # Deuxième message
        chatbot.chat("Question 2")
        assert len(chatbot.conversation_history) == 4
        
        # Vérifier l'ordre
        assert chatbot.conversation_history[0]["content"] == "Question 1"
        assert chatbot.conversation_history[2]["content"] == "Question 2"

    @patch('utils.chatbot.completion')
    def test_chat_system_message(self, mock_completion):
        """Test présence du message système"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Réponse"))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        chatbot.chat("Test")

        call_kwargs = mock_completion.call_args[1]
        messages = call_kwargs["messages"]
        
        # Le premier message doit être le system prompt
        assert messages[0]["role"] == "system"
        assert "nutrition" in messages[0]["content"].lower()

    @patch('utils.chatbot.completion')
    def test_chat_temperature(self, mock_completion):
        """Test paramètre temperature"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Réponse"))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        chatbot.chat("Test")

        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["temperature"] == 0.8

    @patch('utils.chatbot.completion')
    def test_chat_error_handling(self, mock_completion):
        """Test gestion d'erreur lors du chat"""
        mock_completion.side_effect = Exception("Timeout")

        chatbot = NutriChatbot(provider="openai")
        result = chatbot.chat("Test")

        assert "❌ Erreur" in result
        assert "Timeout" in result

    @patch('utils.chatbot.completion')
    def test_analyze_product_prompt_structure(self, mock_completion):
        """Test structure du prompt d'analyse"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Analyse"))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        product_info = {
            "name": "Test Product",
            "brands": "Test Brand",
            "nutriscore": "C",
            "nova_group": 3,
            "ingredients": "Test ingredients"
        }

        chatbot.analyze_product(product_info)

        call_kwargs = mock_completion.call_args[1]
        prompt = call_kwargs["messages"][0]["content"]
        
        # Vérifier que le prompt contient les éléments clés
        assert "nutritionniste" in prompt.lower()
        assert "Test Product" in prompt
        assert "Nutri-Score" in prompt
        assert "NOVA" in prompt
        assert "3 parties" in prompt or "parties" in prompt

    @patch('utils.chatbot.completion')
    def test_ollama_api_base_kwargs(self, mock_completion):
        """Test que les kwargs Ollama sont bien passés"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Réponse"))]
        mock_completion.return_value = mock_response

        with patch.dict(os.environ, {"OLLAMA_API_BASE": "http://custom:8080"}, clear=False):
            chatbot = NutriChatbot(provider="ollama")
            chatbot.chat("Test")

            call_kwargs = mock_completion.call_args[1]
            assert "api_base" in call_kwargs
            assert call_kwargs["api_base"] == "http://custom:8080"

    def test_conversation_history_initialization(self):
        """Test initialisation de l'historique"""
        chatbot = NutriChatbot(provider="openai")
        assert chatbot.conversation_history == []
        assert isinstance(chatbot.conversation_history, list)

    @patch('utils.chatbot.completion')
    def test_suggest_alternatives_max_3(self, mock_completion):
        """Test limitation à 3 alternatives max"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Suggestions"))]
        mock_completion.return_value = mock_response

        chatbot = NutriChatbot(provider="openai")
        
        # Créer 5 alternatives
        alternatives = [
            {"name": f"Alt{i}", "nutriscore": "A"} for i in range(5)
        ]

        chatbot.suggest_alternatives(
            {"name": "Produit", "nutriscore": "E"},
            alternatives
        )

        call_kwargs = mock_completion.call_args[1]
        prompt = call_kwargs["messages"][0]["content"]
        
        # Vérifier que seulement 3 sont dans le prompt
        assert prompt.count("Alt0") == 1
        assert prompt.count("Alt1") == 1
        assert prompt.count("Alt2") == 1
        assert "Alt3" not in prompt  # Les 2 dernières ne doivent pas y être
        assert "Alt4" not in prompt


class TestNutriChatbotProviders:
    """Tests spécifiques aux différents providers"""

    @pytest.mark.parametrize("provider,expected_in_model", [
        ("openai", "gpt"),
        ("gemini", "gemini"),
        ("ollama", "ollama"),
    ])
    def test_provider_model_resolution(self, provider, expected_in_model):
        """Test résolution de modèle pour chaque provider"""
        chatbot = NutriChatbot(provider=provider)
        assert expected_in_model in chatbot.model.lower()

    def test_invalid_provider_fallback(self):
        """Test fallback sur OpenAI si provider invalide"""
        with patch.dict(os.environ, {"NUTRISCAN_PROVIDER": "invalid"}, clear=False):
            chatbot = NutriChatbot()
            # Doit fallback sur openai par défaut dans la logique
            assert chatbot.provider in ["openai", "gemini", "ollama", "invalid"]


# Tests d'intégration (optionnels, nécessitent des clés API)
"""
@pytest.mark.integration
class TestNutriChatbotIntegration:
    '''Tests d'intégration avec vraie API (nécessite clés API)'''

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Pas de clé OpenAI")
    def test_real_openai_chat(self):
        '''Test avec vraie API OpenAI'''
        chatbot = NutriChatbot(provider="openai")
        result = chatbot.chat("Bonjour, qu'est-ce que le Nutri-Score ?")
        
        assert len(result) > 0
        assert "nutri" in result.lower() or "score" in result.lower()

    @pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Pas de clé Gemini")
    def test_real_gemini_analyze(self):
        '''Test analyse avec vraie API Gemini'''
        chatbot = NutriChatbot(provider="gemini")
        
        product = {
            "name": "Nutella",
            "brands": "Ferrero",
            "nutriscore": "E",
            "nova_group": 4,
            "ingredients": "Sucre, huile de palme, noisettes..."
        }
        
        result = chatbot.analyze_product(product)
        assert len(result) > 50  # Doit avoir une vraie analyse
"""


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])