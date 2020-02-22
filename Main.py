import csv
import numpy as np
import os


####### INPUT ########
first_name = input("Enter First Name:")
last_name = input("Enter Last Name:")
date_of_birth = input("Enter Date of Birth (MM-DD-YYYY):")
social_security = input("Enter Social Security Number (XXX-XX-XXXX):")
print("Running WBC Differential...")

#give specimen info and unique id
from datetime import datetime
from uuid import uuid4
uniqueid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
accession = uniqueid
specimen_type = "Blood Smear"
delta = np.timedelta64(5,'h') #EST(eastern) is -5 of UCT(universal)
todays_datetime = np.datetime64('now') - delta# timestamp right now
specinfo = [accession, todays_datetime, specimen_type,  first_name, last_name, date_of_birth, social_security]
specimen_images = [] #location of image to have a diff performed

#give specimen image location
test_dir = os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/sample_specimen")
test_imgs = [os.path.expanduser("~/Desktop/WBC_Recognition_DEMO/sample_specimen/{}").format(i) for i in os.listdir(test_dir)]
numpred = 100 # number to predivt or output in the screen has to be divisible by 10




####### PREDICT RESULTS, SAVE IN DATABASE,  AND RUN APPLICATION ########
#PREDICT GIVEN IMAGES
from BloodCellRecognitionClassify import patient_WBC_images
patientWBCimages1 = patient_WBC_images(specinfo, test_imgs)
specimen_info, specimen_fig, specimen_prediction  = patientWBCimages1.predict_images(numpred)


#GENERATE SPECIMEN DIFFERENTIAL CLASS (the count for the WBC Differential)
from Generate_Diff import specimen_differential
specimen1 = specimen_differential()
diff_results = specimen1.generate_results(specimen_prediction)



#SAVE THE RECORD (RESULTS AND IMAGES) ON A DATABASE
header = ["Accession ID","Accession Date/Time","Specimen Type","First Name","Last Name","Date of Birth (MM-DD-YYYY)","Social Security Number","Eosinophils%","Lymphocytes%","Monocytes%","Neutrophils%"]
row_results = specinfo + diff_results
filename = "records/diff_records.csv"
#save results
try:
    f = open(filename)
    with open(filename, 'a', newline='') as myfile:  # a means append, it will create a new file if it doesnt exist
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(row_results)
        print("\nPatient File Saved")
except IOError:
    with open(filename, 'a', newline='') as myfile:  # a means append, it will create a new file if it doesnt exist
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        wr.writerow(row_results)
        print("\nPatient File Saved")
#save the images based on unique id (accesson)
specimen_fig.savefig("records/images/"+str(accession))






#RUN THE APPLICATION FOR VIEWING
## Call class for another WBC_GUI file (Will view everything)
#includes images with subplots
#includes generated wbc differetial results
from WBC_GUI import ScrollableWindow
#fig.savefig('test.png')#save the result into a picture
ScrollableWindow(specimen_info, specimen_fig, diff_results)#show info,predictions of image subplots (fig), and numeric diff results on window


