
import requests
from deepeval import evaluate
from deepeval.test_case import LLMTestCase

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt):
    """Función para consultar el modelo Mistral en Ollama"""
    response = requests.post(OLLAMA_URL, json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    try:
        data = response.json()
        output = data["response"].strip()
        print(f"Prompt: {prompt}\nRespuesta del modelo: {output}")
        return output
    except KeyError:
        print("Respuesta inesperada de Ollama:", response.text)
        raise SystemExit("No se encontró la clave 'response' en la respuesta. Verifica que el modelo esté descargado y el contenedor esté listo.")

# Métrica personalizada simple
class SimpleContainsMetric:
    def __init__(self, name="SimpleContains"):
        self.name = name
        
    def measure(self, test_case):
        expected = test_case.expected_output.lower()
        actual = test_case.actual_output.lower()
        
        # Verificar si la respuesta contiene la palabra clave esperada
        score = 1.0 if expected in actual else 0.0
        
        return {
            "score": score,
            "reason": f"Expected '{expected}' {'found' if score == 1.0 else 'not found'} in actual output"
        }

def test_model_simple(prompt, expected_keyword):
    """Función simple para probar el modelo"""
    actual_output = query_ollama(prompt)
    
    # Verificación manual simple
    if expected_keyword.lower() in actual_output.lower():
        print(f"✅ PASÓ: Encontró '{expected_keyword}' en la respuesta")
        return True
    else:
        print(f"❌ FALLÓ: No encontró '{expected_keyword}' en la respuesta")
        return False

def test_model_deepeval(prompt, expected_output):
    """Función para probar el modelo usando DeepEval sin APIs externas"""
    # Obtener la respuesta del modelo
    actual_output = query_ollama(prompt)
    
    # Crear el test case
    test_case = LLMTestCase(
        input=prompt,
        actual_output=actual_output,
        expected_output=expected_output
    )
    
    # Usar métrica personalizada
    metric = SimpleContainsMetric()
    result = metric.measure(test_case)
    
    print(f"Resultado: {result['reason']} (Score: {result['score']})")
    print(f"Test completado: '{prompt}' -> Esperado: '{expected_output}', Obtenido: '{actual_output}'")
    
    return result['score'] == 1.0

if __name__ == "__main__":
    print("=== TESTS SIMPLES ===")
    # Test 1 - Simple
    test_model_simple("¿Cuál es la capital de Francia?", "París")
    print()
    
    # Test 2 - Simple
    test_model_simple("¿Cuánto es 2 + 2?", "4")
    print()
    
    # Test 3 - Simple
    test_model_simple("¿Quién escribió Cien años de soledad?", "García Márquez")
    print()
    
    print("=== TESTS CON DEEPEVAL (MÉTRICA PERSONALIZADA) ===")
    # Test con DeepEval usando métrica personalizada
    test_model_deepeval("¿Cuál es la capital de Francia?", "París")
    print()
    
    print("Evaluaciones completadas.")
