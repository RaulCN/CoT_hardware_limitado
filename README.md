# Chain-of-Thought (CoT) (Hardware Limitado)

Um projeto experimental que testa conceitos de estado da arte em Inteligência Artificial, como **Chain-of-Thought (CoT)**, utilizando modelos de linguagem recentes (como o **Gemma 3B** e **DeepSeek 7B**) em ambientes de extrema restrição de hardware. O objetivo é demonstrar que é possível realizar tarefas avançadas de IA com recursos limitados, contribuindo para a **democratização da tecnologia** e sua aplicação em contextos como:

- **Países emergentes**: Onde o acesso a hardware de ponta é limitado.
- **Startups**: Que precisam criar protótipos com custos reduzidos.
- **Estudantes e curiosos**: Que desejam explorar IA sem a necessidade de equipamentos caros.

A ideia central é **fazer muito com pouco**, promovendo a **emancipação** por meio da tecnologia.

## Funcionalidades

- **Geração de Respostas com CoT**: O modelo gera respostas detalhadas, explicando seu raciocínio passo a passo (Chain-of-Thought).
- **Otimização para Hardware Limitado**: O código é projetado para funcionar em sistemas com pouca memória RAM (a partir de 6 GB).
- **Monitoramento de Recursos**: Logs detalhados mostram o uso de memória e o tempo de processamento.
- **Fácil Configuração**: Basta um modelo GGUF (como o Gemma 3B ou DeepSeek 7B) e um ambiente Python básico.

## Como Usar

### Pré-requisitos

1. **Python 3.8 ou superior**
2. **Modelo GGUF**: Baixe um modelo compatível (ex: `gemma-3-4b-it-Q4_K_M.gguf` ou `deepseek-7b-Q4_K_M.gguf`) e coloque-o no diretório do projeto.
3. **Dependências**:
   ```bash
   pip install llama-cpp-python psutil
   ```

### Executando o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/pensamento-profundo-r1.git
   cd pensamento-profundo-r1
   ```

2. Execute o script:
   ```bash
   python Pensamento_Profundo_R1_hardware_limitado_7.py
   ```

3. Digite uma pergunta quando solicitado. Exemplo:
   ```
   Digite a sua pergunta: Explique a gravidade para uma criança de 5 anos.
   ```

4. Aguarde o processamento e veja a resposta gerada.

### Exemplo de Saída (prompt usado no script, log salvo na posta output)

```
==================================================
Resultado: Imagine que a Terra é um grande amigo que gosta de abraçar tudo! Ela tem uma força secreta que a puxa para baixo...
Tempo de processamento: 00:02:16
Memória usada para carregar o modelo: 2690.93 MB
==================================================
```

### Análise dos Resultados

1. **Qualidade da Resposta**:
   - A resposta gerada pelo modelo é **clara, estruturada e adequada** para o público-alvo (crianças de 5 anos).
   - O uso de **analogias** (Terra como um "grande amigo" ou "ímã gigante") e **exemplos do dia a dia** (jogar uma bola, água caindo do balde) torna o conceito de gravidade fácil de entender.

2. **Eficiência em Hardware Limitado**:
   - O projeto demonstra que é possível executar modelos de linguagem avançados em sistemas com **apenas 6 GB de RAM**.
   - O tempo de processamento (2 minutos e 16 segundos) é **aceitável** para um ambiente de hardware limitado.

3. **Aplicação de Chain-of-Thought (CoT)**:
   - O modelo aplicou a técnica de **CoT** de forma eficaz, explicando seu raciocínio passo a passo antes de fornecer a resposta final.
   - Isso mostra que técnicas avançadas de IA podem ser utilizadas mesmo em sistemas modestos.

---

### Conclusão

Os resultados demonstram que é possível **fazer muito com pouco**, trazendo conceitos de IA de ponta para ambientes de hardware limitado. Isso abre portas para a **democratização da tecnologia**, permitindo que países emergentes, startups, estudantes e curiosos explorem o potencial da IA sem a necessidade de investimentos elevados em infraestrutura.
```

## Tecnologias Utilizadas

- **LLM (Large Language Models)**: Modelos como Gemma 3B e DeepSeek 7B, otimizados para hardware limitado.
- **Chain-of-Thought (CoT)**: Técnica que permite ao modelo explicar seu raciocínio passo a passo.
- **llama-cpp-python**: Biblioteca para carregar e executar modelos GGUF de forma eficiente.
- **Psutil**: Para monitoramento de uso de memória e CPU.

## Limitações

- **Hardware Necessário**: Requer pelo menos 6 GB de RAM.
- **Tempo de Processamento**: Pode variar dependendo da complexidade da pergunta e do hardware disponível.
- **Modelos Pequenos**: Modelos como Gemma 3B e DeepSeek 7B são eficientes, mas podem não ter o mesmo desempenho que modelos maiores em tarefas complexas.

## Contribuições

Contribuições são bem-vindas! Se você quiser melhorar o projeto, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch com sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

## Contato

Se tiver dúvidas, sugestões ou quiser colaborar, entre em contato:

- **Nome**: Raul Campos Nascimento
- **Email**: rautopiaa@gmail.com

## Agradecimentos

- À comunidade de IA de código aberto, por disponibilizar modelos e ferramentas incríveis.
- Aos desenvolvedores do llama-cpp-python, por tornar a execução de LLMs acessível.
- A todos que acreditam que a tecnologia pode ser uma ferramenta de emancipação e democratização.
