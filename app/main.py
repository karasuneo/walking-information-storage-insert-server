import requests

building_id = "01F8VYXK67BGC1F9RP1E4S9YAK"
floor_id = "01F8VYXK67BGC1F9RP1E4S9YTV"
x = 3700
y = 2800

url = f"http://localhost:8000/api/buildings/{building_id}/floors/{floor_id}/coordinates/{x}/{y}"

# アップロードするファイルを指定
files = {
    "fp_model_file": (
        "fp_model_file",
        open("./data/demo_ratio_wave.csv", "rb"),
    ),  # ("ファイル名", ファイルオブジェクト)
}


# POSTリクエストで送信
response = requests.post(url, files=files, timeout=1000)


print(response.status_code, response.text)
