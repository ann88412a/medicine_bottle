import glob

with open('/home/chengyu/Documents/Dio/medicine_bottle/pill/cyho/train.txt','w') as f:
    for item in glob.glob('/home/chengyu/Documents/Dio/plan_4_data_1213/*.png'):
        f.write('%s\n' % item)