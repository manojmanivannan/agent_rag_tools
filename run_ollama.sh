#!/bin/bash

MODEL_NAME=$1

echo "Starting Ollama server"
ollama serve &

sleep 5

echo "Pulling $MODEL_NAME"
ollama pull $MODEL_NAME &

echo "Pulling $MODEL_NAME"
while [ "$(ollama list | grep $MODEL_NAME)" == "" ]; do
	echo "Waiting to pull $MODEL_NAME"
	sleep 10
done

echo "Starting litellm"
litellm --model ollama_chat/$MODEL_NAME --drop_params
