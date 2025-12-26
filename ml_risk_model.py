import os
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any

class RiskNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(3, 16)  # Inputs: amount (norm), velocity, history
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)   # Output: risk prob (0-1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.sigmoid(self.fc3(x))

# Train stub (runs once)
def train_model(num_samples=100):
    model = RiskNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.BCELoss()
    
    # Synthetic training data: [norm_amount, velocity (fake), history (fake)] -> label (0/1)
    X = torch.tensor(np.random.rand(num_samples, 3).astype(np.float32))
    y = ((X[:, 0] > 0.5).float()).unsqueeze(1)  # Fixed: .float() for Torch bools
    
    for epoch in range(50):  # Quick train
        out = model(X)
        loss = criterion(out, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    torch.save(model.state_dict(), 'risk_model.pth')
    return model

# Load/infer
def infer_risk(entity: Dict[str, Any]) -> str:
    if not os.path.exists('risk_model.pth'):
        model = train_model()
    else:
        model = RiskNet()
        model.load_state_dict(torch.load('risk_model.pth'))
    model.eval()
    
    amount = entity.get('amount', 0) / 1000000.0  # Normalize
    velocity = entity.get('velocity', np.random.rand())  # Stub
    history = entity.get('history_score', np.random.rand())  # Stub
    inputs = torch.tensor([[amount, velocity, history]], dtype=torch.float32)
    
    with torch.no_grad():
        prob = model(inputs).item()
    
    return 'low' if prob < 0.4 else 'medium' if prob < 0.6 else 'high'

if __name__ == "__main__":
    print("Model trained. Example infer:", infer_risk({"amount": 75000, "velocity": 0.2, "history_score": 0.8}))
