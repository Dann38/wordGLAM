import torch
from torch.nn import Linear, BCELoss, BCEWithLogitsLoss, CrossEntropyLoss, GELU, HuberLoss
from torch.nn.functional import relu
from torch_geometric.nn import BatchNorm, TAGConv
from typing import List


class NodeGLAM(torch.nn.Module):
    def __init__(self,  input_, h, output_):
        super(NodeGLAM, self).__init__()
        self.activation = GELU()
        self.batch_norm1 = BatchNorm(input_)

        self.linear1 = Linear(input_, h[0]) 
        self.tag1 = TAGConv(h[0], h[1])

        self.linear2 = Linear(h[1], h[2]) 
        self.tag2 = TAGConv(h[2], h[3])

        self.linear5 = Linear(h[3] +input_, h[4])
        self.linear6 =Linear(h[4], h[5])
        # self.classifer1 = Linear(h[5], output_)
        self.classifer1 = Linear(h[5], h[5]//2)
        self.classifer2 = Linear(h[5]//2, output_)

        

    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        x = self.batch_norm1(x)
        
        h = self.linear1(x)
        h = self.activation(h)
        h = self.tag1(h, edge_index)
        h = self.activation(h)
        
        h = self.linear2(h)
        h = self.activation(h)
        h = self.tag2(h, edge_index)
        h = self.activation(h)

        a = torch.cat([x, h], dim=1)
        a = self.linear5(a)
        a = self.activation(a)
        a = self.linear6(a)

        cl = self.classifer1(self.activation(a))
        cl = self.classifer2(self.activation(cl))
        cl = torch.softmax(cl, dim=-1)
        # a = torch.softmax(a, dim=-1)
        return a, cl

class EdgeGLAM(torch.nn.Module):
    def __init__(self, input_, h, output_):
        super(EdgeGLAM, self).__init__()
        self.activation = GELU()
        self.batch_norm2 = BatchNorm(input_, output_)
        self.linear1 = Linear(input_, h[0]) 
        # self.linear2 = Linear(h[0], output_)
        self.linear2 = Linear(h[0], h[0]//2)

        self.classifier1 = Linear(h[0]//2, h[0]//4)
        self.classifier2 = Linear(h[0]//4, output_)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.batch_norm2(x)
        h = self.linear1(x)
        h = self.linear2(self.activation(h))
        h = self.classifier1(self.activation(h))
        h = self.classifier2(self.activation(h))
        h = torch.sigmoid(h)
        return torch.squeeze(h, 1)

class CustomLoss(torch.nn.Module):
    def __init__(self, params):
        super(CustomLoss, self).__init__()
                    #BCELoss
        self.bce = BCEWithLogitsLoss(pos_weight=torch.tensor(params['edge_imbalance']))
        self.ce = CrossEntropyLoss(weight=torch.tensor(params['publaynet_imbalance']))
        self.edge_coef:float = params['edge_coef']
        self.node_coef:float = params['node_coef']

    def forward(self, n_pred, n_true, e_pred, e_true):
        loss = self.node_coef*self.ce(n_pred, n_true) + self.edge_coef*self.bce(e_pred, e_true)
        return loss

class TorchModel(torch.nn.Module):
    def __init__(self, params):
        super(TorchModel, self).__init__()
        self.node_emb = NodeGLAM(params["node_featch"], params["H1"], 5)
        self.bin_edge_emb = EdgeGLAM(2*params["node_featch"]+2*params["H1"][-1] + params["edge_featch"], params["H2"], 1)

    def forward(self, X: torch.Tensor, Y: torch.Tensor, sp_A: torch.Tensor, i:List[int]):
        Node_emb, Node_class = self.node_emb(X, sp_A)
        Omega = torch.cat([Node_emb[i[0]], Node_emb[i[1]], X[i[0]], X[i[1]], Y],dim=1)
        E_pred = self.bin_edge_emb(Omega)
        return Node_class, E_pred
    

