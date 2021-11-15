# to-down backtrack parsing
# analise sintatica descendente com retorno

'''
  IMPLEMENTAR:
    * ser capaz de utilizar mais de um sibmolo nao terminal
    * ser capaz de utilizar mais do que 9 regras de producao por simbolo nao terminal
    * reconhecer cadeia vazia (v) (K, D, Z)
'''

w = input("entre a cadeia: ")
terminals = ["+", "-", "*", "/", "(", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
non_terminals = ["I","S","K","T","Z","F","N","D"]
prod_rules_I = ["S"]
prod_rules_S = ["TK"]
prod_rules_K = ["+TK", "-TK", "v"]
prod_rules_T = ["FZ"]
prod_rules_Z = ["*FZ", "/FZ", "v"]
prod_rules_F = ["(S)", "N", "-N"]
prod_rules_N = ["1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D"]
prod_rules_D = ["0D", "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "v"]
enumerable_prod_rules = ["S0", "S1", "S2"]

i = 0         # localizacao do ponteiro de entrada
s = "q"       # estado do algoritmo
alpha = []    # list 1 para o historico de regras de produção
beta = []     # list 2 para a configuracao das folhas da arvore de derivacao
generated_w = []
belongs_to_language = False

def tree_expanse(rule_count):
  s = "q"
  rule = prod_rules_S[rule_count]
  alpha.append("S{0}".format(rule_count))
  if len(beta) != 0:
    beta.pop(0)
  for symbol in rule[::-1]:
    beta.insert(0, symbol)

def sucessfull_match():
  global i 
  i += 1
  s = "q"
  alpha.append(beta[0]) # passa para beta o topo de alpha
  beta.pop(0)  # remove o entao topo de beta

def backtracking():
  global i 
  i -= 1
  s = "b"
  alpha_top = alpha[len(alpha)-1]

  if alpha_top in terminals:
    beta.insert(0, alpha[len(alpha)-1]) # adiciona em beta o topo de alpha
    alpha.pop(len(alpha)-1) # remove o topo de alpha

  elif alpha_top in enumerable_prod_rules:
    index = []
    for symbol in alpha_top:
      index.append(symbol)
    # print(beta)
    for i in range(0, len(prod_rules_S[int(index[1])])):
      # print(i)
      beta.pop(0)
    beta.insert(0, index[0]) # adiciona em beta o topo de alpha (Sn)
    alpha.pop(len(alpha)-1) # remove o topo de alpha (Sn)

def split_w(w):
  symbols = []
  for i in w:
    symbols.append(i)

  return symbols

def list_to_string(list):
  string = ""
  for symbol in list:
    string += str(symbol) + ""
  return string

def debug(alpha, beta, w, symbols_count):
  print("alpha:",alpha)
  print("beta:",beta)
  print("beta[symbols_count]:",beta[0])
  print("w[symbols_count]:",w[symbols_count])
  print("symbols_count:",symbols_count)
  print()

def top_down_backtrack_parsing():
  list_w = split_w(w)
  qty_w = len(list_w)
  symbols_count = 0
  rule_count = 0

  tree_expanse(rule_count)

  while(symbols_count < qty_w):
    # Debug
    debug(alpha, beta, w, symbols_count)

    if rule_count > len(prod_rules_S) - 1: 
      return False

    if beta[0] in non_terminals:
      tree_expanse(rule_count)
      print("treee expanded for: alpha {} and beta {}".format(alpha, beta))

    while(beta[0] != list_w[symbols_count]):
      if symbols_count >= qty_w or rule_count > len(prod_rules_S) - 1: 
        # belongs_to_language = False
        return False

      if len(alpha) > 0 :
        if beta[0] in non_terminals:
          tree_expanse(rule_count)
          print("treee expanded for: alpha {} and beta {}".format(alpha, beta))
        
        if beta[0] != list_w[symbols_count]:
          backtracking()
          print("backtracking for: beta {} and w {}, at count {}".format(beta, w, symbols_count))
          rule_count += 1

    if beta[0] == list_w[symbols_count]:
      print("sucessful match for: beta {} and w {}, at count {}\n".format(beta, w, symbols_count))
      sucessfull_match()
      generated_w.append(alpha[len(alpha)-1])
      print("generated w by now:", generated_w)
      rule_count = 0
      symbols_count += 1

    # Debug
    # generated_w_string = list_to_string(generated_w)
    # print(w)
    # print(generated_w_string)

    if w == list_to_string(generated_w):
      # belongs_to_language = True
      return True

result = top_down_backtrack_parsing()

print("\nDoes w = {0} belongs to the language: {1}".format(w, result))