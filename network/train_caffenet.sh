#!/usr/bin/env sh

./build/tools/caffe train \
    --solver=models/productos_caffenet/solver.prototxt 2>&1 | tee \
    models/productos_caffenet/model_train.log
