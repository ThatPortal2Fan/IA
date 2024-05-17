# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 104:
# 106037 Gonçalo Rocha
# 106713 Martim Ferreira

import sys
from sys import stdin
from utils import np
from search import (
    Problem
)

pointdown = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
pointup = ["FC", "BC", "BE", "BD", "VD", "VC", "LV"]
pointleft = ["FE", "BB", "BE", "BC", "VC", "VE", "LH"]
pointright = ["FD", "BB", "BD", "BC", "VB", "VD", "LH"]

fontes=["FC","FD","FB","FE"]
bifurcacoes=["BC","BD","BB","BE"]
voltas=["VC","VD","VB","VE"]
ligacoes=["LH","LV"]


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem,b):
        """List the nodes reachable in one step from this node."""
        actions = problem.actions(self.state,b)
        lista = [[]]*len(actions)
        i=0
        for action in actions:
            lista[i]=[self.child_node(problem, action),b]
            i+=1
        return lista

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    
    def __init__(self, board):
        self.board = board
        self.tamanho = len(board)
        self.possibilidades = [[]]*len(board)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[int(np.sqrt(self.tamanho)*row+col)]
        
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if (row==0):
            return ("None",self.board[int(np.sqrt(self.tamanho)*(row+1)+col)])
        elif (row==np.sqrt(self.tamanho)-1):
            return (self.board[int(np.sqrt(self.tamanho)*(row-1)+col)],"None")
        return (self.board[int(np.sqrt(self.tamanho)*(row-1)+col)],self.board[int(np.sqrt(self.tamanho)*(row+1)+col)])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if (col==0):
            return ("None",self.board[int(np.sqrt(self.tamanho)*row+col+1)])
        elif (col==np.sqrt(self.tamanho)-1):
            return (self.board[int(np.sqrt(self.tamanho)*row+col-1)],"None")
        return (self.board[int(np.sqrt(self.tamanho)*row+col-1)],self.board[int(np.sqrt(self.tamanho)*row+1+col)])

    @staticmethod
    def parse_instance():
        
        line = stdin.read().split()
        
        return Board(line)

    def show(self):
        tamanho=self.tamanho
        lado=np.sqrt(tamanho)
        line=-1
        result = ""
        for i in range(tamanho):
            if (i%lado==0):
                line+=1
                if(i!=0):
                    result += "\n"
            if (i%lado == lado-1):
                result += self.get_value(line,i%lado)
            else:
                result += self.get_value(line,i%lado)+"\t"
        return result

    def change_piece(self, row: int, col: int,change ):
        self.board[int(np.sqrt(self.tamanho)*row+col)]=change

    def get_board(self):
        return self.board
    # TODO: outros metodos da classe

    def draw(self):
        lado=int(np.sqrt(self.tamanho))
        result = ""
        for i in range(lado):
            for j in range(lado):
                if len(self.possibilidades[lado*i+j]) == 1:
                    if self.get_value(i,j) == "FC":
                        result += u'\u2568'
                    elif self.get_value(i,j) == "FB":
                        result += u'\u2565'
                    elif self.get_value(i,j) == "FE":
                        result += u'\u2561'
                    elif self.get_value(i,j) == "FD":
                        result += u'\u255e'
                    elif self.get_value(i,j) == "BC":
                        result += u'\u2569'
                    elif self.get_value(i,j) == "BB":
                        result += u'\u2566'
                    elif self.get_value(i,j) == "BE":
                        result += u'\u2563'
                    elif self.get_value(i,j) == "BD":
                        result += u'\u2560'
                    elif self.get_value(i,j) == "VC":
                        result += u'\u255d'
                    elif self.get_value(i,j) == "VB":
                        result += u'\u2554'
                    elif self.get_value(i,j) == "VE":
                        result += u'\u2557'
                    elif self.get_value(i,j) == "VD":
                        result += u'\u255a'
                    elif self.get_value(i,j) == "LH":
                        result += u'\u2550'
                    elif self.get_value(i,j) == "LV":
                        result += u'\u2551'
                else:
                    result += " "
            result+="\n"
        return result

class PipeManiaState:
    state_id = 0

    def __init__(self, board, possibilidades):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.board.possibilidades = possibilidades


    def __lt__(self, other):
        return self.id < other.id

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[int(np.sqrt(self.board.tamanho)*row+col)]
    
    def DFS_visit(self, board: Board, row, col, visit):
        position = int(np.sqrt(board.tamanho)*row+col)

        last = int(np.sqrt(board.tamanho))-1
        
        visit[position] = 1
        
        if board.get_value(row, col) == "FC":
            if row == 0 or board.get_value(row-1, col) not in pointdown:
                return False
            elif visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                if not self.DFS_visit(board, row-1, col, visit):
                    return False
        elif board.get_value(row, col) == "FB":
            if row == last or board.get_value(row+1, col) not in pointup:
                return False
            elif visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                if not self.DFS_visit(board, row+1, col, visit):
                    return False
        elif board.get_value(row, col) == "FE":
            if col == 0 or board.get_value(row, col-1) not in pointright:
                return False
            elif visit[int(np.sqrt(board.tamanho)*(row)+col-1)] == 0:
                if not self.DFS_visit(board, row, col-1, visit):
                    return False
        elif board.get_value(row, col) == "FD":
            if col == last or board.get_value(row, col+1) not in pointleft:
                return False
            elif visit[int(np.sqrt(board.tamanho)*(row)+col+1)] == 0:
                if not self.DFS_visit(board, row, col+1, visit):
                    return False
        elif board.get_value(row, col) == "BC":
            if col == last or row == 0 or col == 0 or board.get_value(row-1, col) not in pointdown or board.get_value(row, col-1) not in pointright or board.get_value(row, col+1) not in pointleft:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                    if not self.DFS_visit(board, row-1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col-1)] == 0:
                    if not self.DFS_visit(board, row, col-1, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col+1)] == 0:
                    if not self.DFS_visit(board, row, col+1, visit):
                        return False
        elif board.get_value(row, col) == "BB":
            if row == last or col == last or col == 0 or board.get_value(row+1, col) not in pointup or board.get_value(row, col-1) not in pointright or board.get_value(row, col+1) not in pointleft:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                    if not self.DFS_visit(board, row+1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col-1)] == 0:
                    if not self.DFS_visit(board, row, col-1, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col+1)] == 0:
                    if not self.DFS_visit(board, row, col+1, visit):
                        return False
        elif board.get_value(row, col) == "BE":
            if row == last or row == 0 or col == 0 or board.get_value(row-1, col) not in pointdown or board.get_value(row+1, col) not in pointup or board.get_value(row, col-1) not in pointright:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                    if not self.DFS_visit(board, row-1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                    if not self.DFS_visit(board, row+1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col-1)] == 0:
                    if not self.DFS_visit(board, row, col-1, visit):
                        return False
        elif board.get_value(row, col) == "BD":
            if row == last or row == 0 or col == last or board.get_value(row-1, col) not in pointdown or board.get_value(row, col+1) not in pointleft or board.get_value(row+1, col) not in pointup:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                    if not self.DFS_visit(board, row-1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                    if not self.DFS_visit(board, row+1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col+1)] == 0:
                    if not self.DFS_visit(board, row, col+1, visit):
                        return False
        elif board.get_value(row, col) == "VC":
            if row == 0 or col == 0 or board.get_value(row-1, col) not in pointdown or board.get_value(row, col-1) not in pointright:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                    if not self.DFS_visit(board, row-1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col-1)] == 0:
                    if not self.DFS_visit(board, row, col-1, visit):
                        return False
        elif board.get_value(row, col) == "VB":
            if row == last or col == last or board.get_value(row+1, col) not in pointup or board.get_value(row, col+1) not in pointleft:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                    if not self.DFS_visit(board, row+1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col+1)] == 0:
                    if not self.DFS_visit(board, row, col+1, visit):
                        return False
        elif board.get_value(row, col) == "VE":
            if row == last or col == 0 or board.get_value(row+1, col) not in pointup or board.get_value(row, col-1) not in pointright:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                    if not self.DFS_visit(board, row+1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col-1)] == 0:
                    if not self.DFS_visit(board, row, col-1, visit):
                        return False
        elif board.get_value(row, col) == "VD":
            if row == 0 or col == last or board.get_value(row-1, col) not in pointdown or board.get_value(row, col+1) not in pointleft:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                    if not self.DFS_visit(board, row-1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col+1)] == 0:
                    if not self.DFS_visit(board, row, col+1, visit):
                        return False
        elif board.get_value(row, col) == "LV":
            if row == 0 or row == last or board.get_value(row-1, col) not in pointdown or board.get_value(row+1, col) not in pointup:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*(row-1)+col)] == 0:
                    if not self.DFS_visit(board, row-1, col, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*(row+1)+col)] == 0:
                    if not self.DFS_visit(board, row+1, col, visit):
                        return False
        elif board.get_value(row, col) == "LH":
            if col == 0 or col == last or board.get_value(row, col-1) not in pointright or board.get_value(row, col+1) not in pointleft:
                return False
            else:
                if visit[int(np.sqrt(board.tamanho)*row+col-1)] == 0:
                    if not self.DFS_visit(board, row, col-1, visit):
                        return False
                if visit[int(np.sqrt(board.tamanho)*row+col+1)] == 0:
                    if not self.DFS_visit(board, row, col+1, visit):
                        return False
        
        
        visit[position] = 2
        return True
    
    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board=board
        self.initial = PipeManiaState(Board(board.get_board().copy()), [[]]*len(board.get_board()))

    def actions(self, state: PipeManiaState,b: int): #mudar actions para tuplo com row, col e possibilidades para a peça
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        lista=[]
        counter=-1
        for v in range(self.board.tamanho):
            if len(self.initial.board.possibilidades[v])>1:
                counter+=1
                row = v//int(np.sqrt(self.board.tamanho))
                col = v%int(np.sqrt(self.board.tamanho))
                if counter==b:
                    for i in state.board.possibilidades[v]:
                        lista.append((row,col,i))
        
        return lista

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_possibilidades = [[]]*state.board.tamanho
        i = 0
        for v in state.board.possibilidades:
            new_possibilidades[i] = v.copy()
            i+=1
        new_state=PipeManiaState(Board(state.board.get_board().copy()), new_possibilidades)
        new_state.board.change_piece(action[0],action[1],action[2])
        new_state.board.possibilidades[int(np.sqrt(new_state.board.tamanho)*action[0]+action[1])]=[new_state.board.get_value(action[0],action[1])]
        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        visit = []
        for v in state.board.get_board():
            visit.append(0) # 0: não visitado, 1: visitado, 2: fechado
        state.DFS_visit(state.board, 0, 0, visit)
        for v in visit:
            if v != 2:
                return False
        return True
    
    def fix_sides(self):
        last = int(np.sqrt(self.board.tamanho))-1

        for v in range(self.board.tamanho):
            row = v//int(np.sqrt(self.board.tamanho))
            col = v%int(np.sqrt(self.board.tamanho))
            if row == 0 or col == 0 or row == last or col == last:
                if row == 0 and col == 0 and self.board.get_value(row, col) in voltas:
                    self.board.change_piece(row, col, "VB")
                    self.board.possibilidades[v] = ["VB"]
                elif row == 0 and col == 0 and self.board.get_value(row, col) in fontes:
                    self.board.change_piece(row, col, "FD")
                    self.board.possibilidades[v] = ["FD", "FB"]
                elif row == 0 and col == last and self.board.get_value(row, col) in voltas:
                    self.board.change_piece(row, col, "VE")
                    self.board.possibilidades[v] = ["VE"]
                elif row == 0 and col == last and self.board.get_value(row, col) in fontes:
                    self.board.change_piece(row, col, "FB")
                    self.board.possibilidades[v] = ["FB","FE"]
                elif row == last and col == last and self.board.get_value(row, col) in voltas:
                    self.board.change_piece(row, col, "VC")
                    self.board.possibilidades[v] = ["VC"]
                elif row == last and col == last and self.board.get_value(row, col) in fontes:
                    self.board.change_piece(row, col, "FE")
                    self.board.possibilidades[v] = ["FE","FC"]
                elif row == last and col == 0 and self.board.get_value(row, col) in voltas:
                    self.board.change_piece(row, col, "VD")
                    self.board.possibilidades[v] = ["VD"]
                elif row == last and col == 0 and self.board.get_value(row, col) in fontes:
                    self.board.change_piece(row, col, "FC")
                    self.board.possibilidades[v] = ["FC","FD"]
                elif row == 0 and self.board.get_value(row, col) in bifurcacoes:
                    self.board.change_piece(row, col, "BB")
                    self.board.possibilidades[v] = ["BB"]
                elif row == 0 and self.board.get_value(row, col) in ligacoes:
                    self.board.change_piece(row, col, "LH")
                    self.board.possibilidades[v] = ["LH"]
                elif row == 0 and self.board.get_value(row,col) in voltas:
                    self.board.change_piece(row, col, "VB")
                    self.board.possibilidades[v] = ["VB","VE"]
                elif row == 0 and self.board.get_value(row,col) in fontes:
                    self.board.change_piece(row, col, "FB")
                    self.board.possibilidades[v] = ["FE","FB","FD"]
                elif row == last and self.board.get_value(row, col) in bifurcacoes:
                    self.board.change_piece(row, col, "BC")
                    self.board.possibilidades[v] = ["BC"]
                elif row == last and self.board.get_value(row, col) in ligacoes:
                    self.board.change_piece(row, col, "LH")
                    self.board.possibilidades[v] = ["LH"]
                elif row == last and self.board.get_value(row,col) in voltas:
                    self.board.change_piece(row, col, "VC")
                    self.board.possibilidades[v] = ["VC","VD"]
                elif row == last and self.board.get_value(row,col) in fontes:
                    self.board.change_piece(row, col, "FC")
                    self.board.possibilidades[v] = ["FC","FE","FD"]
                elif col == 0 and self.board.get_value(row, col) in bifurcacoes:
                    self.board.change_piece(row, col, "BD")
                    self.board.possibilidades[v] = ["BD"]
                elif col == 0 and self.board.get_value(row, col) in ligacoes:
                    self.board.change_piece(row, col, "LV")
                    self.board.possibilidades[v] = ["LV"]
                elif col == 0 and self.board.get_value(row,col) in voltas:
                    self.board.change_piece(row, col, "VD")
                    self.board.possibilidades[v] = ["VD", "VB"]
                elif col == 0 and self.board.get_value(row,col) in fontes:
                    self.board.change_piece(row, col, "FD")
                    self.board.possibilidades[v] = ["FD","FC","FB"]
                elif col == last and self.board.get_value(row, col) in bifurcacoes:
                    self.board.change_piece(row, col, "BE")
                    self.board.possibilidades[v] = ["BE"]
                elif col == last and self.board.get_value(row, col) in ligacoes:
                    self.board.change_piece(row, col, "LV")
                    self.board.possibilidades[v] = ["LV"]
                elif col == last and self.board.get_value(row,col) in voltas:
                    self.board.change_piece(row, col, "VE")
                    self.board.possibilidades[v] = ["VE","VC"]
                elif col == last and self.board.get_value(row,col) in fontes:
                    self.board.change_piece(row, col, "FE")
                    self.board.possibilidades[v] = ["FE","FC","FB"]
        self.initial = PipeManiaState(Board(self.board.get_board().copy()), self.board.possibilidades)

    def define_possibilities(self):
        for v in range(self.board.tamanho):
            row = v//int(np.sqrt(self.board.tamanho))
            col = v%int(np.sqrt(self.board.tamanho))
            if self.board.get_value(row,col) in fontes:
                self.board.possibilidades[v] = fontes.copy()
            elif self.board.get_value(row,col) in voltas:
                self.board.possibilidades[v] = voltas.copy()
            elif self.board.get_value(row,col) in bifurcacoes:
                self.board.possibilidades[v] = bifurcacoes.copy()
            elif self.board.get_value(row,col) in ligacoes:
                self.board.possibilidades[v] = ligacoes.copy()
    
 
    def infer_position(self, row, col,state: PipeManiaState):
        changes = False
        side = int(np.sqrt(state.board.tamanho))
        last = side-1
        if state.board.get_value(row, col) in fontes:
            # cima
            if row != 0 and (len(state.board.possibilidades[side*(row-1)+col]) == 1 or (state.board.get_value(row-1, col) in voltas and len(state.board.possibilidades[side*(row-1)+col]) == 2)):
                if (len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) in pointdown) or (state.board.get_value(row-1, col) in voltas and "VC" not in state.board.possibilidades[side*(row-1)+col] and "VD" not in state.board.possibilidades[side*(row-1)+col]):
                    state.board.change_piece(row,col,"FC")
                    state.board.possibilidades[side*row+col] = ["FC"]
                    return True
                elif "FC" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) not in pointdown) or (state.board.get_value(row-1, col) in voltas and "VB" not in state.board.possibilidades[side*(row-1)+col] and "VE" not in state.board.possibilidades[side*(row-1)+col])):
                    state.board.possibilidades[side*row+col].remove("FC")
                    if state.board.get_value(row,col) == "FC" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            # baixo
            if row != last and (len(state.board.possibilidades[side*(row+1)+col]) == 1 or state.board.get_value(row+1, col) in voltas and len(state.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) in pointup) or (state.board.get_value(row+1, col) in voltas and "VB" not in state.board.possibilidades[side*(row+1)+col] and "VE" not in state.board.possibilidades[side*(row+1)+col]):
                    state.board.change_piece(row,col,"FB")
                    state.board.possibilidades[side*row+col] = ["FB"]
                    return True
                elif "FB" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) not in pointup) or (state.board.get_value(row+1, col) in voltas and "VC" not in state.board.possibilidades[side*(row+1)+col] and "VD" not in state.board.possibilidades[side*(row+1)+col])):
                    state.board.possibilidades[side*row+col].remove("FB")
                    if state.board.get_value(row,col) == "FB" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            # esquerda
            if col != 0 and (len(state.board.possibilidades[side*row+col-1]) == 1 or state.board.get_value(row, col-1) in voltas and len(state.board.possibilidades[side*row+col-1]) == 2):
                if (len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) in pointright) or (state.board.get_value(row, col-1) in voltas and "VC" not in state.board.possibilidades[side*row+col-1] and "VE" not in state.board.possibilidades[side*row+col-1]):
                    state.board.change_piece(row,col,"FE")
                    state.board.possibilidades[side*row+col] = ["FE"]
                    return True
                elif "FE" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) not in pointright) or (state.board.get_value(row, col-1) in voltas and "VB" not in state.board.possibilidades[side*row+col-1] and "VD" not in state.board.possibilidades[side*row+col-1])):
                    state.board.possibilidades[side*row+col].remove("FE")
                    if state.board.get_value(row,col) == "FE" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            # direita
            if col != last and (len(state.board.possibilidades[side*row+col+1]) == 1 or state.board.get_value(row, col+1) in voltas and len(state.board.possibilidades[side*row+col+1]) == 2):
                if (len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) in pointleft) or (state.board.get_value(row, col+1) in voltas and "VD" not in state.board.possibilidades[side*row+col+1] and "VB" not in state.board.possibilidades[side*row+col+1]):
                    state.board.change_piece(row,col,"FD")
                    state.board.possibilidades[side*row+col] = ["FD"]
                    return True
                elif "FD" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) not in pointleft) or (state.board.get_value(row, col+1) in voltas and "VC" not in state.board.possibilidades[side*row+col+1] and "VE" not in state.board.possibilidades[side*row+col+1])):
                    state.board.possibilidades[side*row+col].remove("FD")
                    if state.board.get_value(row,col) == "FD" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
        elif state.board.get_value(row, col) in bifurcacoes:
            #cima
            if len(state.board.possibilidades[side*(row+1)+col]) == 1 or (state.board.get_value(row+1, col) in voltas and len(state.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) not in pointup) or (state.board.get_value(row+1, col) in voltas and "VC" not in state.board.possibilidades[side*(row+1)+col] and "VD" not in state.board.possibilidades[side*(row+1)+col]):
                    state.board.change_piece(row,col,"BC")
                    state.board.possibilidades[side*row+col] = ["BC"]
                    return True
                elif "BC" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) in pointup) or (state.board.get_value(row+1, col) in voltas and "VB" not in state.board.possibilidades[side*(row+1)+col] and "VE" not in state.board.possibilidades[side*(row+1)+col])):
                    state.board.possibilidades[side*row+col].remove("BC")
                    if state.board.get_value(row,col) == "BC" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            #baixo
            if len(state.board.possibilidades[side*(row-1)+col]) == 1 or (state.board.get_value(row-1, col) in voltas and len(state.board.possibilidades[side*(row-1)+col]) == 2):
                if (len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) not in pointdown) or (state.board.get_value(row-1, col) in voltas and "VB" not in state.board.possibilidades[side*(row-1)+col] and "VE" not in state.board.possibilidades[side*(row-1)+col]):
                    state.board.change_piece(row,col,"BB")
                    state.board.possibilidades[side*row+col] = ["BB"]
                    return True
                elif "BB" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) in pointdown) or (state.board.get_value(row-1, col) in voltas and "VC" not in state.board.possibilidades[side*(row-1)+col] and "VD" not in state.board.possibilidades[side*(row-1)+col])):
                    state.board.possibilidades[side*row+col].remove("BB")
                    if state.board.get_value(row,col) == "BB" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            #esquerda
            if len(state.board.possibilidades[side*row+col+1]) == 1 or state.board.get_value(row, col+1) in voltas and len(state.board.possibilidades[side*row+col+1]) == 2:
                if (len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) not in pointleft) or (state.board.get_value(row, col+1) in voltas and "VE" not in state.board.possibilidades[side*row+col+1] and "VC" not in state.board.possibilidades[side*row+col+1]):
                    state.board.change_piece(row,col,"BE")
                    state.board.possibilidades[side*row+col] = ["BE"]
                    return True
                elif "BE" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) in pointleft) or (state.board.get_value(row, col+1) in voltas and "VB" not in state.board.possibilidades[side*row+col+1] and "VD" not in state.board.possibilidades[side*row+col+1])):
                    state.board.possibilidades[side*row+col].remove("BE")
                    if state.board.get_value(row,col) == "BE" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            #direita
            if len(state.board.possibilidades[side*row+col-1]) == 1 or state.board.get_value(row, col-1) in voltas and len(state.board.possibilidades[side*row+col-1]) == 2:
                if (len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) not in pointright) or (state.board.get_value(row, col-1) in voltas and "VB" not in state.board.possibilidades[side*row+col-1] and "VD" not in state.board.possibilidades[side*row+col-1]):
                    state.board.change_piece(row,col,"BD")
                    state.board.possibilidades[side*row+col] = ["BD"]
                    return True
                elif "BD" in state.board.possibilidades[side*row+col] and ((len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) in pointright) or (state.board.get_value(row, col-1) in voltas and "VC" not in state.board.possibilidades[side*row+col-1] and "VE" not in state.board.possibilidades[side*row+col-1])):
                    state.board.possibilidades[side*row+col].remove("BD")
                    if state.board.get_value(row,col) == "BD" and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
        elif state.board.get_value(row,col) in ligacoes:
            #baixo
            if len(state.board.possibilidades[side*(row+1)+col]) == 1 or (state.board.get_value(row+1, col) in voltas and len(state.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) not in pointup) or (state.board.get_value(row+1, col) in voltas and "VC" not in state.board.possibilidades[side*(row+1)+col] and "VD" not in state.board.possibilidades[side*(row+1)+col]):
                    state.board.change_piece(row,col,"LH")
                    state.board.possibilidades[side*row+col] = ["LH"]
                    return True
                elif (len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) in pointup) or (state.board.get_value(row+1, col) in voltas and "VB" not in state.board.possibilidades[side*(row+1)+col] and "VE" not in state.board.possibilidades[side*(row+1)+col]):
                    state.board.change_piece(row,col,"LV")
                    state.board.possibilidades[side*row+col] = ["LV"]
                    return True
            #cima
            if len(state.board.possibilidades[side*(row-1)+col]) == 1 or (state.board.get_value(row-1, col) in voltas and len(state.board.possibilidades[side*(row-1)+col]) == 2):
                if (len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) not in pointdown) or (state.board.get_value(row-1, col) in voltas and "VB" not in state.board.possibilidades[side*(row-1)+col] and "VE" not in state.board.possibilidades[side*(row-1)+col]):
                    state.board.change_piece(row,col,"LH")
                    state.board.possibilidades[side*row+col] = ["LH"]
                    return True
                elif (len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) in pointdown) or (state.board.get_value(row-1, col) in voltas and "VC" not in state.board.possibilidades[side*(row-1)+col] and "VD" not in state.board.possibilidades[side*(row-1)+col]):
                    state.board.change_piece(row,col,"LV")
                    state.board.possibilidades[side*row+col] = ["LV"]
                    return True
            #direita
            if len(state.board.possibilidades[side*row+col+1]) == 1 or state.board.get_value(row, col+1) in voltas and len(state.board.possibilidades[side*row+col+1]) == 2:
                if (len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) not in pointleft) or (state.board.get_value(row, col+1) in voltas and "VE" not in state.board.possibilidades[side*row+col+1] and "VC" not in state.board.possibilidades[side*row+col+1]):
                    state.board.change_piece(row,col,"LV")
                    state.board.possibilidades[side*row+col] = ["LV"]
                    return True
                elif (len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) in pointleft) or (state.board.get_value(row, col+1) in voltas and "VB" not in state.board.possibilidades[side*row+col+1] and "VD" not in state.board.possibilidades[side*row+col+1]):
                    state.board.change_piece(row,col,"LH")
                    state.board.possibilidades[side*row+col] = ["LH"]
                    return True
            #esquerda
            if len(state.board.possibilidades[side*row+col-1]) == 1 or state.board.get_value(row, col-1) in voltas and len(state.board.possibilidades[side*row+col-1]) == 2:
                if (len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) not in pointright) or (state.board.get_value(row, col-1) in voltas and "VB" not in state.board.possibilidades[side*row+col-1] and "VD" not in state.board.possibilidades[side*row+col-1]):
                    state.board.change_piece(row,col,"LV")
                    state.board.possibilidades[side*row+col] = ["LV"]
                    return True
                elif (len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) in pointright) or (state.board.get_value(row, col-1) in voltas and "VC" not in state.board.possibilidades[side*row+col-1] and "VE" not in state.board.possibilidades[side*row+col-1]):
                    state.board.change_piece(row,col,"LH")
                    state.board.possibilidades[side*row+col] = ["LH"]
                    return True
        else: #voltas
            # cima
            if row != 0 and (len(state.board.possibilidades[side*(row-1)+col]) == 1 or (state.board.get_value(row-1, col) in voltas and len(state.board.possibilidades[side*(row-1)+col]) == 2)):
                if (len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) in pointdown) or (state.board.get_value(row-1, col) in voltas and "VC" not in state.board.possibilidades[side*(row-1)+col] and "VD" not in state.board.possibilidades[side*(row-1)+col]):
                    if "VB" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VB")
                        changes = True
                    if "VE" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VE")
                        changes = True
                    if state.board.get_value(row,col) in ["VB", "VE"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
                elif (len(state.board.possibilidades[side*(row-1)+col]) == 1 and state.board.get_value(row-1,col) not in pointdown) or (state.board.get_value(row-1, col) in voltas and "VB" not in state.board.possibilidades[side*(row-1)+col] and "VE" not in state.board.possibilidades[side*(row-1)+col]):
                    if "VC" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VC")
                        changes = True
                    if "VD" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VD")
                        changes = True
                    if state.board.get_value(row,col) in ["VC", "VD"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            # baixo
            if row != last and (len(state.board.possibilidades[side*(row+1)+col]) == 1 or state.board.get_value(row+1, col) in voltas and len(state.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) in pointup) or (state.board.get_value(row+1, col) in voltas and "VB" not in state.board.possibilidades[side*(row+1)+col] and "VE" not in state.board.possibilidades[side*(row+1)+col]):
                    if "VC" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VC")
                        changes = True
                    if "VD" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VD")
                        changes = True
                    if state.board.get_value(row,col) in ["VC", "VD"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
                elif (len(state.board.possibilidades[side*(row+1)+col]) == 1 and state.board.get_value(row+1,col) not in pointup) or (state.board.get_value(row+1, col) in voltas and "VC" not in state.board.possibilidades[side*(row+1)+col] and "VD" not in state.board.possibilidades[side*(row+1)+col]):
                    if "VB" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VB")
                        changes = True
                    if "VE" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VE")
                        changes = True
                    if state.board.get_value(row,col) in ["VB", "VE"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            # esquerda
            if col != 0 and (len(state.board.possibilidades[side*row+col-1]) == 1 or state.board.get_value(row, col-1) in voltas and len(state.board.possibilidades[side*row+col-1]) == 2):
                if (len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) in pointright) or (state.board.get_value(row, col-1) in voltas and "VC" not in state.board.possibilidades[side*row+col-1] and "VE" not in state.board.possibilidades[side*row+col-1]):
                    if "VB" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VB")
                        changes = True
                    if "VD" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VD")
                        changes = True
                    if state.board.get_value(row,col) in ["VB", "VD"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
                elif (len(state.board.possibilidades[side*row+col-1]) == 1 and state.board.get_value(row,col-1) not in pointright) or (state.board.get_value(row, col-1) in voltas and "VB" not in state.board.possibilidades[side*row+col-1] and "VD" not in state.board.possibilidades[side*row+col-1]):
                    if "VC" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VC")
                        changes = True
                    if "VE" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VE")
                        changes = True
                    if state.board.get_value(row,col) in ["VC", "VE"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
            # direita
            if col != last and (len(state.board.possibilidades[side*row+col+1]) == 1 or state.board.get_value(row, col+1) in voltas and len(state.board.possibilidades[side*row+col+1]) == 2):
                if (len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) in pointleft) or (state.board.get_value(row, col+1) in voltas and "VD" not in state.board.possibilidades[side*row+col+1] and "VB" not in state.board.possibilidades[side*row+col+1]):
                    if "VC" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VC")
                        changes = True
                    if "VE" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VE")
                        changes = True
                    if state.board.get_value(row,col) in ["VC", "VE"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
                elif (len(state.board.possibilidades[side*row+col+1]) == 1 and state.board.get_value(row,col+1) not in pointleft) or (state.board.get_value(row, col+1) in voltas and "VC" not in state.board.possibilidades[side*row+col+1] and "VE" not in state.board.possibilidades[side*row+col+1]):
                    if "VB" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VB")
                        changes = True
                    if "VD" in state.board.possibilidades[side*row+col]:
                        state.board.possibilidades[side*row+col].remove("VD")
                        changes = True
                    if state.board.get_value(row,col) in ["VB", "VD"] and len(state.board.possibilidades[side*row+col])>0:
                        state.board.change_piece(row,col,state.board.possibilidades[side*row+col][0])
        return changes

    
    def infer_layer( self,layer,state: PipeManiaState):
        changes = True
        changed = False
        side = int(np.sqrt(state.board.tamanho))
        while changes:
            changes = False
            for x in range(layer,int(np.sqrt(self.board.tamanho)-layer)):
                if len(state.board.possibilidades[side*x+layer]) > 1:
                    changes = self.infer_position(x,layer,state)
                if len(state.board.possibilidades[side*layer+x]) > 1:
                    changes = self.infer_position(layer,x,state)
                if len(state.board.possibilidades[side*x+side-layer-1]) > 1:
                    changes = self.infer_position(x,side-layer-1,state)
                if len(state.board.possibilidades[side*(side-layer-1)+x]) > 1:
                    changes = self.infer_position(side-layer-1,x,state)
                if changes:
                    changed = True
        return changed

    
    def infer(self,state: PipeManiaState):
        layer = 0
        while layer < int(np.ceil(np.sqrt(state.board.tamanho)/2)):
            if self.infer_layer(layer, state) and layer != 0:
                layer -= 1
            else:
                layer += 1
        

    def change_all(self, frontier):
        pass


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    def depth_first_tree_search(self):
        """
        [Figure 3.7]
        Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Repeats infinitely in case of loops.
        """
        frontier = [[Node(self.initial),-1]]  # Stack
        
        while frontier:

            todo = frontier.pop()
            node = todo[0]
            b=todo[1]
            self.infer(node.state)
            #return node
            if self.goal_test(node.state):
                return node
            elif [] in node.state.board.possibilidades:
                self.change_all(frontier)
            else:
                b+=1
                frontier.extend(node.expand(self,b))
        return None

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    problem.define_possibilities()
    problem.fix_sides()
    problem.infer(problem.initial)
    
    # Obter o nó solução usando a procura em profundidade:
    
    goal_node = problem.depth_first_tree_search()
    print(goal_node.state.board.show())
    #print("Is goal?", problem.goal_test(goal_node.state))
   
    
    # Verificar se foi atingida a solução
    #print("Is goal?", problem.goal_test(goal_node.state))
    #print(problem.goal_test(PipeManiaState(problem.board)))
    #print(goal_node.state.board.show())

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
