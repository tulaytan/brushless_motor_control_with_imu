class Kalman:

    # Kalman sınıfın constructor fonksiyonu
    def __init__(self):

        # Kalman filtresi değişkenleri

        self.QAngle = 0.001 # Accelometer için işlem gürültü varyans değeri set ediliyor
        self.QBias = 0.003 # Jiroskop sapması için işlem gürültü varyans değeri set ediliyor
        self.RMeasure = 0.03 # Ölçüm gürültüsünün varyans değeri set ediliyor

        self.angle = 0.0 # Açı resetlenir
        self.bias = 0.0 # Sapma resetlenir
        self.rate = 0.0 # Oran resetlenir

        self.P=[[0.0,0.0],[0.0,0.0]] # Hata kovaryans matrisi. Bu matris 2*2'liktir. 
        
        self.K=[0.0,0.0] # Kalman kazanç vektörü

    def getAngle(self,newAngle, newRate,dt):

        # Zaman güncelleme denklemleri 
        #Adım 1:

        self.rate = newRate - self.bias  # newRate son Jiroskop ölçüm değeridir.  
        self.angle += dt * self.rate 

        # Tahmini hata kovaryansını güncelle - Önümüzdeki hata kovaryansını yansıtın
        #Adım 2:

        self.P[0][0] += dt * (dt*self.P[1][1] -self.P[0][1] - self.P[1][0] + self.QAngle)
        self.P[0][1] -= dt * self.P[1][1]
        self.P[1][0] -= dt * self.P[1][1]
        self.P[1][1] += self.QBias * dt

        #Adım 4: Değişim Kovaryansı (Innovation covariance)

        s = self.P[0][0] + self.RMeasure # Tahmini hata

        #Adım 5: Kalman Kazancı Hesaplama (Kalman Gain)
        
        self.K[0] = self.P[0][0]/s
        self.K[1] = self.P[1][0]/s
        
        #Adım 3: Değişim (Innovation)
        y = newAngle - self.angle # Açı farkı

        #Adım 6: Açı güncellenir (Update the Angle)
        self.angle += self.K[0] * y
        self.bias  += self.K[1] * y

        #Adım 7: Tahmin hata varyansı hesaplanır (Calculate estimation error covariance - Update the error covariance)
        P00Temp = self.P[0][0]
        P01Temp = self.P[0][1]

        self.P[0][0] -= self.K[0] * P00Temp
        self.P[0][1] -= self.K[0] * P01Temp
        self.P[1][0] -= self.K[1] * P00Temp
        self.P[1][1] -= self.K[1] * P01Temp

        return self.angle

    def setAngle(self,angle):
        self.angle = angle

    def getQAngle(self,QAngle):
        return self.QAngle

    def setQAngle(self,QAngle):
        self.QAngle = QAngle

    def getQBias(self,QBias):
        return self.QBias

    def setQBias(self,QBias):
        self.QBias = QBias
        
    def  getRMeasure(self,RMeasure):
        return self.RMeasure

    def setRMeasure(self,RMeasure):
        self.RMeasure = RMeasure

    def getRate(self,rate):
        return self.rate





