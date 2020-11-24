#!/bin/bash

pip install --target package/ .
pushd package/
zip -r deployment-package.zip ./*
popd
mv package/deployment-package.zip .
zip -g deployment-package.zip lambda_function.py
