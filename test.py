import os
import glob
import argparse
import matplotlib
import pandas as pd 
import numpy as np
# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from tensorflow.keras.layers import Layer, InputSpec
from utils import predict, load_images, display_images
from matplotlib import pyplot as plt

# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='nyu.h5', type=str, help='Trained Keras model file.')
parser.add_argument('--input', default='examples/*.png', type=str, help='Input filename or folder.')
args = parser.parse_args()

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

print('Loading model...')

# Load model into GPU / CPU
model = load_model(args.model, custom_objects=custom_objects, compile=False)

print('\nModel loaded ({0}).'.format(args.model))

# Input images
inputs = load_images( glob.glob(args.input) )
print('\nLoaded ({0}) images of size {1}.'.format(inputs.shape[0], inputs.shape[1:]))

# Compute results
outputs = predict(model, inputs)
dout = pd.DataFrame(np.squeeze(outputs[0]))

dout.to_excel("depth_info.xlsx")
plt.imshow(outputs[0], cmap='gray')
plt.savefig('out.png')
  


#matplotlib problem on ubuntu terminal fix
#matplotlib.use('TkAgg')   

# Display results
out_img,in_img = display_images(outputs.copy(),inputs.copy())
#plt.figure(figsize=(10,5))
plt.axis('off')
plt.imshow(out_img[0])
plt.savefig('test.png',bbox_inches='tight', pad_inches=0)
#plt.show()

#plt.figure(figsize=(10,5))
plt.axis('off')
plt.imshow(in_img[0])
plt.savefig('test_org.png',bbox_inches='tight', pad_inches=0)
plt.show()