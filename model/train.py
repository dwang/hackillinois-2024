from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(data="./TACO.yaml", epochs=100, imgsz=352)
print(results)

model.export(format="edgetpu")
