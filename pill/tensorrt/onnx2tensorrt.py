import tensorrt as trt


onnx_file = 'pill/tensorrt/yolov7-tiny.onnx'
trt_file = 'pill/tensorrt/yolov7-tiny.trt'
batch_size = 1

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
"""Takes an ONNX file and creates a TensorRT engine to run inference with"""
with trt.Builder(TRT_LOGGER) as builder, builder.create_network(EXPLICIT_BATCH) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
    # builder.max_workspace_size = 1<<28 # 256MiB
    config = builder.create_builder_config()
    config.max_workspace_size = 1 << 28
    builder.max_batch_size = batch_size
    config.fp16_mode = True # fp32_mode -> False
    # Parse model file
    with open(onnx_file, 'rb') as model:
        print('Beginning ONNX file parsing')
        if not parser.parse(model.read()):
            print ('ERROR: Failed to parse the ONNX file.')
            for error in range(parser.num_errors):
                print (parser.get_error(error))
    print('Completed parsing of ONNX file')
    engine = builder.build_cuda_engine(network)
    print("Completed creating Engine")
    with open(trt_file, "wb") as f:
        f.write(engine.serialize())