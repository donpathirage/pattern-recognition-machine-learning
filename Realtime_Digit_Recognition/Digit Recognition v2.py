
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
rect, digits, x, y = [], [], 0, 0
font = cv2.FONT_HERSHEY_SIMPLEX

def show_webcam(model1, mirror=False):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    kernel = np.ones((3,3),np.uint8)
    while True:
        rect = []
        _, img = cam.read()

        if mirror:
            img = cv2.flip(img, 1)

        im_copy = img.copy()

        gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        blur = cv2.GaussianBlur(gray,(21,21),0)
        th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,        cv2.THRESH_BINARY_INV,11,2)

        dilation = cv2.dilate(th3, kernel, iterations = 2)

        _, contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in contours:
            x = c[:,0][:,0]
            y = c[:,0][:,1]
            minx = np.min(x)
            maxx = np.max(x)
            miny = np.min(y)
            maxy = np.max(y)

            rect.append([minx, maxx, miny, maxy])

        digits = []
        r2 = []
        for r in rect:
            try:
                digit = dilation[r[2]-5 : r[3]+5, r[0]-5 : r[1]+5]
                digit = cv2.erode(digit, kernel, iterations = 3)

                digit = cv2.resize(digit, (28,28), interpolation = cv2.INTER_AREA)


                digits.append(digit)

                r2.append(r)


            except:
                pass

        for i in range(len(digits)):
            prediction = 0
            sum = 0
            sum += model1.predict(np.array(np.round(digits[i]/255)).reshape(1,28,28,1))
            # sum += model2.predict(np.array(np.round(digits[i]/255)).reshape(1,28,28,1))
            # sum += model3.predict(np.array(np.round(digits[i]/255)).reshape(1,28,28,1))
            # sum += model4.predict(np.array(np.round(digits[i]/255)).reshape(1,28,28,1))
            prediction = np.argmax(sum)
            im_copy = cv2.rectangle(im_copy,(r2[i][0],r2[i][2]),(r2[i][1],r2[i][3]),(0,0,255),3)
            cv2.putText(im_copy, str(prediction), (r2[i][0]-4,r2[i][2]-4), font, 1, (175,255,155))



        cv2.imshow('Original ', im_copy)


        if cv2.waitKey(1) == 27:

            break  # esc to quit


    for digit in digits:
        plt.figure()
        plt.imshow(digit, cmap = 'gray')

    cv2.destroyAllWindows()


    return digits




model1 = tf.keras.models.load_model('MNIST_Classifier-v2-ALL.model')   #Trained on entire augmented dataset including test set (Best performer)
#model2 = tf.keras.models.load_model('MNIST_Classifier-v2-E.model')    #Random Erosion dataset
#model3 = tf.keras.models.load_model('MNIST_Classifier-v2-D.model')    #Random Dilation dataset
# model4 = tf.keras.models.load_model('MNIST_Classifier-v2-ED.model')  #Random Erosion or Dilation dataset

show_webcam(model1, mirror=False)
