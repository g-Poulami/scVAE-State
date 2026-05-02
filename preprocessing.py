import scanpy as sc
import argparse
import os

def main(args):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print("Loading real-world PBMC 3k dataset...")
    adata = sc.datasets.pbmc3k()

    # Biological QC: Filter stressed/dead cells (High Mitochondrial content)
    adata.var['mt'] = adata.var_names.str.startswith('MT-') 
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)
    adata = adata[adata.obs.pct_counts_mt < 5, :].copy() 
    
    # Normalization & Feature Selection
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=args.hvg, subset=True)

    adata.write(args.output)
    print(f"Preprocessed data saved to {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--hvg", type=int, default=2000)
    main(parser.parse_args())