from pypylon import pylon
import cv2
import numpy as np

# Identificando a câmera
tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()

if len(devices) == 0:
    print("Nenhuma câmera encontrada.")
else:
    camera = pylon.InstantCamera()
    tl_factory = pylon.TlFactory.GetInstance()
    camera.Attach(tl_factory.CreateDevice(devices[0]))
    camera.Open()

    if camera.IsOpen():
        print("Câmera aberta com sucesso.")

        # Configurando a câmera para gravar vídeo
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)  # Captura contínua
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        # A câmera tem 14 fps. Resolução máxima:  2748px X 3840px
        video_writer = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 14, (camera.Width.Value, camera.Height.Value))

        # Configurando as dimensões desejadas para a tela
        display_width = 800
        display_height = 600

        # Ajuste de brilho
        brightness = 50  # Valor de ajuste de brilho (-100 a 100)

        while True:
            if not camera.IsGrabbing():
                break

            # Verificando se o usuário pressionou a tecla 'q' para interromper a gravação
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                # Convertendo a imagem para formato adequado
                image = converter.Convert(grab_result)
                frame = image.GetArray()

                # Ajustando o brilho
                frame_adjusted = cv2.addWeighted(frame, 1 + brightness / 100, np.zeros(frame.shape, frame.dtype), 0, 0)

                # Redimensionando o frame para as dimensões desejadas
                resized_frame = cv2.resize(frame_adjusted, (display_width, display_height))

                # Exibindo o frame capturado
                cv2.imshow('Frame', resized_frame)

                # Gravando o frame no vídeo
                video_writer.write(frame_adjusted)

            grab_result.Release()

        camera.StopGrabbing()
        camera.Close()
        video_writer.release()
        cv2.destroyAllWindows()
        print("Vídeo gravado com sucesso.")
    else:
        print("Falha ao abrir a câmera.")
