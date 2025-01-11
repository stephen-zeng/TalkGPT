# TalkGPT
打造你自己的真·聊天·机器人~~（从名字都可以看出来这玩意儿能发声罢）~~
效果图：
![](https://raw.githubusercontent.com/stephen-zeng/TalkGPT/master/img/oversee.png)

# 部署要求
本项目的前后端分离，前端可以部署在任何位置，后端需要部署在可以直接访问（除了中国大陆，包括港澳台，之外的地方）或通过代理访问OpenAI服务器的地方。

# 后端
+ 先安装`ffmpeg`、`pyenv`和`screen`，安装和配置pyenv的文章[这里直达](https://gist.github.com/trongnghia203/9cc8157acb1a9faad2de95c3175aa875)
+ 运行以下命令准备环境
```bash
pyenv install 3.13.0
pyenv virtualenv 3.13.0 talkgpt
pyenv activate talkgpt
```
+ 然后将项目clone下来，进入`TalkGPT/backend`，将`.env-example`重命名为`.env`，进入更改环境变量。环境变量有4个
+ + OPENAI_API_KEY - 这里是自己的API秘钥，当使用密码时会使用这个秘钥
+ + PASSWORD - 这里是密码，你可以使用密码来方便地使用自己的KEY
+ + PORT - 这里是你的websocket服务器将会使用的端口
+ + PROXY - 这里选填，如果你需要使用代理的话就填上自己的HTTP代理地址
+ 环境变量设置好后，运行一下命令
```bash
pip install -r packages.txt
python main.py
```
不出意外的话，此时后端程序就开始运行了。

# 前端
+ 先安装`nodejs`，`npm`，`nvm`。我的环境是本地Mac，node版本是23.1.0；服务器Debian，node版本20.16.0。这里直达[安装地址](https://nodejs.org/en/download)
+ 将项目clone下来，然后进入`TalkGPT/frontend/src`，将`example.main.js`重命名为`main.js`，打开，修改里面的后端服务器websocket地址：
```js
const socket = io('wss://your-own-backend-server.com/');
// 将 "wss://your-own-backend-server.com/" 修改成你自己的后端服务器地址 
```
+ 然后返回`TalkGPT/frontend`，运行一下命令部署
```bash
npm install
npm install -g serve
npm run build
serve dist
```
然后，你应该可以通过3000端口访问TalkGPT了。可能会提示你安装`xsel`，当然是可以装的，如果你想装的话。

# 使用
网页加载好之后，需要首先点击底下的播放按钮以连接到OpenAI的服务器，然后会要求用户输入密码或API Key。输入之后需要再次连接，连接成功后会要求用户新建对话，新建对话成功后即可开始使用。

# 注意
+ 现阶段不支持多用户同时使用，如果新的连接创建会自动断开上一个连接
+ 现阶段查看对话内容和语音不用鉴权，如果有隐私对话记得完成后及时删除
+ 语音仅可在连接上OpenAI服务器且GPT返回任何语音消息之前更换，一旦GPT回复消息，就需要先断开连接，再重新连接才能更换语音。