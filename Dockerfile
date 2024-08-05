FROM ollama/ollama
RUN apt update && apt install -y python3 python3-pip
RUN pip install litellm[proxy]
COPY ./run_ollama.sh /tmp/run_ollama.sh
RUN chmod +x /tmp/run_ollama.sh
EXPOSE 11434
# litellm", "--model" ,"ollama_chat/mistral"]
