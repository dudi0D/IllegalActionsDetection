from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("best.pt")
results = model.predict('validation_set')
for i in results:
    i.show()