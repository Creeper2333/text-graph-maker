from PIL import Image,ImageDraw,ImageFont
from io import StringIO,BytesIO
import numpy as np
import re
import os
import string
import time

class image_process():
    img_path=str()
    grey_image=None
    img_w=int()
    img_h=int()
    text_line=int()
    text_col=int()
    text_arranged=str()
    text=str()
    text_size=int() # > 13px
    repeat=bool()
    mode=str() # cn-全角，en-半角
    color_mode=str() # L-灰度，RGB-彩色

    def __init__(self,image_path,text,text_size=4,repeat=True,mode='cn',color_mode='L') -> None:
        self.img_path=image_path
        original_image=Image.open(image_path) # 需要关闭文件，不然会一直占用
        self.grey_image=original_image.convert(color_mode)
        original_image.close()

        self.img_w=original_image.width
        self.img_h=original_image.height
        self.text=text
        self.text_size=text_size
        self.repeat=repeat
        self.mode=mode
        self.color_mode=color_mode

    def estimate_text_number(self):
        scale=1
        if self.mode=='en':scale=2
        self.text_col=((self.img_w-self.img_w%self.text_size)/self.text_size+1)*scale
        self.text_line=(self.img_h-self.img_h%self.text_size)/self.text_size+1
        #print(self.text_line)

    def arrange_text(self):
        text_len=len(self.text)
        total_text_num=self.text_line*self.text_col # 总字数
        not_enough=total_text_num%text_len # 相当于是总字数比文本多出来的
        repeat_needed=(total_text_num-not_enough)/text_len # 需要重复几次源文本

        result=self.text*int(repeat_needed)+self.text[0:int(not_enough)] # 生成目标文本
        for i in re.findall('.{'+str(int(self.text_col))+'}',result):
            self.text_arranged=self.text_arranged+i+'\n'
        self.text_arranged.strip()
        #print(self.text_col*self.text_size,self.text_line*self.text_size,self.img_w,self.img_h)

    def generate_text_img(self):
        image=Image.new(self.color_mode,(self.img_w,self.img_h),color='white')
        font=ImageFont.truetype('c:/Windows/Fonts/simhei.ttf',self.text_size)
        draw_tbl=ImageDraw.Draw(image)
        draw_tbl.text((0,0),self.text_arranged,fill='#000000',font=font,spacing=2)

        image.save('tmp.png','PNG')
        image.close()

    def text_img_to_target(self):
        img=Image.open('tmp.png')
        img_array=np.array(img)
        img.close()
        img_grey=np.array(self.grey_image)
        shape=img_array.shape
        height=shape[0]
        width=shape[1]
        if(self.color_mode=='L'):
            for h in range(height):
                for w in range(width):
                    g=img_array[h,w]
                    if g !=255:
                        img_array[h,w]=img_grey[h,w]
                    else:img_array[h,w]=255
        else:
            for h in range(height):
                for w in range(width):
                    (r,g,b)=img_array[h,w]
                    if (r,g,b) != (255,255,255):
                        img_array[h,w]=img_grey[h,w]
                    else:img_array[h,w]=(255,255,255)
        img_target=Image.fromarray(np.uint8(img_array))
        img_target.save('target.png','png')

    def generate(self):
        start_time=time.process_time()
        self.estimate_text_number()
        self.arrange_text()
        self.generate_text_img()
        self.text_img_to_target()
        end_time=time.process_time()
        print('Process finished in {0} secs.'.format(end_time-start_time))