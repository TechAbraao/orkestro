from source.app.utils.decorators.database import database_connection
import requests

### EvolutionAPI - Suspeita dá pra gente analisar isso no futuro pr oque substituir
class WhatsAppService:
    def __init__(self):
        ## a instância é o nome dessa porra
        self.evolution_api_instance = 'teste' # aqui rs


    @database_connection
    def get_instance_connect(self):
        instance = self.evolution_api_instance
        url = f'http://evolution_api:8080/instance/connect/{instance}'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            res = response.json()
            return res.get("base64")
        except Exception as e:
            return e


    @database_connection
    def get_verify_status(self):
        instance = self.evolution_api_instance
        url = f'http://evolution_api:8080/instance/connectionState/{instance}'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            res = response.json()
            return res
        except Exception as e:
            return e

    @database_connection
    def logout_instance(self):
        instance = self.evolution_api_instance
        url = f'http://evolution_api:8080/instance/logout/{instance}'

        try:
            response = requests.delete(url, timeout=10)
            response.raise_for_status()
            res = response.json()
            return res
        except Exception as e:
            return e
