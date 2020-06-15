def CountingMinutesI(str): 
    l=str.split('-')
    
    l1=l[0].split(':')
    l2=l[1].split(':')
    
    if 'am' in l1[1]:
        l1[1]= l1[1].replace('am','')
        l1[0]= int(l1[0])
    elif 'pm' in l1[1]:
        l1[1]= l1[1].replace('pm','')
        l1[0]= int(l1[0])+12
    l1[1] = int(l1[1])
    
    if 'am' in l2[1]:
        l2[1]= l2[1].replace('am','')
        l2[0]= int(l2[0])
    elif 'pm' in l2[1]:
        l2[1]= l2[1].replace('pm','')
        l2[0]= int(l2[0])+12 
    l2[1] = int(l2[1])
    
    hour = l2[0] - l1[0]
    minute = l2[1] - l1[1]
    if hour < 0: hour +=24
    if minute < 0: minute +=60
    
    return hour*60 + minute
    
# keep this function call here  
print CountingMinutesI(raw_input())



12:30pm-12:00am