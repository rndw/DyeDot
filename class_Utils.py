import pickle
import hashlib


class Ptools:

    def __init__(self):
        pass

    def head(self, n=10):
        return self[:n]

    def tail(self, n=10):
        return self[len(self) - n - 1:]


class DataUtils:

    def __init__(self):
        pass

    def resumeBck(self, objsToWrite, graphObjs, outDir):
        self.objsToWrite = objsToWrite
        self.graphObjs = graphObjs
        self.outDir = outDir

        if not self.outDir.endswith('/'):
            self.outDir = self.outDir + '/'

        for item in self.objsToWrite.keys():
            # print(idx, item)
            with open(self.outDir + item + '_DDbackup.txt', 'w') as f:
                f.writelines(str(objsToWrite[item]))  # can only write strings, not dictionaries
                #f.writelines('{}:{}\n'.format(k, v) for k, v in self.objsToWrite[item].items())

        with open(self.outDir + 'DDbackup.pickle', 'wb') as file:
            pickle.dump(self.objsToWrite, file)
        with open(self.outDir + 'DDbackup_graphs.pickle', 'wb') as file:
            pickle.dump(self.graphObjs, file)

        md5 = hashlib.md5()
        ## Add md5sum to check pickle file
        ## Not sure how useful this would be
        with open(self.outDir + 'DDbackup.pickle', 'rb') as file:
            data = file.read()  # block size added as 2**20 - remove
            md5.update(data)
            with open(self.outDir + 'pickleMD5.txt', 'w') as md5file:
                md5file.write(str(md5.hexdigest()))
                print(md5.hexdigest())

    def resumeFromBck(self, bckPath):
        self.bckPath = bckPath

        if not self.bckPath.endswith('/'):
            self.bckPath = self.bckPath + '/'
            with open(self.bckPath + 'DDbackup.pickle', 'rb') as resumeFile:
                objsToWrite = pickle.load(resumeFile)
            with open(self.bckPath + 'DDbackup_graphs.pickle', 'rb') as resumeFile:
                graphObjs = pickle.load(resumeFile)
        return objsToWrite, graphObjs
