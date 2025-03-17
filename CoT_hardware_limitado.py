import datetime
import os
import gc
import time
import psutil
import signal
import sys
from llama_cpp import Llama

# Configuração para reduzir logs desnecessários
os.environ["LLAMA_CPP_LOG_LEVEL"] = "ERROR"

class DeepThoughtR1:
    def __init__(self, model_path: str, log_dir: str = "logs", output_dir: str = "output", n_ctx: int = 2048, **kwargs):
        self.log_dir = log_dir
        self.output_dir = output_dir
        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Define um arquivo de log padrão para uso inicial
        self.output_file = os.path.join(self.output_dir, f"default_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.kwargs = kwargs
        self.model = None
        self.initialized = False
        
        # Configurar monitoramento de memória
        self.memory_threshold = 6000  # 6GB em MB
        self.initial_memory = self._check_memory_usage()
        self._log_to_file(f"Memória inicial: {self.initial_memory:.2f} MB")
        
    def __del__(self):
        if self.model is not None:
            self.model = None
        gc.collect()
        
    def _initialize_model(self):
        if not self.initialized:
            try:
                gc.collect()
                self._log_to_file(f"Carregando modelo de {self.model_path}")
                
                # Mede a memória antes de carregar o modelo
                memory_before = self._check_memory_usage()
                
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=self.n_ctx,
                    n_threads=4,
                    n_batch=512,
                    use_mlock=False,
                    verbose=False,
                    **self.kwargs
                )
                
                # Mede a memória após carregar o modelo
                memory_after = self._check_memory_usage()
                memory_used = memory_after - memory_before
                
                self.initialized = True
                gc.collect()
                
                self._log_to_file(f"Memória usada para carregar o modelo: {memory_used:.2f} MB")
                return memory_used
                
            except Exception as e:
                error_msg = f"Erro ao inicializar modelo: {str(e)}"
                self._log_to_file(error_msg)
                self.model = None
                gc.collect()
                raise
                
    def _log_to_file(self, message):
        """Salva mensagem no arquivo de log de saída com buffer otimizado"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.output_file, 'a', encoding='utf-8', buffering=8192) as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"Erro ao salvar no arquivo de log: {str(e)}")

    def _check_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    def _is_memory_critical(self):
        return self._check_memory_usage() > self.memory_threshold

    def _sanitize_filename(self, s):
        """Remove caracteres inválidos e formata para uso em nome de arquivo"""
        return ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in s).replace(' ', '_').strip('_')[:50]  # Limita a 50 caracteres

    def process_question(self, question, max_retries=3):
        """Processa a pergunta sem timeout, permitindo que o modelo termine o processamento."""
        start_time_session = time.time()
        session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self._log_to_file(f"\n{'#' * 50}")
        self._log_to_file(f"Início da sessão: {session_id}")
        self._log_to_file(f"Pergunta recebida: {question}")
        self._log_to_file(f"Uso de memória inicial: {self._check_memory_usage():.2f} MB")
        
        for attempt in range(max_retries):
            try:
                # Gera nome de arquivo baseado na pergunta
                safe_question = self._sanitize_filename(question)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{safe_question}_{timestamp}.txt"
                self.output_file = os.path.join(self.output_dir, filename)
                
                if self._is_memory_critical():
                    self._log_to_file("AVISO: Uso de memória crítico. Tentando liberar recursos...")
                    gc.collect()
                    time.sleep(1)
                    
                # Inicializa o modelo e mede a memória usada
                memory_used = self._initialize_model()
                
                start_time = time.time()
                
                # Modificação para incluir CoT
                prompt = f"Pergunta: {question}\n\nPor favor, pense passo a passo e explique seu raciocínio em detalhes antes de fornecer a resposta final. Certifique-se de que a resposta seja completa e bem estruturada.\n\nResposta:"
                
                # Gera a resposta sem timeout
                response = self.model(
                    prompt,
                    max_tokens=1024,  # Aumente o número de tokens
                    stop=None,  # Remova as sequências de parada
                    echo=False,
                    temperature=0.7,
                    top_p=0.95
                )
                
                processing_time = time.time() - start_time
                
                answer = response['choices'][0]['text'].strip()
                time_msg = self._format_time_duration(processing_time)
                
                self._log_to_file(f"Resposta gerada em {time_msg}")
                self._log_to_file(f"RESPOSTA: {answer}")
                
                end_time_session = time.time()
                total_session_time = end_time_session - start_time_session
                self._log_to_file(f"Fim da sessão: {session_id}")
                self._log_to_file(f"Tempo total da sessão: {self._format_time_duration(total_session_time)}")
                self._log_to_file(f"Uso de memória final: {self._check_memory_usage():.2f} MB")
                self._log_to_file(f"{'#' * 50}\n")
                
                return answer, time_msg, memory_used
                
            except Exception as e:
                error_msg = f"Erro ao processar pergunta (tentativa {attempt + 1}/{max_retries}): {str(e)}"
                self._log_to_file(error_msg)
                self._log_to_file(f"Detalhes do erro: {repr(e)}")  # Adiciona detalhes do erro
                self.model = None
                self.initialized = False
                gc.collect()
                
                if attempt < max_retries - 1:
                    time.sleep(5)  # Espera antes de tentar novamente
                else:
                    end_time_session = time.time()
                    total_session_time = end_time_session - start_time_session
                    self._log_to_file(f"Fim da sessão: {session_id}")
                    self._log_to_file(f"Tempo total da sessão: {self._format_time_duration(total_session_time)}")
                    self._log_to_file(f"Uso de memória final: {self._check_memory_usage():.2f} MB")
                    self._log_to_file(f"{'-' * 50}\n")
                    return f"Erro no processamento após {max_retries} tentativas: {str(e)}", "00:00:00", 0.0

    def _format_time_duration(self, seconds):
        """Formata o tempo em horas, minutos e segundos"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def setup_emergency_cleanup():
    def emergency_handler(signum, frame):
        print("\nRecebido sinal de interrupção. Limpando recursos...")
        gc.collect()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, emergency_handler)
    signal.signal(signal.SIGTERM, emergency_handler)

def optimize_system():
    gc.set_threshold(100, 5, 5)
    process = psutil.Process(os.getpid())
    print(f"Memória inicial do processo: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    print("Dica: Feche outros programas para liberar memória")

def main():
    optimize_system()
    setup_emergency_cleanup()
    
    model_path = "/home/rauto/gemma-3-4b-it-Q4_K_M.gguf"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    main_log = os.path.join(output_dir, f"main_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    def log_to_main(message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(main_log, 'a', encoding='utf-8', buffering=8192) as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"Erro ao escrever no log principal: {str(e)}")
    
    # Solicita a pergunta ao usuário
    question = input("Digite a sua pergunta: ")
    log_to_main(f"Pergunta escolhida: {question}")
    
    thinker = DeepThoughtR1(model_path, output_dir=output_dir)
    result, processing_time, memory_used = thinker.process_question(question)
    
    log_to_main(f"Resultado: {result}")
    log_to_main(f"Tempo de processamento: {processing_time}")
    log_to_main(f"Memória usada para carregar o modelo: {memory_used:.2f} MB")
    
    print(f"\n{'=' * 50}")
    print(f"Resultado: {result}")
    print(f"Tempo de processamento: {processing_time}")
    print(f"Memória usada para carregar o modelo: {memory_used:.2f} MB")
    print(f"{'=' * 50}")
    
    del thinker
    gc.collect()

if __name__ == "__main__":
    main()
