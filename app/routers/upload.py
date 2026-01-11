from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List
import os
import uuid
from pathlib import Path
import shutil

router = APIRouter()

# Configurações
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILES_PER_AD = 5

def validate_image(file: UploadFile) -> None:
    """Valida tipo e tamanho do arquivo"""
    # Valida extensão
    file_ext = Path(file.filename or "").suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Valida content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo deve ser uma imagem"
        )

def save_upload_file(upload_file: UploadFile) -> str:
    """Salva arquivo e retorna o caminho relativo"""
    # Gera nome único
    file_ext = Path(upload_file.filename or "").suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Salva arquivo
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return f"/uploads/{unique_filename}"

@router.post("/upload", response_model=dict)
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Upload de imagens para anúncios.
    Máximo de 5 imagens por upload.
    Tamanho máximo: 5MB por arquivo.
    Formatos aceitos: jpg, jpeg, png, webp
    """
    if len(files) > MAX_FILES_PER_AD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Máximo de {MAX_FILES_PER_AD} imagens por anúncio"
        )
    
    uploaded_urls = []
    
    for file in files:
        # Valida arquivo
        validate_image(file)
        
        # Verifica tamanho (lê o arquivo para obter o tamanho)
        file.file.seek(0, 2)  # Move para o final
        file_size = file.file.tell()
        file.file.seek(0)  # Volta para o início
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo {file.filename} excede o tamanho máximo de 5MB"
            )
        
        # Salva arquivo
        try:
            file_url = save_upload_file(file)
            uploaded_urls.append(file_url)
        except Exception as e:
            # Remove arquivos já salvos em caso de erro
            for url in uploaded_urls:
                file_path = UPLOAD_DIR / Path(url).name
                if file_path.exists():
                    file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar arquivo: {str(e)}"
            )
    
    return {
        "message": f"{len(uploaded_urls)} imagem(ns) enviada(s) com sucesso",
        "urls": uploaded_urls
    }

@router.delete("/upload/{filename}")
async def delete_image(filename: str):
    """Deleta uma imagem do servidor"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )
    
    try:
        file_path.unlink()
        return {"message": "Imagem deletada com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar arquivo: {str(e)}"
        )
