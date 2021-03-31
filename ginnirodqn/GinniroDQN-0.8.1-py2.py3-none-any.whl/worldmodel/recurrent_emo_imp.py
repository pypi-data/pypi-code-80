import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.autograd import Variable

class AttentionGRUCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(AttentionGRUCell, self).__init__()
        self.hidden_size = hidden_size

        self.Wr = nn.Linear(input_size, hidden_size)
        torch.nn.init.xavier_normal_(self.Wr.state_dict()['weight'])

        self.Ur = nn.Linear(hidden_size, hidden_size)
        torch.nn.init.xavier_normal_(self.Ur.state_dict()['weight'])

        self.W = nn.Linear(input_size, hidden_size)
        torch.nn.init.xavier_normal_(self.W.state_dict()['weight'])

        self.U = nn.Linear(hidden_size, hidden_size)
        torch.nn.init.xavier_normal_(self.U.state_dict()['weight'])

    def forward(self, fact, C, g):
        r = torch.sigmoid(self.Wr(fact) + self.Ur(C))
        h_tilda = torch.tanh(self.W(fact) + r * self.U(C))
        g = g.unsqueeze(1).expand_as(h_tilda)
        h = g * h_tilda + (1-g) * C
        return h

class AttentionGRU(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(AttentionGRU, self).__init__()
        self.hidden_size = hidden_size
        self.AGRUCell = AttentionGRUCell(input_size, hidden_size)

    def forward(self, facts, G):
        batch_num, sen_num, embedding_size = facts.size()
        C = Variable(torch.zeros(self.hidden_size))
        for sid in range(sen_num):
            fact = facts[:, sid, :]
            g = G[:, sid]
            if sid == 0:
                # C = C.unsqueeze(0).expand_as(fact)
                C = Variable(torch.zeros(batch_num, self.hidden_size))
            C = self.AGRUCell(fact, C, g)
        return C

class MemoryNet(nn.Module):
    def __init__(self, feature_size, hidden_size):
        super(MemoryNet, self).__init__()
        self.AGRU = AttentionGRU(feature_size, hidden_size)

        self.z1 = nn.Linear(2 * feature_size, hidden_size)
        self.z2 = nn.Linear(hidden_size, 1)
        self.next_mem = nn.Linear(feature_size + hidden_size, hidden_size)
        torch.nn.init.xavier_normal_(self.z1.state_dict()['weight'])
        torch.nn.init.xavier_normal_(self.z2.state_dict()['weight'])
        torch.nn.init.xavier_normal_(self.next_mem.state_dict()['weight'])

    def make_interaction(self, facts, questions):
        # facts.size() -> (#batch, #sentence, #hidden = #input_size)
        # questions.size() -> (#batch, 1, #hidden)
        # prevM.size() -> (#batch, #sentence=1, #hidden = #input_size)
        # z.size() -> (#batch, #sentence, 4 * #input_size)
        # G.size() -> (#batch, #sentence)

        batch_num, sen_num, embedding_size = facts.size()
        questions = questions.expand_as(facts)

        z = torch.cat([
            facts * questions,
            torch.abs(facts - questions)], dim=2)
        z = z.view(-1, 2 * embedding_size)

        G = torch.tanh(self.z1(z))
        G = self.z2(G)
        G = G.view(batch_num, -1)
        G = torch.softmax(G, dim=-1)

        return G

    def forward(self, facts, questions):
        # facts.size() -> (#batch, #sentence, #hidden=#embedding)
        # questions.size() -> (#batch, #sentence=1, #hidden)
        # prevM.size() -> (#batch, #sentence=1, #hidden)
        # G.size() -> (#batch, #sentence)
        # C.size() -> (#batch, #hidden)
        # concat.size() -> (#batch, 3 * #hidden)

        G = self.make_interaction(facts, questions)
        C = self.AGRU(facts, G)

        concat = torch.cat([C, questions.squeeze(1)], dim=1)

        next_mem = F.relu(self.next_mem(concat))
        return next_mem

class RecurrentEmoWorldModel(nn.Module):

    def __init__(self,
                 agent_action_size,
                 hidden_size,
                 state_size,
                 user_action_size,
                 reward_size=1,
                 termination_size=1,
                 goal_hidden_size=1,
                 his_hidden_size=1,
                 emotion_size=4):

        super(RecurrentEmoWorldModel, self).__init__()

        self.hidden_size = hidden_size

        self.dmn = MemoryNet(feature_size=his_hidden_size, hidden_size=hidden_size)

        self.linear_g2q = nn.Linear(goal_hidden_size, his_hidden_size)

        self.linear_i2h = nn.Linear(state_size+goal_hidden_size, hidden_size)
        self.agent_emb = nn.Embedding(agent_action_size, hidden_size)

        self.linear_h2r = nn.Linear(hidden_size*2, reward_size)
        self.linear_h2t = nn.Linear(hidden_size*2, termination_size)
        self.linear_h2a = nn.Linear(hidden_size*2, user_action_size)
        self.linear_h2e = nn.Linear(hidden_size*2, emotion_size)

    def initHidden(self, s):
        batch_size, _ = s.shape

        return torch.zeros([batch_size, self.hidden_size])

    def forward(self, s, g, a, his):

        s = torch.cat([s, g], dim=1)

        question = self.linear_g2q(g).unsqueeze(1)
        his_mem = self.dmn(his, question)

        h_s = self.linear_i2h(s)
        h_a = self.agent_emb(a).squeeze(1)

        h = F.tanh(torch.cat([h_s+h_a, his_mem], dim=-1))

        reward = self.linear_h2r(h)
        term = self.linear_h2t(h)
        action = F.log_softmax(self.linear_h2a(h), 1)
        emo_state = F.sigmoid(self.linear_h2e(h))

        return reward, term, action, emo_state

    def predict(self, s, g, a, his):

        with torch.no_grad():
            reward, term, action, emo_state = self.forward(s, g, a, his)

        return reward, torch.sigmoid(term), action.argmax(1), emo_state