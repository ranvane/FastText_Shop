echo  "设置Git代理"
# 设置http、https::
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
# 设置socks:
git config --global http.proxy 'socks5://127.0.0.1:7890'
git config --global https.proxy 'socks5://127.0.0.1:7890'



echo  "测试打包工作流"
git add -A
git commit -m "初始化上传"
echo -e "\n开始推送远程仓库.................\n"
git push origin
echo -e "\n推送远程仓库完成.................\n"

## 取消代理
echo  "取消Git代理"
git config --global --unset http.proxy
git config --global --unset https.proxy
