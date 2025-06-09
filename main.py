import sys
import re
import datetime

class Produto:
    def __init__(self, nome, sku, quantidade, validade):
        self.nome = nome
        self.sku = sku
        self.quantidade = quantidade
        self.validade = validade
        
    def __str__(self):
        return f"Produto(nome={self.nome}, sku={self.sku}, quantidade={self.quantidade}, validade={self.validade})"

class SymbolTable:
    def __init__(self):
        self.entrada = {}
        self.estoque = {}
        self.auxiliary = {}
        
    # Caso um estado inicial de estoque tenha sido definido, 
    def importaProduto(self, posicao, produto):
        if posicao not in self.estoque:
            self.estoque[posicao] = []
        self.estoque[posicao].append(produto)
        

    def entradaItem(self, key, item): # Entrada do produto
        if key not in self.entrada:
            self.entrada[key] = [item]
        else:
            self.entrada[key].append(item)
                
    def receber(self, key, quantidade): # Recebe uma chave e uma quantidade a ser recebida
        if key not in self.entrada:
            raise Exception(f"Não é possível receber o produto {key}, não existe esse SKU no sistema")
        if len(self.entrada[key]) == 0:
            raise Exception(f"Não é possível receber o produto {key}, não existe esse SKU no sistema")
        if quantidade <= 0:
            raise Exception("Quantidade a ser recebida não pode ser negativa ou zero")
        
        quantidade_disponivel = sum(produto.quantidade for produto in self.entrada[key])
        if quantidade > quantidade_disponivel:
            raise Exception(f"Não é possível receber o produto {key}, não foi inserida uma quantidade suficiente no estoque para receber {quantidade} unidades")
        
        if "recebimento" not in self.estoque:
            self.estoque["recebimento"] = []
        
        produtos_ordenados = sorted(self.entrada[key], key=lambda x: x.validade)
        for produto in produtos_ordenados:
            if produto.quantidade >= quantidade:
                novoProduto = Produto(produto.nome, produto.sku, quantidade, produto.validade)
                self.estoque["recebimento"].append(novoProduto)
                produto.quantidade -= quantidade
                break
            else:
                quantidade -= produto.quantidade
                self.estoque["recebimento"].append(produto)
                produto.quantidade = 0
                
        # Remove todos os produtos com o sku que não foram recebidos
        del self.entrada[key]
        
    def alocar(self, key, quantidade, posicao):
        # Remove um produto que estava na recebimento e aloca na posição escolhida
        if quantidade <= 0:
            raise Exception("Quantidade a ser alocada não pode ser negativa ou zero")
                
        quantidade_disponivel = sum(produto.quantidade for produto in self.estoque["recebimento"] if produto.sku == key)
        
        if quantidade > quantidade_disponivel:
            raise Exception(f"Não é possível alocar o produto {key}, não há quantidade suficiente no estoque")
        
        if posicao not in self.estoque:
            self.estoque[posicao] = []
            self.estoque = dict(sorted(self.estoque.items()))
        
        produtos_ordenados = sorted(self.estoque["recebimento"], key=lambda x: x.validade)
        for produto in produtos_ordenados:
            if produto.sku == key:
                if produto.quantidade >= quantidade:
                    novoProduto = Produto(produto.nome, produto.sku, quantidade, produto.validade)
                    self.estoque[posicao].append(novoProduto)
                    produto.quantidade -= quantidade
                    break
                else:
                    quantidade -= produto.quantidade
                    self.estoque[posicao].append(produto)
                    produto.quantidade = 0
                    
        for produto in self.estoque["recebimento"][:]:
            if produto.quantidade == 0:
                self.estoque["recebimento"].remove(produto)
                
        # Unifica produtos iguais na posição de destino
        self.unificaProdutosIguais(posicao)
                
    def conferir(self, sku, posicao = ""):
        # Se não definir a posicao mostra a quantidade total do SKU em todo o estoque
        total = 0
        if posicao == "":
            for posicao, produtos in self.estoque.items():
                for produto in produtos:
                    if produto.sku == sku:
                        total += produto.quantidade
        else:
            if posicao not in self.estoque:
                raise Exception(f"Posição {posicao} não encontrada no estoque")
            produtos = self.estoque[posicao]
            for produto in produtos:
                if produto.sku == sku:
                    total += produto.quantidade
        
        return total
    
    def mover(self, sku, quantidade, posicaoInicial, posicaoFinal):
        if quantidade <= 0:
            raise Exception("Quantidade a ser movida não pode ser negativa ou zero")
        
        if posicaoInicial not in self.estoque:
            raise Exception(f"Posição inicial {posicaoInicial} não encontrada no estoque")
        
        if posicaoFinal not in self.estoque:
            self.estoque[posicaoFinal] = []
            self.estoque = dict(sorted(self.estoque.items()))
        
        produtos_inicial = self.estoque[posicaoInicial]
        produtos_inicial = sorted(produtos_inicial, key=lambda x: x.validade)
        total = quantidade
        
        for produto in produtos_inicial:
            if produto.sku == sku:
                if produto.quantidade >= total:
                    novoProduto = Produto(produto.nome, produto.sku, total, produto.validade)
                    self.estoque[posicaoFinal].append(novoProduto)
                    produto.quantidade -= total
                    if produto.quantidade == 0:
                        self.estoque[posicaoInicial].remove(produto)
                    total = 0
                else:
                    total -= produto.quantidade
                    novoProduto = Produto(produto.nome, produto.sku, produto.quantidade, produto.validade)
                    self.estoque[posicaoFinal].append(novoProduto)
                    self.estoque[posicaoInicial].remove(produto)
        
        if total > 0:
            raise Exception(f"Não foi possível mover {quantidade} unidades do SKU {sku} da posição {posicaoInicial} para a posição {posicaoFinal}, quantidade insuficiente")
        
        # Unifica produtos iguais
        self.unificaProdutosIguais(posicaoFinal)
                            
        return
                            
    # print
    def exibirPosicao(self,posicao):
        if posicao not in self.estoque:
            raise Exception(f"Posição {posicao} não encontrada no estoque")
        
        produtos = self.estoque[posicao]
        if len(produtos) == 0:
            return f"Nenhum produto encontrado na posição {posicao}"
        
        resultado = []
        for produto in produtos:
            resultado.append(f"Produto: {produto.nome}, SKU: {produto.sku}, Quantidade: {produto.quantidade}, Validade: {produto.validade}")
        
        return "\n".join(resultado)
    
    def exibirSKU(self, sku):
        total = 0
        resultado = []
        for posicao, produtos in self.estoque.items():
            for produto in produtos:
                if produto.sku == str(sku):
                    total += produto.quantidade
                    resultado.append(f"Posição: {posicao}, Produto: {produto.nome}, SKU: {produto.sku}, Quantidade: {produto.quantidade}, Validade: {produto.validade}")
        
        if total == 0:
            return f"Nenhum produto encontrado com o SKU {sku}"
        
        return "\n".join(resultado)
    
    def validade(self, sku, posicao, dias):
        if posicao not in self.estoque:
            raise Exception(f"Posição {posicao} não encontrada no estoque")
        
        produtos = self.estoque[posicao]
        produtos_ordenados = sorted(produtos, key=lambda x: x.validade)
        quantidade = 0
        for produto in produtos_ordenados:
            if produto.sku == str(sku):
                if (produto.validade - datetime.date.today()).days <= dias:
                    quantidade += produto.quantidade
                else:
                    break
        
        return quantidade
            
    # Remove determinada quantia de um SKU, se definir a posicao ele remove de uma posição específica, se não remove da primeira
    def diminuirQuantidade(self, sku, quantidade,posicao=""):
        if quantidade <= 0:
            raise Exception("Quantidade a ser diminuída não pode ser negativa ou zero")
        quantidade_total = self.conferir(sku, posicao)
        if quantidade > quantidade_total:
            raise Exception(f"Não é possível diminuir {quantidade} unidades do SKU {sku}, quantidade insuficiente no estoque")
        total = quantidade
        if posicao == "":
            for posicao, produtos in self.estoque.items():
                produtos_ordenados = sorted(produtos, key=lambda x: x.validade)
                for produto in produtos_ordenados:
                    if produto.sku == sku:
                        if produto.quantidade >= total:
                            produto.quantidade -= total
                            if produto.quantidade == 0:
                                produtos.remove(produto)
                        else:
                            total -= produto.quantidade
                            produtos.remove(produto)
                        if total == 0:
                            return
                        
        else:
            if posicao not in self.estoque:
                raise Exception(f"Posição {posicao} não encontrada no estoque")
            produtos = self.estoque[posicao]
            quantidade_total = self.conferir(sku, posicao)
            if quantidade_total < total:
                raise Exception(f"Não é possível diminuir {total} unidades do SKU {sku} na posição {posicao}, quantidade insuficiente")
            produtos_ordenados = sorted(self.estoque[posicao], key=lambda x: x.validade)
            for produto in produtos_ordenados:
                if produto.sku == sku:
                    if produto.quantidade >= total:
                        produto.quantidade -= total
                        if produto.quantidade == 0:
                            produtos.remove(produto)
                    else:
                        total -= produto.quantidade
                        produtos.remove(produto)
                    if total == 0:
                        return
                    
    def unificaProdutosIguais(self, posicao):
        agrupados = {}
        for produto in self.estoque[posicao]:
            chave = (produto.sku, produto.validade)
            if chave not in agrupados:
                agrupados[chave] = Produto(produto.nome, produto.sku, produto.quantidade, produto.validade)
            else:
                agrupados[chave].quantidade += produto.quantidade
        # Substitui a lista antiga pela nova, agrupada
        self.estoque[posicao] = list(agrupados.values())
        
    def createAuxiliaryVar(self, identifier, type):
        if identifier in self.auxiliary:
            raise Exception(f"Variável auxiliar {identifier} já existe")
        self.auxiliary[identifier] = (type, None)
        
    def setAuxiliaryVar(self, identifier, value):
        if identifier not in self.auxiliary:
            raise Exception(f"Variável auxiliar {identifier} não existe")
        if self.auxiliary[identifier][0] != value[0]:
            raise Exception(f"Tipo da variável auxiliar {identifier} não corresponde ao tipo do valor")
        self.auxiliary[identifier] = (self.auxiliary[identifier][0], value[1])
    
    def getAuxiliaryVar(self, identifier):
        if identifier not in self.auxiliary:
            raise Exception(f"Variável auxiliar {identifier} não existe")
        return self.auxiliary[identifier]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
class Node():
    def __init__(self,value,children):
        self.value = value
        self.children = children
        
    def evaluate(self,st):
        pass
    
class WhileOp(Node):
    def evaluate(self,st):
        condition_type, condition_value = self.children[0].evaluate(st)
        if condition_type != "BOOL":
            raise Exception("While Condition must be a boolean")
        
        while condition_value:
            self.children[1].evaluate(st)
            condition_type, condition_value = self.children[0].evaluate(st)
            if condition_type != "BOOL":
                raise Exception("While Condition must be a boolean")
            
class IfOp(Node):
    def evaluate(self,st):
        condition_type, condition_value = self.children[0].evaluate(st)
        if condition_type != "BOOL":
            raise Exception("IF Condition must be a boolean")
        
        if condition_value:
            return self.children[1].evaluate(st)
        elif len(self.children) == 3: # Se existir "else"
            return self.children[2].evaluate(st)
            
class Read(Node):
    def evaluate(self,st):
        return ("INT",int(input()))
    
class NoOp(Node):
    def evaluate(self,st):
        pass

class BinOp(Node):
    def evaluate(self,st):
        type_left, value_left = self.children[0].evaluate(st)
        type_right, value_right = self.children[1].evaluate(st)
        same_type = type_left == type_right
        
        if self.value == "+":
            if type_left == "INT" and type_right == "INT":
                return ("INT",value_left + value_right)
            elif type_left == "STR" and type_right == "STR":
                return ("STR", str(value_left) + str(value_right))
            else:
                value_left = str(value_left).lower() if type_left == "BOOL" else str(value_left)
                value_right = str(value_right).lower() if type_right == "BOOL" else str(value_right)
                
                return ("STR", value_left + value_right)
            
        elif self.value == "-":
            if same_type and type_left == "INT":
                return ("INT",value_left - value_right)
            else:
                raise Exception("Invalid operation for -")
    
        elif self.value == "*":
            if same_type and type_left == "INT":
                return ("INT",value_left * value_right)
            else:
                raise Exception("Invalid operation for *")
        
        elif self.value == "/":
            if same_type and type_left == "INT":
                return ("INT",value_left // value_right)
            else:
                raise Exception("Invalid operation for /")
        
        elif self.value == "||":
            if same_type:
                return ("BOOL", value_left or value_right)
            else:
                raise Exception("Invalid operation for ||")
        
        elif self.value == "&&":
            if same_type:
                return ("BOOL", value_left and value_right)
            else:
                raise Exception("Invalid operation for &&")
        
        elif self.value == ">":
            if same_type:
                return ("BOOL", value_left > value_right)
            else:
                raise Exception("Invalid operation for >")
        
        elif self.value == "<":
            if same_type:
                return ("BOOL", value_left < value_right)
            else:
                raise Exception("Invalid operation for <")
        
        elif self.value == "==":
            if same_type:
                return ("BOOL", value_left == value_right)       
        else:
            raise Exception("Invalid operator for ==")
        
class UnOp(Node):
    def evaluate(self,st):
        type, value = self.children[0].evaluate(st)
        if self.value == "+":
            if type == "INT":
                return ("INT", value)
            else:
                raise Exception("Invalid operation for +")
        
        elif self.value == "-":
            if type == "INT":
                return ("INT", -value)
            else:
                raise Exception("Invalid operation for -")
        
        elif self.value == "!":
            if type == "BOOL":
                return ("BOOL", not value)
            else:
                raise Exception("Invalid operation for !")
        else:
            raise Exception(f"Invalid operator for UnOp: {self.value}")
        
class IntVal(Node):
    def evaluate(self,st):
        return ("INT", self.value)
    
class BoolVal(Node):
    def evaluate(self,st):
        return ("BOOL", self.value)
    
class VarType(Node):
    def evaluate(self,st):
        return self.value
    
class Identifier(Node):
    def evaluate(self, st):
        return st.getAuxiliaryVar(self.value)
    
class VarDec(Node):
    def evaluate(self, st):
        identifier = self.children[0].value
        type = self.children[1].value
    
        if type == "INT":
            st.createAuxiliaryVar(identifier, "INT")
        elif type == "BOOL":
            st.createAuxiliaryVar(identifier, "BOOL")
        else:
            raise Exception(f"Invalid variable type: {type}. Only INT and BOOL are allowed.")
        
        if len(self.children) == 3:
            value_type, value = self.children[2].evaluate(st)
            if value_type != type:
                raise Exception(f"Type mismatch: expected {type}, got {value_type}")
            st.setAuxiliaryVar(identifier, (type, value))
        
class Assign(Node):
    def evaluate(self, st):
        st.setAuxiliaryVar(self.children[0].value, self.children[1].evaluate(st))
        
class Print(Node):
    def evaluate(self, st):
        # two types of prints: print(sku) and print(posicao)
        if len(self.children) == 1:
            identifier = self.children[0].value
            if identifier.isdigit():
                sku = int(identifier)
                print(st.exibirSKU(sku))
            else:
                posicao = identifier
                print(st.exibirPosicao(posicao))
        
        
class Block(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)
                        
class EntradaOp(Node):
    def evaluate(self, st):
        nome = self.children[0].value
        sku = self.children[1].value
        quantidade = self.children[2].evaluate(st)[1]
        validade = self.children[3].value
        validade = datetime.date(validade[2], validade[1], validade[0]) if isinstance(validade, tuple) else validade
        produto = Produto(nome, sku, quantidade, validade)
        st.entradaItem(sku, produto)
        
class ReceberOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        quantidade = self.children[1].evaluate(st)[1]
        st.receber(sku, quantidade)
        
class AlocarOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        quantidade = self.children[1].evaluate(st)[1]
        posicao = self.children[2].value
        st.alocar(sku, quantidade, posicao)
        
class MoverOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        quantidade = self.children[1].evaluate(st)[1]
        posicaoInicial = self.children[2].value
        posicaoFinal = self.children[3].value
        st.mover(sku, quantidade, posicaoInicial, posicaoFinal)
        
class VenderOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        quantidade = self.children[1].evaluate(st)[1]
        if len(self.children) == 3:
            posicao = self.children[2].value
            st.diminuirQuantidade(sku, quantidade, posicao)
        else:
            st.diminuirQuantidade(sku, quantidade)
            
class DescartarOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        quantidade = self.children[1].evaluate(st)[1]
        posicao = self.children[2].value if len(self.children) == 3 else ""
        st.diminuirQuantidade(sku, quantidade, posicao)
        
class ConferirOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        posicao = self.children[1].value if len(self.children) == 2 else ""
        return ("INT", st.conferir(sku, posicao))
        
class ValidadeOp(Node):
    def evaluate(self, st):
        sku = self.children[0].value
        posicao = self.children[1].value
        dias = self.children[2].evaluate(st)[1]
        quantidade = st.validade(sku, posicao, dias)
        return ("INT", quantidade)
        
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()
        
    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position += 1
            
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return
        
        atual = self.source[self.position]
        
        if atual.isdigit():
            next_value = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                next_value += self.source[self.position]
                self.position += 1
            
            self.next = Token("INT", next_value)
            
        elif atual == "+":
            self.next = Token("PLUS", "+")
            self.position += 1
            
        elif atual == "-":
            self.next = Token("MINUS", "-")
            self.position += 1
        
        elif atual == "*":
            self.next = Token("MULT", "*")
            self.position += 1 
            
        elif atual == "/":
            self.next = Token("DIV", "/")
            self.position += 1
            
        elif atual == "(":
            self.next = Token("OPEN_PAR", "(")
            self.position += 1
            
        elif atual == ")":
            self.next = Token("CLOSE_PAR", ")")
            self.position += 1
            
        elif atual == "=":
            # Verifica se o próximo é "=":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                self.next = Token("EQUAL", "==")
                self.position += 2
            else:
                self.next = Token("ASSIGN", "=")
                self.position += 1
            
        elif atual == "{":
            self.next = Token("OPEN_BRACKET", "{")
            self.position += 1
        
        elif atual == "}":
            self.next = Token("CLOSE_BRACKET", "}")
            self.position += 1
            
        elif atual == "\n":
            self.next = Token("NEW_LINE", "")
            self.position += 1
            
        elif atual == "|":
            # Verifica se é o próximo é "|":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "|":
                self.next = Token("OR", "||")
                self.position += 2
            else:
                raise Exception("Invalid token")
            
        elif atual == "&":
            # Verifica se é o próximo é "&":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "&":
                self.next = Token("AND", "&&")
                self.position += 2
            else:
                raise Exception("Invalid token")
        
        elif atual == "!":
            self.next = Token("NOT", "!")
            self.position += 1
        
        elif atual == ">":
            self.next = Token("GREATER", ">")
            self.position += 1
            
        elif atual == "<":
            self.next = Token("LESS", "<")
            self.position += 1
            
        elif atual == ",":
            self.next = Token("COMMA", ",")
            self.position += 1
        
        elif atual.isalpha() or atual == "_" or atual == "'" or atual == '"':
            next_value = ""
            is_text = False
            
            if atual == '"':
                is_text = True
                next_value += atual
                self.position += 1
                
            while self.position < len(self.source):
                if is_text:
                    next_value += self.source[self.position]
                    self.position += 1
                    if self.source[self.position] == '"':
                        next_value += self.source[self.position]
                        self.position += 1
                        break
                
                elif self.source[self.position].isalnum() or self.source[self.position] == "_":
                    next_value += self.source[self.position]
                    self.position += 1
                else:
                    break
                
            # Palavras reservadas
            if next_value == "exibir":
                self.next = Token("PRINT", next_value)
            elif next_value == "enquanto":
                self.next = Token("WHILE", next_value)
            elif next_value == "se":
                self.next = Token("IF", next_value)
            elif next_value == "senao":
                self.next = Token("ELSE", next_value)
            elif next_value == "entrada":
                self.next = Token("ENTRADA", next_value)
            elif next_value == "receber":
                self.next = Token("RECEBER", next_value)
            elif next_value == "mover":
                self.next = Token("MOVER", next_value)
            elif next_value == "alocar":
                self.next = Token("ALOCAR", next_value)
            elif next_value == "vender":
                self.next = Token("VENDER", next_value)
            elif next_value == "descartar":
                self.next = Token("DESCARTAR", next_value)
            elif next_value == "estoque":
                self.next = Token("CONFERIR", next_value)
            elif next_value == "validade":
                self.next = Token("VALIDADE", next_value)
            elif next_value == "hoje":
                self.next = Token("HOJE", next_value)
                
            elif next_value == "int_var":
                self.next = Token("VAR", "INT")
            elif next_value == "bool_var":
                self.next = Token("VAR", "BOOL")
            elif next_value == "true":
                self.next = Token("BOOL", next_value)
            elif next_value == "false":
                self.next = Token("BOOL", next_value)
    
            else:
                self.next = Token("NOME", next_value)
            
        else:
            raise Exception(f"Invalid token, _{atual}_")
                
        

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
                                           
    def parseBlock(self):   
        final_result = Block("Block", [])
        
        if self.tokenizer.next.type == "OPEN_BRACKET":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type == "NEW_LINE":
                self.tokenizer.selectNext()
            else:
                raise Exception("Invalid block")
            
            while self.tokenizer.next.type != "CLOSE_BRACKET":
                final_result.children.append(self.parseStatement())
                
            self.tokenizer.selectNext()
            
        else:
            raise Exception(f"Invalid block: got {self.tokenizer.next.type}")
            
        return final_result
        
    def parseStatement(self):
        final_result = NoOp("", [])
        
        # Entrada
        if self.tokenizer.next.type == "OPEN_PAR":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "NOME":
                product_name = self.tokenizer.next.value
            else:
                raise Exception("Invalid statement, expected product name")
            self.tokenizer.selectNext()
            if not self.tokenizer.next.type == "COMMA":
                raise Exception("Invalid statement, expected comma after product name")
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "INT":
                product_sku = self.tokenizer.next.value
            else:
                raise Exception("Invalid statement, expected product sku")
            self.tokenizer.selectNext()
            if not self.tokenizer.next.type == "CLOSE_PAR":
                raise Exception("Invalid statement, expected closing parenthesis")
            self.tokenizer.selectNext()
            if not self.tokenizer.next.type == "ASSIGN":
                raise Exception("Invalid statement, expected assignment operator")
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR": 
                self.tokenizer.selectNext()
                quantity = self.parseExpression()
                if not self.tokenizer.next.type == "COMMA":
                    raise Exception(f"Invalid statement, expected comma after quantity, received {self.tokenizer.next.type}")
                self.tokenizer.selectNext()
                expiration_date = self.parseExpDate()
                if not self.tokenizer.next.type == "CLOSE_PAR":
                    raise Exception("Invalid statement, expected closing parenthesis")
                self.tokenizer.selectNext()
                final_result = EntradaOp("Entrada", [Identifier(product_name, []), Identifier(product_sku, []), quantity, Identifier(expiration_date, [])])
            else:
                raise Exception(f"Invalid statement in entrada: {self.tokenizer.next.type}")
            
        # Receber
        elif self.tokenizer.next.type == "RECEBER":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    product_sku = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        quantity = self.parseExpression()
                        if self.tokenizer.next.type == "CLOSE_PAR":
                            self.tokenizer.selectNext()
                            final_result = ReceberOp("Assign", [Identifier(product_sku, []), quantity])
                        else:
                            raise Exception("Invalid statement, expected closing parenthesis")
                    else:
                        raise Exception("Invalid statement, expected comma after product sku")
                else:
                    raise Exception("Invalid statement, expected product sku")
            else:
                raise Exception("Invalid statement, expected opening parenthesis")
            
        # Alocar(sku, quantidade, posicao)
        elif self.tokenizer.next.type == "ALOCAR":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    product_sku = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        quantity = self.parseExpression()
                        if self.tokenizer.next.type == "COMMA":
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "NOME":
                                position = self.tokenizer.next.value
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "CLOSE_PAR":
                                    self.tokenizer.selectNext()
                                    final_result = AlocarOp("Alocar", [Identifier(product_sku, []), quantity, Identifier(position, [])])
                                else:
                                    raise Exception("Invalid statement, expected closing parenthesis")
                            else:
                                raise Exception("Invalid statement, expected position name")
                            
        # Mover(sku, quantidade, posicaoInicial, posicaoFinal)
        elif self.tokenizer.next.type == "MOVER":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    product_sku = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        quantity = self.parseExpression()
                        if self.tokenizer.next.type == "COMMA":
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "NOME":
                                position_initial = self.tokenizer.next.value
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "COMMA":
                                    self.tokenizer.selectNext()
                                    if self.tokenizer.next.type == "NOME":
                                        position_final = self.tokenizer.next.value
                                        self.tokenizer.selectNext()
                                        if self.tokenizer.next.type == "CLOSE_PAR":
                                            self.tokenizer.selectNext()
                                            final_result = MoverOp("Mover", [Identifier(product_sku, []), quantity, Identifier(position_initial, []), Identifier(position_final, [])])
                                        else:
                                            raise Exception("Invalid statement, expected closing parenthesis")
                                    else:
                                        raise Exception("Invalid statement, expected final position name")
                                else:
                                    raise Exception("Invalid statement, expected comma after initial position")
                            else:
                                raise Exception("Invalid statement, expected initial position name")
                        else:
                            raise Exception("Invalid statement, expected comma after quantity")
                    else:
                        raise Exception("Invalid statement, expected comma after product sku")
                else:
                    raise Exception("Invalid statement, expected product sku")
        
        # Vender (sku, quantidade) posicao é opcional
        elif self.tokenizer.next.type == "VENDER":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    product_sku = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        quantity = self.parseExpression()
                        if self.tokenizer.next.type == "CLOSE_PAR":
                            self.tokenizer.selectNext()
                            final_result = VenderOp("Vender", [Identifier(product_sku, []), quantity])
                        elif self.tokenizer.next.type == "COMMA":
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "NOME":
                                position = self.tokenizer.next.value
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "CLOSE_PAR":
                                    self.tokenizer.selectNext()
                                    final_result = VenderOp("Vender", [Identifier(product_sku, []), quantity, Identifier(position, [])])
                                else:
                                    raise Exception("Invalid statement, expected closing parenthesis")
                            else:
                                raise Exception("Invalid statement, expected position name")
                        else:
                            raise Exception("Invalid statement, expected closing parenthesis")
                    else:
                        raise Exception("Invalid statement, expected comma after product sku")
                else:
                    raise Exception("Invalid statement, expected product sku")
                
        # Descartar(sku, quantidade, posicao)
        elif self.tokenizer.next.type == "DESCARTAR":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    product_sku = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        quantity = self.parseExpression()
                        if self.tokenizer.next.type == "COMMA":
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "NOME":
                                position = self.tokenizer.next.value
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "CLOSE_PAR":
                                    self.tokenizer.selectNext()
                                    final_result = DescartarOp("Descartar", [Identifier(product_sku, []), quantity, Identifier(position, [])])
                                else:
                                    raise Exception("Invalid statement, expected closing parenthesis")
                            else:
                                raise Exception("Invalid statement, expected position name")
                        elif self.tokenizer.next.type == "CLOSE_PAR":
                            self.tokenizer.selectNext()
                            final_result = DescartarOp("Descartar", [Identifier(product_sku, []), quantity])
                        else:
                            raise Exception("Invalid statement, expected closing parenthesis")
                    else:
                        raise Exception("Invalid statement, expected comma after product sku")
                else:
                    raise Exception("Invalid statement, expected product sku")
                
        # Exibir (posicao ou sku)
        elif self.tokenizer.next.type == "PRINT":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "NOME":
                    identifier_name = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "CLOSE_PAR":
                        self.tokenizer.selectNext()
                        final_result = Print("Print", [Identifier(identifier_name, [])])
                    else:
                        raise Exception("Invalid statement, expected closing parenthesis")
                elif self.tokenizer.next.type == "INT":
                    sku = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "CLOSE_PAR":
                        self.tokenizer.selectNext()
                        final_result = Print("Print", [Identifier(sku, [])])
                    else:
                        raise Exception("Invalid statement, expected closing parenthesis")
            
        # Variaveis auxiliares:
        elif self.tokenizer.next.type == "VAR":
            var_type = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "NOME":
                identifier_name = self.tokenizer.next.value
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "ASSIGN":
                    self.tokenizer.selectNext()
                    value = self.parseBExpression()
                    if self.tokenizer.next.type == "NEW_LINE":
                        self.tokenizer.selectNext()
                        final_result = VarDec("VarDec", [Identifier(identifier_name, []), VarType(var_type, []), value])
                    else:
                        raise Exception(f"Invalid statement, got {self.tokenizer.next.type} expected new line after variable declaration")
                elif self.tokenizer.next.type == "NEW_LINE":
                    self.tokenizer.selectNext()
                    final_result = VarDec("VarDec", [Identifier(identifier_name, []), VarType(var_type, [])])
                    
        elif self.tokenizer.next.type == "NOME":
            identifier_name = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.selectNext()
                value = self.parseBExpression()
                if self.tokenizer.next.type == "NEW_LINE":
                    self.tokenizer.selectNext()
                    final_result = Assign("Assign", [Identifier(identifier_name, []), value])
                else:
                    raise Exception("Invalid statement, expected new line after assignment")
            else:
                raise Exception("Invalid statement, expected assignment operator after identifier")
            
        elif self.tokenizer.next.type == "WHILE":
            self.tokenizer.selectNext()
            condition = self.parseBExpression()
            expression = self.parseBlock()
            final_result = WhileOp("while", [condition, expression])
            
        elif self.tokenizer.next.type == "IF":
            self.tokenizer.selectNext()
            
            condition = self.parseBExpression()
            
            expression = self.parseBlock()
            if self.tokenizer.next.type == "ELSE":
                self.tokenizer.selectNext()
                expression2 = self.parseBlock()
                final_result = IfOp("if", [condition, expression, expression2])
            else:
                final_result = IfOp("if", [condition, expression])
            
        elif self.tokenizer.next.type == "NEW_LINE":
            self.tokenizer.selectNext()
        else:
            raise Exception(f"Invalid statement, got {self.tokenizer.next.type}, {self.tokenizer.next.value}")
            
        return final_result
    
    def parseExpDate(self):
        if self.tokenizer.next.type == "INT":
            dia = int(self.tokenizer.next.value)
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "DIV":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    mes = int(self.tokenizer.next.value)
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "DIV":
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.type == "INT":
                            ano = int(self.tokenizer.next.value)
                            self.tokenizer.selectNext()
                            return (dia, mes, ano)
                        else:
                            raise Exception("Invalid year in expiration date")
                    else:
                        raise Exception("Invalid expiration date format, expected '/' after month")
                else:
                    raise Exception("Invalid month in expiration date")
                
    
    def parseBExpression(self):
        result = self.parseBTerm()
        
        while self.tokenizer.next.type == "OR":
            self.tokenizer.selectNext()
            result = BinOp("||", [result, self.parseBTerm()])
            
        return result
            
    def parseBTerm(self):
        result = self.parseRelExpression()
        
        while self.tokenizer.next.type == "AND":
            self.tokenizer.selectNext()
            result = BinOp("&&", [result, self.parseRelExpression()])
            
        return result
    
    def parseRelExpression(self):
        result = self.parseExpression()
        
        while self.tokenizer.next.type in ["GREATER", "LESS", "EQUAL"]:
            if self.tokenizer.next.type == "GREATER":
                self.tokenizer.selectNext()
                result = BinOp(">", [result, self.parseExpression()])
                
            elif self.tokenizer.next.type == "LESS":
                self.tokenizer.selectNext()
                result = BinOp("<", [result, self.parseExpression()])
                
            elif self.tokenizer.next.type == "EQUAL":
                self.tokenizer.selectNext()
                result = BinOp("==", [result, self.parseExpression()])
                
        return result
    
    def parseExpression(self):
        result = self.parseTerm()
        
        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.selectNext()
                result = BinOp("+", [result, self.parseTerm()])
                
            elif self.tokenizer.next.type == "MINUS":
                self.tokenizer.selectNext()
                result = BinOp("-", [result, self.parseTerm()])
                
        return result
    
    def parseTerm(self):
        result = self.parseFactor()
        
        while self.tokenizer.next.type in ["MULT", "DIV"]:

            if self.tokenizer.next.type == "MULT":
                self.tokenizer.selectNext()
                result = BinOp("*", [result, self.parseFactor()])
        
                
            elif self.tokenizer.next.type == "DIV":
                    self.tokenizer.selectNext()
                    result = BinOp("/", [result, self.parseFactor()])     
        
        return result
    
    def parseFactor(self):
        # Conferir ( SKU, Posicao ) -> retorna a quantidade de itens na posição, se nao tiver posicao, retorna todos os itens do SKU
        if self.tokenizer.next.type == "CONFERIR":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    sku = int(self.tokenizer.next.value)
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.type == "NOME":
                            position = self.tokenizer.next.value
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "CLOSE_PAR":
                                self.tokenizer.selectNext()
                                return ConferirOp("Conferir", [Identifier(sku, []), Identifier(position, [])])
                            else:
                                raise Exception("Invalid statement, expected closing parenthesis")
                        else:
                            raise Exception("Invalid statement, expected position name")
                    elif self.tokenizer.next.type == "CLOSE_PAR":
                        self.tokenizer.selectNext()
                        return ConferirOp("Conferir", [Identifier(sku, [])])
                    else:
                        raise Exception("Invalid statement, expected closing parenthesis")
                    
        # Validade (sku, posicao, dias) -> retorna a quantidade de produtos com validade dentro dos dias especificados
        elif self.tokenizer.next.type == "VALIDADE":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    sku = int(self.tokenizer.next.value)
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.type == "NOME":
                            position = self.tokenizer.next.value
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "COMMA":
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "INT":
                                    days = int(self.tokenizer.next.value)
                                    self.tokenizer.selectNext()
                                    if self.tokenizer.next.type == "CLOSE_PAR":
                                        self.tokenizer.selectNext()
                                        return ValidadeOp("Validade", [Identifier(sku, []), Identifier(position, []), IntVal(days, [])])
                                    else:
                                        raise Exception("Invalid statement, expected closing parenthesis")
                                else:
                                    raise Exception("Invalid statement, expected days")
                            else:
                                raise Exception("Invalid statement, expected closing parenthesis")
                        else:
                            raise Exception("Invalid statement, expected position name")
                    else:
                        raise Exception("Invalid statement, expected comma after sku")
                else:
                    raise Exception("Invalid statement, expected sku")
        
        elif self.tokenizer.next.type == "NOME":
            result = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return result
        
        elif self.tokenizer.next.type == "BOOL":
            value = True if self.tokenizer.next.value.lower() == "true" else False
            result = BoolVal(value, [])
            self.tokenizer.selectNext()
            return result
        
        elif self.tokenizer.next.type == "INT":
            result = IntVal(int(self.tokenizer.next.value), [])
            self.tokenizer.selectNext()
            return result
        
        elif self.tokenizer.next.type == "PLUS":
            self.tokenizer.selectNext()
            result = UnOp("+", [self.parseFactor()])
            return result
        
        elif self.tokenizer.next.type == "MINUS":
            self.tokenizer.selectNext()
            result = UnOp("-", [self.parseFactor()])
            return result
        
        elif self.tokenizer.next.type == "NOT":
            self.tokenizer.selectNext()
            result = UnOp("!", [self.parseFactor()])
            return result
        
        elif self.tokenizer.next.type == "READ":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPEN_PAR":
                self.tokenizer.selectNext()
                result = Read("Scan", [])
                
                if self.tokenizer.next.type == "CLOSE_PAR":
                    self.tokenizer.selectNext()
                    return result
                
                else:
                    raise Exception("Parenthesis was not closed in read")
        
        elif self.tokenizer.next.type == "OPEN_PAR":
            self.tokenizer.selectNext()
            resultado = self.parseBExpression()
            
            if self.tokenizer.next.type == "CLOSE_PAR":
                self.tokenizer.selectNext()
                return resultado
            
            else:
                raise Exception("Parenthesis was not closed in expression")
            
        else:
            raise Exception(f"Invalid input for parseFactor: {self.tokenizer.next.type}")
        
    def run(self, code):
        self.tokenizer = Tokenizer(code)
        resultado = self.parseBlock()
        
        if self.tokenizer.next.type != "EOF":
            raise Exception("Code must end with EOF")
        
        return resultado
    
class PrePro():
    def __init__(self, code):
        self.code = code
        
    def filter(self):
        new_code = ""
        
        new_code += re.sub(r'//.*', '', self.code) + " "
        new_code = re.sub(r'\t', '    ', new_code)
            
        self.code = new_code
        return self.code
    
def exportSymbolTable(symbol_table):
    with open("estoque.txt", "w") as file:
        for key, value in symbol_table.estoque.items():
            file.write(f"{key}: {'; '.join([str(produto) for produto in value])}\n")
         
def importInitialStock(st, filename="estoque.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                posicao, produtos = line.strip().split(": ")
                posicao = posicao.strip()
                produtos = produtos.split("; ")
                for produto in produtos:
                    nome, sku, quantidade, validade = produto.split(", ")
                    nome = nome.split("=")[1].strip()
                    sku = str(sku.split("=")[1].strip())
                    quantidade = int(quantidade.split("=")[1].strip())
                    
                    validade = validade.replace(")","").split("=")[1].strip()
                    ano, mes, dia = map(int, validade.split("-"))
                    validade = datetime.date(ano, mes, dia)
                    
                    st.importaProduto(posicao, Produto(nome, sku, quantidade, validade))

    except FileNotFoundError:
        print(f"File {filename} not found. No initial stock to import.")
        return
    
    
def main():
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        code = file.read()
    
    code = PrePro(code).filter()
    parser = Parser(Tokenizer(code))
    result = parser.run(code)
    
    st = SymbolTable()
    if len(sys.argv) > 2:
        importInitialStock(st, sys.argv[2])
    
    for posicao, produtos in st.estoque.items():
        print(f"{posicao}: {', '.join([str(produto) for produto in produtos])}")
    result.evaluate(st)
    
    exportSymbolTable(st)
if __name__ == "__main__":
    main()