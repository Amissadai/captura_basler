from pypylon import pylon
<<<<<<< HEAD
=======
import cv2
import numpy as np
>>>>>>> nova-branch

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
        camera.StartGrabbing(1)
        grab = camera.RetrieveResult(2000, pylon.TimeoutHandling_Return)

        if grab.GrabSucceeded():
            img = grab.GetArray()
            print(f'Tamanho da imagem: {img.shape}')
        
        camera.Close()
    else:
        print("Falha ao abrir a câmera.")
