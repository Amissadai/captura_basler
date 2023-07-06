from pypylon import pylon
import cv2

# Inicializar o sistema Pylon
pylon.PylonInitialize()

# Criar um objeto de câmera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Abrir a câmera
camera.Open()

# Configurar algumas opções da câmera
camera.Width.SetValue(640)
camera.Height.SetValue(480)
camera.PixelFormat.SetValue("BGR8")
camera.AcquisitionFrameRate.setValue(60)

# Criar um objeto GrabResult para receber os frames da câmera
grabResult = pylon.GrabResult()

# Loop principal
while camera.IsGrabbing():
    # Acionar a captura de imagem
    camera.RetrieveResult(5000, grabResult, pylon.TimeoutHandling_ThrowException)
    
    # Verificar se o frame foi capturado com sucesso
    if grabResult.GrabSucceeded():
        # Converter o resultado para uma imagem do OpenCV
        img = grabResult.Array
        
        # Exibir o frame capturado
        cv2.imshow('Camera Basler', img)
    
    # Verificar se a tecla 'q' foi pressionada para encerrar o programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
camera.Close()
camera.DestroyDevice()
cv2.destroyAllWindows()
pylon.PylonTerminate()
