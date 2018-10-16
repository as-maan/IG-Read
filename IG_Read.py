# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:54:19 2018

@author: amaan
"""
import IG_Functions
import time as samay
import csv
dt = 5 

# Get Date
date = IG_Functions.get_date()
date = date['date']
#print(date)

# Get Time

time = IG_Functions.get_time()
sec = time['sec']
time = time['time']
#print(time)

# Write Log File Header
header = zip(['Log started at - '],[time])
t = 0
start = 0
end = 0

with open('/media/amaan/Storage/Work/PPPL/Analysis/SEP/IG_Logs/'+date+'Timed_Activation.2DAT','w') as op:
    writer = csv.writer(op,delimiter='\t')
    writer.writerows(header)
    
    while True:

        val = IG_Functions.serial_read()
        val = val['val']
        
        # Write data to file
        
#        print t, val
        dat = zip([t],[val])
        writer.writerows(dat)
        op.flush()

# Check elapsed time since last data send
        if (end-start) < 3600:
            end = samay.time()
        elif (end-start) >= 3600:
            start = samay.time()
            end = samay.time()
            file_path="/media/amaan/Storage/Work/PPPL/Analysis/SEP/Baked_Timed_Activation_2.eps"
            IG_Functions.send_email("maan.anurag@gmail.com", file_path, "amaan@pppl.gov", "SEP pressure profile update", ('Last updated at '+IG_Functions.get_time()['time']+' on '+IG_Functions.get_date()['date']))
        
        if val < 1e-5:
            file_path="/media/amaan/Storage/Work/PPPL/Analysis/SEP/Baked_Timed_Activation_2.eps"
            IG_Functions.send_email("maan.anurag@gmail.com", file_path, "amaan@pppl.gov", "SEP pressure profile update - Over Pressure warning", ('Last updated at '+IG_Functions.get_time()['time']+' on '+IG_Functions.get_date()['date']))
                        
        # Wait for dt
        samay.sleep(dt)
        t = t + dt
        
    

# initialize time



# Initiate reading data every dt
