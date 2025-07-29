"""
Exemplo de uso do PaddleOCR localmente.
Requer: paddleocr, paddlepaddle
"""

import sys

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="pt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ocr_paddle_example.py caminho/para/imagem.png")
        exit(1)
    img_path = sys.argv[1]
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        for box, (text, conf) in line:
            print(f"Texto: {text} (confiança: {conf:.2f})")
