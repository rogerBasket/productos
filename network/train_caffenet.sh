#!/usr/bin/env sh

./build/tools/caffe train \
    --solver=models/cats_dogs_caffenet/solver.prototxt
