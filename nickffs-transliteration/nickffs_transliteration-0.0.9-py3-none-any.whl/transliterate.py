import torch
import torch.nn as nn
import torch.functional as F
import torch.optim as optim
import torchtext as tt
from torchtext.vocab import Vocab
from torch.nn.utils.rnn import pad_sequence, pad_packed_sequence
from torch.utils.data import DataLoader
import pickle

def load_vocab(path):
  '''
     You need the pickle files (.pkl) for this with only the vocab files
  '''
  output = open(path, 'rb')
  vocab = pickle.load(output)
  return vocab


def load_model(model_weights_path:str = "better2129Mar21.pt"):
    """
        Need the [hinglish_vocab.pkl, hindi_vocab.pkl] files in the same directory as the code
    """

    # imports()

    hi_en_char_vocab = load_vocab('hinglish_vocab.pkl')
    hi_char_vocab = load_vocab('hindi_vocab.pkl')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    class Encoder(nn.Module):
        def __init__(self, 
                    input_dim, 
                    hid_dim, 
                    n_layers, 
                    n_heads, 
                    pf_dim,
                    dropout, 
                    device,
                    max_length = 40):
            super().__init__()

            self.device = device
            
            self.tok_embedding = nn.Embedding(input_dim, hid_dim)
            self.pos_embedding = nn.Embedding(max_length, hid_dim)
            
            self.layers = nn.ModuleList([EncoderLayer(hid_dim, 
                                                    n_heads, 
                                                    pf_dim,
                                                    dropout, 
                                                    device) 
                                        for _ in range(n_layers)])
            
            self.dropout = nn.Dropout(dropout)
            
            self.scale = torch.sqrt(torch.FloatTensor([hid_dim])).to(device)
            
        def forward(self, src, src_mask):
            
            #src = [batch size, src len]
            #src_mask = [batch size, 1, 1, src len]
            
            batch_size = src.shape[0]
            src_len = src.shape[1]
            
            pos = torch.arange(0, src_len).unsqueeze(0).repeat(batch_size, 1).to(self.device)
            
            #pos = [batch size, src len]
            
            src = self.dropout((self.tok_embedding(src) * self.scale) + self.pos_embedding(pos))
            
            #src = [batch size, src len, hid dim]
            
            for layer in self.layers:
                src = layer(src, src_mask)
                
            #src = [batch size, src len, hid dim]
                
            return src

    class EncoderLayer(nn.Module):
        def __init__(self, 
                    hid_dim, 
                    n_heads, 
                    pf_dim,  
                    dropout, 
                    device):
            super().__init__()
            
            self.self_attn_layer_norm = nn.LayerNorm(hid_dim)
            self.ff_layer_norm = nn.LayerNorm(hid_dim)
            self.self_attention = MultiHeadAttentionLayer(hid_dim, n_heads, dropout, device)
            self.positionwise_feedforward = PositionwiseFeedforwardLayer(hid_dim, 
                                                                        pf_dim, 
                                                                        dropout)
            self.dropout = nn.Dropout(dropout)
            
        def forward(self, src, src_mask):
            
            #src = [batch size, src len, hid dim]
            #src_mask = [batch size, 1, 1, src len] 
                    
            #self attention
            _src, _ = self.self_attention(src, src, src, src_mask)
            
            #dropout, residual connection and layer norm
            src = self.self_attn_layer_norm(src + self.dropout(_src))
            
            #src = [batch size, src len, hid dim]
            
            #positionwise feedforward
            _src = self.positionwise_feedforward(src)
            
            #dropout, residual and layer norm
            src = self.ff_layer_norm(src + self.dropout(_src))
            
            #src = [batch size, src len, hid dim]
            
            return src

    class MultiHeadAttentionLayer(nn.Module):
        def __init__(self, hid_dim, n_heads, dropout, device):
            super().__init__()
            
            assert hid_dim % n_heads == 0
            
            self.hid_dim = hid_dim
            self.n_heads = n_heads
            self.head_dim = hid_dim // n_heads
            
            self.fc_q = nn.Linear(hid_dim, hid_dim)
            self.fc_k = nn.Linear(hid_dim, hid_dim)
            self.fc_v = nn.Linear(hid_dim, hid_dim)
            
            self.fc_o = nn.Linear(hid_dim, hid_dim)
            
            self.dropout = nn.Dropout(dropout)
            
            self.scale = torch.sqrt(torch.FloatTensor([self.head_dim])).to(device)
            
        def forward(self, query, key, value, mask = None):
            
            batch_size = query.shape[0]
            
            #query = [batch size, query len, hid dim]
            #key = [batch size, key len, hid dim]
            #value = [batch size, value len, hid dim]
                    
            Q = self.fc_q(query)
            K = self.fc_k(key)
            V = self.fc_v(value)
            
            #Q = [batch size, query len, hid dim]
            #K = [batch size, key len, hid dim]
            #V = [batch size, value len, hid dim]
                    
            Q = Q.view(batch_size, -1, self.n_heads, self.head_dim).permute(0, 2, 1, 3)
            K = K.view(batch_size, -1, self.n_heads, self.head_dim).permute(0, 2, 1, 3)
            V = V.view(batch_size, -1, self.n_heads, self.head_dim).permute(0, 2, 1, 3)
            
            #Q = [batch size, n heads, query len, head dim]
            #K = [batch size, n heads, key len, head dim]
            #V = [batch size, n heads, value len, head dim]
                    
            energy = torch.matmul(Q, K.permute(0, 1, 3, 2)) / self.scale
            
            #energy = [batch size, n heads, query len, key len]
            
            if mask is not None:
                energy = energy.masked_fill(mask == 0, -1e10)
            
            attention = torch.softmax(energy, dim = -1)
                    
            #attention = [batch size, n heads, query len, key len]
                    
            x = torch.matmul(self.dropout(attention), V)
            
            #x = [batch size, n heads, query len, head dim]
            
            x = x.permute(0, 2, 1, 3).contiguous()
            
            #x = [batch size, query len, n heads, head dim]
            
            x = x.view(batch_size, -1, self.hid_dim)
            
            #x = [batch size, query len, hid dim]
            
            x = self.fc_o(x)
            
            #x = [batch size, query len, hid dim]
            
            return x, attention

    class PositionwiseFeedforwardLayer(nn.Module):
        def __init__(self, hid_dim, pf_dim, dropout):
            super().__init__()
            
            self.fc_1 = nn.Linear(hid_dim, pf_dim)
            self.fc_2 = nn.Linear(pf_dim, hid_dim)
            
            self.dropout = nn.Dropout(dropout)
            
        def forward(self, x):
            
            #x = [batch size, seq len, hid dim]
            
            x = self.dropout(torch.relu(self.fc_1(x)))
            
            #x = [batch size, seq len, pf dim]
            
            x = self.fc_2(x)
            
            #x = [batch size, seq len, hid dim]
            
            return x

    class Decoder(nn.Module):
        def __init__(self, 
                    output_dim, 
                    hid_dim, 
                    n_layers, 
                    n_heads, 
                    pf_dim, 
                    dropout, 
                    device,
                    max_length = 40):
            super().__init__()
            
            self.device = device
            
            self.tok_embedding = nn.Embedding(output_dim, hid_dim)
            self.pos_embedding = nn.Embedding(max_length, hid_dim)
            
            self.layers = nn.ModuleList([DecoderLayer(hid_dim, 
                                                    n_heads, 
                                                    pf_dim, 
                                                    dropout, 
                                                    device)
                                        for _ in range(n_layers)])
            
            self.fc_out = nn.Linear(hid_dim, output_dim)
            
            self.dropout = nn.Dropout(dropout)
            
            self.scale = torch.sqrt(torch.FloatTensor([hid_dim])).to(device)
            
        def forward(self, trg, enc_src, trg_mask, src_mask):
            
            #trg = [batch size, trg len]
            #enc_src = [batch size, src len, hid dim]
            #trg_mask = [batch size, 1, trg len, trg len]
            #src_mask = [batch size, 1, 1, src len]
                    
            batch_size = trg.shape[0]
            trg_len = trg.shape[1]
            
            pos = torch.arange(0, trg_len).unsqueeze(0).repeat(batch_size, 1).to(self.device)
                                
            #pos = [batch size, trg len]
                
            trg = self.dropout((self.tok_embedding(trg) * self.scale) + self.pos_embedding(pos))
                    
            #trg = [batch size, trg len, hid dim]
            
            for layer in self.layers:
                trg, attention = layer(trg, enc_src, trg_mask, src_mask)
            
            #trg = [batch size, trg len, hid dim]
            #attention = [batch size, n heads, trg len, src len]
            
            output = self.fc_out(trg)
            
            #output = [batch size, trg len, output dim]
                
            return output, attention

    class DecoderLayer(nn.Module):
        def __init__(self, 
                    hid_dim, 
                    n_heads, 
                    pf_dim, 
                    dropout, 
                    device):
            super().__init__()
            
            self.self_attn_layer_norm = nn.LayerNorm(hid_dim)
            self.enc_attn_layer_norm = nn.LayerNorm(hid_dim)
            self.ff_layer_norm = nn.LayerNorm(hid_dim)
            self.self_attention = MultiHeadAttentionLayer(hid_dim, n_heads, dropout, device)
            self.encoder_attention = MultiHeadAttentionLayer(hid_dim, n_heads, dropout, device)
            self.positionwise_feedforward = PositionwiseFeedforwardLayer(hid_dim, 
                                                                        pf_dim, 
                                                                        dropout)
            self.dropout = nn.Dropout(dropout)
            
        def forward(self, trg, enc_src, trg_mask, src_mask):
            
            #trg = [batch size, trg len, hid dim]
            #enc_src = [batch size, src len, hid dim]
            #trg_mask = [batch size, 1, trg len, trg len]
            #src_mask = [batch size, 1, 1, src len]
            
            #self attention
            _trg, _ = self.self_attention(trg, trg, trg, trg_mask)
            
            #dropout, residual connection and layer norm
            trg = self.self_attn_layer_norm(trg + self.dropout(_trg))
                
            #trg = [batch size, trg len, hid dim]
                
            #encoder attention
            _trg, attention = self.encoder_attention(trg, enc_src, enc_src, src_mask)
            
            #dropout, residual connection and layer norm
            trg = self.enc_attn_layer_norm(trg + self.dropout(_trg))
                        
            #trg = [batch size, trg len, hid dim]
            
            #positionwise feedforward
            _trg = self.positionwise_feedforward(trg)
            
            #dropout, residual and layer norm
            trg = self.ff_layer_norm(trg + self.dropout(_trg))
            
            #trg = [batch size, trg len, hid dim]
            #attention = [batch size, n heads, trg len, src len]
            
            return trg, attention

    class Seq2Seq(nn.Module):
        def __init__(self, 
                    encoder, 
                    decoder, 
                    src_pad_idx, 
                    trg_pad_idx, 
                    device):
            super().__init__()
            
            self.encoder = encoder
            self.decoder = decoder
            self.src_pad_idx = src_pad_idx
            self.trg_pad_idx = trg_pad_idx
            self.device = device
            
        def make_src_mask(self, src):
            
            #src = [batch size, src len]
            
            # src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)

            src_mask = torch.ones_like(src).unsqueeze(1).unsqueeze(2)

            #src_mask = [batch size, 1, 1, src len]

            return src_mask
        
        def make_trg_mask(self, trg):
            
            #trg = [batch size, trg len]
            
            # trg_pad_mask = (trg != self.trg_pad_idx).unsqueeze(1).unsqueeze(2)

            trg_pad_mask = torch.ones_like(trg).unsqueeze(1).unsqueeze(2)
            
            #trg_pad_mask = [batch size, 1, 1, trg len]
            
            trg_len = trg.shape[1]
            
            trg_sub_mask = torch.tril(torch.ones((trg_len, trg_len), device = self.device)).bool()
            
            #trg_sub_mask = [trg len, trg len]
                
            trg_mask = trg_pad_mask & trg_sub_mask
            
            #trg_mask = [batch size, 1, trg len, trg len]
            
            return trg_mask

        def forward(self, src, trg):
            
            #src = [batch size, src len]
            #trg = [batch size, trg len]
                    
            src_mask = self.make_src_mask(src)
            trg_mask = self.make_trg_mask(trg)
            
            #src_mask = [batch size, 1, 1, src len]
            #trg_mask = [batch size, 1, trg len, trg len]
            
            enc_src = self.encoder(src, src_mask)
            
            #enc_src = [batch size, src len, hid dim]
                    
            output, attention = self.decoder(trg, enc_src, trg_mask, src_mask)
            
            #output = [batch size, trg len, output dim]
            #attention = [batch size, n heads, trg len, src len]
            
            return output, attention

    INPUT_DIM = len(hi_en_char_vocab)
    OUTPUT_DIM = len(hi_char_vocab)
    HID_DIM = 256
    ENC_LAYERS = 4
    DEC_LAYERS = 4
    ENC_HEADS = 8
    DEC_HEADS = 8
    ENC_PF_DIM = 512
    DEC_PF_DIM = 512
    ENC_DROPOUT = 0.1
    DEC_DROPOUT = 0.1

    enc = Encoder(INPUT_DIM, 
                HID_DIM, 
                ENC_LAYERS, 
                ENC_HEADS, 
                ENC_PF_DIM, 
                ENC_DROPOUT, 
                device)

    dec = Decoder(OUTPUT_DIM, 
                HID_DIM, 
                DEC_LAYERS, 
                DEC_HEADS, 
                DEC_PF_DIM, 
                DEC_DROPOUT, 
                device)

    SRC_PAD_IDX = hi_en_char_vocab.stoi['<pad>']
    TRG_PAD_IDX = hi_char_vocab.stoi['<pad>']

    model = Seq2Seq(enc, dec, SRC_PAD_IDX, TRG_PAD_IDX, device).to(device)

    model.load_state_dict(torch.load(model_weights_path, map_location=device))

    return model, hi_char_vocab, hi_en_char_vocab, device




class Translit():
    def __init__(self, model_weights_path:str = "better2129Mar21.pt"):
        self.model, self.hi_char_vocab, self.hi_en_char_vocab, self.device = load_model(model_weights_path)

    def transliterate(self, word:str):
        def tokenize(word):
            '''
                Tokenize the words
            '''
            return [c for c in word.lower()]
        

        def transliterate_word (word, src_vocab, trg_vocab, model, device, max_len = 40):
            model.eval()
                
            if isinstance(word, str):
                tokens = tokenize(word)
            else:
                tokens = [token.lower() for token in word]

            tokens = ['<sos>'] + tokens + ['<eos>']
                
            src_indexes = [src_vocab.stoi[token] for token in tokens]

            src_tensor = torch.LongTensor(src_indexes).unsqueeze(0).to(device)
            
            src_mask = model.make_src_mask(src_tensor).to(device)
            
            with torch.no_grad():
                enc_src = model.encoder(src_tensor, src_mask).to(device)

            trg_indexes = [trg_vocab.stoi['<sos>']]

            for i in range(max_len):

                trg_tensor = torch.LongTensor(trg_indexes).unsqueeze(0).to(device)

                trg_mask = model.make_trg_mask(trg_tensor).to(device)
                
                with torch.no_grad():
                    output, attention = model.decoder(trg_tensor, enc_src, trg_mask, src_mask)
                
                pred_token = output.argmax(2)[:,-1].item()
                
                trg_indexes.append(pred_token)

                if pred_token == trg_vocab.stoi['<eos>']:
                    break

            trg_tokens = [trg_vocab.itos[i] for i in trg_indexes]
            return trg_tokens[1:]

        res = transliterate_word(word, self.hi_en_char_vocab, self.hi_char_vocab, self.model, self.device, max_len = 40)

        if res[-1] == '<eos>':
            return "".join(res[:-1])
        return "".join(res)