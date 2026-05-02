import torch
import scanpy as sc
from torch.utils.data import DataLoader, TensorDataset
from models.vae_model import VAE
import argparse
import os

def main(args):
    # Ensure models directory exists
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)
    
    adata = sc.read_h5ad(args.data)
    X = torch.FloatTensor(adata.X.toarray())
    dataloader = DataLoader(TensorDataset(X), batch_size=128, shuffle=True)

    model = VAE(input_dim=X.shape[1], latent_dim=args.latent_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print(f"Starting training for {args.epochs} epochs...")
    for epoch in range(args.epochs):
        total_loss = 0
        for batch in dataloader:
            recon, mu, logvar = model(batch[0])
            recon_loss = torch.nn.functional.mse_loss(recon, batch[0], reduction='sum')
            kld_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
            loss = recon_loss + kld_loss
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}: Loss {total_loss/len(dataloader):.2f}")
        
    torch.save(model.state_dict(), args.save_path)
    print("Training complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--latent_dim", type=int, default=10)
    parser.add_argument("--save_path", type=str, required=True)
    main(parser.parse_args())