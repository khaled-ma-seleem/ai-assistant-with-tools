.PHONY: all install_deps install_ollama start_ollama pull_llama run_llama pull_qwen run_qwen run_app setup

all: setup

install_deps:
	pip install -r requirements.txt

install_ollama:
	curl -fsSL https://ollama.com/install.sh | sh

start_ollama:
	mkdir -p logs
	nohup ollama serve > logs/ollama_serve.log 2>&1 & 
	sleep 5

pull_llama:
	ollama pull llama3.2:3b

run_llama:
	mkdir -p logs
	nohup ollama run llama3.2:3b > logs/llama_model.log 2>&1 &
	sleep 30

pull_qwen:
	ollama pull qwen2.5vl:7b

run_qwen:
	mkdir -p logs
	nohup ollama run qwen2.5vl:7b > logs/qwen_model.log 2>&1 &
	sleep 30
	
run_app:
	mkdir -p logs
	nohup python -m streamlit run ui/app.py > logs/web_app.log 2>&1 &

setup: install_deps install_ollama start_ollama pull_llama run_app
