## Requirements:

1. Docker
2. Nvidia-container-toolkit
3. Nvidia GPU drivers (470.x.x and above)


## Running with Docker:

1. Clone repo.
2. Execute `deploy_trt.sh` from repo's root, edit settings if needed.
Also if you want to test API in non-GPU environment you can run service
with `deploy_cpu.sh` script. In this case ONNXRuntime will be used as
inference backend. Go to http://localhost:18081 to access documentation and try API of InsightFace-REST
3. `python handleAPI.py` to run API with FastAPI. Then go to http://localhost:8000/docs to access documentation and try API.
`Note`: here is using the first 10 images submitted to the API for each user to save in the dataset folder. You can edit the number of images saved at `/utils.py` specifically: `if len(listEmbFromData) < 10:`
4. Params of API:

    `idUser`

    `isReset (Default value : 0) ( 1 if you want to reset data folder of id idUser)`

    `fileUpload`

### Based on:
[InsightFace-REST](https://github.com/SthPhoenix/InsightFace-REST)

### Edited by:
[Tung Khong Manh](https://www.linkedin.com/in/tungkm)



