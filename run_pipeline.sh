#!/bin/bash

# Exit on error
set -e

# Configuration variables
DATA_DIR="./data"
RESULTS_DIR="./results"
LOG_DIR="./logs"
EPOCHS=100
LATENT_DIM=10

# Create necessary directories
mkdir -p $DATA_DIR $RESULTS_DIR $LOG_DIR

echo "--- Starting scVAE Pipeline ---"

# Step 1: Data Ingestion and Preprocessing
echo "Step 1: Preprocessing raw scRNA-seq data..."
python3 scripts/preprocess.py \
    --input "pbmc3k" \
    --output "$DATA_DIR/processed_pbmc.h5ad" \
    --hvg 2000 > "$LOG_DIR/preprocess.log" 2>&1

# Step 2: VAE Model Training
echo "Step 2: Training VAE model for $EPOCHS epochs..."
python3 scripts/train.py \
    --data "$DATA_DIR/processed_pbmc.h5ad" \
    --epochs $EPOCHS \
    --latent_dim $LATENT_DIM \
    --save_path "models/vae_weights.pth" > "$LOG_DIR/train.log" 2>&1

# Step 3: Evaluation and Visualization
echo "Step 3: Generating UMAP and Latent Manifolds..."
python3 scripts/evaluate.py \
    --model "models/vae_weights.pth" \
    --data "$DATA_DIR/processed_pbmc.h5ad" \
    --out_dir $RESULTS_DIR > "$LOG_DIR/evaluate.log" 2>&1[cite: 2, 3]

echo "--- Pipeline completed successfully. Results are in $RESULTS_DIR ---"