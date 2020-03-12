import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import gc
from keras import models
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import matplotlib.image as mpimg



class  patient_WBC_images():
    def __init__(self, specimenInfo, test_imgs):
        self.specinfo = specimenInfo
        self.test_imgs = test_imgs

    def predict_images(self, numpred):

        os.environ['KMP_DUPLICATE_LIB_OK']='True'
        model = load_model(os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/model_keras.h5"))
        model.summary()

        print("content",len(self.test_imgs))
        random.shuffle(self.test_imgs)


        ##### Create array of images with class labels #########
        def read_and_process_image(list_of_images):
            X = []
            y = []
            image_counter  = 0
            for image in list_of_images:
                image_counter= image_counter+1
                try:
                    X.append(cv2.resize(cv2.imread(image,cv2.IMREAD_COLOR),(150,150), interpolation= cv2.INTER_CUBIC))

                except:
                    print("An exception occurred")

                if image in self.test_imgs:   #test label 0
                    y.append(0)
                print("Labeling image #",image_counter , " of ", len(self.test_imgs))

            return X



        #predict on the  images of the test set
        X_test= read_and_process_image(self.test_imgs)
        x = np.array(X_test) # the images to be predicted
        test_datagen = ImageDataGenerator(rescale=1./255)


        ##### check results of real vs prediction and view array of images #####
        pred = model.predict_classes(x[0:numpred])
        params = {"ytick.color": "k",
                  "xtick.color": "k",
                  "axes.labelcolor": "k",
                  "axes.edgecolor": "k"}
        plt.rcParams.update(params)
        fig = plt.figure(figsize=(14.3,numpred*.16), num='WBC Classifier') #14.3, 16 for 100 -- 14.3, 160 for 1000
        columns = 10
        rows = len(pred)/columns


        #prediction labels
        text_labels = []
        prediction_x = []


        for ima, i in zip(self.test_imgs[:numpred], range(len(pred))):

            ##labeling the pictures name, prediction, and real
            print ("Labeling Prediction #" + str(i+1))
            if pred[i] == 3:
                text_labels.append('Neutrophil')
            elif pred[i] == 2:
                text_labels.append('Monocyte')
            elif pred[i] == 1:
                text_labels.append('Lymphocyte')
            elif pred[i] == 0:
                text_labels.append('Eosiniphil')
            prediction_x.append(pred[i])





            #showing the text result on the screen
            fig.add_subplot(rows, columns, i +1) #adding rows and columns
            fig.use_sticky_edges = True
            plt.tick_params(labelsize=5) #sizeof the axes ticks
            title_obj = plt.title('Prediction:' + text_labels[i], fontdict={'fontsize': 7})
            plt.setp(title_obj, color='k')
            ##showing the unaltered images
            img=mpimg.imread(ima)
            imgplot = plt.imshow(img)



        # custom figure colors and layout
        fig.set_facecolor("#CEEBFB")#CEEBFB, #A3D6F5, #66A7C5, #EE3233
        fig.tight_layout()
        plt.subplots_adjust(hspace=0, wspace=0.2)
        #plt.show()

        return self.specinfo, fig, prediction_x

