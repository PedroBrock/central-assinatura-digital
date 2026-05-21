import base64
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crypto import gerar_chaves, assinar_documento, validar_assinatura, PRIVATE_KEY_PATH

# Gera as chaves na primeira execução se não existirem
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not PRIVATE_KEY_PATH.exists():
        gerar_chaves()
    yield

app = FastAPI(lifespan=lifespan)

# Libera o frontend chamar a API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentoRequest(BaseModel):
    documento: str

class ValidacaoRequest(BaseModel):
    documento: str
    assinatura: str  


@app.post("/assinar")
def assinar(req: DocumentoRequest):
    """Recebe texto → retorna assinatura em base64"""
    try:
        assinatura_bytes = assinar_documento(req.documento)
        return {
            "assinatura": base64.b64encode(assinatura_bytes).decode("utf-8"),
            "status": "Documento assinado com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validar")
def validar(req: ValidacaoRequest):
    """Recebe texto + assinatura base64 → retorna válido ou inválido"""
    try:
        assinatura_bytes = base64.b64decode(req.assinatura)
        valido = validar_assinatura(req.documento, assinatura_bytes)

        if valido:
            return {"valido": True,  "mensagem": "✅ Assinatura válida! Documento íntegro."}
        else:
            return {"valido": False, "mensagem": "❌ Assinatura inválida! Documento foi alterado."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao validar: {str(e)}")


@app.get("/chave-publica")
def obter_chave_publica():
    """Expõe a chave pública para o frontend exibir (opcional)"""
    with open("keys/public.pem") as f:
        return {"chave_publica": f.read()}