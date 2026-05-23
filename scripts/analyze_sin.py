import sys
import subprocess
import os
from datetime import datetime

def analyze_sin(context_log):
    prompt = f"""
    Eres un monje anciano y sabio de la Abadía. Analiza el siguiente 'pecado' (pérdida de Obsequium) cometido por Guillermo.
    
    Contexto del Log:
    {context_log}
    
    Tarea:
    1. Identifica la regla monástica violada.
    2. Explica por qué es un pecado en el contexto del Horarium y la ubicación.
    3. Da un consejo para evitarlo en el futuro.
    
    Responde en español, de forma breve y con autoridad monástica.
    """
    
    try:
        result = subprocess.run(
            ['ollama', 'run', 'deepseek-r1:1.5b', prompt],
            capture_output=True, text=True, timeout=120
        )
        analysis = result.stdout.strip()
        
        # Save to Wiki
        wiki_path = os.path.expanduser("~/wiki/concepts/lecciones-aprendidas.md")
        os.makedirs(os.path.dirname(wiki_path), exist_ok=True)
        
        with open(wiki_path, "a", encoding="utf-8") as f:
            f.write(f"\n### Lección del {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Suceso:** {context_log}\n")
            f.write(f"**Análisis:**\n{analysis}\n")
            f.write("\n---\n")
            
        return analysis
    except Exception as e:
        return f"Error en la reflexión: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(analyze_sin(sys.argv[1]))
    else:
        print("Uso: python analyze_sin.py 'descripción del suceso'")
