# Retinal Image Detection for Eye Diseases and Conditions using DenseNet-161 and Vision Transformer

A deep learning-based system that classifies retinal images to detect eye diseases and conditions. This project uses **DenseNet-161** for feature extraction and a **Vision Transformer (ViT)** for classification. The tool features a PySide6 GUI and supports storing classification history with MongoDB.

## 🧠 Project Summary

This thesis project aims to assist in the early detection of various retinal conditions using computer vision techniques. By applying a hybrid model that combines CNN and Transformer architectures, the system aims to classify retinal images into multiple categories.

## 🔍 Features

- Upload and preview retinal images
- Perform classification using DenseNet-161 + ViT
- Input patient name and remarks
- Save results with into MongoDB
- View history of classifications with image thumbnails
- Export classification record as PDF

## 📁 Dataset

This system was trained and tested on a publicly available dataset of retinal images, with conditions such as:

- Diabetic Retinopathy
- Age-Related Macular Degeneration
- Myopia
- Central Retinal Vein Occlusion
- Optic Disc Cupping
- Drusen
- Tessellation
- ...and others (including Normal Retina)

⚠️ *Dataset not included in this repository due to size limitations.*
