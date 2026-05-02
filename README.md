# scVAE-State: Deep Generative Modeling of Cellular Latent Manifolds

![Build Status](https://img.shields.io/badge/CI-passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Framework](https://img.shields.io/badge/Framework-PyTorch-orange)

## Project Overview
scVAE-State is a research-grade pipeline designed to model cellular heterogeneity using Variational Autoencoders (VAEs). By training on real-world scRNA-seq data (10x Genomics PBMC 3k), the model learns a continuous latent manifold that represents distinct immune cell states. This project demonstrates how deep generative models can be used to understand why cells respond differently to identical stimuli.

## Key Features
*   **Automated Pipeline:** End-to-end execution from raw data download to biological visualization.
*   **Biological QC:** Integrated filtering for mitochondrial transcript percentage to ensure manifold quality.
*   **Custom Architecture:** PyTorch implementation of a VAE with a Softplus-activated decoder to maintain non-negative gene count reconstruction.
*   **Latent Manifold Analysis:** UMAP projection and latent space traversal for modeling cellular transitions.

## Repository Structure
*   `models/`: Contains the VAE architecture.
*   `scripts/`: Modular scripts for preprocessing, training, and evaluation.
*   `data/`: Directory for processed .h5ad files (gitignored).
*   `figures/`: Generated UMAP and marker gene validation plots.

## Installation
1. Clone the repository:
   `git clone https://github.com/g-Poulami/scVAE-State.git`
2. Install dependencies:
   `pip install -r requirements.txt`

## Usage
Run the entire pipeline with a single command:
`chmod +x run_pipeline.sh`
`./run_pipeline.sh`

## Biological Results & Validation
The model successfully identifies major immune populations in the PBMC 3k dataset. Validation was performed using canonical marker genes:
*   **T-cells:** CD3E, CD4, CD8A
*   **B-cells:** MS4A1, CD19
*   **Monocytes:** LYZ, CD14

### Latent Space Visualization
Below is the UMAP projection of the learned latent manifold, showing distinct clustering of immune subtypes and the distribution of quality control metrics.

![Cell State Manifold](figures/Figure_1.svg)

## License
This project is licensed under the MIT License.
