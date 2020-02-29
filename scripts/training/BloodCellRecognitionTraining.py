import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import gc
#### import keras
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import  img_to_array, load_img


##### training input parameters####

#for 70.5% accuracy, 1e-4 , 64 , 500, 32
learning_rate = 1e-4 #(2e-5) for base and (1e-4) for the normal model
num_epoch = 64 #number of epochs
num_in_set = 600 #number of image per set
batch_size = 32 #should be a factor of 4. (4,16,64,256...) #batchsize


### directory path for mac
train_dir_eos = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/EOSINOPHIL")
train_dir_lym = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/LYMPHOCYTE")
train_dir_mon = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/MONOCYTE")
train_dir_neu = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/NEUTROPHIL")
train_eos = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/EOSINOPHIL/{}").format(i) for i in os.listdir(train_dir_eos)]
train_lym = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/LYMPHOCYTE/{}").format(i) for i in os.listdir(train_dir_lym)]
train_mon = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/MONOCYTE/{}").format(i) for i in os.listdir(train_dir_mon)]
train_neu = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TRAIN/NEUTROPHIL/{}").format(i) for i in os.listdir(train_dir_neu)]

#change to Eosinophil, Lymphocyte, Monocyte, Neutrophil
test_dir = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TEST/MONOCYTE")
test_imgs = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/scripts/training/blood-cells/dataset2-master/dataset2-master/images/TEST/MONOCYTE/{}").format(i) for i in os.listdir(test_dir)]


print("works")
#number of images per class 2000 total of 8000
eos = train_eos[:num_in_set]
lym = train_lym[:num_in_set]
mon = train_mon[:num_in_set]
neu = train_neu[:num_in_set]

train_imgs = eos+lym+mon+neu
random.shuffle(train_imgs)


###### garbage collect #####
del train_eos
del train_lym
del train_mon
del train_neu
gc.collect()


##### Check by viewing images #########
#import matplotlib.image as mpimg
#for ima in train_imgs[0:3]:
    #img=mpimg.imread(ima)
    #imgplot = plt.imshow(img)
    #plt.show()

##### Putting labels in the images #########

def read_and_process_image(list_of_images):
    X = []
    y = []
    image_counter  = 0
    for image in list_of_images:
        image_counter= image_counter+1
        X.append(cv2.resize(cv2.imread(image,cv2.IMREAD_COLOR),(150,150), interpolation= cv2.INTER_CUBIC))
        if image in eos:   #eos label 0
            y.append(0)
        elif image in lym: #lym label 1
            y.append(1)
        elif image in mon: #mon label 2
            y.append(2)
        elif image in neu: #neu label 3
            y.append(3)
        print("Labeling image #",image_counter , " of ", len(train_imgs))

    return X, y

X,y = read_and_process_image(train_imgs) # call the function

###### garbage collect #####
del eos
del lym
del mon
del neu
gc.collect()


##### check array ####
print("X is = " , X) #image array info
print("y is = " , y) #label
            
##### check and view array of images #####
#plt.figure(figsize = (20,10))
#columns = 3
#for i in range(columns):
    #plt.subplot(3/columns+1, columns, i +1)
    #plt.imshow(X[i])
#plt.show()


##### check number of images for each class #####
import seaborn as sns
del train_imgs
gc.collect()
X= np.array(X)
y= np.array(y)
sns.countplot(y)
plt.title("White Blood Cells number of Labels")
plt.show()
print ("Shape of train images is:", X.shape)
print ("Shape of labels is:", y.shape)

##### Split into train and testset #####
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X,y, test_size=0.20, random_state = 2)

print("Shape of train images is:", X_train.shape)
print("Shape of validation images is:", X_val.shape)
print("Shape of labels is:", y_train.shape)
print("Shape of labels is:", y_val.shape)

##### garbage collect #####
del X
del y
gc.collect()

##### get length of train and validattion #####
ntrain = len(X_train)
nval = len(X_val)





### pure pretrained model and weights to improve accuracy
from keras.applications import InceptionResNetV2
conv_base= InceptionResNetV2(weights = 'imagenet', include_top = False, input_shape=(150,150,3))
conv_base.summary
model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(4, activation='softmax'))
model.summary()
print ("number of trainable weights before freezing the conv base:", len(model.trainable_weights))
conv_base.trainable = False
print ("number of trainable weights after freezing the conv base:", len(model.trainable_weights))



####creating the model
model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation = 'relu' , input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation = 'relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3,3), activation = 'relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3,3), activation = 'relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(4, activation='softmax'))
model.summary()

model.compile(loss= 'sparse_categorical_crossentropy', optimizer=optimizers.RMSprop(lr=learning_rate), metrics=['acc'])

#create the augmentation configuration
#prevention for overfitting
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,)
val_datagen = ImageDataGenerator(rescale=1./255)

#create image generators
train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
val_generator = val_datagen.flow(X_val, y_val, batch_size=batch_size)

## The actual training
history = model.fit_generator(train_generator,
                              steps_per_epoch=ntrain // batch_size,
                              epochs=num_epoch,
                              validation_data=val_generator,
                              validation_steps=nval // batch_size)

#Save the model
model.save_weights('model_weights.h5')
model.save('model_keras.h5')

#Check by plotting the training and validation curve
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

#Train and validation accuracy
plt.plot(epochs, acc, 'b', label = 'Training accuracy')
plt.plot(epochs, val_acc, 'r', label = 'Validation accuracy')
plt.title('Training and Validation accuracy')
plt.legend()

plt.figure()
#Train and validation loss
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()

plt.show()

### END OF TRAINING CODE



