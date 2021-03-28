from .data import COLORS #line:1
from .yolact import Yolact #line:2
from .utils .augmentations import FastBaseTransform #line:3
from .utils import timer #line:4
from .utils .functions import SavePath #line:5
from .layers .output_utils import postprocess ,undo_image_transformation #line:6
from .data import cfg ,set_cfg #line:8
import time #line:10
import numpy as np #line:11
import torch #line:12
import random #line:15
from collections import defaultdict #line:16
from PIL import Image #line:17
import matplotlib .pyplot as plt #line:18
import cv2 #line:19
w_aim ,h_aim =256 ,512 #line:24
def show (O0OO0O0OO0O0O0O00 ,size =8 ):#line:28
    plt .figure (figsize =(size ,size ))#line:29
    if np .max (O0OO0O0OO0O0O0O00 )<=1 :#line:30
        plt .imshow (O0OO0O0OO0O0O0O00 ,vmin =0 ,vmax =1 )#line:31
    else :#line:32
        plt .imshow (O0OO0O0OO0O0O0O00 ,vmin =0 ,vmax =255 )#line:33
    plt .gray ()#line:34
    plt .show ()#line:35
    plt .close ()#line:36
    print ()#line:37
def make_args (argv =None ,inpass =None ,outpass =None ,model_path =None ):#line:40
    global args #line:41
    class OO00O0OOO00OO0OOO ():#line:42
        def __init__ (OO0O000O000O0000O ):#line:43
            OO0O000O000O0000O .ap_data_file ='results/ap_data.pkl'#line:44
            OO0O000O000O0000O .bbox_det_file ='results/bbox_detections.json'#line:45
            OO0O000O000O0000O .benchmark =False #line:46
            OO0O000O000O0000O .config =None #line:47
            OO0O000O000O0000O .crop =True #line:48
            OO0O000O000O0000O .cuda =True #line:49
            OO0O000O000O0000O .dataset =None #line:50
            OO0O000O000O0000O .detect =False #line:51
            OO0O000O000O0000O .display =False #line:52
            OO0O000O000O0000O .display_bboxes =True #line:53
            OO0O000O000O0000O .display_lincomb =False #line:54
            OO0O000O000O0000O .display_masks =True #line:55
            OO0O000O000O0000O .display_scores =True #line:56
            OO0O000O000O0000O .display_text =True #line:57
            OO0O000O000O0000O .fast_nms =True #line:58
            OO0O000O000O0000O .image ='None:None'#line:59
            OO0O000O000O0000O .images =None #line:60
            OO0O000O000O0000O .mask_det_file ='results/mask_detections.json'#line:61
            OO0O000O000O0000O .mask_proto_debug =False #line:62
            OO0O000O000O0000O .max_images =-1 #line:63
            OO0O000O000O0000O .no_bar =False #line:64
            OO0O000O000O0000O .no_hash =False #line:65
            OO0O000O000O0000O .no_sort =False #line:66
            OO0O000O000O0000O .output_coco_json =False #line:67
            OO0O000O000O0000O .output_web_json =False #line:68
            OO0O000O000O0000O .resume =False #line:69
            OO0O000O000O0000O .score_threshold =0.15 #line:70
            OO0O000O000O0000O .seed =None #line:71
            OO0O000O000O0000O .shuffle =False #line:72
            OO0O000O000O0000O .top_k =10 #line:73
            OO0O000O000O0000O .trained_model =model_path #line:74
            OO0O000O000O0000O .video =None #line:75
            OO0O000O000O0000O .video_multiframe =1 #line:76
            OO0O000O000O0000O .web_det_path ='web/dets/'#line:77
    args =OO00O0OOO00OO0OOO ()#line:79
    if args .output_web_json :#line:80
        args .output_coco_json =True #line:81
    if args .seed is not None :#line:83
        random .seed (args .seed )#line:84
iou_thresholds =[OOOO00000O000OOOO /100 for OOOO00000O000OOOO in range (50 ,100 ,5 )]#line:179
coco_cats ={}#line:180
coco_cats_inv ={}#line:181
color_cache =defaultdict (lambda :{})#line:182
def prep_display (OO0O000O0OOO00OOO ,O00OO000O00OO0O0O ,O000OO0O000O00000 ,OO0O000OO00OOO0O0 ,OOOOO0OO0OOO0OO0O ,undo_transform =True ,class_color =False ,mask_alpha =0.45 ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:184
    ""#line:187
    if undo_transform :#line:188
        OOOOO0000000OO0O0 =undo_image_transformation (O000OO0O000O00000 ,OOOOO0OO0OOO0OO0O ,OO0O000OO00OOO0O0 )#line:189
        O0OOO0O000O0O00O0 =torch .Tensor (OOOOO0000000OO0O0 )#line:191
    else :#line:192
        O0OOO0O000O0O00O0 =O000OO0O000O00000 /255.0 #line:193
        OO0O000OO00OOO0O0 ,OOOOO0OO0OOO0OO0O ,_OOO000O000O00000O =O000OO0O000O00000 .shape #line:194
    with timer .env ('Postprocess'):#line:196
        OO000OOOO0O0OO0OO =postprocess (O00OO000O00OO0O0O ,OOOOO0OO0OOO0OO0O ,OO0O000OO00OOO0O0 ,visualize_lincomb =args .display_lincomb ,crop_masks =args .crop ,score_threshold =args .score_threshold )#line:199
    with timer .env ('Copy'):#line:203
        if cfg .eval_mask_branch :#line:204
            OO0OO000000O000O0 =OO000OOOO0O0OO0OO [3 ][:args .top_k ]#line:206
        OOO0O0OO0OOOOO0O0 ,OO0O0000OOO00O0O0 ,OOOOOOOOO0O0OOO00 =[OO00O0OOO0O00O00O [:args .top_k ].cpu ().numpy ()for OO00O0OOO0O00O00O in OO000OOOO0O0OO0OO [:3 ]]#line:207
    OO0O0O000000OO00O =np .array (OOO0O0OO0OOOOO0O0 ,str )#line:210
    OO0O0O000000OO00O [OO0O0O000000OO00O =='0']='person'#line:211
    OO0O0O000000OO00O [OO0O0O000000OO00O =='24']='backpack'#line:212
    OO0O0O000000OO00O [OO0O0O000000OO00O =='26']='handbag'#line:213
    OO0O0O000000OO00O [OO0O0O000000OO00O =='27']='tie'#line:214
    if verbose >0 :#line:215
        print ('detected: {}'.format (OO0O0O000000OO00O ))#line:216
    O0O00O00O0OO00O0O =min (args .top_k ,OOO0O0OO0OOOOO0O0 .shape [0 ])#line:220
    for O00O000OOO0OOO000 in range (O0O00O00O0OO00O0O ):#line:221
        if OO0O0000OOO00O0O0 [O00O000OOO0OOO000 ]<args .score_threshold :#line:222
            O0O00O00O0OO00O0O =O00O000OOO0OOO000 #line:223
            break #line:224
    if O0O00O00O0OO00O0O ==0 :#line:231
        O0000O0O00000000O =np .ones ((h_aim ,w_aim ),'uint8')*255 #line:232
        return O0000O0O00000000O #line:233
    def OO000O0000O0O00OO (O00000O00OO00000O ,on_gpu =None ):#line:237
        global color_cache #line:238
        O0OO0OOO0OOOOOO00 =(OOO0O0OO0OOOOO0O0 [O00000O00OO00000O ]*5 if class_color else O00000O00OO00000O *5 )%len (COLORS )#line:239
        if on_gpu is not None and O0OO0OOO0OOOOOO00 in color_cache [on_gpu ]:#line:241
            return color_cache [on_gpu ][O0OO0OOO0OOOOOO00 ]#line:242
        else :#line:243
            O00OO0O000OOOO000 =COLORS [O0OO0OOO0OOOOOO00 ]#line:244
            if not undo_transform :#line:245
                O00OO0O000OOOO000 =(O00OO0O000OOOO000 [2 ],O00OO0O000OOOO000 [1 ],O00OO0O000OOOO000 [0 ])#line:247
            if on_gpu is not None :#line:248
                O00OO0O000OOOO000 =torch .Tensor (O00OO0O000OOOO000 ).to (on_gpu ).float ()/255. #line:249
                color_cache [on_gpu ][O0OO0OOO0OOOOOO00 ]=O00OO0O000OOOO000 #line:250
            return O00OO0O000OOOO000 #line:254
    if args .display_masks and cfg .eval_mask_branch :#line:257
        OO0OO000000O000O0 =OO0OO000000O000O0 [:O0O00O00O0OO00O0O ,:,:,None ]#line:259
        OO0OO000000O000O0 =np .array (OO0OO000000O000O0 )#line:262
        OO0OO000000O000O0 =OO0OO000000O000O0 .reshape (OO0OO000000O000O0 .shape [:-1 ])#line:264
        O0000O0O00OOOOO0O =[]#line:269
        O0O00O00OO0O00O0O =len (OO0O000O0OOO00OOO )*len (OO0O000O0OOO00OOO [0 ])#line:271
        O00OOOO0OO000O0OO ,O0O0OO0O000O0OO0O =0 ,0 #line:273
        OOOOOO0O0OOO00O0O =None #line:274
        for O0OOO0O0OOOOO0000 in range (len (OOO0O0OO0OOOOO0O0 )):#line:275
            if OOO0O0OO0OOOOO0O0 [O0OOO0O0OOOOO0000 ]==0 and np .sum (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ,:,:])>O0O00O00OO0O00O0O *0.15 *0.5 :#line:276
                O00OOOO0OO000O0OO =np .sum (np .array (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ]))#line:277
                if O00OOOO0OO000O0OO >O0O0OO0O000O0OO0O :#line:278
                    O0O0OO0O000O0OO0O =O00OOOO0OO000O0OO #line:279
                    OOOOOO0O0OOO00O0O =O0OOO0O0OOOOO0000 #line:280
        if OOOOOO0O0OOO00O0O is not None :#line:281
            O0000O0O00OOOOO0O .append (OOOOOO0O0OOO00O0O )#line:282
        O00OOOO0OO000O0OO ,O0O0OO0O000O0OO0O =0 ,0 #line:284
        OOOOOO0O0OOO00O0O =None #line:285
        for O0OOO0O0OOOOO0000 in range (len (OOO0O0OO0OOOOO0O0 )):#line:286
            if OOO0O0OO0OOOOO0O0 [O0OOO0O0OOOOO0000 ]==24 and np .sum (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ,:,:])>O0O00O00OO0O00O0O *0.009 *0.5 :#line:287
                O00OOOO0OO000O0OO =np .sum (np .array (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ]))#line:288
                if O00OOOO0OO000O0OO >O0O0OO0O000O0OO0O :#line:289
                    O0O0OO0O000O0OO0O =O00OOOO0OO000O0OO #line:290
                    OOOOOO0O0OOO00O0O =O0OOO0O0OOOOO0000 #line:291
        if OOOOOO0O0OOO00O0O is not None :#line:292
            O0000O0O00OOOOO0O .append (OOOOOO0O0OOO00O0O )#line:293
        O00OOOO0OO000O0OO ,O0O0OO0O000O0OO0O =0 ,0 #line:295
        OOOOOO0O0OOO00O0O =None #line:296
        for O0OOO0O0OOOOO0000 in range (len (OOO0O0OO0OOOOO0O0 )):#line:297
            if OOO0O0OO0OOOOO0O0 [O0OOO0O0OOOOO0000 ]==26 and np .sum (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ,:,:])>O0O00O00OO0O00O0O *0.009 *0.5 :#line:298
                O00OOOO0OO000O0OO =np .sum (np .array (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ]))#line:299
                if O00OOOO0OO000O0OO >O0O0OO0O000O0OO0O :#line:300
                    O0O0OO0O000O0OO0O =O00OOOO0OO000O0OO #line:301
                    OOOOOO0O0OOO00O0O =O0OOO0O0OOOOO0000 #line:302
        if OOOOOO0O0OOO00O0O is not None :#line:303
            O0000O0O00OOOOO0O .append (OOOOOO0O0OOO00O0O )#line:304
        O00OOOO0OO000O0OO ,O0O0OO0O000O0OO0O =0 ,0 #line:306
        OOOOOO0O0OOO00O0O =None #line:307
        for O0OOO0O0OOOOO0000 in range (len (OOO0O0OO0OOOOO0O0 )):#line:308
            if OOO0O0OO0OOOOO0O0 [O0OOO0O0OOOOO0000 ]==27 and np .sum (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ,:,:])>O0O00O00OO0O00O0O *0.0025 *0.5 :#line:309
                O00OOOO0OO000O0OO =np .sum (np .array (OO0OO000000O000O0 [O0OOO0O0OOOOO0000 ]))#line:310
                if O00OOOO0OO000O0OO >O0O0OO0O000O0OO0O :#line:311
                    O0O0OO0O000O0OO0O =O00OOOO0OO000O0OO #line:312
                    OOOOOO0O0OOO00O0O =O0OOO0O0OOOOO0000 #line:313
        if OOOOOO0O0OOO00O0O is not None :#line:314
            O0000O0O00OOOOO0O .append (OOOOOO0O0OOO00O0O )#line:315
        if verbose >0 :#line:319
            print ('valid index: {}'.format (O0000O0O00OOOOO0O ))#line:320
        if len (O0000O0O00OOOOO0O )==0 :#line:323
            O0000O0O00000000O =np .ones ((h_aim ,w_aim ,3 ),'uint8')*255 #line:324
            return O0000O0O00000000O #line:325
        OO0OO000000O000O0 =OO0OO000000O000O0 [O0000O0O00OOOOO0O ]#line:331
        O000OO00O000OO00O =np .max (OO0OO000000O000O0 ,axis =0 )#line:335
        OOOOO000O0OOO0OOO =np .ones ((5 ,5 ),np .uint8 )#line:359
        OOO0OO0OOOO0O00O0 =cv2 .morphologyEx (O000OO00O000OO00O ,cv2 .MORPH_CLOSE ,OOOOO000O0OOO0OOO )#line:360
        OOO0OO0OOOO0O00O0 =np .array (OOO0OO0OOOO0O00O0 ,'uint8')#line:362
        try :#line:365
            _OOO000O000O00000O ,OO000OOO00OO0O000 ,_OOO000O000O00000O =cv2 .findContours (OOO0OO0OOOO0O00O0 ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:366
        except :#line:367
            OO000OOO00OO0O000 ,_OOO000O000O00000O =cv2 .findContours (OOO0OO0OOOO0O00O0 ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:368
        O0O0OOO00000OO0OO =max (OO000OOO00OO0O000 ,key =lambda O000O0OOO00OOO00O :cv2 .contourArea (O000O0OOO00OOO00O ))#line:371
        OOOOOOOO0O00OO00O =np .zeros_like (OOO0OO0OOOO0O00O0 )#line:374
        O00O00O0OOO0O0O0O =cv2 .drawContours (OOOOOOOO0O00OO00O ,[O0O0OOO00000OO0OO ],-1 ,color =255 ,thickness =-1 )#line:375
        OO0OOO0000O000O0O =np .min (np .where (O00O00O0OOO0O0O0O >0 )[0 ])#line:379
        O0OOO0O0000OO0OO0 =np .max (np .where (O00O00O0OOO0O0O0O >0 )[0 ])#line:380
        O0O0OO0O0OOOO0OOO =np .min (np .where (O00O00O0OOO0O0O0O >0 )[1 ])#line:381
        O00000O00O0000000 =np .max (np .where (O00O00O0OOO0O0O0O >0 )[1 ])#line:382
        OO0O000O0OOO00OOO [:,:,0 ][O00O00O0OOO0O0O0O ==0 ]=255 #line:386
        OO0O000O0OOO00OOO [:,:,1 ][O00O00O0OOO0O0O0O ==0 ]=255 #line:387
        OO0O000O0OOO00OOO [:,:,2 ][O00O00O0OOO0O0O0O ==0 ]=255 #line:388
        O000OO0O000O00000 =cv2 .cvtColor (OO0O000O0OOO00OOO ,cv2 .COLOR_BGR2RGB )#line:392
        O000OO0O000O00000 =Image .fromarray (O000OO0O000O00000 )#line:393
        O000OO0O000O00000 =O000OO0O000O00000 .crop ((O0O0OO0O0OOOO0OOO ,OO0OOO0000O000O0O ,O00000O00O0000000 ,O0OOO0O0000OO0OO0 ))#line:400
        OOOOO0OO0OOO0OO0O ,OO0O000OO00OOO0O0 =O000OO0O000O00000 .size #line:401
        O00O00OO00OOOOOO0 =int (h_aim *0.95 )#line:404
        O000OO0O000O00000 =O000OO0O000O00000 .resize ((int (OOOOO0OO0OOO0OO0O *O00O00OO00OOOOOO0 /OO0O000OO00OOO0O0 ),O00O00OO00OOOOOO0 ),Image .BICUBIC )#line:405
        OOOOO0OO0OOO0OO0O ,OO0O000OO00OOO0O0 =O000OO0O000O00000 .size #line:406
        OO000OOO000OO000O =Image .new ('RGB',(w_aim ,h_aim ),(255 ,255 ,255 ))#line:410
        OO000OOO000OO000O .paste (O000OO0O000O00000 ,(w_aim //2 -OOOOO0OO0OOO0OO0O //2 ,int (h_aim *0.03 )))#line:411
        return OO000OOO000OO000O #line:417
    return OOOOO0000000OO0O0 #line:469
def evalimage (OOOO00OOOOOOO00OO ,OOO0OOOOOO00O00OO :Yolact ,O000OO0OO00000O0O :str ,save_path :str =None ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:473
    O0OO0O0OOO0O00OO0 =torch .from_numpy (OOOO00OOOOOOO00OO ).float ()#line:475
    OOOO0O0OOO0OOO0OO =FastBaseTransform ()(O0OO0O0OOO0O00OO0 .unsqueeze (0 ))#line:476
    OO0OOO000O0O0O000 =OOO0OOOOOO00O00OO (OOOO0O0OOO0OOO0OO )#line:477
    OO0000OOOO0000O0O =prep_display (OOOO00OOOOOOO00OO ,OO0OOO000O0O0O000 ,O0OO0O0OOO0O00OO0 ,None ,None ,undo_transform =False ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:480
    return OO0000OOOO0000O0O #line:486
def evaluate (O0OOO000O0O00O0OO :Yolact ,OO0O0OO000000O000 ,O00OO0O0O0000OO00 ,train_mode =False ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:491
    O0OOO000O0O00O0OO .detect .use_fast_nms =args .fast_nms #line:492
    cfg .mask_proto_debug =args .mask_proto_debug #line:493
    OO000OOO000000000 ,O0O00OO0OO0OO000O =args .image .split (':')#line:495
    O000O00000OO0OO00 =evalimage (O00OO0O0O0000OO00 ,O0OOO000O0O00O0OO ,OO000OOO000000000 ,O0O00OO0OO0OO000O ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:496
    return O000O00000OO0OO00 #line:497
class tool_mask :#line:533
    def __init__ (OOOOOO0000OO000O0 ,OOOOO0O000OOOOOO0 ,verbose =1 ):#line:534
        OOOOOO0000OO000O0 .verbose =verbose #line:535
        make_args (model_path =OOOOO0O000OOOOOO0 )#line:538
        if args .config is None :#line:540
            OOOOO0O000OOOOOO0 =SavePath .from_str (args .trained_model )#line:541
            args .config =OOOOO0O000OOOOOO0 .model_name +'_config'#line:543
            set_cfg (args .config )#line:545
        with torch .no_grad ():#line:547
            if OOOOOO0000OO000O0 .verbose >0 :#line:550
                print ('Loading mask model...',end ='')#line:551
                OO0OO0OOOOOO000O0 =time .time ()#line:552
            OOOOOO0000OO000O0 .net =Yolact ()#line:553
            OOOOOO0000OO000O0 .net .load_weights (args .trained_model )#line:554
            OOOOOO0000OO000O0 .net .eval ()#line:556
            if OOOOOO0000OO000O0 .verbose >0 :#line:557
                O0OOOO0O0O00O0OO0 =time .time ()#line:558
                print ('Done.({}s)'.format (round (O0OOOO0O0O00O0OO0 -OO0OO0OOOOOO000O0 ,2 )))#line:559
            if args .cuda :#line:561
                OOOOOO0000OO000O0 .net =OOOOOO0000OO000O0 .net #line:563
    def __del__ (O00OO000O0O00O0O0 ):#line:567
        pass #line:568
    def do_mask (OO0O00OO0O00O0O0O ,O0O000OO0OOO000OO ,w_aim =256 ,h_aim =512 ):#line:571
        if OO0O00OO0O00O0O0O .verbose >0 :#line:574
            O0OO0OO000OO0O00O =time .time ()#line:575
        O0O000OO0OOO000OO =cv2 .cvtColor (O0O000OO0OOO000OO ,cv2 .COLOR_RGB2BGR )#line:578
        with torch .no_grad ():#line:580
            OOO0OO00OOOO0O0OO =None #line:582
            OOO00OO0OOO0OO000 =evaluate (OO0O00OO0O00O0O0O .net ,OOO0OO00OOOO0O0OO ,O0O000OO0OOO000OO ,w_aim =w_aim ,h_aim =h_aim ,verbose =OO0O00OO0O00O0O0O .verbose )#line:584
        if OO0O00OO0O00O0O0O .verbose >0 :#line:588
            O0O00OOOOOO0O0OOO =time .time ()#line:589
            print ('mask end.({}s)'.format (round (O0O00OOOOOO0O0OOO -O0OO0OO000OO0O00O ,2 )))#line:590
        return np .array (OOO00OO0OOO0OO000 ,'uint8')#line:591
if __name__ =='__main__':#line:595
    pass #line:597
