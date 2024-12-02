
# Automação de Download de Relatórios Municipais do FNDE

Este projeto automatiza o download de relatórios em formato PDF do site do FNDE para todos os municípios brasileiros, lidando com o reCAPTCHA por meio do serviço **2Captcha**.

## Funcionalidades
- Resolução automatizada de reCAPTCHA utilizando a API 2Captcha.
- Registro de municípios já processados em um arquivo (`municipios_tentados.txt`).
- Verificação de arquivos PDF já baixados para evitar duplicações.
- Navegação automática pelo site do FNDE utilizando Selenium.

---

## Configuração do Projeto

### 1. Pré-requisitos
Certifique-se de ter instalado:
- **Python 3.x**
- **Google Chrome** e **ChromeDriver** compatíveis com sua versão do navegador.

Instale as bibliotecas necessárias executando:
```bash
pip install -r requirements.txt
```

### 2. Criar o arquivo de chave da API (`api_key.txt`)
Crie um arquivo chamado `api_key.txt` na raiz do projeto e adicione sua chave de API do 2Captcha, **sem aspas**:
```
sua-api-key-aqui
```

### 3. Estrutura do Projeto
- `api_key.txt`: Contém a chave de API para o serviço 2Captcha.
- `municipios_tentados.txt`: Armazena os códigos dos municípios já processados.
- `requirements.txt`: Lista de dependências do Python.
- `main.py`: Código principal do projeto.

### 4. Dependências (requirements.txt)
O arquivo `requirements.txt` deve incluir:
```
selenium
requests
```

Certifique-se de que as dependências estão instaladas executando:
```bash
pip install -r requirements.txt
```

---

## Como Executar

1. **Carregue a chave da API**
   A chave da API é carregada automaticamente do arquivo `api_key.txt`.

2. **Execute o Script**
   Para iniciar o processo de download, execute o seguinte comando:
   ```bash
   python main.py
   ```

3. **Parâmetros**
   - `site_key`: A chave do site para o reCAPTCHA.
   - `estados`: Lista de códigos das Unidades Federativas (UFs) que serão processadas.

---

## Explicação do Código

- **`carregar_api_key`**: Lê a chave da API do arquivo `api_key.txt`.
- **`resolver_recaptcha`**: Solicita a resolução do reCAPTCHA para a página atual.
- **`verificar_pdf_baixado`**: Verifica se o PDF para o município já foi baixado.
- **`verificar_e_registrar_tentativa`**: Registra municípios processados para evitar repetições.
- **`iniciar_driver`**: Inicializa o navegador Chrome para automação com Selenium.
- **`executar_processo_download`**: Função principal que processa todos os estados e municípios.

---

## Notas Importantes
- **Tempo para resolução do CAPTCHA**: O script verifica a resolução do reCAPTCHA a cada 5 segundos por até 20 tentativas.
- **Pasta de Downloads**: Certifique-se de que os arquivos PDF sejam salvos corretamente no diretório padrão de downloads do sistema.

