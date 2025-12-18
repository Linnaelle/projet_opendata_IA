import os
from litellm import completion
from typing import List, Dict

class NutriChatbot:
    """Chatbot nutrition avec LiteLLM"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.conversation_history: List[Dict] = []
    
    def analyze_product(self, product_info: Dict) -> str:
        """Génère une analyse IA d'un produit"""
        prompt = f"""
Tu es un nutritionniste expert. Analyse ce produit alimentaire et donne des conseils clairs.

Produit: {product_info['name']} ({product_info['brands']})
Nutri-Score: {product_info['nutriscore']}
NOVA: {product_info['nova_group']}
Ingrédients: {product_info['ingredients'][:500]}

Fournis une analyse en 3 parties:
1. 📊 Qualité nutritionnelle (2-3 phrases)
2. ⚠️ Points d'attention (additifs, allergènes, ultra-transformation)
3. 💡 Recommandation (consommer occasionnellement/régulièrement/à éviter)

Reste concis et pédagogue.
"""
        
        try:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur d'analyse: {str(e)}"
    
    def suggest_alternatives(self, product_info: Dict, alternatives: List[Dict]) -> str:
        """Suggère des alternatives plus saines"""
        alt_text = "\n".join([
            f"- {alt['name']} (Nutri-Score: {alt['nutriscore']})"
            for alt in alternatives[:3]
        ])
        
        prompt = f"""
Produit actuel: {product_info['name']} (Nutri-Score {product_info['nutriscore']})

Alternatives trouvées:
{alt_text}

Explique en 2-3 phrases pourquoi ces alternatives sont meilleures et ce qui les différencie.
"""
        
        try:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur: {str(e)}"
    
    def chat(self, user_message: str, context: str = "") -> str:
        """Chat interactif sur la nutrition"""
        self.conversation_history.append({
            "role": "user",
            "content": f"{context}\n\nQuestion: {user_message}" if context else user_message
        })
        
        try:
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un assistant nutrition bienveillant et pédagogue."},
                    *self.conversation_history
                ],
                temperature=0.8
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        except Exception as e:
            return f"❌ Erreur: {str(e)}"