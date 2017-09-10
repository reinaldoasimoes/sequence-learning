- Install required packages  
sudo apt-get update  
sudo apt-get install python-pip python-dev libatlas-base-dev gcc gfortran g++  
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose  
#sudo pip install numpy scipy    
#sudo pip install scikit-learn  

- Install Tensorflow  
sudo pip install tensorflow      # Python 2.7; CPU support (no GPU support)  
or upgrade  
sudo pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.3.0-cp27-none-linux_x86_64.whl  
NOTE: since we use 32-bit system for MuseSDK, check the following link for Tensorflow ion 32-bit system: http://cudamusing.blogspot.com/2015/11/building-tensorflow-for-jetson-tk1.html  


- Install Keras  
sudo pip install keras  
or upgrade  
sudo pip install git+git://github.com/fchollet/keras.git --upgrade

- Install h5py for loading/saving models  
sudo apt-get install libhdf5-dev  
sudo pip install h5py