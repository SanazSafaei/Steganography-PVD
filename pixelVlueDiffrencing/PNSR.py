import cv2
import numpy as np
import math

class PNSR:

    def __init__(self,org,final):
        self.org=org
        self.final=final
        self.size=self.org.shape

    def MeanSquareError(self):

        sub=self.org-self.final
        print("sub",sub)
        pow_sub=np.power(sub,2)
        sum_pixels= np.sum(pow_sub[:,:])
        print(sum_pixels)
        avg=np.divide(sum_pixels,(self.size[0]*self.size[1]))
        avg_rad=np.sqrt(avg)
        print(avg_rad)
        mse=np.sum(avg_rad)
        result=self.psnre(mse)
        return result


    def psnre(self,result):
        if(result>0):
            psnre=10*math.log((255*255/result),10)
        else:
            psnre=99

        return psnre
