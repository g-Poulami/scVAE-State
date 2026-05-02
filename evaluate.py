import torch
import scanpy as sc
import argparse
import os
from models.vae_model import VAE

def main(args):
    # Ensure figures directory exists
    os.makedirs('figures', exist_ok=True)

    adata = sc.read_h5ad(args.data)
    model = VAE(input_dim=adata.n_vars, latent_dim=10)
    model.load_state_dict(torch.load(args.model))
    model.eval()

    # Get Latent Space (z)
    with torch.no_grad():
        X = torch.FloatTensor(adata.X.toarray())
        mu, _ = model.encode(X)
        adata.obsm['X_vae'] = mu.numpy()

    # Recalculate metrics to ensure columns like n_genes_by_counts exist
    sc.pp.calculate_qc_metrics(adata, inplace=True)

    # UMAP and Clustering
    sc.pp.neighbors(adata, use_rep='X_vae')
    sc.tl.umap(adata)
    
    # Save visualization
    sc.pl.umap(adata, color=['n_genes_by_counts', 'pct_counts_mt'], save='_vae_results.png')
    print("Results saved to figures/umap_vae_results.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--data", type=str, required=True)
    main(parser.parse_args())