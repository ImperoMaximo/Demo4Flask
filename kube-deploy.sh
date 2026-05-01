#!/bin/bash

minikube start

cd deployment

kubectl create secret tls d4f-secrets-tls \
  --cert=tls.crt \
  --key=tls.key

kubectl apply -f d4f-secrets.yaml
kubectl apply -f d4f-config.yaml
kubectl apply -f postgres.yaml
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f ingress.yaml

minikube status

kubectl get pods
kubectl get services
kubectl get all

kubectl rollout restart deployment frontend-deployment
kubectl rollout restart deployment postgres-deployment
kubectl rollout restart deployment backend-deployment