import glob

with open('jetson_train.txt','w') as f:
    for item in glob.glob('/home/medical/pill_data/all/*.png'):
        f.write('%s\n' % item)