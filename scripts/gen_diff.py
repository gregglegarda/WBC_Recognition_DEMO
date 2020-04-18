#GENERATE SPECIMEN DIFFERENTIAL CLASS
import numpy as np

class specimen_differential():
    def __init__ (self):
        self.e = 0
        self.l = 0
        self.m = 0
        self.n = 0
        self.total = 0

        self.eflag = 0
        self.lflag = 0
        self.mflag = 0
        self.nflag = 0
        self.totalflag = 0

        self.normality = 'NORMAL'

    def generate_results(self, predicted_labels):

        # normal ranges of wbc
        ep_ref_range_H = 10
        ep_ref_range_L = 0
        lp_ref_range_H = 50
        lp_ref_range_L = 40
        mp_ref_range_H = 20
        mp_ref_range_L = 10
        np_ref_range_H = 35
        np_ref_range_L = 25

        for i in range(len(predicted_labels)):
            if predicted_labels [i] == 0:
                self.e+=1
            elif predicted_labels [i] == 1:
                self.l+=1
            elif predicted_labels [i] == 2:
                self.m+=1
            elif predicted_labels [i] == 3:
                self.n+=1
        self.total = self.e + self.l + self.m + self.n



        # normal or out of range
        if float(self.n) > np_ref_range_H or float(self.n) < np_ref_range_L:
            if float(self.n) > np_ref_range_H:
                self.normality = 'OUT OF RANGE'
            else:
                self.normality = 'OUT OF RANGE'

        if float(self.l) > lp_ref_range_H or float(self.l) < lp_ref_range_L:
            if float(self.l) > lp_ref_range_H:
                self.normality = 'OUT OF RANGE'
            else:
                self.normality = 'OUT OF RANGE'

        if float(self.m) > mp_ref_range_H or float(self.m) < mp_ref_range_L:
            if float(self.m) > mp_ref_range_H:
                self.normality = 'OUT OF RANGE'
            else:
                self.normality = 'OUT OF RANGE'

        if float(self.e) > ep_ref_range_H or float(self.e) < ep_ref_range_L:
            if float(self.e) > ep_ref_range_H:
                self.normality = 'OUT OF RANGE'
            else:
                self.normality = 'OUT OF RANGE'



        print("\n--------------------------", "\nWBC DIFERRENTIAL RESULTS","\n--------------------------")
        print("\n------------","\nWBC COUNT:","\n------------", "\nEosinophils:", self.e ,"\nLymphocytes:", self.l ,"\nMonocytes:", self.m,"\nNeutrophils:", self.n)
        print("\n------------","\nWBC PERCENT %:","\n------------","\nEosinophils:", self.e/self.total*100 ,"%\nLymphocytes:", self.l/self.total*100 ,"%\nMonocytes:", self.m/self.total*100,"%\nNeutrophils:", self.n/self.total*100, "%")

        if self.normality == 'NORMAL':
            final_result = 'NORMAL'
            return [self.e, self.l, self.m, self.n, self.normality, final_result], self.normality
        else:
            return [self.e, self.l, self.m, self.n, self.normality], self.normality

#END OF SPECIMEN DIFFERENTIAL CLASS
