#Importing the MNIST Dataset
from keras.datasets import mnist
#Importing the Packages
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
#Loading the Dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()
#Reshaping the Input for the CNN
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train/=255
X_test/=255
number_of_classes = 10
Y_train = np_utils.to_categorical(y_train, number_of_classes)
Y_test = np_utils.to_categorical(y_test, number_of_classes)
#Creating the CNN !
model = Sequential()
#Convolution
model.add(Conv2D(32, (3, 3), input_shape=(28,28,1)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
#Pooling
model.add(MaxPooling2D(pool_size=(2,2)))
#Convolution
model.add(Conv2D(64,(3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
#Pooling
model.add(MaxPooling2D(pool_size=(2,2)))
#Flattening
model.add(Flatten())
# Adding the Fully connected layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(Activation('softmax'))
#Compiling the CNN
model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
#Data Augmentation
gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3,
                         height_shift_range=0.08, zoom_range=0.08)
test_gen = ImageDataGenerator()
#Creating Batches
train_generator = gen.flow(X_train, Y_train, batch_size=64)
test_generator = test_gen.flow(X_test, Y_test, batch_size=64)
#Training the Data
model.fit_generator(train_generator, steps_per_epoch=60000//64, epochs=2, 
                    validation_data=test_generator, validation_steps=10000//64)
score = model.evaluate(X_test, Y_test)
#Printing the Accuraccy of the CNN
print()
print('Test accuracy: ', score[1])