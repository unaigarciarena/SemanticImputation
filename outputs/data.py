import numpy as np
import matplotlib.pyplot as plt
sizes = [1,5,10,15,20,25,30]

ds = ["STS", "ARLPC", "IntPer", "Tquest", "DTW", "ERP"]
#ds = ["DTW", "ERP"]


#ims = ["Linear Int.", "Pchip Int.", "Quad. Int.", "Spline Int.", "Kalman", "EM", "MICE", "Kalman+Reg", "EM+Reg", "MICE+Reg", "L.Inter+Reg", "Kalman+Pol.Reg", "EM+Pol.Reg", "MICE+Pol.Reg", "L.Inter+Pol.Reg"]
# Aqúí poner los métodos de imputación que se quieran mostrar (en el mismo orden que en distances.py.py
ims = ["Linear Int.", "Pchip Int.", "Quad. Int.", "Spline Int.", "Kalman", "EM", "MICE", "EM+Reg", "Kal+Pol.Reg"]
tot = np.zeros((len(ims), len(sizes)))

#ims = ["Linear Int.", "Kalman", "MICE", "Regression", "Polish. Reg."]
for d in range(4,5):  # Aquí seleccionar qué distancias se quieren mostrar
    for j in range(len(sizes)):
        aux = np.loadtxt("Len" + str(sizes[j]) + "D" + str(d) + "R" + str(0) + ".csv")

        for i in range(1, 30):
            aux = aux + np.loadtxt("Len" + str(sizes[j]) + "D" + str(d) + "R" + str(i) + ".csv")
            #if i == 1:
                #print(aux)
        #print("")
        #print(tot[:,-1])
        tot[:,j] = aux/30
    #print(tot)
    for i in range(tot.shape[0]):
        #if not (i == 1 or i == 5 or i == 6 or i == 3 or i == 9 or i ==7 or i == 8 or i == 10 or i == 13):
        plt.plot(tot[i,:], label=ims[i])
    plt.ylabel("Quality")
    plt.xlabel("Chunk length")
    plt.title("IM quality on different missing chunk lengths, using " + ds[d] + " distance")
    plt.xticks(range(0,len(sizes)), sizes)
    plt.legend()
    plt.show()
#print(tot)