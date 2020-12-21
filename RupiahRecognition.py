import cv2
import numpy as np
import sys
from pydub import AudioSegment
from pydub.playback import play
from tkinter import *
import tkinter.messagebox
from forex_python.converter import CurrencyRates
# --------------------------------------------------------------------------------------------------------
MIN_POINT = 35  
tk = Tk()
tk.title('Rupiah Detection')
tk.resizable(width=False, height=False)
tk.configure(background="gray")

class uang:
    def __init__(c):
        def StartButton():
            def feature():
                detector = cv2.xfeatures2d.SIFT_create() 
                matcher = cv2.BFMatcher(cv2.NORM_L1) 
                return detector, matcher

            def play_Sound(cash):
                if cash == 'Rp1000':
                    sound = AudioSegment.from_wav("SRC/Sound/1000.wav")
                    play(sound)
                elif cash == 'Rp2000':
                    sound = AudioSegment.from_wav("SRC/Sound/2000.wav")
                    play(sound)
                elif cash == 'Rp5000':
                    sound = AudioSegment.from_wav("SRC/Sound/5000.wav")
                    play(sound)
                elif cash == 'Rp10000':
                    sound = AudioSegment.from_wav("SRC/Sound/10000.wav")
                    play(sound)
                elif cash == 'Rp20000':
                    sound = AudioSegment.from_wav("SRC/Sound/20000.wav")
                    play(sound)
                elif cash == 'Rp50000':
                    sound = AudioSegment.from_wav("SRC/Sound/50000.wav")
                    play(sound)
                elif cash == 'Rp100000':
                    sound = AudioSegment.from_wav("SRC/Sound/100000.wav")
                    play(sound)
                return sound
                    

            def filter_matches(kp1, kp2, matches, ratio=0.75):  
                mkp1, mkp2 = [], []
                for m,n in matches:
                    if m.distance < n.distance * ratio:
                        good_point = m #jika m=m[1] maka bentuk kotak hijaunya tidak karuan
                        mkp1.append(kp1[good_point.queryIdx])
                        mkp2.append(kp2[good_point.trainIdx])
                p1 = np.float32([kp.pt for kp in mkp1])
                p2 = np.float32([kp.pt for kp in mkp2])
                kp_pairs = zip(mkp1, mkp2)
                return p1, p2, kp_pairs


            def explore_match(win, img1, img2, kp_pairs, status=None, H=None):
                vis = np.zeros((630, 940), np.uint8)
                vis[h1:480, :w1] = img3
                vis[:h1, :w1] = img1
                vis[:h2, w1:w1 + w2] = img2
                vis[480:630, :940] = img4
                vis[480:630, :940] = img5

                
                vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
                if H is not None:
                    corner = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
                    corner = np.int32(cv2.perspectiveTransform(corner.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0))
                    cv2.polylines(vis, [corner], True, (0, 255, 0))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(vis, showText, (corner[0][0], corner[0][1]), font, 1, (0, 0, 255), 2)
                    cv2.putText(vis, showDollar + 'USD', (corner[1][0], corner[0][1]), font, 1, (0, 255, 255), 2)
                #if status is None:
                    #status = np.ones(len(kp_pairs), np.bool_)
                return vis

            def text():
                cv2.putText(img2, 'Press b For Back', (10,470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.putText(img2, 'Press p for pause/unpause', (320,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(img4, 'Information about the Indonesian currency will appear here', (25,75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)
                cv2.putText(img3, 'USD 1    = IDR '+US1,(5,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)
                cv2.putText(img3, 'USD 5    = IDR '+US5,(5,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)
                cv2.putText(img3, 'USD 20   = IDR '+US20,(5,180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)
                cv2.putText(img3, 'USD 50   = IDR '+US50,(5,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)
                cv2.putText(img3, 'USD 100  = IDR '+US100,(5,260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)




            def match_and_draw(win, checksound, found, count):
                text()
                if (len(kp2) > 0):
                    raw_matches = matcher.knnMatch(desc1, desc2, k=2) 
                    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches)
                    if len(p1) >= MIN_POINT:
                        #match ketemu
                        if not found:
                            checksound = True    
                        found = True
                        count = count + 1
                        H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
                        #print(status)
                        vis = explore_match(win, img1, img2, kp_pairs, status,H)
                    else:
                        #belum ketemu match
                        found = False
                        checksound = False
                        H, status = None, None
                        count = 0
                        vis = np.zeros((630, 940), np.uint8)
                        vis[:h1, :w1] = img1
                        vis[:h2, w1:w1 + w2] = img2
                        vis[480:630, :940] = img4
                        vis[h1:480, :w1] = img3
                           
                    cv2.imshow('Rupiah Detection', vis)
                    if (count > 3):
                        checksound = False
                        play_Sound(showText)
                        cv2.waitKey(-1)
                        count = 0

                return found, checksound, count


            # --------------------------------------------------------------------------------------------------------
            cv2.useOptimized()
            cap = cv2.VideoCapture(0)
            detector, matcher = feature()
            k = CurrencyRates()


            checksound = True
            found = False
            searchIndex = 1
            count = 0

            #Preload Data sebelum masuk ke kamera 
            img_source1 = cv2.imread('SRC/1rbF.bmp', 0)
            img_info1 = cv2.imread('SRC/CashInfo/1rbFinfo.bmp', 0)
            Exc1 = "{:.2f}".format(k.convert('IDR','USD',1000))
            temp_kp1, temp_desc1 = detector.detectAndCompute(img_source1, None)

            img_source2 = cv2.imread('SRC/1rbF2.bmp', 0)
            img_info2 = cv2.imread('SRC/CashInfo/1rbF2info.bmp', 0)
            temp_kp2, temp_desc2 = detector.detectAndCompute(img_source2, None)

            img_source3 = cv2.imread('SRC/1rbB2.bmp', 0)
            img_info3 = cv2.imread('SRC/CashInfo/1rbB2info.bmp', 0)
            temp_kp3, temp_desc3 = detector.detectAndCompute(img_source3, None)

            img_source4 = cv2.imread('SRC/2rbF.bmp', 0)
            img_info4 = cv2.imread('SRC/CashInfo/2rbFinfo.bmp', 0)
            Exc2 = "{:.2f}".format(k.convert('IDR','USD',2000))
            temp_kp4, temp_desc4 = detector.detectAndCompute(img_source4, None)

            img_source5 = cv2.imread('SRC/2rbF2.bmp', 0)
            img_info5 = cv2.imread('SRC/CashInfo/2rbF2info.bmp', 0)
            temp_kp5, temp_desc5 = detector.detectAndCompute(img_source5, None)

            img_source6 = cv2.imread('SRC/2rbB2.bmp', 0)
            img_info6 = cv2.imread('SRC/CashInfo/2rbB2info.bmp', 0)
            temp_kp6, temp_desc6 = detector.detectAndCompute(img_source6, None)

            img_source7 = cv2.imread('SRC/5rbF.bmp', 0)
            Exc5 = "{:.2f}".format(k.convert('IDR','USD',5000))
            img_info7 = cv2.imread('SRC/CashInfo/5rbFinfo.bmp', 0)
            temp_kp7, temp_desc7 = detector.detectAndCompute(img_source7, None)

            img_source8 = cv2.imread('SRC/5rbF2.bmp', 0)
            img_info8 = cv2.imread('SRC/CashInfo/5rbF2info.bmp', 0)
            temp_kp8, temp_desc8 = detector.detectAndCompute(img_source8, None)

            img_source9 = cv2.imread('SRC/5rbB2.bmp', 0)
            img_info9 = cv2.imread('SRC/CashInfo/5rbB2info.bmp', 0)
            temp_kp9, temp_desc9 = detector.detectAndCompute(img_source9, None)

            img_source10 = cv2.imread('SRC/10rbF.bmp', 0)
            Exc10 = "{:.2f}".format(k.convert('IDR','USD',10000))
            img_info10 = cv2.imread('SRC/CashInfo/10rbFinfo.bmp', 0)
            temp_kp10, temp_desc10 = detector.detectAndCompute(img_source10, None)

            img_source11 = cv2.imread('SRC/10rbB.bmp', 0)
            img_info11 = cv2.imread('SRC/CashInfo/10rbBinfo.bmp', 0)
            temp_kp11, temp_desc11 = detector.detectAndCompute(img_source11, None)

            img_source12 = cv2.imread('SRC/10rbF2.bmp', 0)
            img_info12 = cv2.imread('SRC/CashInfo/10rbF2info.bmp', 0)
            temp_kp12, temp_desc12 = detector.detectAndCompute(img_source12, None)

            img_source13 = cv2.imread('SRC/20rbF.bmp', 0)
            Exc20 = "{:.2f}".format(k.convert('IDR','USD',20000))
            img_info13 = cv2.imread('SRC/CashInfo/20rbFinfo.bmp', 0)
            temp_kp13, temp_desc13 = detector.detectAndCompute(img_source13, None)

            img_source14 = cv2.imread('SRC/20rbB.bmp', 0)
            img_info14 = cv2.imread('SRC/CashInfo/20rbBinfo.bmp', 0)
            temp_kp14, temp_desc14 = detector.detectAndCompute(img_source14, None)

            img_source15 = cv2.imread('SRC/20rbF2.bmp', 0)
            img_info15 = cv2.imread('SRC/CashInfo/20rbF2info.bmp', 0)
            temp_kp15, temp_desc15 = detector.detectAndCompute(img_source15, None)

            img_source16 = cv2.imread('SRC/20rbB2.bmp', 0)
            img_info16 = cv2.imread('SRC/CashInfo/20rbB2info.bmp', 0)
            temp_kp16, temp_desc16 = detector.detectAndCompute(img_source16, None)

            img_source17 = cv2.imread('SRC/50rbF.bmp', 0)
            Exc50 = "{:.2f}".format(k.convert('IDR','USD',50000))
            img_info17 = cv2.imread('SRC/CashInfo/50rbFinfo.bmp', 0)
            temp_kp17, temp_desc17 = detector.detectAndCompute(img_source17, None)

            img_source18 = cv2.imread('SRC/50rbF2.bmp', 0)
            img_info18 = cv2.imread('SRC/CashInfo/50rbF2info.bmp', 0)
            temp_kp18, temp_desc18 = detector.detectAndCompute(img_source18, None)

            img_source19 = cv2.imread('SRC/50rbB2.bmp', 0)
            img_info19 = cv2.imread('SRC/CashInfo/50rbB2info.bmp', 0)
            temp_kp19, temp_desc19 = detector.detectAndCompute(img_source19, None)

            img_source20 = cv2.imread('SRC/100RbF.bmp', 0)
            Exc100 = "{:.2f}".format(k.convert('IDR','USD',100000))
            img_info20 = cv2.imread('SRC/CashInfo/100rbinfo.bmp', 0)
            temp_kp20, temp_desc20 = detector.detectAndCompute(img_source20, None)

            img_source21 = cv2.imread('SRC/100RbB.bmp', 0)
            img_info21 = cv2.imread('SRC/CashInfo/100rbBinfo.bmp', 0)
            temp_kp21, temp_desc21 = detector.detectAndCompute(img_source21, None)

            img_source22 = cv2.imread('SRC/100RbF2.bmp', 0)
            img_info22 = cv2.imread('SRC/CashInfo/100rbinfo.bmp', 0)
            temp_kp22, temp_desc22 = detector.detectAndCompute(img_source22, None)

            img_source23 = cv2.imread('SRC/100rbB2.bmp', 0)
            img_info23 = cv2.imread('SRC/CashInfo/100rbB2info.bmp', 0)
            temp_kp23, temp_desc23 = detector.detectAndCompute(img_source23, None)

            US1   = str(int(k.convert('USD','IDR',1)))
            US5   = str(int(k.convert('USD','IDR',5)))
            US20  = str(int(k.convert('USD','IDR',20)))
            US50  = str(int(k.convert('USD','IDR',50)))
            US100 = str(int(k.convert('USD','IDR',100)))



            while (True):
                # switch template
                if not found:
                    if searchIndex <= 23:
                        if searchIndex == 1:
                            img1 = img_source1
                            kp1 = temp_kp1
                            desc1 = temp_desc1
                            showText = 'Rp1000'
                            showDollar = Exc1
                            img5 = img_info1
                        elif searchIndex == 2:
                            img1 = img_source2
                            kp1 = temp_kp2
                            desc1 = temp_desc2
                            showText = 'Rp1000'
                            showDollar = Exc2
                            img5 = img_info2
                        elif searchIndex == 3:
                            img1 = img_source3
                            kp1 = temp_kp3
                            desc1 = temp_desc3
                            showText = 'Rp1000'
                            showDollar = Exc2
                            img5 = img_info3
                        elif searchIndex == 4:
                            img1 = img_source4
                            kp1 = temp_kp4
                            desc1 = temp_desc4
                            showText = 'Rp2000'
                            showDollar = Exc2
                            img5 = img_info4
                        elif searchIndex == 5:
                            img1 = img_source5
                            kp1 = temp_kp5
                            desc1 = temp_desc5
                            showText = 'Rp2000'
                            showDollar = Exc2
                            img5 = img_info5
                        elif searchIndex == 6:
                            img1 = img_source6
                            kp1 = temp_kp6
                            desc1 = temp_desc6
                            showText = 'Rp2000'
                            showDollar = Exc2
                            img5 = img_info6
                        elif searchIndex == 7:
                            img1 = img_source7
                            kp1 = temp_kp7
                            desc1 = temp_desc7
                            showText = 'Rp5000'
                            showDollar = Exc5
                            img5 = img_info7
                        elif searchIndex == 8:
                            img1 = img_source8
                            kp1 = temp_kp8
                            desc1 = temp_desc8
                            showText = 'Rp5000'
                            showDollar = Exc5
                            img5 = img_info8
                        elif searchIndex == 9:
                            img1 = img_source9
                            kp1 = temp_kp9
                            desc1 = temp_desc9
                            showText = 'Rp5000'
                            showDollar = Exc5
                            img5 = img_info9
                        elif searchIndex == 10:
                            img1 = img_source10
                            kp1 = temp_kp10
                            desc1 = temp_desc10
                            showText = 'Rp10000'
                            showDollar = Exc10
                            img5 = img_info10
                        elif searchIndex == 11:
                            img1 = img_source11
                            kp1 = temp_kp11
                            desc1 = temp_desc11
                            showText = 'Rp10000'
                            showDollar = Exc10
                            img5 = img_info11
                        elif searchIndex == 12:
                            img1 = img_source12
                            kp1 = temp_kp12
                            desc1 = temp_desc12
                            showText = 'Rp10000'
                            showDollar = Exc10
                            img5 = img_info12
                        elif searchIndex == 13:
                            img1 = img_source13
                            kp1 = temp_kp13
                            desc1 = temp_desc13
                            showText = 'Rp20000'
                            showDollar = Exc50
                            img5 = img_info13
                        elif searchIndex == 14:
                            img1 = img_source14
                            kp1 = temp_kp14
                            desc1 = temp_desc14
                            showText = 'Rp20000'
                            showDollar = Exc50
                            img5 = img_info14
                        elif searchIndex == 15:
                            img1 = img_source15
                            kp1 = temp_kp15
                            desc1 = temp_desc15
                            showText = 'Rp20000'
                            showDollar = Exc50
                            img5 = img_info15
                        elif searchIndex == 16:
                            img1 = img_source16
                            kp1 = temp_kp16
                            desc1 = temp_desc16
                            showText = 'Rp20000'
                            showDollar = Exc50
                            img5 = img_info16
                        elif searchIndex == 17:
                            img1 = img_source17
                            kp1 = temp_kp17
                            desc1 = temp_desc17
                            showText = 'Rp50000'
                            showDollar = Exc50
                            img5 = img_info17
                        elif searchIndex == 18:
                            img1 = img_source18
                            kp1 = temp_kp18
                            desc1 = temp_desc18
                            showText = 'Rp50000'
                            showDollar = Exc50
                            img5 = img_info18
                        elif searchIndex == 19:
                            img1 = img_source19
                            kp1 = temp_kp19
                            desc1 = temp_desc19
                            showText = 'Rp50000'
                            showDollar = Exc50
                            img5 = img_info19
                        elif searchIndex == 20:
                            img1 = img_source20
                            kp1 = temp_kp20
                            desc1 = temp_desc20
                            showText = 'Rp100000'
                            showDollar = Exc100
                            img5 = img_info20
                        elif searchIndex == 21:
                            img1 = img_source21
                            kp1 = temp_kp21
                            desc1 = temp_desc21
                            showText = 'Rp100000'
                            showDollar = Exc100
                            img5 = img_info21
                        elif searchIndex == 22:
                            img1 = img_source22
                            kp1 = temp_kp22
                            desc1 = temp_desc22
                            showText = 'Rp100000'
                            showDollar = Exc100
                            img5 = img_info22
                        elif searchIndex == 23:
                            img1 = img_source23
                            kp1 = temp_kp23
                            desc1 = temp_desc23
                            showText = 'Rp100000'
                            showDollar = Exc100
                            img5 = img_info23

                        searchIndex = searchIndex + 1
                    else:
                        searchIndex = 1
                        img1 = img_source1
                        img5 = img_info1

                # Capture frame-by-frame
                ret, frame = cap.read()
                #tk.withdraw()
                
                img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                img3 = cv2.imread('SRC/CashInfo/img3.jpg', 0)
                img4 = np.zeros((150,940),np.uint8)

                h1, w1 = img1.shape #150x300
                h2, w2 = img2.shape #480x640
                h3, w3 = img3.shape
                h4, w4 = img4.shape
                h5, w5 = img5.shape


                # calculate features
                kp2, desc2 = detector.detectAndCompute(img2, None)

                found, checksound, count = match_and_draw('find_obj', checksound, found, count)

                #print('FPS = ', 1 / time)

                if cv2.waitKey(1) == ord('p'):
                    cv2.waitKey(-1)
                elif cv2.waitKey(1) == ord('b'):
                    cap.release()
                    cv2.destroyAllWindows()
                    #tk.deiconify()
                    break

        def aboutButton():
            JAbout = Tk()
            JAbout.resizable(width=False,height=False)
            JAbout.title('About')
            JAbout.configure(background='yellow')
            JAbout.geometry("400x250")
            TAbout = Label(JAbout,text="This application will help you to get to know Indonesian \n" 
                                        "currency and information about pictures on that currency \n\n"
                                        ,bg='yellow',font='Verdana 9 bold')
            TAbout1 = Label(JAbout,text="\t\t      How To Use This App \n"
                                            "1.Click button Start on main menu to detect the money \n"
                                            "2.Show money to camera \n"
                                            "3.If it has been detected, it will display information about the money\n"
                                            "   and pause the camera\n"
                                            "4.Press 'p' to pause/unpause the camera screen\n"
                                            "5.Press 'b' to return to main menu",anchor='sw', justify=LEFT)
            TAbout2 = Label(JAbout,text="\nThis application was made by\n" 
                                "Farid Rizqi Septiansyah\n"
                                "52417206"
                                ,bg='yellow',font='Verdana 9 bold')
            B3 = Button(JAbout, text='Close',font='Verdana 10 bold',bg='blue', fg='white', command=JAbout.destroy)

            TAbout.pack()
            TAbout1.pack()
            TAbout2 .pack()
            B3.pack(side=BOTTOM)
            JAbout.mainloop()
        def exitButton():    
            tk.destroy()
    
        L1 = Label(tk, text='RUPIAH DETECTION', font=("times new roman",20),fg="white",bg="maroon",height=2).grid(row=0,rowspan=2,columnspan=2,padx=5,pady=5)
        B1 = Button(tk, text="START",font=("times new roman",20),bg="#0D47A1",fg='white',command = StartButton,width=10).grid(row=3,columnspan=2,pady=5)
        B2 = Button(tk, text="ABOUT",font=("times new roman",20),bg="#0D47A1",fg='white',command = aboutButton,width=10).grid(row=6,columnspan=2,pady=5)
        B3 = Button(tk, text=" EXIT ",font=("times new roman",20),bg="#0D47A1",fg='white',command = exitButton,width=10).grid(row=9,columnspan=2,pady=5)
        tk.mainloop()


jalan = uang()
jalan

            

