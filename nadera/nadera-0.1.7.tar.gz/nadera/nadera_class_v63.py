""#line:3
import time #line:4
import numpy as np #line:5
import cv2 #line:6
import matplotlib .pyplot as plt #line:7
from keras .preprocessing .image import ImageDataGenerator #line:9
from keras .models import model_from_json #line:10
np .set_printoptions (suppress =True )#line:12
rename =True #line:21
names =['Elegant','Romantic','Ethnic','Country','Active','Mannish','Futurism','Sophisticated']#line:23
order =[5 ,6 ,7 ,0 ,1 ,2 ,3 ,4 ]#line:26
rotation_range =2 #line:29
width_shift_range =0.02 #line:30
height_shift_range =0.02 #line:31
channel_shift_range =40.0 #line:32
shear_range =0.02 #line:33
zoom_range =[1.0 ,1.1 ]#line:34
horizontal_flip =True #line:35
vertical_flip =False #line:36
batch_size =1 #line:39
average_num =10 #line:42
img_save =False #line:45
g_size =3 #line:48
logo_file ='nadera.png'#line:50
QR_file ='QR.png'#line:51
def show (O000O0O0O00000O0O ,name ='_'):#line:53
    plt .figure (figsize =(8 ,8 ))#line:54
    if np .max (O000O0O0O00000O0O )>1 :#line:55
        O000O0O0O00000O0O =np .array (O000O0O0O00000O0O ,dtype =int )#line:56
        plt .imshow (O000O0O0O00000O0O ,vmin =0 ,vmax =255 )#line:57
    else :#line:58
        plt .imshow (O000O0O0O00000O0O ,vmin =0 ,vmax =1 )#line:59
    plt .gray ()#line:60
    if img_save :#line:61
        plt .savefig (name +'.png')#line:62
    else :#line:63
        plt .show ()#line:64
    plt .close ()#line:65
class tool_nadera :#line:82
    def __init__ (OO000OOO00OOOOO00 ,OOOO00OO00OO00O00 ,OO00OOO0000O00000 ,verbose =1 ):#line:83
        OO000OOO00OOOOO00 .verbose =verbose #line:84
        if OO000OOO00OOOOO00 .verbose >0 :#line:91
            print ('Loading nadera model...',end ='')#line:92
            O00O00OOOO0000OO0 =time .time ()#line:93
        O0OOOOO00OOOO0OOO =open (OOOO00OO00OO00O00 ,'r')#line:94
        OOO0OO0O000O0OOO0 =O0OOOOO00OOOO0OOO .read ()#line:95
        O0OOOOO00OOOO0OOO .close ()#line:96
        if OO000OOO00OOOOO00 .verbose >0 :#line:97
            OO0OO000O0O000O0O =time .time ()#line:98
            print ('Done.({}s)'.format (round (OO0OO000O0O000O0O -O00O00OOOO0000OO0 ,2 )))#line:99
        if OO000OOO00OOOOO00 .verbose >0 :#line:101
            print ('Loading nadera weights...',end ='')#line:102
            O00O00OOOO0000OO0 =time .time ()#line:103
        OO000OOO00OOOOO00 .model =model_from_json (OOO0OO0O000O0OOO0 )#line:105
        OO000OOO00OOOOO00 .model .load_weights (OO00OOO0000O00000 )#line:106
        OO000OOO00OOOOO00 .model .trainable =False #line:107
        if OO000OOO00OOOOO00 .verbose >0 :#line:110
            OO0OO000O0O000O0O =time .time ()#line:111
            print ('Done.({}s)'.format (round (OO0OO000O0O000O0O -O00O00OOOO0000OO0 ,2 )))#line:112
        class OOO0OOOO0000O0O0O (ImageDataGenerator ):#line:118
            def __init__ (O0O0OOOO0OO0OO0O0 ,*OO0OO0000O000OO00 ,**O0O0000000OOO0000 ):#line:119
                super ().__init__ (*OO0OO0000O000OO00 ,**O0O0000000OOO0000 )#line:120
            def make_line (OOO00OO000O00OO00 ,O0O0OOO00OOO0O0OO ):#line:122
                OO00OOO0OOO00OOOO =cv2 .cvtColor (O0O0OOO00OOO0O0OO ,cv2 .COLOR_RGB2GRAY )#line:124
                OO00OOO0OOO00OOOO =np .uint8 (OO00OOO0OOO00OOOO )#line:125
                O000O00OO0O0O000O =cv2 .Canny (OO00OOO0OOO00OOOO ,threshold1 =50 ,threshold2 =200 )#line:126
                O000O00OO0O0O000O =O000O00OO0O0O000O .reshape ((512 ,256 ,1 ))#line:127
                return O000O00OO0O0O000O #line:128
            def make_beta (O00OOOO000O000OOO ,OO0O0OO0000000O00 ):#line:130
                O00O00OOOOOO000OO =cv2 .GaussianBlur (OO0O0OO0000000O00 ,(9 ,9 ),0 )#line:132
                OOO0OOO00OOOO0OO0 =np .sum (O00O00OOOOOO000OO ,axis =2 )#line:134
                OOO0OOO00OOOO0OO0 [OOO0OOO00OOOO0OO0 <252 *3 ]=255 #line:135
                OOO0OOO00OOOO0OO0 [OOO0OOO00OOOO0OO0 >=252 *3 ]=0 #line:136
                O000OOOOOOO00O000 =np .ones ((5 ,5 ),np .uint8 )#line:138
                OOO0OOO00OOOO0OO0 =cv2 .erode (OOO0OOO00OOOO0OO0 ,O000OOOOOOO00O000 ,iterations =1 )#line:139
                OOO0OOO00OOOO0OO0 =OOO0OOO00OOOO0OO0 .reshape ((512 ,256 ,1 ))#line:144
                return OOO0OOO00OOOO0OO0 #line:145
            def make_blur (O000OO00000OOO000 ,OOOO0000O00O00OOO ):#line:147
                O0OO0OOOOO0O00O0O =cv2 .GaussianBlur (OOOO0000O00O00OOO ,(51 ,51 ),0 )#line:149
                return O0OO0OOOOO0O00O0O #line:150
            def flow (O00O00OO0OOOOOOO0 ,*O00O00O0OOOO0O0OO ,**OO00O00OO0OO00OOO ):#line:152
                OO0OOO00O0000OOO0 =super ().flow (*O00O00O0OOOO0O0OO ,**OO00O00OO0OO00OOO )#line:153
                O00O0OOO000OO00O0 =np .zeros ((batch_size ,512 ,256 ,1 ))#line:155
                OO00000O0O0OO0000 =np .zeros ((batch_size ,512 ,256 ,1 ))#line:156
                O0O0OO0OO0OOO00OO =np .zeros ((batch_size ,512 ,256 ,3 ))#line:157
                O0000O00OO000OOOO =np .zeros ((batch_size ,8 ))#line:158
                while True :#line:160
                    OOOO00O00000O0O0O ,OOO00OO00O00OOOOO =next (OO0OOO00O0000OOO0 )#line:161
                    for OOO0OO0000O0OO0OO ,O0OOOO000OO0O0OO0 in enumerate (OOOO00O00000O0O0O ):#line:164
                        OO00000O0O0OO0000 [OOO0OO0000O0OO0OO ]=O00O00OO0OOOOOOO0 .make_beta (O0OOOO000OO0O0OO0 )/255.0 #line:166
                        O000O0OO000OOOOOO =OO00000O0O0OO0000 [OOO0OO0000O0OO0OO ].reshape (OO00000O0O0OO0000 [OOO0OO0000O0OO0OO ].shape [:2 ])#line:167
                        O00O000OOOOO00OO0 =np .random .uniform (-channel_shift_range ,channel_shift_range )#line:170
                        O0OOOO000OO0O0OO0 =np .clip (O0OOOO000OO0O0OO0 +O00O000OOOOO00OO0 ,0 ,255 )#line:171
                        O0OOOO000OO0O0OO0 [:,:,0 ][O000O0OO000OOOOOO ==0 ]=255 #line:174
                        O0OOOO000OO0O0OO0 [:,:,1 ][O000O0OO000OOOOOO ==0 ]=255 #line:175
                        O0OOOO000OO0O0OO0 [:,:,2 ][O000O0OO000OOOOOO ==0 ]=255 #line:176
                        O00O0OOO000OO00O0 [OOO0OO0000O0OO0OO ]=O00O00OO0OOOOOOO0 .make_line (O0OOOO000OO0O0OO0 )/255.0 #line:178
                        O0O0OO0OO0OOO00OO [OOO0OO0000O0OO0OO ]=O00O00OO0OOOOOOO0 .make_blur (O0OOOO000OO0O0OO0 )/255.0 #line:179
                        O0000O00OO000OOOO [OOO0OO0000O0OO0OO ]=OOO00OO00O00OOOOO [OOO0OO0000O0OO0OO ]#line:180
                    yield [O00O0OOO000OO00O0 ,OO00000O0O0OO0000 ,O0O0OO0OO0OOO00OO ],O0000O00OO000OOOO #line:182
        OO000OOO00OOOOO00 .MIDG =OOO0OOOO0000O0O0O (rescale =1.0 ,rotation_range =rotation_range ,width_shift_range =width_shift_range ,height_shift_range =height_shift_range ,shear_range =shear_range ,zoom_range =zoom_range ,horizontal_flip =horizontal_flip ,vertical_flip =vertical_flip ,)#line:194
    def do_nadera (O00000O00OO00OO0O ,OOOOO0O00OOOO000O ,mode =''):#line:198
        if O00000O00OO00OO0O .verbose >0 :#line:200
            OOOO0OOOOOOOOOOO0 =time .time ()#line:201
        O0O00OOO0OOO00OOO =np .array ([OOOOO0O00OOOO000O ])#line:204
        OOO00O0OOOOOOO000 =[[0 for OO00OOOO0OOO0O0O0 in range (8 )]for OOOO0OO00OO0OO0O0 in range (len (O0O00OOO0OOO00OOO ))]#line:208
        OOO00O0OOOOOOO000 =np .array (OOO00O0OOOOOOO000 )#line:209
        '''
        #======================================
        # 生成器の確認
        #======================================
        #生成器に1枚だけ入れる
        gen_test = self.MIDG.flow(np.array([x_test[0]]), np.array([y_train[0]]), batch_size=batch_size)
        
        #5*5で生成して確認
        gen_ims_line = []
        gen_ims_beta = []
        gen_ims_blur = []
        for i in range(g_size**2):
            x_tmp, y_tmp = next(gen_test)
            gen_ims_line.append(deepcopy(x_tmp[0][0].reshape((512, 256))))
            gen_ims_beta.append(deepcopy(x_tmp[1][0].reshape((512, 256))))
            gen_ims_blur.append(deepcopy(x_tmp[2][0]))
            #print(y_tmp[0])
        
        stacks_line = []
        for i in range(g_size):
            stack = np.concatenate(gen_ims_line[g_size*i:g_size*(i + 1)], axis=1)
            stacks_line.append(stack)
        stacks_line = np.concatenate(stacks_line, axis=0)
        show(stacks_line, name='stacks_line')
        
        stacks_beta = []
        for i in range(g_size):
            stack = np.concatenate(gen_ims_beta[g_size*i:g_size*(i + 1)], axis=1)
            stacks_beta.append(stack)
        stacks_beta = np.concatenate(stacks_beta, axis=0)
        show(stacks_beta, name='stacks_beta')
        
        stacks_blur = []
        for i in range(g_size):
            stack = np.concatenate(gen_ims_blur[g_size*i:g_size*(i + 1)], axis=1)
            stacks_blur.append(stack)
        stacks_blur = np.concatenate(stacks_blur, axis=0)
        show(stacks_blur, name='stacks_blur')
        '''#line:250
        for OOOOO000O00OO000O in range (len (O0O00OOO0OOO00OOO [:])):#line:254
            O00OO00000O0O000O =O00000O00OO00OO0O .MIDG .flow (np .array ([O0O00OOO0OOO00OOO [OOOOO000O00OO000O ]]),np .array ([OOO00O0OOOOOOO000 [OOOOO000O00OO000O ]]),batch_size =batch_size )#line:257
            if np .min (O0O00OOO0OOO00OOO [OOOOO000O00OO000O ])==255 :#line:270
                OOOO000OOOO000O0O =np .array ([np .zeros (len (names ))],float )#line:271
            else :#line:272
                OOOO000OOOO000O0O =O00000O00OO00OO0O .model .predict_generator (O00OO00000O0O000O ,steps =average_num ,use_multiprocessing =False ,workers =1 )#line:273
            OOOO000OOOO000O0O [OOOO000OOOO000O0O <0.0 ]=0.0 #line:284
            OOOO000OOOO000O0O [OOOO000OOOO000O0O >0.7 ]=0.7 #line:285
            OOOO000OOOO000O0O *=(100.0 /70.0 )#line:286
            OO0O0O00OOOOOO0O0 =np .mean (OOOO000OOOO000O0O ,axis =0 )#line:290
            OOOO0O0OOOOOO0OOO =np .std (OOOO000OOOO000O0O ,axis =0 )#line:291
            """
            meanは0.0-1.0の８つの値
            """#line:296
            O0O00OOOO0OO000O0 =np .array (names )#line:298
            if rename :#line:300
                O0O00OOOO0OO000O0 =O0O00OOOO0OO000O0 [order ]#line:301
                OO0O0O00OOOOOO0O0 =OO0O0O00OOOOOO0O0 [order ]#line:302
                OOOO0O0OOOOOO0OOO =OOOO0O0OOOOOO0OOO [order ]#line:303
            if O00000O00OO00OO0O .verbose >0 :#line:305
                OO0000OO000O00O0O =time .time ()#line:306
                print ('nadera end.({}s)'.format (round (OO0000OO000O00O0O -OOOO0OOOOOOOOOOO0 ,2 )))#line:307
            if mode =='values':#line:310
                return O0O00OOOO0OO000O0 ,OO0O0O00OOOOOO0O0 ,OOOO0O0OOOOOO0OOO #line:311
            else :#line:312
                O0O0O0OOO0OOOOOOO =np .argmax (OO0O0O00OOOOOO0O0 )#line:313
                return O0O00OOOO0OO000O0 [O0O0O0OOO0OOOOOOO ],OO0O0O00OOOOOO0O0 [O0O0O0OOO0OOOOOOO ],OOOO0O0OOOOOO0OOO [O0O0O0OOO0OOOOOOO ]#line:314
if __name__ =='__main__':#line:320
    pass #line:322
