import glob

with open('train.txt','w') as f:
    for item in glob.glob('/home/fritingo/Documents/pill_data/all/*.png'):
        f.write('%s\n' % item)