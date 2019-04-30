#!/usr/bin/env python3
import pdb 
#pdb.set_trace()
import torch
from torch.autograd import Variable
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
#librerias para cargar datos de manera eficiente
from torch.utils.data import DataLoader, TensorDataset
import torchvision
import torchvision.transforms as transforms
import cv2
from pathlib import Path
import matplotlib.pyplot as plt # for plotting
from PIL import Image
from readNeuronal import Net


tranformadaTraining = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])


dataTraining = torchvision.datasets.ImageFolder('./products_assets',transform=tranformadaTraining)
dataLoaderTraining = DataLoader(dataTraining,batch_size=4,shuffle=False)

clasesEntramiento = dataTraining.classes

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

redneuronal = Net().to(device)



def mostrarImagen(img):
   
    img = img / 2 + 0.5   
    npimg = img.numpy()

    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

#permite guardar las clases 
"""
def loadClassesOfFolder():
    p = Path('./products_assets') 
    for x in p.iterdir():
        if x.is_dir():
            ubicacionDirectorio = str(x)
            listaNombreDirectorio = ubicacionDirectorio.split('/')
            
            
            clasesEntramiento.append(listaNombreDirectorio[1])
"""





def entrenamiento():

    NUMBER_EPOCHS = 2
    LEARNING_RATIO = 1e-2
    lossFunction = nn.CrossEntropyLoss()
    optimizador = optim.SGD(redneuronal.parameters(),lr=LEARNING_RATIO)
    cantidadLosscalculado = 0
    lossTotal = 0

    for epoch in range(NUMBER_EPOCHS):

        dataTrainingIter = iter(dataLoaderTraining)
        for data,labels in dataTrainingIter:
            redneuronal.zero_grad()
            data,labels = Variable(data.float().to(device)),Variable(labels.to(device))
            ouput = redneuronal(data)
            loss = lossFunction(ouput,labels)
            loss.backward()
            optimizador.step()
            lossTotal+=loss.item()
            cantidadLosscalculado+=1
        
        if epoch%5==0:
            lossPromedio = (lossTotal/cantidadLosscalculado)
            print('funcion de perdida promedio '+str(lossPromedio))
            print('cantidad de ciclos '+str(epoch+1))
            lossTotal = 0
            cantidadLosscalculado = 0


def testDataTraining():
    folderImagenes = Path('./imagentest')
    valorBaseImagen = 2073600
    valorWitdh = 720
    valorHeight = 960
    for folder in folderImagenes.iterdir():
        imagen = cv2.imread(str(folder))
        if imagen.size<valorBaseImagen:
            imagen = cv2.resize(imagen,(valorWitdh,valorHeight),cv2.INTER_CUBIC)
        else:
            imagen = cv2.resize(imagen,(valorWitdh,valorHeight),cv2.INTER_AREA)
        
       imagenTensor = torch.from_numpy(imagen)
       ouput = redneuronal(imagenTensor.to(device))
       _,prediccion = torch.max(ouput.data,1)
       print('La prediccion es :')

       print(clasesEntramiento[prediccion[0].item()])

       print('la ubicacion de la imagen es ')
       print(str(folder))
     





    
def saveModel():
    torch.save(redneuronal.state_dict(),'./modelo/modelo1.pt')


def loadModel():
    ubicacion = 'modelo1.pt'
    try:
        redneuronal.load_state_dict(torch.load('./modelo/'+ubicacion))
        redneuronal.eval()
        



entrenamiento()
saveModel()
testDataTraining()
