import time

from selenium  import  webdriver
from  selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from io import BytesIO

class Bilibili(object):
        def __init__(self):

            self.driver=webdriver.Firefox(executable_path="/Users/huxueqiang/Documents/Python阶段6/day5/geckodriver")
            #隐式等待
            self.driver.implicitly_wait(3)
            self.url="https://passport.bilibili.com/login"
            self.user_name="13926267586"
            self.password="bili13926267586"

        def input(self):
            self.driver.get(self.url)
            #获取标签
            user_el=self.driver.find_element_by_id("login-username")
            #输入账号
            user_el.send_keys(self.user_name)
            #输入密码
            pwd_el=self.driver.find_element_by_id("login-passwd")

            pwd_el.send_keys(self.password)

        def get_screenshot(self):
            #截图处理
            screen_shot=self.driver.get_screenshot_as_png()
            screen_shot=Image.open(BytesIO(screen_shot))
            return screen_shot

        def get_position(self):
            # 定位锁按钮 模拟点击
            lock_el = self.driver.find_element_by_xpath("//div[@class='gt_ajax_tip gt_ready']")
            lock_el.click()
            # 定位图片对象
            image=self.driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']")
            time.sleep(2)

            # 获取图片对象的坐标
            location=image.location
            print(location)
            # 获取图片对象的尺寸
            size=image.size
            print(size)
            shot=self.get_screenshot()
            print(shot.size)
            # 计算图片的截取区域
            left=2*location["x"]
            top=2*location["y"]
            right=2*(location["x"]+size["width"])
            bottom=2*(location["y"]+size["height"])
            return left,top,right,bottom



        def get_image(self):
            #获取验证码的位置
            position=self.get_position()
            print(position)
            #屏幕截图
            screenshot1=self.get_screenshot()
            #抠出没有滑块和阴影的验证码图片
            capture1=screenshot1.crop(position)
            with open("1.png","wb") as f:
                capture1.save(f)
            #点击验证码拖动按钮
            block_el=self.driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
            block_el.click()
            #等待错误信息消失
            time.sleep(3)
            #屏幕截图
            screenshot2=self.get_screenshot()
            #抠图
            capture2=screenshot2.crop(position)
            with open("2.png","wb") as f:
                capture2.save(f)

            return capture1,capture2
        def pixel_compare(self,image1,image2,x,y):
            pixel1=image1.load()[x,y]
            pixel2=image2.load()[x,y]
            # print(pixel1,pixel2)
            base_value=60
            if abs(pixel1[0]-pixel2[0])<base_value and abs(pixel1[1]-pixel2[1])<base_value and abs((pixel1[2]-pixel2[2])<base_value):

                return True
            else:
                return False




        def get_gap(self,image1,image2):
            #偏移值
            left=120
            print(image1.size)
            for i in range(left,image1.size[0]):
                for j in range(1,image1.size[1]):
                    #获取一个坐标点，然后在两张图上核对该坐标点的颜色差距
                    if not self.pixel_compare(image1,image2,i,j):
                        left=i
                        return round(left/2-10)
            return left


        def block_slide(self,offset):
            #通过偏移量模拟操作
            #步伐
            pace=[]
            #当前位移
            current=0
            #中间点
            middle=offset*(3/5)
            t=0.3
            v=0
            while current<offset:
                if current<middle:
                    a=2
                else:
                    a=-3
                v0=v
                v=v0+a*t
                move=v0*t+1/2*a*t*t
                current+=move
                pace.append(round(move))
            return pace
        def op_button(self,pace):
            #拖动滑块
            block_el=self.driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
            ActionChains(self.driver).click_and_hold(block_el).perform()
            # ActionChains(self.driver).move_by_offset(xoffset=100, yoffset=0).perform()
            # ActionChains(self.driver).move_by_offset(xoffset=-100, yoffset=0).perform()

            for i in pace:
                ActionChains(self.driver).move_by_offset(xoffset=i,yoffset=0).perform()
            ActionChains(self.driver).release().perform()


        def capture(self):

            #滑动验证码处理
            #1获取验证码图片/有拼图的图片
            image1,image2=self.get_image()
            #2比较两张验证码图片滑块的偏移量
            offset=self.get_gap(image1,image2)
            print(offset)
            #3使用偏移值计算移动操作
            pace=self.block_slide(offset)
            #4操作滑块 模拟登陆
            self.op_button(pace)
        def run(self):
            #主逻辑 1.进入登录页面 输入账号密码
            self.input()
            self.capture()
            time.sleep(3)
            # self.driver.close()
            #2.处理验证码
if __name__ == '__main__':
    bilibili=Bilibili()
    bilibili.run()
