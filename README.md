# Bypass Sliding Verification Code

该项目主要实现了`滑动验证码`认证的用户登录场景。本项目以微步社区为例，演示了如何自动完成登录平台的过程。除登录微步社区外，该脚本也可通过简单的修改实现登录其他类似滑块验证码的网站。

## 主要功能

- 自动打开网页
- 输入用户名和密码
- 点击登录按钮
- 处理滑动验证码
- 跳转到登录页面

## 使用用法

(1)克隆这个仓库到本地：

```bash
git clone https://github.com/Mr-Aur0ra/ThreatBook-Login.git
```

(2)安装所需的依赖：

```bash
pip install -r requirements.txt
```

(3)修改 `login.py` 脚本中的用户名和密码为你的实际账户信息(72-73行)：

```python
username_element.send_keys("YOUR_USERNAME")
password_element.send_keys("YOUR_PASSWORD")
```

(4)运行脚本：

```bash
python3 login.py
```



## 注意事项

- 本脚本仅用于教育和学习目的，请勿用于非法用途。
- 在使用本脚本时，请遵循网站的使用条款和隐私政策。

## 贡献

欢迎贡献你的代码或提出改进意见。如果你遇到了问题或有疑问，可以在Issues中提出。

## 许可

这个项目基于[MIT 许可证](LICENSE) 进行分发和使用。

## 参考文章

参考文章1：https://cloud.tencent.com/developer/article/1791907

参考文章2：https://juejin.cn/post/6970289221038931976
