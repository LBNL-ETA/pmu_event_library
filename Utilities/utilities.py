import os
import sys
import random
import matplotlib.pyplot as plt
import pandas as pd

def print_library_contents(path):
    """
    Prints out information relating to event library structure and provides a sample event to display contents.
    
    Prints the number of events in the library, and divides events by PV generation, printing how many events fall into each catagory.
    Then, for each catagory, prints the timestamps of all events which are contained within that category. A random event folder is 
    selected, and a random PMU is sampled from that event. All data streams collected by that PMU are printed out, and a sample
    plot of the event is displayed.
    
    Args:
    
        path: a string relating the path to the 'Event_Library' directory. Should not need to be altered.
        
    Generates:
    
        A print-out of event library contents.
    """
    
    classifications = os.listdir(path)
    
    structure = {}
    
    for classification in classifications:
        structure[classification]={}
        structure[classification]['path']=path+'/'+classification
        structure[classification]['event_count'] = len(os.listdir(structure[classification]['path']))
        structure[classification]['labels']=os.listdir(structure[classification]['path'])
        structure[classification]['labels'].sort()
        
    print 'Total events in the library: ', (structure[classifications[0]]['event_count']+structure[classifications[1]]['event_count'])
    print 'Total number of events occurring during PV Generation: ', structure['PV']['event_count']
    print 'Total number of events occurring without PV Generation: ', structure['No_PV']['event_count']
    print ' '
    print 'PV Event Timestamps: '
    for item in structure['PV']['labels']:
        print str(item[5:7])+'/'+str(item[8:10])+'/'+str(item[0:4])+' '+str(item[11:13])+':'+str(item[13:15])+':'+str(item[15:18])
    print ' '
    print 'No PV Event Timestamps: '
    for item in structure['No_PV']['labels']:
        print str(item[5:7])+'/'+str(item[8:10])+'/'+str(item[0:4])+' '+str(item[11:13])+':'+str(item[13:15])+':'+str(item[15:18])
    
    random_directory = random.randint(0,len(classifications)-1)
    random_event=random.randint(0,len(structure[classifications[random_directory]]['labels'])-1)
    item = structure[classifications[random_directory]]['labels'][random_event]
    print ' ' 
    print 'Randomly Selected Event: ', classifications[random_directory], str(item[5:7])+'/'+str(item[8:10])+'/'+str(item[0:4])+' '+str(item[11:13])+':'+str(item[13:15])+':'+str(item[15:18])
    
    path = structure[classifications[random_directory]]['path']+'/'+structure[classifications[random_directory]]['labels'][random_event]
    
    locs = []
    
    if 'B90_raw_data.csv' in os.listdir(path):
        locs.append('B90')
    if 'FG_raw_data.csv' in os.listdir(path):
        locs.append('FG')
    if 'FL_raw_data.csv' in os.listdir(path):
        locs.append('FL')
        
    random_loc = random.randint(0,len(locs)-1)
    
    if locs[random_loc] == 'B90':
        loc_title = 'Building 90'
    if locs[random_loc] == 'FG':
        loc_title = 'FLEXGRID PV Array'
    if locs[random_loc] == 'FL':
        loc_title = 'FLEXLAB'
        
    print 'Randomly Selected PMU: ', loc_title
    print ' '
    
        
    voltage_data = pd.read_csv(path+'/'+locs[random_loc]+'_raw_data.csv')
    
    print 'Raw event data contains measurements of: '
    for key in voltage_data:
        if key != 'Unnamed: 0':
            print key
        
    index = range(len(voltage_data['L1-Mag [Vrms]']))
    for i in index:
        index[i]=i/120.
    
    plt.plot(index,voltage_data['L1-Mag [Vrms]'])
    plt.plot(index,voltage_data['L2-Mag [Vrms]'])
    plt.plot(index,voltage_data['L3-Mag [Vrms]'])
    plt.title('Event Voltage Evolution at '+loc_title)
    plt.xlabel('Time [s]')
    plt.ylabel('Volt [Vrms]')
    plt.legend(['Phase 1','Phase 2','Phase 3'], loc=4)

    return