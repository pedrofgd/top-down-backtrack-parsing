# to-down backtrack parsing
# analise sintatica descendente com retorno

'''
  IMPLEMENTAR:
    * ser capaz de utilizar mais de um sibmolo nao terminal
    * ser capaz de utilizar mais do que 9 regras de producao por simbolo nao terminal
    * reconhecer cadeia vazia (v) (K, D, Z)
    * adicionar o simbolo $ no final de beta
'''

# Implementar cadeia vazia (o restante acho que esta funcionando)

# Obs:
# * 0 nao e reconhecido como primeiro simbolo
# * Em w = 1+1 o primeiro 1 esta sendo reconhecido, mas o + ainda nao

w = input("entre a cadeia: ")

terminals = ["+", "-", "*", "/", "(", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
non_terminals = ["I","S","K","T","Z","F","N","D"]

prod_rules_count_for_symbol = {'I': 1,'S': 1,'K': 3,'T': 1,'Z': 3,'F': 3,'N': 9,'D': 11}
prod_rules = {
  'I0': 'S',
  'S0': "TK",
  'K0': "+TK", 'K1': "-TK", 'K2': "v",
  'T0': "FZ", 
  'Z0': "*FZ", 'Z1': "/FZ", 'Z2': "v",
  'F0': "(S)", 'F1': "N", 'F2': "-N",
  'N0': "1D", 'N1': "2D", 'N2': "3D", 'N3': "4D", 'N4': "5D", 'N5': "6D", 'N6': "7D", 'N7': "8D", 'N8': "9D",
  'D0': "0D", 'D1': "1D", 'D2': "2D", 'D3': "3D", 'D4': "4D", 'D5': "5D", 'D6': "6D", 'D7': "7D", 'D8': "8D", 'D9': "9D", 'D10': "v"
}

enumerable_prod_rules = []
for key in prod_rules:
  enumerable_prod_rules.append(key)

alpha = [] # list 1 para o historico de regras de produção
beta = [] # list 2 para a configuracao das folhas da arvore de derivacao
generated_w = []
belongs_to_language = False

def tree_expanse(rule_count, rule_symbol):
  if rule_symbol == None:
    formated_prod_rule = 'I0'
  else:
    formated_prod_rule = "{0}{1}".format(rule_symbol, rule_count)
    print('formated_prod_rule:',formated_prod_rule)
  
  rule = prod_rules.get(formated_prod_rule)
  if rule == None:
    return False

  alpha.append(formated_prod_rule)
  if len(beta) != 0:
    beta.pop(0)
  for symbol in rule[::-1]:
    beta.insert(0, symbol)

  print("treee expanded for: alpha {} and beta {}".format(alpha, beta))
  return True

def sucessfull_match():
  alpha.append(beta[0]) # passa para beta o topo de alpha
  beta.pop(0)  # remove o entao topo de beta

def backtracking():
  alpha_top = alpha[len(alpha)-1]

  if alpha_top in terminals:
    beta.insert(0, alpha[len(alpha)-1]) # adiciona em beta o topo de alpha
    alpha.pop(len(alpha)-1) # remove o topo de alpha

  elif alpha_top in enumerable_prod_rules:
    # acredito que nao vai mais ser necessario utilizar o index, ja que o proprio alpha top e a key
    index = []
    for symbol in alpha_top:
      index.append(symbol)
    symbol_rule = prod_rules.get(alpha_top)
    for i in range(0, len(symbol_rule)):
      beta.pop(0)
    
    beta.insert(0, index[0]) # adiciona em beta o topo de alpha (Sn)
    alpha.pop(len(alpha)-1) # remove o topo de alpha (Sn)

    print("backtracking for: beta {} and w {} and alpha {}".format(beta, w, alpha))

print("starting top_down_backtrack_parsing")
def top_down_backtrack_parsing():
  list_w = split_w(w)
  qty_w = len(list_w)
  symbols_count = 0
  rule_count = 0
  rule_symbol_count = 0

  # primeira expansao
  if len(alpha) == 0:
    expanse_result = tree_expanse(rule_count, None)
    if expanse_result == False:
      return False
  # acho que isso nao faz diferenca, mas confirmar:
  else:
    rule_symbol = alpha[len(alpha)-1][0]
    expanse_result = tree_expanse(rule_count, rule_symbol)
    if expanse_result == False:
      return False

  while(symbols_count < qty_w): # enquanto nao encontrar todos os simbolos
    debug(alpha, beta, w, symbols_count)

    looking_for_symbol = ''
    if beta[0] in non_terminals:
      looking_for_symbol = beta[0]
    else:
      looking_for_symbol = alpha[len(alpha)-1] # se topo de beta (beta[0]) for um terminal, olha para topo de alpha para expandir

    looking_for_symbol_number_of_rules = prod_rules_count_for_symbol.get(looking_for_symbol)
    if rule_count > looking_for_symbol_number_of_rules and rule_symbol_count > len(enumerable_prod_rules) -1: 
      return False

    if beta[0] in non_terminals:
      rule_symbol = beta[0][0]
      print('rule_symbol:', rule_symbol)
      expanse_result = tree_expanse(rule_count, rule_symbol)
      if expanse_result == False:
        backtracking()

    internal_rule_count = 0
    while(beta[0] != list_w[symbols_count]):
      print()
      if symbols_count >= qty_w or internal_rule_count > looking_for_symbol_number_of_rules: 
        print("symbols_count: {}, qty_w: {}, internal_rule_count: {}, looking_for_symbols_rules_number: {}, looking_for_symbol: {}"          
          .format(symbols_count, qty_w, internal_rule_count, looking_for_symbol_number_of_rules, looking_for_symbol))
        return False

      # acho que isso:
      # if internal_rule_count < looking_for_symbol_number_of_rules:
      # nao vai mais servir de nada

      if internal_rule_count <= looking_for_symbol_number_of_rules:
        if len(alpha) > 0 :
          if beta[0] in non_terminals:
            if beta[0] != looking_for_symbol:
              looking_for_symbol = beta[0]
              looking_for_symbol_number_of_rules = prod_rules_count_for_symbol.get(looking_for_symbol)
              if rule_count > looking_for_symbol_number_of_rules and rule_symbol_count > len(enumerable_prod_rules) -1: 
                return False
              internal_rule_count = 0
            rule_symbol = beta[0][0]
            expanse_result = tree_expanse(internal_rule_count, rule_symbol)
            if expanse_result == False:
              backtracking()

          else:
            if beta[0] != list_w[symbols_count]:
              internal_rule_count += 1
              backtracking()

    rule_count += 1
    
    # sucessfull match
    if beta[0] == list_w[symbols_count]:
      print("sucessful match for: beta {} and w {}, at count {}\n".format(beta, w, symbols_count))
      sucessfull_match()
      generated_w.append(alpha[len(alpha)-1])
      print("generated w by now:", generated_w)
      rule_count = 0
      symbols_count += 1
    else:
      rule_count += 1
      print("incrementando rule_count +1 = {}".format(rule_count))

    if w == list_to_string(generated_w):
      return True

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

result = top_down_backtrack_parsing()

print("\nDoes w = {0} belongs to the language: {1}".format(w, result))