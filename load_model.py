# -*- coding: utf-8 -*-
import ml2rt
import redisai as rai

from src.utils.config import Config


if __name__ == '__main__':
    config = Config()
    if not Config.validate_configs():
        exit(1)

    connection_rai = rai.Client(host='localhost', port='6379')
    model = ml2rt.load_model('resources/bert.rai')
    connection_rai.modelset("bert", 'onnx', config.device, model)
