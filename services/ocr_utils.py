# Utilitário para OCR usando PaddleOCR
from paddleocr import PaddleOCR

def extrair_texto_ocr(caminho_arquivo):
    ocr = PaddleOCR(use_angle_cls=True, lang='pt')
    resultado = ocr.ocr(caminho_arquivo, cls=True)
    textos = []
    for linha in resultado:
        for res in linha:
            textos.append(res[1][0])
    return "\n".join(textos)
