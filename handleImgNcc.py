import os

from utils import call2InsightRest

# caculate min distance of everyone in data

dir_path = os.path.dirname(os.path.realpath(__file__))
imgssDir = dir_path + '/imagesss'
print(imgssDir)
imgsDirList = []
results = []
for imgDir in os.listdir(imgssDir):
    user_id = imgDir.split('_2021')[0]
    res = call2InsightRest(file=os.path.join(imgssDir, imgDir), user_id=user_id, server='http://localhost:18081/extract',
                           isReset=False)
    if isinstance(res, str):
        print(res)
    else:
        _min = min(res)
        results.append(_min)

print(results)
print(min(results))
print(max(results))





# COPY  each person two images from imgsDir to imgssDir


# import shutil

# dir_path = os.path.dirname(os.path.realpath(__file__))
# imgssDir = dir_path + '/imagess'
# imgsDir = dir_path + '/images'
# imgsDirDic = {}
# for imgDir in os.listdir(imgsDir):
#     user_id = imgDir.split('_2021')[0]
#     if user_id in imgsDirDic:
#         imgsDirDic[user_id] += 1
#     else:
#         imgsDirDic[user_id] = 1
#     if imgsDirDic[user_id] <= 2:
#         try:
#             shutil.copyfile(imgsDir + '/' + imgDir, imgssDir + '/' + imgDir)
#             print("File copied successfully.")
#         except:
#             print("Error occurred while copying file.")

