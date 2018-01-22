import http.client, urllib.request, urllib.parse, urllib.error, base64
import pygal
import json

import cv2
#密钥 1: 8102dc90f547474698c211dc5f2d82b3

#密钥 2: 1267e870becb44d18629e020ac75fa9c
headers = {
    # Request headers
    # 请求头
    'Content-Type': 'application/octet-stream',
    #content-type可以有application/octet-stream和application/json json是传网络图片上去的，octet-stream是传本地图片上去的
    'Ocp-Apim-Subscription-Key': '8102dc90f547474698c211dc5f2d82b3',
    #填微软页面申请的api key
}


params = urllib.parse.urlencode({
})

#定义过滤器和捕捉画面
#分类器
faceCascade = cv2.CascadeClassifier("E:\\opencv\\sources\\data\\haarcascades_cuda\\haarcascade_frontalface_alt_tree.xml")
#捕捉_开启摄像头
capture = cv2.VideoCapture(0)

#try:
#n=1
#ret,frame = capture.read()
#frame = getFace(frame)
#while(capture.isOpened()): #捕获器也就是摄像头开着读取一帧又返回画出，读取一帧又返回画出
    #n=n+1
ret,frame = capture.read()  #捕获其中一帧
if ret == True:
    cv2.imwrite('output.jpg',frame)
#释放资源并销毁窗口
capture.release()
        #cv2.imshow("Face Detection",frame) #把绘制好的frame实时显示出来
        #退出cv2
        #if (cv2.waitKey(1)&0xFF)==ord('q') or n > 5:
            #break
    #else:
        #break

img = open('output.jpg','rb').read()
#建立https连接
conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
#POST请求
#如果是网络图片，params和headers中间那个参数是一个json语句
#{"url":YOUR IMAGE URL}
conn.request("POST", "/emotion/v1.0/recognize?%s" % params, img, headers)
#接收返回的数据包
response = conn.getresponse()
data = response.read()
parsed = json.loads(data)
json.dumps(parsed,sort_keys=True,indent=2)
for it in parsed:
    exp = it['scores']
print(exp)
pie_chart = pygal.Pie()
pie_chart.title = 'emotion data processing'
for key,value in exp.items():
    pie_chart.add(key,value)
pie_chart.render_to_file('data.svg')
#print(data)
#f = open('my_data.json','a')
#f.write(parsed)
#f.close

#with open("my_data.json") as file_obj:
    #expre = json.load(file_obj)

#with open("my_data.txt",'w') as file_obj:
    #json.dump(data,file_obj)
#result = data.json()
#expre = data['scores']
#print(expre)
conn.close()

#except Exception as e:
#print("[Errno {0}] {1}".format(e.errno, e.strerror))

#cv2.destroyAllWindows()