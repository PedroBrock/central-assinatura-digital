# 🔐 Central de Assinatura Digital
> Projeto acadêmico — Simulação simplificada do DocuSign usando criptografia RSA e SHA-256

---

## 📌 O que é este projeto

Sistema web de assinatura digital de documentos que demonstra na prática dois conceitos fundamentais de segurança da informação:

- **Integridade**: garante que o documento não foi alterado após a assinatura
- **Autenticidade**: garante que a assinatura veio de quem diz ser

Se uma única letra do documento for alterada após a assinatura, o sistema detecta a violação e exibe um erro.

---

## 🗂️ Estrutura do repositório

```
central-assinatura/
├── backend/
│   ├── main.py          
│   ├── crypto.py        
│   ├── requirements.txt 
│   └── keys/            
│       ├── private.pem  
│       └── public.pem   
└── frontend/            
    └── ...
```

---

## ⚙️ Como funciona — Explicação técnica

### 1. Geração de chaves RSA
Ao iniciar o servidor pela primeira vez, o sistema gera automaticamente um par de chaves RSA de **2048 bits** e salva em arquivos `.pem`:
- **Chave privada** (`private.pem`): usada para **assinar** — fica em segredo
- **Chave pública** (`public.pem`): usada para **validar** — pode ser compartilhada

### 2. Assinatura do documento
```
Texto do documento
       ↓
   SHA-256                → gera um hash de 32 bytes (tamanho fixo, único por conteúdo)
       ↓
RSA-PSS com chave privada → cifra o hash
       ↓
  Assinatura (Base64)     → string que representa a assinatura do documento
```

### 3. Validação da assinatura
```
Texto recebido + Assinatura recebida
       ↓                        ↓
   SHA-256               RSA-PSS com chave pública
       ↓                        ↓
  Hash novo          Hash original (decifrado)
            ↓
         Iguais? → ✅ Documento íntegro
         Diferentes? → ❌ Documento foi violado
```

### Por que o SHA-256?
O SHA-256 é uma função de hash criptográfico: qualquer alteração mínima no texto (uma letra, um espaço) gera um hash completamente diferente. Isso torna impossível modificar o documento sem invalidar a assinatura.

---

## 🚀 Instalação e execução do backend

### Pré-requisitos
- Python 3.8 ou superior
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/PedroBrock/central-assinatura.git
cd central-assinatura/backend

# 2. (Recomendado) Crie um ambiente virtual
python -m venv venv

# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
uvicorn main:app --reload
```

O servidor estará disponível em: `http://localhost:8000`

A documentação interativa (Swagger) estará em: `http://localhost:8000/docs`

> As chaves RSA são geradas automaticamente em `keys/` na primeira execução.

---

## 📡 Endpoints da API

### `POST /assinar`
Recebe o texto do documento e retorna a assinatura digital em Base64.

**Body:**
```json
{
  "documento": "Contrato entre Pedro e uma empresa"
}
```

**Resposta:**
```json
{
  "assinatura": "base64_da_assinatura...",
  "status": "Documento assinado com sucesso"
}
```

---

### `POST /validar`
Recebe o documento e a assinatura e verifica se o documento é autêntico.

**Body:**
```json
{
  "documento": "Contrato entre Pedro e uma empresa",
  "assinatura": "base64_da_assinatura..."
}
```

**Resposta (sucesso):**
```json
{
  "valido": true,
  "mensagem": "✅ Assinatura válida! Documento íntegro."
}
```

**Resposta (documento alterado):**
```json
{
  "valido": false,
  "mensagem": "❌ Assinatura inválida! Documento foi alterado."
}
```

---

### `GET /chave-publica`
Retorna a chave pública RSA em formato PEM (útil para o frontend exibir).

---

## 🌐 Informações para o Frontend

A API aceita e retorna **JSON**. O CORS está habilitado para qualquer origem (`*`), então o frontend pode rodar em qualquer porta localmente sem problemas.

**URL base local:** `http://localhost:8000`

**Fluxo esperado na tela:**
1. Usuário digita ou cola o texto do contrato
2. Clica em **"Assinar Documento"** → chama `POST /assinar` → exibe a assinatura Base64
3. (Opcionalmente altera o texto para demonstrar a violação)
4. Clica em **"Validar Assinatura"** → chama `POST /validar` → exibe resultado **verde** (válido) ou **vermelho** (violado)

---

## 🛠️ Dependências

| Biblioteca | Versão | Uso |
|---|---|---|
| `fastapi` | latest | Framework web para os endpoints |
| `uvicorn` | latest | Servidor ASGI para rodar o FastAPI |
| `cryptography` | latest | Geração de chaves RSA e operações de assinatura |
| `hashlib` | built-in | Cálculo do hash SHA-256 (padrão do Python) |

---

## 📚 Conceitos abordados

- Criptografia assimétrica (RSA)
- Função de hash criptográfico (SHA-256)
- Assinatura digital (RSA-PSS)
- Integridade e autenticidade de documentos
- API REST com FastAPI
- Formato PEM para armazenamento de chaves

---
