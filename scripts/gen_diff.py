#GENERATE SPECIMEN DIFFERENTIAL CLASS

class specimen_differential():
    def __init__ (self):
        self.e = 0
        self.l = 0
        self.m = 0
        self.n = 0
        self.total = 0

    def generate_results(self, predicted_labels):

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


        print("\n--------------------------", "\nWBC DIFERRENTIAL RESULTS","\n--------------------------")
        print("\n------------","\nWBC COUNT:","\n------------", "\nEosinophils:", self.e ,"\nLymphocytes:", self.l ,"\nMonocytes:", self.m,"\nNeutrophils:", self.n)
        print("\n------------","\nWBC PERCENT %:","\n------------","\nEosinophils:", self.e/self.total*100 ,"%\nLymphocytes:", self.l/self.total*100 ,"%\nMonocytes:", self.m/self.total*100,"%\nNeutrophils:", self.n/self.total*100, "%")

        return [self.e, self.l, self.m, self.n]

#END OF SPECIMEN DIFFERENTIAL CLASS
