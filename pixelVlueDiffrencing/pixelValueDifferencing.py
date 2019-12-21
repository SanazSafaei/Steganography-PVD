import cv2
import math
import PNSR
import copy


class PVD:

    def __init__(self, msg, img):
        self.msg = msg
        self.img = img

    def msgToBinary(self):
        stringBinary = ' '.join(map(bin, bytearray(self.msg, 'utf8')))
        stringBinary = stringBinary.replace(" ", "")
        # print(stringBinary[2:])
        stringBinary = stringBinary.replace("0b", "")
        # stringBinary = stringBinary.split()
        # intBinary = int(stringBinary)
        return stringBinary

    def range_table(self, d):
        R = [(0, 7), (8, 15), (16, 31), (32, 63), (64, 127), (128, 255)]
        for i in R:
            if i[0] <= d:
                if i[1] >= d:
                    bits = int(math.log2(i[1] - i[0]))
                    print("bits : ",bits)
                    return (i[0], bits)

    def pvd(self):
        secretMsg = self.msgToBinary()
        print("msg : ",secretMsg)
        print("msg size : ",len(secretMsg))
        msg_counter = 0
        I = cv2.imread(self.img, cv2.IMREAD_GRAYSCALE)
        I2 = copy.deepcopy(I)
        height, width = I.shape
        print("image size : ",I.shape)
        flag = False
        p1 = 0
        for h in range(0, height):
            if msg_counter == len(secretMsg) - 1:
                break
            if h % 2 == 0:  # if row is even we should iterate at the first of row
                iterate_w = range(0, width, 1)
            else:  # if row is odd we should iterate at the end of row
                iterate_w = range(width - 1, -1, -1)
            for w in iterate_w:
                if msg_counter >= len(secretMsg) - 1:
                    break
                if flag:  # if p1 refreshed
                    p0 = I[h][w]
                    d = p0 - p1
                    print("d : ",d)
                    temp = self.range_table(d)
                    if msg_counter + temp[1] <= len(secretMsg):
                        # print(secretMsg[msg_counter:msg_counter + temp[1]])
                        msg_temp = int(secretMsg[msg_counter:msg_counter + temp[1]],2)
                        print("msg temp : ", msg_temp, secretMsg[msg_counter:msg_counter + temp[1]])
                    elif msg_counter + temp[1] >= len(secretMsg) and msg_counter<len(secretMsg):
                        msg_temp = int(secretMsg[msg_counter:])
                        print("msg temp : ",msg_temp , secretMsg[msg_counter:])
                    msg_counter = msg_counter + temp[1]
                    print("msg counter : ",msg_counter)
                    if msg_counter >= len(secretMsg) - 1:
                        break
                    d2 = math.fabs(temp[0] + msg_temp)
                    print("d' : ",d2)
                    m = math.fabs(d - d2)
                    print("m : ",m)
                    if d % 2 == 1:
                        print("pixel 1 : ", p1 + math.floor(m / 2))
                        print("before picture : ",I2[h][w])
                        I2[h][w] = p1 + math.floor(m / 2)
                        print("in picture : ", I2[h][w])
                        if h % 2 == 1 and h == 0:
                            # print("I")
                            print("pixel 0 : ", p0 - math.ceil(m / 2))
                            print("before picture : ", I2[h-1][w-1])
                            I2[h - 1][width - 1] = p0 - math.ceil(m / 2)
                            print("in picture : ", I2[h-1][w-1])
                        else:
                            print("pixel 0 : ", p0 - math.ceil(m / 2))
                            print("before picture : ", I2[h][w-1])
                            I2[h][w - 1] = p0 - math.ceil(m / 2)
                            print("in picture : ", I2[h][w-1])
                    else:
                        print("pixel 1 : ",p1 + math.ceil(m / 2))
                        print("before picture : ", I2[h][w])
                        I2[h][w] = p1 + math.ceil(m / 2)
                        print("in picture : ", I2[h][w])
                        if h % 2 == 1 and h == 0:
                            print("pixel 0 : ", p0 - math.floor(m / 2))
                            print("before picture : ", I2[h-1][w-1])
                            I2[h - 1][width - 1] = p0 - math.floor(m / 2)
                            print("in picture : ", I2[h - 1][w - 1])
                        else:
                            print("pixel 0 : ",p0 - math.floor(m / 2))
                            print("before picture : ", I2[h][w-1])
                            I2[h][w - 1] = p0 - math.floor(m / 2)
                            print("in picture : ", I2[h][w - 1])
                else:
                    p1 = I[h][w]
                flag = not flag
        # cv2.imshow("withmsg",I2)
        # cv2.imshow("orginal",I)
        # cv2.waitKey()
        return [I,I2]


msg = "hi"
img = "The-original-cameraman-image.png"

p = PVD(msg, img)
temp=p.pvd()
psnre=PNSR.PNSR(temp[0],temp[1])
cv2.imshow("withmsg",temp[1])
cv2.imshow("orginal",temp[0])
cv2.waitKey()
print(psnre.MeanSquareError())