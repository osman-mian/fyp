import cv2
import svmutil as svm
import numpy as np
import slidingWindow as sw

class DoorDetector:
    def __init__ (self,modelName):
        self.hog = cv2.HOGDescriptor()
        self.windowModel = svm.svm_load_model(modelName)
        
    def detectDoor(self, img, horOffset, verOffset):
        #print len(img.shape)
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Window = sw.SlidingWindow(64,128,img,horOffset,verOffset,20,20)
        horWin, verWin = Window.getWindows()
        windows = horWin*verWin
        #print "windows %d " % windows
        #print "windows %d " % horWin
        #print "windows %d " % verWin 
        features = np.zeros((windows,3780),dtype = np.float)
        ones = np.ones((windows,1),dtype = np.float)
        labels = ones.ravel()
        for i in range(0,windows):
            #print i
            imag = Window.getNextFrame()
	    imag = cv2.resize(imag,(64,128))
            #cv2.imshow("Hello",imag)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            feature = self.hog.compute(imag)
            feature = np.transpose(feature);
            features[i] = feature
        labelsList = labels.tolist()
        featuresList = features.tolist()
        p_label, p_acc, p_val = svm.svm_predict(labelsList, featuresList, self.windowModel)
        return (p_label,p_acc,p_val)
        
        
'''        
        while imag != None:
            imag = Window.getNextFrame()
            if(imag != None):
                feature = hog.compute(imag)
'''        
                   
        
