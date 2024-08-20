import onnx
import torch
import torch.onnx
from BikeNumberPredictor import BikeNumberPredictor


input_dim = 18
model = BikeNumberPredictor(input_dim)
model.load_state_dict(torch.load('model_not_norm.pth', weights_only=True))
model.eval()

dummy_input = torch.randn(1, input_dim)

torch.onnx.export(model, 
                  dummy_input, 
                  "bike_predictor.onnx",
                  export_params=True,
                  opset_version=11,
                  do_constant_folding=True,
                  input_names = ['input'],
                  output_names = ['output'],
                  dynamic_axes={'input' : {0 : 'batch_size'},
                                'output' : {0 : 'batch_size'}})

print("Modèle exporté avec succès en ONNX")

import onnx

onnx_model = onnx.load("bike_predictor.onnx")
onnx.checker.check_model(onnx_model)

print("Modèle ONNX vérifié avec succès")