import serial
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    
    mlx_shape = (12,16)
    
    plt.ion()
    fig,ax = plt.subplots(figsize=(8,5))
    therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
    cbar = fig.colorbar(therm1) # setup colorbar for temps
    cbar.set_label('Temperature [$^{\circ}$C]',fontsize=10) # colorbar label
    
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush() 
    #ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if len(line) >200:
                df = np.fromstring(line, dtype = float, sep=',')
                if df.shape ==(192,):
                    for obj in ax.findobj(match = type(plt.Circle(1,1))):
                        obj.remove() #clear circle
                    
                    data_array = np.reshape(df, mlx_shape)
                    res = np.where(data_array == np.min(data_array))
                    
                    min_idx = list(zip(res[1],res[0]))[0]
                    
                    circ = plt.Circle((15-min_idx[0],min_idx[1]), 1, color ='r', fill = False)
                    ax.add_patch(circ)
                    
                    
                    therm1.set_data(np.fliplr(data_array)) # flip left to right
                    therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
                    cbar.on_mappable_changed(therm1) # update colorbar range
                    plt.pause(0.001) # required

