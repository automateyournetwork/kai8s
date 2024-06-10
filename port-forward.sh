#!/bin/bash

# Start port-forwarding
kubectl port-forward pod/ollama-pod 11434:11434
