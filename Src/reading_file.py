tmpFile = open('writing.txt','a')
for item in range(10):
    tmpFile.write('{0}\n'.format(item))
tmpFile.close()