#!/bin/bash
# Build all CodeSphere Docker execution images
set -e

echo "🐳 Building CodeSphere Docker images..."

echo "→ Building Python image..."
docker build -t codesphere-python ./docker/python/

echo "→ Building C++ image..."
docker build -t codesphere-cpp ./docker/cpp/

echo "→ Building Java image..."
docker build -t codesphere-java ./docker/java/

echo "✓ All images built successfully!"
docker images | grep codesphere
