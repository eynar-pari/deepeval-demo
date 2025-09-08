# Eynar Pari
Este proyecto es una muestra simple de como usar deepeval para testear modelos de IA, como ejemplo usaremos Mistral

## Requisitos previos
- Docker / Docker-Compose instalado
- Python ultima version

## Pasos Para correr ele ejemplo

1. **Clona o descarga este repositorio y abre una terminal en la carpeta `deepeval-demo`.**

2. **Inicia el modelo con Docker Compose:**

```powershell
docker-compose up -d
```

Esto descargará y levantará Ollama con el modelo Mistral.

3. **Descarga el modelo Mistral dentro del contenedor:**

```powershell
docker exec -it deepeval-ollama-1 ollama run mistral
```

4. **Instala las dependencias de Python:**

```powershell
pip install -r requirements.txt
```
5. **Ejecuta el script de ejemplo:**

```powershell
python deepeval_test.py
```
