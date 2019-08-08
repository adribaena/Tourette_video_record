from __future__ import division
import random , csv, funcionesExtras, itertools
from psychopy import visual, gui,core, data,  event, logging, prefs
from psychopy.hardware import joystick
from scipy.spatial import distance
from numpy import angle
import math
import numpy as np
import time
import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os
import utiles_audiovideo as uav
import random




tiempos = [60, 60 , 90 , 90 , 120 , 120]


text_t = 'INTENTA CONTROLAR TODOS LOS TICS'


text_nt = 'PUEDES TENER TICS'


fix_time = 2



# el resto es automatico 


random.shuffle(tiempos)
t1 = np.copy(tiempos)
random.shuffle(tiempos)
t2 = np.copy(tiempos)


cosa = np.array(t1).tolist()
cosa2 = np.array(t2).tolist()



times = []
for i in range(0,len(cosa)):
    times.append(cosa[i])
    times.append(cosa2[i])



print(times)


info = {'info_subject': 'SJ1', 'starts_with':['TICK','NO_TICK']}
dialog = gui.DlgFromDict(dictionary= info, title='select condition to start')


if dialog.OK:
    infoUser = dialog.data
    #Subject's data is saved in infoUser and are ready to print them on each file
else:
    print('user cancelled')
    core.quit()


eleccion = info['starts_with']

if eleccion == 'TICK' : 
    lista = ['C','NC']*len(tiempos)
else :
    lista = ['NC','C']*len(tiempos)


print(lista)


mywin = visual.Window([1366,768], fullscr = True, monitor='testMonitor', color='black',units='deg', allowGUI = False)
respClock = core.Clock()


fixation = visual.ShapeStim(mywin, 
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor="white"
)



respClock = core.Clock()



while respClock.getTime() < fix_time:
    fixation.draw()
    mywin.flip()




continuar = 0
for index in range(len(lista)):
    
    stim = lista[index]
    if stim == 'C' : 
        text = text_t
    else : 
        text = text_nt
    
    stimP = visual.TextStim(mywin, text)
    respClock_d = core.Clock()
    time_d = times[index]
    
    print('the stim is :', stim)
    print('the stim has :', str(time_d),' seconds')
    
    name_file =  'video_' + info['info_subject'] +'_trial_' + str(index + 1) + '_cond_' +   stim +  '_time_' + str(time_d)
    
    
    print(name_file)
    
    uav.file_manager(name_file)
    
    uav.start_AVrecording(name_file)

    while respClock_d.getTime() < time_d: 
        stimP.draw()
        mywin.flip()
    time.sleep(.5)
    uav.stop_AVrecording(name_file)
    time.sleep(.5)
    
    while continuar == 0:
        text_p = 'Paused,  press  space  to  Continue'
        stimP = visual.TextStim(mywin, text_p)
        stimP.draw()
        mywin.flip()
        if 'space' in event.getKeys():
            continuar = 1
            event.clearEvents()
    continuar = 0
