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
    
    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    
    def __init__(self, board ):
        self.board = board
        self.tamanho = len(board)

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
                result += self.get_value(line,i%lado)+"\ t"
        return result

    def change_piece(self, row: int, col: int,change ):
        self.board[int(np.sqrt(self.tamanho)*row+col)]=change

    def get_board(self):
        return self.board
    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board=board

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        f=("FC","FD","FB","FE")
        b=("BC","BD","BB","BE")
        v=("VC","VD","VB","VE")
        l=("LH","LV")
        new_state=PipeManiaState(Board(state.board.get_board().copy()))
        piece=new_state.board.get_value(action[0],action[1])
        if (piece in f):
            if (action[2]==True):
                if(f.index(piece)!=3):
                    new_state.board.change_piece(action[0],action[1],f[f.index(piece)+1])
                else:
                    new_state.board.change_piece(action[0],action[1],f[0])
            else:
                if(f.index(piece)!=0):
                    new_state.board.change_piece(action[0],action[1],f[f.index(piece)-1])
                else:
                    new_state.board.change_piece(action[0],action[1],f[3])

        elif(piece in b):
            if (action[2]==True):
                if(b.index(piece)!=3):
                    new_state.board.change_piece(action[0],action[1],b[b.index(piece)+1])
                else:
                    new_state.board.change_piece(action[0],action[1],b[0])
            else:
                if(b.index(piece)!=0):
                    new_state.board.change_piece(action[0],action[1],b[b.index(piece)-1])
                else:
                    new_state.board.change_piece(action[0],action[1],b[3])
                
        elif(piece in v):
            if (action[2]==True):
                if(v.index(piece)!=3):
                    new_state.board.change_piece(action[0],action[1],v[v.index(piece)+1])
                else:
                    new_state.board.change_piece(action[0],action[1],v[0])
            else:
                if(v.index(piece)!=0):
                    new_state.board.change_piece(action[0],action[1],v[v.index(piece)-1])
                else:
                    new_state.board.change_piece(action[0],action[1],v[3])
                
        else:
            if(l.index(piece)==0):
                new_state.board.change_piece(action[0],action[1],l[1])
            else:
                new_state.board.change_piece(action[0],action[1],l[0])
            
                
        return new_state

    def DFS_visit(self, board: Board, row, col, visit):
        position = int(np.sqrt(board.tamanho)*row+col)

        pointdown = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
        pointup = ["FC", "BC", "BE", "BD", "VD", "VC", "LV"]
        pointleft = ["FE", "BB", "BE", "BC", "VC", "VE", "LH"]
        pointright = ["FD", "BB", "BD", "BC", "VB", "VD", "LH"]
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

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        visit = []
        for v in state.board.get_board():
            visit.append(0) # 0: não visitado, 1: visitado, 2: fechado
        self.DFS_visit(state.board, 0, 0, visit)
        for v in visit:
            if v != 2:
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Criar um estado com a configuração inicial:
    s0 = PipeManiaState(board)
    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (0, 1, True))
    s2 = problem.result(s1, (0, 1, True))
    s3 = problem.result(s2, (0, 2, True))
    s4 = problem.result(s3, (0, 2, True))
    s5 = problem.result(s4, (1, 0, True))
    s6 = problem.result(s5, (1, 1, True))
    s7 = problem.result(s6, (2, 0, False)) # anti-clockwise (exemplo de uso)
    s8 = problem.result(s7, (2, 0, False)) # anti-clockwise (exemplo de uso)
    s9 = problem.result(s8, (2, 1, True))
    s10 = problem.result(s9, (2, 1, True))
    s11 = problem.result(s10, (2, 2, True))
    
    print("Is goal?", problem.goal_test(s5))
    print("Is goal?", problem.goal_test(s11))
    print("Solution:\n", s11.board.show(), sep="")

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
