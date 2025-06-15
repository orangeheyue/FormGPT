from paddleocr import TableStructureRecognition
model = TableStructureRecognition(model_name="SLANet")
output = model.predict(input="/Users/orange/code/FormGPT/Output/page_1.png", batch_size=1)