import cv2
import time
import numpy as np
global img
global point1, point2

lsPointsChoose = []
tpPointsChoose = []
pointsCount = 0
count = 0
pointsMax = 6

def mouse(event, x, y, flags, param):
    """
    Check FPU precision mode was not changed during test collection.
    The clumsy way we do it here is mainly necessary because numpy
    still uses yield tests, which can execute code at test collection
    time.
    """
    global flag, horizontal, vertical, flag_hor, flag_ver, dx, dy, sx, sy, dst, x1, y1, x2, y2, x3, y3, f1, f2
    global zoom, scroll_har, scroll_var, img_w, img_h, img, dst1, win_w, win_h, show_w, show_h
    global img, point1, point2,dst1
    count =0
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        if flag == 0:
            if horizontal and 0 < x < win_w and win_h - scroll_w < y < win_h:
                flag_hor = 1  # 鼠标在水平滚动条上
            elif vertical and win_w - scroll_w < x < win_w and 0 < y < win_h:
                flag_ver = 1  # 鼠标在垂直滚动条上
            if flag_hor or flag_ver:
                flag = 1  # 进行滚动条垂直
                x1, y1, x2, y2, x3, y3 = x, y, dx, dy, sx, sy  # 使鼠标移动距离都是相对于初始滚动条点击位置，而不是相对于上一位置
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        if flag == 1:
            if flag_hor:
                w = (x - x1)/2  # 移动宽度
                dx = x2 + w * f1  # 原图x
                if dx < 0:  # 位置矫正
                    dx = 0
                elif dx > img_w - show_w:
                    dx = img_w - show_w
                sx = x3 + w  # 滚动条x
                if sx < 0:  # 位置矫正
                    sx = 0
                elif sx > win_w - scroll_har:
                    sx = win_w - scroll_har
            if flag_ver:
                h = y - y1  # 移动高度
                dy = y2 + h * f2  # 原图y
                if dy < 0:  # 位置矫正
                    dy = 0
                elif dy > img_h - show_h:
                    dy = img_h - show_h
                sy = y3 + h  # 滚动条y
                if sy < 0: # 位置矫正
                    sy = 0
                elif sy > win_h - scroll_var:
                    sy = win_h - scroll_var
            dx, dy = int(dx), int(dy)
            img1 = img[dy:dy + show_h, dx:dx + show_w]  # 截取显示图片
            print(dy, dy + show_h, dx, dx + show_w)
            dst = img1.copy()
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        flag, flag_hor, flag_ver = 0, 0, 0
        x1, y1, x2, y2, x3, y3 = 0, 0, 0, 0, 0, 0
    elif event == cv2.EVENT_MOUSEWHEEL:  # 滚轮
        if flags > 0:  # 滚轮上移
            zoom += wheel_step
            if zoom > 1 + wheel_step * 20:  # 缩放倍数调整
                zoom = 1 + wheel_step * 20
        else:  # 滚轮下移
            zoom -= wheel_step
            if zoom < wheel_step:  # 缩放倍数调整
                zoom = wheel_step
        zoom = round(zoom, 2)  # 取2位有效数字
        img_w, img_h = int(img_original_w * zoom), int(img_original_h * zoom)  # 缩放都是相对原图，而非迭代
        # img_zoom = cv2.resize(img_original, (img_w, img_h), interpolation=cv2.INTER_AREA)
        if img_original_w / img_original_h >= img_w / img_h:
            img_zoom = cv2.resize(img_original, (img_w, int(img_original_h * img_w / img_original_w)))
        else:
            img_zoom = cv2.resize(img_original, (int(img_original_w * img_original_w / img_original_h), img_h))
        horizontal, vertical = 0, 0
        if img_h <= win_h and img_w <= win_w:
            dst1 = img_zoom
            cv2.resizeWindow("img", img_w, img_h)
            scroll_har, scroll_var = 0, 0
            f1, f2 = 0, 0
        else:
            if img_w > win_w and img_h > win_h:
                horizontal, vertical = 1, 1
                scroll_har, scroll_var = win_w * show_w / img_w, win_h * show_h / img_h
                f1, f2 = (img_w - show_w) / (win_w - scroll_har), (img_h - show_h) / (win_h - scroll_var)
            elif img_w > win_w and img_h <= win_h:
                show_h = img_h
                win_h = show_h + scroll_w
                scroll_har, scroll_var = win_w * show_w / img_w, 0
                f1, f2 = (img_w - show_w) / (win_w - scroll_har), 0
            elif img_w <= win_w and img_h > win_h:
                show_w = img_w
                win_w = show_w + scroll_w
                scroll_har, scroll_var = 0, win_h * show_h / img_h
                f1, f2 = 0, (img_h - show_h) / (win_h - scroll_var)
            dx, dy = dx * zoom, dy * zoom  # 缩放后显示图片相对缩放图片的坐标
            sx, sy = dx / img_w * (win_w - scroll_har), dy / img_h * (win_h - scroll_var)
            img = img_zoom.copy()  # 令缩放图片为原图
            dx, dy = int(dx), int(dy)
            img1 = img[dy:dy + show_h, dx:dx + show_w]
            dst = img1.copy()

    if horizontal and vertical:
        sx, sy = int(sx), int(sy)
        # 对dst1画图而非dst，避免鼠标事件不断刷新使显示图片不断进行填充
        dst1 = cv2.copyMakeBorder(dst, 0, scroll_w, 0, scroll_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.rectangle(dst1, (sx, show_h), (int(sx + scroll_har), win_h), (181, 181, 181), -1)  # 画水平滚动条
        cv2.rectangle(dst1, (show_w, sy), (win_w, int(sy + scroll_var)), (181, 181, 181), -1)  # 画垂直滚动条
    elif horizontal == 0 and vertical:
        sx, sy = int(sx), int(sy)
        dst1 = cv2.copyMakeBorder(dst, 0, 0, 0, scroll_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.rectangle(dst1, (show_w, sy), (win_w, int(sy + scroll_var)), (181, 181, 181), -1)  # 画垂直滚动条
    elif horizontal and vertical == 0:
        sx, sy = int(sx), int(sy)
        dst1 = cv2.copyMakeBorder(dst, 0, scroll_w, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.rectangle(dst1, (sx, show_h), (int(sx + scroll_har), win_h), (181, 181, 181), -1)  # 画水平滚动条

    cv2.imshow("img", dst1)
    img2 = dst1.copy() #EVENT_RBUTTONDOWN
    if event == cv2.EVENT_RBUTTONDOWN:         #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 5)
        cv2.imshow('img', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_RBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), 5)
        cv2.imshow('img', img2)
    elif event == cv2.EVENT_RBUTTONUP :         #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 5)

        cv2.imshow('img', img2)
        cv2.destroyAllWindows()
        min_x = min(point1[0],point2[0])+dx
        min_y = min(point1[1],point2[1])+dy
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] -point2[1])
        cut_img = img[min_y:min_y+height, min_x:min_x+width]
        # cv2.imwrite(tmp_path, cut_img,[int(cv2.IMWRITE_PNG_COMPRESSION),1])

        #
        src =cut_img.copy()
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)#BGR转HSV
        low_hsv = np.array([0,43,46])#这里要根据HSV表对应  ##156
        # ，填入三个min值（表在下面）
        high_hsv = np.array([10,255,255])#这里填入三个max值 #180
        mask = cv2.inRange(hsv,lowerb=low_hsv,upperb=high_hsv)#提取掩膜

        #黑色背景转透明部分
        mask_contrary = mask.copy()
        mask_contrary[mask_contrary==0]=1
        mask_contrary[mask_contrary==255]=0#把黑色背景转白色
        mask_bool = mask_contrary.astype(bool)
        mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
        #这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
        mask_img=cv2.cvtColor(mask_img,cv2.COLOR_BGR2BGRA)
        mask_img[mask_bool]=[0,0,0,0]
        #这里如果背景本身就是白色，可以不需要这个操作，或者不需要转成透明背景就不需要这里的操作

        cv2.imwrite(tmp_path,mask_img,[int(cv2.IMWRITE_PNG_COMPRESSION),0])
        cv2.imwrite(tmp_path_2,cut_img,[int(cv2.IMWRITE_PNG_COMPRESSION),0])

        # cv2.imwrite('test_wangye'+str(count)+'.png', mask_img,[int(cv2.IMWRITE_PNG_COMPRESSION),1])
        # cv2.waitKey(1)
        # cv2.destroyAllWindows()

def plot_view(image):
    """
     Check FPU precision mode was not changed during the test.
    """
    time.sleep(4)

def test_main(img_path,save_path,save_path_2):
    """Fit and plot a univariate or bivariate kernel density estimate."""
    global horizontal, vertical,sx, sy , flag, flag_hor, flag_ver,dst,scroll_w
    global show_h,scroll_har,win_h,show_w,win_w,scroll_har,scroll_var
    global x1, y1, x2, y2, x3, y3,img_h, img_w,dx, dy,img,img_original
    global  wheel_step, zoom,zoom_w, zoom_h, f1, f2,img_original_w,img_original_h
    global tmp_path,tmp_path_2
    tmp_path =save_path
    tmp_path_2 = save_path_2
    img_original = cv2.imread(img_path)
    img_original_h, img_original_w = img_original.shape[0:2]  # 原图宽高
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.moveWindow("img", 300, 100)
    img = img_original.copy()
    img_h, img_w = img.shape[0:2]  # 原图宽高
    show_h, show_w = 600, 800  # 显示图片宽高
    horizontal, vertical = 0, 0  # 原图是否超出显示图片
    dx, dy = 0, 0  # 显示图片相对于原图的坐标
    scroll_w = 16  # 滚动条宽度
    sx, sy = 0, 0  # 滚动块相对于滚动条的坐标
    flag, flag_hor, flag_ver = 0, 0, 0  # 鼠标操作类型，鼠标是否在水平滚动条上，鼠标是否在垂直滚动条上
    x1, y1, x2, y2, x3, y3 = 0, 0, 0, 0, 0, 0  # 中间变量
    win_w, win_h = show_w + scroll_w, show_h + scroll_w  # 窗口宽高
    scroll_har, scroll_var = win_w * show_w / img_w, win_h * show_h / img_h  # 滚动条水平垂直长度
    wheel_step, zoom = 0.05, 1  # 缩放系数， 缩放值
    zoom_w, zoom_h = img_w, img_h  # 缩放图宽高
    f1, f2 = (img_w - show_w) / (win_w - scroll_har), (img_h - show_h) / (win_h - scroll_var)  # 原图可移动部分占滚动条可移动部分的比例

    if img_h <= show_h and img_w <= show_w:
        cv2.resizeWindow("img2", win_w, win_h)
    else:
        if img_w > show_w:
            horizontal = 1
        if img_h > show_h:
            vertical = 1
        i = img[dy:dy + show_h, dx:dx + show_w]
        dst = i.copy()
    cv2.resizeWindow("img", win_w, win_h)
    # cv2.setMouseCallback('img', on_mouse)
    cv2.setMouseCallback('img', mouse)

    #
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def img_resize(image,width_new,height_new):
    """Flexibly plot a univariate distribution of observations.

    This function combines the matplotlib ``hist`` function (with automatic
    calculation of a good default bin size) with the seaborn :func:`kdeplot`
    and :func:`rugplot` functions. It can also fit ``scipy.stats``
    distributions and plot the estimated PDF over the data."""
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    # width_new = 2000
    # height_new = 2000
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    plot_view(img_new)
    return img_new

def valuechange(img_path,final_path,size_red_size,size_red_size_g,size_red_size_B):
         """Plot datapoints in an array as sticks on an axis."""
         img = cv2.imread(img_path)
         (B,G,R) = cv2.split(img)#提取R、G、B分量
         src =img.copy()

         hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)#BGR转HSV
         print(hsv[0])
         low_hsv = np.array([156,43,46])#这里要根据HSV表对应
         # ，填入三个min值（表在下面）
         high_hsv = np.array([180,255,255])#这里填入三个max值
         mask = cv2.inRange(hsv,lowerb=low_hsv,upperb=high_hsv)#提取红色掩膜


         # res = cv2.bitwise_and(img,img,mask=mask)
         # res =[size_red_size,size_red_size_g,size_red_size_B]
         # cv2.imshow('xxxx',res)

         print(size_red_size)
         print(size_red_size_g)
         print(size_red_size_B)

         # test_color = colorsys.hsv_to_rgb(size_red_size, size_red_size_g, size_red_size_B)
         # green = np.uint8([[[size_red_size,size_red_size_g,size_red_size_B]]])
         # hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
         # print(hsv_green[0][0])
         color_1=[size_red_size_B,size_red_size_g,size_red_size]
         # 给目标像素赋值
         # src[mask!=0]=color_1    ###给目标图像
         #
         # cv2.imshow('color',src)
         # cv2.waitKey(0)
        # # #黑色背景转透明部分
         mask_contrary = mask.copy()
         mask_contrary[mask_contrary==0]=1
         mask_contrary[mask_contrary==255]=0#把黑色背景转白色
         mask_bool = mask_contrary.astype(bool)
         mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
         #这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
         mask_img=cv2.cvtColor(mask_img,cv2.COLOR_BGR2BGRA)
         mask_img[mask_bool]=[0,0,0,0]

         src[mask!=0]=color_1
         cv2.imshow('color_2',src)
         cv2.waitKey(0)

         #这里如果背景本身就是白色，可以不需要这个操作，或者不需要转成透明背景就不需要这里的操作
         # cv2.imwrite(tmp_path,mask_img,[int(cv2.IMWRITE_PNG_COMPRESSION),1])
         cv2.imwrite(final_path, mask,[int(cv2.IMWRITE_PNG_COMPRESSION),0])


def on_mouse(event, x, y, flags, param):
    global img, point1, point2, count, pointsMax
    global lsPointsChoose, tpPointsChoose  # 存入选择的点
    global pointsCount  # 对鼠标按下的点计数
    global img2, ROI_bymouse_flag
    img2 = img.copy()  # 此行代码保证每次都重新再原图画  避免画多了

    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        pointsCount = pointsCount + 1
        print('pointsCount:', pointsCount)
        point1 = (x, y)
        print (x, y)
        # 画出点击的点
        cv2.circle(img2, point1, 10, (0, 255, 0), 2)

        # 将选取的点保存到list列表里
        lsPointsChoose.append([x, y])  # 用于转化为darry 提取多边形ROI
        tpPointsChoose.append((x, y))  # 用于画点
        # ----------------------------------------------------------------------
        # 将鼠标选的点用直线连起来
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(img2, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        # ----------------------------------------------------------------------
        # ----------点击到pointMax时可以提取去绘图----------------
        if (pointsCount == pointsMax):
            # -----------绘制感兴趣区域-----------
            ROI_byMouse()
            ROI_bymouse_flag = 1
            lsPointsChoose = []

        cv2.imshow('src', img2)
    # -------------------------右键按下清除轨迹-----------------------------
    if event == cv2.EVENT_RBUTTONDOWN:  # 右键点击
        print("right-mouse")
        pointsCount = 0
        tpPointsChoose = []
        lsPointsChoose = []
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(img2, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        cv2.imshow('src', img2)

def ROI_byMouse():
    global src, ROI, ROI_flag, mask2
    mask = np.zeros(img.shape, np.uint8)
    pts = np.array([lsPointsChoose], np.int32)  # pts是多边形的顶点列表（顶点集）
    pts = pts.reshape((-1, 1, 2))
    # 这里 reshape 的第一个参数为-1, 表明这一维的长度是根据后面的维度的计算出来的。
    # OpenCV中需要先将多边形的顶点坐标变成顶点数×1×2维的矩阵，再来绘制

    # --------------画多边形---------------------
    mask = cv2.polylines(mask, [pts], True, (255, 0, 0))
    ##-------------填充多边形---------------------
    mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))
    # cv2.imshow('mask', mask2)
    # cv2.imwrite('mask.bmp', mask2)
    ROI = cv2.bitwise_and(mask2, img)

    cv2.imshow('ROI_1', ROI)
    src =ROI.copy()
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)#BGR转HSV
    low_hsv = np.array([156,43,46])#这里要根据HSV表对应
    # ，填入三个min值（表在下面）
    high_hsv = np.array([183,255,255])#这里填入三个max值
    mask = cv2.inRange(hsv,lowerb=low_hsv,upperb=high_hsv)#提取掩膜

    #黑色背景转透明部分
    mask_contrary = mask.copy()
    mask_contrary[mask_contrary==0]=1
    mask_contrary[mask_contrary==255]=0#把黑色背景转白色
    mask_bool = mask_contrary.astype(bool)
    mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
    #这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
    mask_img=cv2.cvtColor(mask_img,cv2.COLOR_BGR2BGRA)
    mask_img[mask_bool]=[0,0,0,0]
    cv2.imwrite(tmp_path, mask_img,[int(cv2.IMWRITE_PNG_COMPRESSION),0])


def final_main(input_path,save_path):
    global img
    global tmp_path
    tmp_path = save_path
    img = cv2.imread(input_path)
    # ---------------------------------------------------------
    # --图像预处理，设置其大小
    # height, width = img.shape[:2]
    # size = (int(width * 0.3), int(height * 0.3))
    # img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    # ------------------------------------------------------------
    ROI = img.copy()
    cv2.namedWindow('src')
    cv2.setMouseCallback('src', on_mouse)
    cv2.imshow('src', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#if __name__ == '__main__':
 #   img_resize(img,point1,point2)
# tmp='test_tmp.png'
# cv2.imwrite(tmp,P,[int(cv2.IMWRITE_PNG_COMPRESSION),1])