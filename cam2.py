# predi puskane otvarqsh control panel i pishesh:
# pip install opencv-python
# pip install Umat
#zaz Umat sigurno shte kaje che lipsva neshto i za vsqko edno posle pishesh
# pip install ...
#... - tova koeto e kazano che lipsva
# moje da probvash dali shte trugna bez Umat i ako trugne moje da ne se svalq
#!!Ako se otvarq s Idle da e otvoren SAMO 1 file shtoto inache dava nqkakva greshka
import cv2

cam=[]
br=int(input("nqnq: "))

def show_webcam(mirror=False):
    #masiv ot prazni prozorci 
    cam.append(cv2.VideoCapture(0))
    
    while True:
        #chete kakvo ima na kamerata i go slaga v promenliva
        #!ako se mahne rval ne raboti! ne znam zashto
        rval, frame = cam[0].read()
        if mirror:
            #obrushta kamerata
            frame = cv2.flip(frame, 1)
        for i in range(br):
            #ot i pravi string
            a=str(i+1)
            #pokazva frame-a
            cv2.imshow('nqnq'+a, frame)

        if cv2.waitKey(10) == 27: #izliza ot cikula pri natiskane na esc
            break
    #zatvarq vsichki prozorci
    cv2.destroyAllWindows()

#vika funkciqta kato kazva che e mirrored ekrana i tq go pravi da ne e mirrored
show_webcam(mirror=True)
