import re
import cv2
import time
import requests
from selenium import webdriver
from matplotlib import pyplot as plt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def identify_gap(bg,tp,out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg) # 背景图片
    tp_img = cv2.imread(tp) # 缺口图片
    
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
    
    # 绘制方框
    th, tw = tp_pic.shape[:2] 
    tl = max_loc # 左上角点的坐标
    br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
    cv2.imwrite(out, bg_img) # 保存在本地
    
    # 返回缺口的X坐标
    return tl[0] 





def main():
    # 创建Chrome浏览器实例
    browser = webdriver.Chrome()
    
    # 访问登录页面
    browser.get('https://passport.threatbook.cn/login?service=x&callbackURL=https://x.threatbook.com/v5/node/db3fae7d2dd14bf0/8963c70f2b71019b?redirectURL=https%253A%252F%252Fx.threatbook.com%252F')
    
    # 设置一个显式等待
    wait = WebDriverWait(browser, 10)
    
    # 等待"密码登录"按钮出现并点击
    password_login_xpath = '/html/body/div/div/div/div[2]/div/div[2]/div[1]/div/div[3]/div[2]'
    password_login_element = wait.until(EC.element_to_be_clickable((By.XPATH, password_login_xpath)))
    password_login_element.click()
    
    # 输入用户名和密码
    username_xpath = '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[1]/div[1]/div/div[1]/input'
    password_xpath = '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[1]/div[2]/div[1]/div/div[1]/input'
    username_element = wait.until(EC.presence_of_element_located((By.XPATH, username_xpath)))
    password_element = wait.until(EC.presence_of_element_located((By.XPATH, password_xpath)))
    username_element.send_keys("你的用户名")
    password_element.send_keys("你的密码")
    
    time.sleep(2)
    # 点击"登录"按钮进行登录
    login_button_xpath = '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[2]/div/input'
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    login_button.click()



    # 获取互动验证码背景图URL
    bg_image_div_xpath = '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]'
    bg_image_div_element = wait.until(EC.presence_of_element_located((By.XPATH, bg_image_div_xpath)))
    style_attribute = bg_image_div_element.get_attribute('style')
    bp_image_url = re.search(r'url\("(.+)"\);', style_attribute).group(1)
    
    # 获取互动验证码缺口图URL
    tp_image_div_xpath = '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]'
    tp_image_div_element = wait.until(EC.presence_of_element_located((By.XPATH, tp_image_div_xpath)))
    style_attribute = tp_image_div_element.get_attribute('style')
    tp_image_url = re.search(r'url\("(.+)"\);', style_attribute).group(1)
    

    # 下载互动验证码背景图
    response = requests.get(bp_image_url)
    if response.status_code == 200:
        with open("bp_image.png", "wb") as file:
            file.write(response.content)
        #print("验证码背景图已成功保存到: bp_image.png")
        pass
    else:
        print("无法下载验证码背景图，状态码:", response.status_code)
    
    response = requests.get(tp_image_url)
    if response.status_code == 200:
        with open("tp_image.png", "wb") as file:
            file.write(response.content)
        #print("验证码缺口已成功保存到: bp_image.png")
        pass
    else:
        print("无法下载验证码缺口图，状态码:", response.status_code)
    
    bp_image = "bp_image.png"
    tp_image = "tp_image.png"
    match_image = "match.png"

    time.sleep(2)
    # 缺口匹配，并返回缺口的X坐标
    tl = identify_gap(bp_image,tp_image,match_image) 

    # 等待滑块按钮可见并可交互,获取拖动方块的开始位置
    wait = WebDriverWait(browser, 10)
    move_button = browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]')


    # 模拟拖动方块
    move = ActionChains(browser)
    move.click_and_hold(move_button).move_by_offset(tl, 0).release().perform()


    time.sleep(10)

if __name__ == "__main__":
    main()











