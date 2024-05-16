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
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

pointdown = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
pointup = ["FC", "BC", "BE", "BD", "VD", "VC", "LV"]
pointleft = ["FE", "BB", "BE", "BC", "VC", "VE", "LH"]
pointright = ["FD", "BB", "BD", "BC", "VB", "VD", "LH"]

fontes=["FC","FD","FB","FE"]
bifurcacoes=["BC","BD","BB","BE"]
voltas=["VC","VD","VB","VE"]
ligacoes=["LH","LV"]


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    
    def __init__(self, board ):
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
        print(result)
        print(type(result))
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
            for k in range(3):
                for j in range(lado):
                    if k==0 and self.get_value(i,j) in pointup:
                        result += " ^ "
                    elif k==1:
                        if self.get_value(i,j) in pointleft and self.get_value(i,j) in pointright:
                            result += "< >"
                        elif self.get_value(i,j) in pointleft:
                            result += "<  "
                        elif self.get_value(i,j) in pointright:
                            result += "  >"
                        else:
                            result += "   "
                    elif k==2 and self.get_value(i,j) in pointdown:
                        result += " v "
                    else:
                        result += "   "
                result+="\n"
        return result

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1


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
        self.initial = PipeManiaState(Board(board.get_board().copy()))

    def actions(self, state: PipeManiaState): #mudar actions para tuplo com row, col e possibilidades para a peça
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        lista=[]
        for v in range(self.board.tamanho):
            if not self.board.blocked[v]:
                row = v//int(np.sqrt(self.board.tamanho))
                col = v%int(np.sqrt(self.board.tamanho))
                lista.append((row,col,True))
                lista.append((row,col,False))
        return lista

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_state=PipeManiaState(Board(state.board.get_board().copy()))
        piece=new_state.board.get_value(action[0],action[1])
        if (piece in fontes):
            if (action[2]==True):
                if(fontes.index(piece)!=3):
                    new_state.board.change_piece(action[0],action[1],fontes[fontes.index(piece)+1])
                else:
                    new_state.board.change_piece(action[0],action[1],fontes[0])
            else:
                if(fontes.index(piece)!=0):
                    new_state.board.change_piece(action[0],action[1],fontes[fontes.index(piece)-1])
                else:
                    new_state.board.change_piece(action[0],action[1],fontes[3])

        elif(piece in bifurcacoes):
            if (action[2]==True):
                if(bifurcacoes.index(piece)!=3):
                    new_state.board.change_piece(action[0],action[1],bifurcacoes[bifurcacoes.index(piece)+1])
                else:
                    new_state.board.change_piece(action[0],action[1],bifurcacoes[0])
            else:
                if(bifurcacoes.index(piece)!=0):
                    new_state.board.change_piece(action[0],action[1],bifurcacoes[bifurcacoes.index(piece)-1])
                else:
                    new_state.board.change_piece(action[0],action[1],bifurcacoes[3])
                
        elif(piece in voltas):
            if (action[2]==True):
                if(voltas.index(piece)!=3):
                    new_state.board.change_piece(action[0],action[1],voltas[voltas.index(piece)+1])
                else:
                    new_state.board.change_piece(action[0],action[1],voltas[0])
            else:
                if(voltas.index(piece)!=0):
                    new_state.board.change_piece(action[0],action[1],voltas[voltas.index(piece)-1])
                else:
                    new_state.board.change_piece(action[0],action[1],voltas[3])
                
        else:
            if(ligacoes.index(piece)==0):
                new_state.board.change_piece(action[0],action[1],ligacoes[1])
            else:
                new_state.board.change_piece(action[0],action[1],ligacoes[0])
            
                
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

    def define_possibilities(self):
        for v in range(self.board.tamanho):
            row = v//int(np.sqrt(self.board.tamanho))
            col = v%int(np.sqrt(self.board.tamanho))
            if self.board.get_value(row,col) in fontes:
                self.board.possibilidades[v] = fontes
            elif self.board.get_value(row,col) in voltas:
                self.board.possibilidades[v] = voltas
            elif self.board.get_value(row,col) in bifurcacoes:
                self.board.possibilidades[v] = bifurcacoes
            elif self.board.get_value(row,col) in ligacoes:
                self.board.possibilidades[v] = ligacoes
    
 
    def infer_position(self, row, col):
        changes = False
        side = int(np.sqrt(self.board.tamanho))
        last = side-1
        print(row, col)
        if self.board.get_value(row, col) in fontes:
            # cima
            if row != 0 and (len(self.board.possibilidades[side*(row-1)+col]) == 1 or (self.board.get_value(row-1, col) in voltas and len(self.board.possibilidades[side*(row-1)+col]) == 2)):
                if (len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) in pointdown) or (self.board.get_value(row-1, col) in voltas and "VC" not in self.board.possibilidades[side*(row-1)+col] and "VD" not in self.board.possibilidades[side*(row-1)+col]):
                    self.board.change_piece(row,col,"FC")
                    self.board.possibilidades[side*row+col] = ["FC"]
                    print("bloqueou FC")
                    return True
                elif "FC" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) not in pointdown) or (self.board.get_value(row-1, col) in voltas and "VB" not in self.board.possibilidades[side*(row-1)+col] and "VE" not in self.board.possibilidades[side*(row-1)+col])):
                    self.board.possibilidades[side*row+col].remove("FC")
                    if self.board.get_value(row,col) == "FC":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu FC")
            # baixo
            if row != last and (len(self.board.possibilidades[side*(row+1)+col]) == 1 or self.board.get_value(row+1, col) in voltas and len(self.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) in pointup) or (self.board.get_value(row+1, col) in voltas and "VB" not in self.board.possibilidades[side*(row+1)+col] and "VE" not in self.board.possibilidades[side*(row+1)+col]):
                    self.board.change_piece(row,col,"FB")
                    self.board.possibilidades[side*row+col] = ["FB"]
                    print("bloqueou FB")
                    return True
                elif "FB" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) not in pointup) or (self.board.get_value(row+1, col) in voltas and "VC" not in self.board.possibilidades[side*(row+1)+col] and "VD" not in self.board.possibilidades[side*(row+1)+col])):
                    self.board.possibilidades[side*row+col].remove("FB")
                    if self.board.get_value(row,col) == "FB":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu FB")
            # esquerda
            if col != 0 and (len(self.board.possibilidades[side*row+col-1]) == 1 or self.board.get_value(row, col-1) in voltas and len(self.board.possibilidades[side*row+col-1]) == 2):
                if (len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) in pointright) or (self.board.get_value(row, col-1) in voltas and "VC" not in self.board.possibilidades[side*row+col-1] and "VE" not in self.board.possibilidades[side*row+col-1]):
                    self.board.change_piece(row,col,"FE")
                    self.board.possibilidades[side*row+col] = ["FE"]
                    print("bloqueou FE")
                    return True
                elif "FE" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) not in pointright) or (self.board.get_value(row, col-1) in voltas and "VB" not in self.board.possibilidades[side*row+col-1] and "VD" not in self.board.possibilidades[side*row+col-1])):
                    self.board.possibilidades[side*row+col].remove("FE")
                    if self.board.get_value(row,col) == "FE":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu FE")
            # direita
            if col != last and (len(self.board.possibilidades[side*row+col+1]) == 1 or self.board.get_value(row, col+1) in voltas and len(self.board.possibilidades[side*row+col+1]) == 2):
                if (len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) in pointleft) or (self.board.get_value(row, col+1) in voltas and "VD" not in self.board.possibilidades[side*row+col+1] and "VB" not in self.board.possibilidades[side*row+col+1]):
                    self.board.change_piece(row,col,"FD")
                    self.board.possibilidades[side*row+col] = ["FD"]
                    print("bloqueou FD")
                    return True
                elif "FD" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) not in pointleft) or (self.board.get_value(row, col+1) in voltas and "VC" not in self.board.possibilidades[side*row+col+1] and "VE" not in self.board.possibilidades[side*row+col+1])):
                    self.board.possibilidades[side*row+col].remove("FD")
                    if self.board.get_value(row,col) == "FD":
                        print(len(self.board.possibilidades[side*row+col]))
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu FD")
        elif self.board.get_value(row, col) in bifurcacoes:
            #cima
            if len(self.board.possibilidades[side*(row+1)+col]) == 1 or (self.board.get_value(row+1, col) in voltas and len(self.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) not in pointup) or (self.board.get_value(row+1, col) in voltas and "VC" not in self.board.possibilidades[side*(row+1)+col] and "VD" not in self.board.possibilidades[side*(row+1)+col]):
                    self.board.change_piece(row,col,"BC")
                    self.board.possibilidades[side*row+col] = ["BC"]
                    print("bloqueou BC")
                    return True
                elif "BC" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) in pointup) or (self.board.get_value(row+1, col) in voltas and "VB" not in self.board.possibilidades[side*(row+1)+col] and "VE" not in self.board.possibilidades[side*(row+1)+col])):
                    self.board.possibilidades[side*row+col].remove("BC")
                    if self.board.get_value(row,col) == "BC":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu BC")
            #baixo
            if len(self.board.possibilidades[side*(row-1)+col]) == 1 or (self.board.get_value(row-1, col) in voltas and len(self.board.possibilidades[side*(row-1)+col]) == 2):
                if (len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) not in pointdown) or (self.board.get_value(row-1, col) in voltas and "VB" not in self.board.possibilidades[side*(row-1)+col] and "VE" not in self.board.possibilidades[side*(row-1)+col]):
                    self.board.change_piece(row,col,"BB")
                    self.board.possibilidades[side*row+col] = ["BB"]
                    print("bloqueou BB")
                    return True
                elif "BB" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) in pointdown) or (self.board.get_value(row-1, col) in voltas and "VC" not in self.board.possibilidades[side*(row-1)+col] and "VD" not in self.board.possibilidades[side*(row-1)+col])):
                    self.board.possibilidades[side*row+col].remove("BB")
                    if self.board.get_value(row,col) == "BB":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu BB")
            #esquerda
            if len(self.board.possibilidades[side*row+col+1]) == 1 or self.board.get_value(row, col+1) in voltas and len(self.board.possibilidades[side*row+col+1]) == 2:
                if (len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) not in pointleft) or (self.board.get_value(row, col+1) in voltas and "VE" not in self.board.possibilidades[side*row+col+1] and "VC" not in self.board.possibilidades[side*row+col+1]):
                    self.board.change_piece(row,col,"BE")
                    self.board.possibilidades[side*row+col] = ["BE"]
                    print("bloqueou BE")
                    return True
                elif "BE" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) in pointleft) or (self.board.get_value(row, col+1) in voltas and "VB" not in self.board.possibilidades[side*row+col+1] and "VD" not in self.board.possibilidades[side*row+col+1])):
                    self.board.possibilidades[side*row+col].remove("BE")
                    if self.board.get_value(row,col) == "BE":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu BE")
            #direita
            if len(self.board.possibilidades[side*row+col-1]) == 1 or self.board.get_value(row, col-1) in voltas and len(self.board.possibilidades[side*row+col-1]) == 2:
                if (len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) not in pointright) or (self.board.get_value(row, col-1) in voltas and "VB" not in self.board.possibilidades[side*row+col-1] and "VD" not in self.board.possibilidades[side*row+col-1]):
                    self.board.change_piece(row,col,"BD")
                    self.board.possibilidades[side*row+col] = ["BD"]
                    print("bloqueou BD")
                    return True
                elif "BD" in self.board.possibilidades[side*row+col] and ((len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) in pointright) or (self.board.get_value(row, col-1) in voltas and "VC" not in self.board.possibilidades[side*row+col-1] and "VE" not in self.board.possibilidades[side*row+col-1])):
                    self.board.possibilidades[side*row+col].remove("BD")
                    if self.board.get_value(row,col) == "BD":
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    print("removeu BD")
        elif self.board.get_value(row,col) in ligacoes:
            #baixo
            if len(self.board.possibilidades[side*(row+1)+col]) == 1 or (self.board.get_value(row+1, col) in voltas and len(self.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) not in pointup) or (self.board.get_value(row+1, col) in voltas and "VC" not in self.board.possibilidades[side*(row+1)+col] and "VD" not in self.board.possibilidades[side*(row+1)+col]):
                    self.board.change_piece(row,col,"LH")
                    self.board.possibilidades[side*row+col] = ["LH"]
                    print("bloqueou LH")
                    return True
                elif (len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) in pointup) or (self.board.get_value(row+1, col) in voltas and "VB" not in self.board.possibilidades[side*(row+1)+col] and "VE" not in self.board.possibilidades[side*(row+1)+col]):
                    self.board.change_piece(row,col,"LV")
                    self.board.possibilidades[side*row+col] = ["LV"]
                    print("bloqueou LV")
                    return True
            #cima
            if len(self.board.possibilidades[side*(row-1)+col]) == 1 or (self.board.get_value(row-1, col) in voltas and len(self.board.possibilidades[side*(row-1)+col]) == 2):
                if (len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) not in pointdown) or (self.board.get_value(row-1, col) in voltas and "VB" not in self.board.possibilidades[side*(row-1)+col] and "VE" not in self.board.possibilidades[side*(row-1)+col]):
                    self.board.change_piece(row,col,"LH")
                    self.board.possibilidades[side*row+col] = ["LH"]
                    print("bloqueou LH")
                    return True
                elif (len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) in pointdown) or (self.board.get_value(row-1, col) in voltas and "VC" not in self.board.possibilidades[side*(row-1)+col] and "VD" not in self.board.possibilidades[side*(row-1)+col]):
                    self.board.change_piece(row,col,"LV")
                    self.board.possibilidades[side*row+col] = ["LV"]
                    print("bloqueou LV")
                    return True
            #direita
            if len(self.board.possibilidades[side*row+col+1]) == 1 or self.board.get_value(row, col+1) in voltas and len(self.board.possibilidades[side*row+col+1]) == 2:
                if (len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) not in pointleft) or (self.board.get_value(row, col+1) in voltas and "VE" not in self.board.possibilidades[side*row+col+1] and "VC" not in self.board.possibilidades[side*row+col+1]):
                    self.board.change_piece(row,col,"LV")
                    self.board.possibilidades[side*row+col] = ["LV"]
                    print("bloqueou LV")
                    return True
                elif (len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) in pointleft) or (self.board.get_value(row, col+1) in voltas and "VB" not in self.board.possibilidades[side*row+col+1] and "VD" not in self.board.possibilidades[side*row+col+1]):
                    self.board.change_piece(row,col,"LH")
                    self.board.possibilidades[side*row+col] = ["LH"]
                    print("bloqueou LH")
                    return True
            #esquerda
            if len(self.board.possibilidades[side*row+col-1]) == 1 or self.board.get_value(row, col-1) in voltas and len(self.board.possibilidades[side*row+col-1]) == 2:
                if (len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) not in pointright) or (self.board.get_value(row, col-1) in voltas and "VB" not in self.board.possibilidades[side*row+col-1] and "VD" not in self.board.possibilidades[side*row+col-1]):
                    self.board.change_piece(row,col,"LV")
                    self.board.possibilidades[side*row+col] = ["LV"]
                    print("bloqueou LV")
                    return True
                elif (len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) in pointright) or (self.board.get_value(row, col-1) in voltas and "VC" not in self.board.possibilidades[side*row+col-1] and "VE" not in self.board.possibilidades[side*row+col-1]):
                    self.board.change_piece(row,col,"LH")
                    self.board.possibilidades[side*row+col] = ["LH"]
                    print("bloqueou LH")
                    return True
        else: #voltas
            # cima
            if row != 0 and (len(self.board.possibilidades[side*(row-1)+col]) == 1 or (self.board.get_value(row-1, col) in voltas and len(self.board.possibilidades[side*(row-1)+col]) == 2)):
                if (len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) in pointdown) or (self.board.get_value(row-1, col) in voltas and "VC" not in self.board.possibilidades[side*(row-1)+col] and "VD" not in self.board.possibilidades[side*(row-1)+col]):
                    if "VB" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VB")
                        print("removeu VB")
                    if "VE" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VE")
                        print("removeu VE")
                    if self.board.get_value(row,col) in ["VB", "VE"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
                elif (len(self.board.possibilidades[side*(row-1)+col]) == 1 and self.board.get_value(row-1,col) not in pointdown) or (self.board.get_value(row-1, col) in voltas and "VB" not in self.board.possibilidades[side*(row-1)+col] and "VE" not in self.board.possibilidades[side*(row-1)+col]):
                    if "VC" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VC")
                        print("removeu VC")
                    if "VD" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VD")
                        print("removeu VD")
                    if self.board.get_value(row,col) in ["VC", "VD"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
            # baixo
            if row != last and (len(self.board.possibilidades[side*(row+1)+col]) == 1 or self.board.get_value(row+1, col) in voltas and len(self.board.possibilidades[side*(row+1)+col]) == 2):
                if (len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) in pointup) or (self.board.get_value(row+1, col) in voltas and "VB" not in self.board.possibilidades[side*(row+1)+col] and "VE" not in self.board.possibilidades[side*(row+1)+col]):
                    if "VC" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VC")
                        print("removeu VC")
                    if "VD" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VD")
                        print("removeu VD")
                    if self.board.get_value(row,col) in ["VC", "VD"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
                elif (len(self.board.possibilidades[side*(row+1)+col]) == 1 and self.board.get_value(row+1,col) not in pointup) or (self.board.get_value(row+1, col) in voltas and "VC" not in self.board.possibilidades[side*(row+1)+col] and "VD" not in self.board.possibilidades[side*(row+1)+col]):
                    if "VB" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VB")
                        print("removeu VB")
                    if "VE" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VE")
                        print("removeu VE")
                    if self.board.get_value(row,col) in ["VB", "VE"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
            # esquerda
            if col != 0 and (len(self.board.possibilidades[side*row+col-1]) == 1 or self.board.get_value(row, col-1) in voltas and len(self.board.possibilidades[side*row+col-1]) == 2):
                if (len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) in pointright) or (self.board.get_value(row, col-1) in voltas and "VC" not in self.board.possibilidades[side*row+col-1] and "VE" not in self.board.possibilidades[side*row+col-1]):
                    if "VB" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VB")
                        print("removeu VB")
                    if "VD" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VD")
                        print("removeu VD")
                    if self.board.get_value(row,col) in ["VB", "VD"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
                elif (len(self.board.possibilidades[side*row+col-1]) == 1 and self.board.get_value(row,col-1) not in pointright) or (self.board.get_value(row, col-1) in voltas and "VB" not in self.board.possibilidades[side*row+col-1] and "VD" not in self.board.possibilidades[side*row+col-1]):
                    if "VC" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VC")
                        print("removeu VC")
                    if "VE" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VE")
                        print("removeu VE")
                    if self.board.get_value(row,col) in ["VC", "VE"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
            # direita
            if col != last and (len(self.board.possibilidades[side*row+col+1]) == 1 or self.board.get_value(row, col+1) in voltas and len(self.board.possibilidades[side*row+col+1]) == 2):
                if (len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) in pointleft) or (self.board.get_value(row, col+1) in voltas and "VD" not in self.board.possibilidades[side*row+col+1] and "VB" not in self.board.possibilidades[side*row+col+1]):
                    if "VC" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VC")
                        print("removeu VC")
                    if "VE" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VE")
                        print("removeu VE")
                    if self.board.get_value(row,col) in ["VC", "VE"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
                elif (len(self.board.possibilidades[side*row+col+1]) == 1 and self.board.get_value(row,col+1) not in pointleft) or (self.board.get_value(row, col+1) in voltas and "VC" not in self.board.possibilidades[side*row+col+1] and "VE" not in self.board.possibilidades[side*row+col+1]):
                    if "VB" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VB")
                        print("removeu VB")
                    if "VD" in self.board.possibilidades[side*row+col]:
                        self.board.possibilidades[side*row+col].remove("VD")
                        print("removeu VD")
                    if self.board.get_value(row,col) in ["VB", "VD"]:
                        self.board.change_piece(row,col,self.board.possibilidades[side*row+col][0])
                    changes = True
        return changes

    
    def infer_layer(self, layer):
        changes = True
        changed = False
        side = int(np.sqrt(self.board.tamanho))
        while changes:
            changes = False
            for x in range(layer,int(np.sqrt(self.board.tamanho)-layer)):
                if len(self.board.possibilidades[side*x+layer]) > 1:
                    changes = self.infer_position(x,layer)
                if len(self.board.possibilidades[side*layer+x]) > 1:
                    changes = self.infer_position(layer,x)
                if len(self.board.possibilidades[side*x+side-layer-1]) > 1:
                    changes = self.infer_position(x,side-layer-1)
                if len(self.board.possibilidades[side*(side-layer-1)+x]) > 1:
                    changes = self.infer_position(side-layer-1,x)
                if changes:
                    changed = True
        return changed

    
    def infer(self):
        layer = 0
        while layer < int(np.ceil(np.sqrt(self.board.tamanho)/2)):
            print(self.board.draw())
            if self.infer_layer(layer) and layer != 0:
                layer -= 1
            else:
                layer += 1



    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    problem.define_possibilities()
    problem.fix_sides()
    problem.infer()
    print(problem.board.draw())
    # Obter o nó solução usando a procura em profundidade:
    #goal_node = breadth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    #print("Is goal?", problem.goal_test(goal_node.state))
    #print("Solution:\n", goal_node.state.board.print(), sep="")
    print(problem.goal_test(PipeManiaState(problem.board)))

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
