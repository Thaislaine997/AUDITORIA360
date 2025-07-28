from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='pt')

# Exemplo de uso: resultado = ocr.ocr('caminho/para/imagem.png', cls=True)
# print(resultado)
