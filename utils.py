import os
import base64
import shutil
import requests
import ujson
import json
import random
from scipy.spatial import distance

session = requests.Session()
session.trust_env = False


def file2base64(file):
    encoded = base64.b64encode(file.file.read()).decode('ascii')
    return encoded


def callApi(target, server):
    images = dict(data=target)
    req = dict(images=images,
               threshold=0.6,
               extract_embedding=True,
               embed_only=False,  # If set to true API expects each image to be 112x112 face crop
               limit_faces=0,  # Limit maximum number of processed faces, 0 = no limit
               api_ver='2'
               )
    resp = session.post(server, json=req, timeout=120)
    content = ujson.loads(resp.content)
    images = content.get('data')
    faces = images[0].get('faces', [])
    try:
        a = faces[0].get('vec')
    except:
        return "There is no person in the picture"
    return a


def writeEmbeded2Text(embedded, folderUserPath):
    listEmbed = os.listdir(folderUserPath)
    randomDir = str(random.randint(1, 20)) + ".txt"
    t = 0
    while randomDir in listEmbed:
        randomDir = str(random.randint(1, 20)) + ".txt"
        t += 1
        if t > 100:
            break
    if randomDir not in listEmbed:
        with open(os.path.join(folderUserPath, randomDir), "w+") as filehandle:
            json.dump(embedded, filehandle)


def call2InsightRest(file, user_id, isReset=0, server='http://localhost:18081/extract'):
    target = [file2base64(file)]
    embFromApi = callApi(target, server)

    if (isinstance(embFromApi, str)):
        return embFromApi

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataPath = os.path.join(dir_path, 'dataset')
    if not os.path.exists(dataPath):
        os.mkdir(dataPath)
    folderUserPath = os.path.join(dataPath, str(user_id))
    if isReset:
        shutil.rmtree(folderUserPath)
    if not os.path.exists(folderUserPath):
        os.mkdir(folderUserPath)
    listEmbFromData = os.listdir(folderUserPath)

    if len(listEmbFromData) <= 9:
        writeEmbeded2Text(embFromApi, folderUserPath)
        return "Add Success"
    else:
        listEmbedDirs = [os.path.join(folderUserPath, dirid) for dirid in os.listdir(folderUserPath)]
        listEmbbed = []
        for listEmbedDir in listEmbedDirs:
            if listEmbedDir[-3:] == 'txt':
                with open(listEmbedDir, "r") as filehandle:
                    listEmbbed.append(json.load(filehandle))

        distsEuc = []
        distsCos = []
        for embFromData in listEmbbed:
            distsEuc.append(distance.euclidean(embFromApi, embFromData))
            distsCos.append(distance.cosine(embFromApi, embFromData))

        mindistEuc = min(distsEuc)
        mindistCos = min(distsCos)
        return [mindistEuc, mindistCos]
