# Clase que nos ayudara a crear un NFA
# Atributos:
#   start - Estado inicial
#   end - Estado final
import itertools


class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # Funcion para mostrar el NFA
    def show(self):
        self.start.show()
    # Funcion para obtener todos los estados

    def getAllStates(self):
        return list(self.start.getAllStates())
    # Funcion para obtener todos los estados en orden

    def getAllStatesInOrder(self):
        return self.start.getAllStatesInOrder()
    # Funcion para obtener todos los simbolos
    # NO USAR ESTA FUNCION mejor obtener los simbolos de la expresion regular

    def getAllSymbols(self):
        return list(self.start.getAllSymbols())
    # Funcion para asginar nombre a todos los estados

    def setNameToAllStates(self, name=0):
        for state in self.getAllStatesInOrder():
            state.setName(f"q{name}")
            name += 1


# Clase que nos ayudara a representar un estado
# Atributos:
#   transitions - Diccionario que contiene las transiciones del estado
class State:
    def __init__(self, transitions=None, name=None):
        self.transitions = transitions if transitions else {}
        self.name = name

    # Funcion para agregar una transicion
    # Parametros:
    #  symbol - Simbolo de la transicion
    #  state - Estado al que se llega
    def addTransition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

    # Funcion para agregar un nombre al estado
    # Parametros:
    #  name - Nombre del estado
    def setName(self, name):
        self.name = name

    # Clase que nos ayudara a mostrar el NFA
    def show(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        statesNames = []
        clave = ""
        for key in self.transitions:
            clave = key
            for state in self.transitions[key]:
                statesNames.append(state.name)
        print(f"{self.name} -- {clave} -> {statesNames}")
        for key in self.transitions:
            for state in self.transitions[key]:
                state.show(visited)

    # Funcion para obtener todos los estados en orden
    def getAllStatesInOrder(self, visited=None):
        if visited is None:
            visited = []
        if self in visited:
            return
        visited.append(self)
        for key in self.transitions:
            for state in self.transitions[key]:
                state.getAllStatesInOrder(visited)
        return visited

    # Funcion para obtener todos los estados
    def getAllStates(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        for key in self.transitions:
            for state in self.transitions[key]:
                state.getAllStates(visited)
        return visited

    # Funcion para obtener todos los simbolos de la transiciones del estado
    # Parametros:
    # symbol - Simbolo de la transicion
    def getTransition(self, symbol):
        if symbol in self.transitions:
            return self.transitions[symbol]
        return None

    # Funcion para obtener todos los simbolos
    # NO USAR ESTA FUNCION mejor obtener los simbolos de la expresion regular
    def getAllSymbols(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        for key in self.transitions:
            visited.add(key)
            for state in self.transitions[key]:
                state.getAllSymbols(visited)
        return visited

# simbolo de epsilon = &
# Algoritmo de Thompson para convertir una expresion regular a un NFA
# Apoyo https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b


def Thompson(Regex):
    NFAstack = []
    for char in Regex:

        if char == '|':
            nfa2 = NFAstack.pop()
            nfa1 = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa1.start)
            start.addTransition('&', nfa2.start)
            nfa1.end.addTransition('&', end)
            nfa2.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '?':
            nfa2 = NFAstack.pop()
            nfa1 = NFAstack.pop()
            nfa1.end.transitions = {
                **nfa1.end.transitions, ** nfa2.start.transitions}
            NFAstack.append(NFA(nfa1.start, nfa2.end))

        elif char == '*':
            nfa = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa.start)
            start.addTransition('&', end)
            nfa.end.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '+':
            nfa = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa.start)
            nfa.end.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        else:
            end = State()
            start = State(transitions={char: [end]})
            NFAstack.append(NFA(start, end))

    return NFAstack.pop()

# Funcion para obtener todos los estados alcanzables desde un estado a través de epsilon


def epsilonClosure(state):
    if state is None:
        return set()
    closure = set()
    closure.add(state)
    if '&' in state.transitions:
        for state in state.transitions['&']:
            closure = closure.union(epsilonClosure(state))
    return closure

# Funcion para obtener todos los estados alcanzables desde un conjunto de estados a través de epsilon


def epsilonClosureOfSet(states):
    closure = set()
    for state in states:
        closure = closure.union(epsilonClosure(state))
    return closure

# Funcion para obtener los nombres de los estados en string


def getFixedName(states):
    newName = ""
    numbers = []
    for state in states:
        numbers.append(int(state.name[1:]))

    numbers.sort()
    for number in numbers:
        newName += f"{number},"

    return newName[:-1]

# Funcion para obtener todos los estados alcanzables desde un conjunto de estados a través de un simbolo


def getTransions(states, symbol):
    transiciones = set()
    for state in states:
        if symbol in state.transitions:
            for state in state.transitions[symbol]:
                transiciones.add(state)
    return transiciones

# Funcion para obtener todos los estados por nombre
# Parametros:
#  states - Conjunto de estados
#  names - Nombres de los estados en lista


def getStatesByName(states, names):
    statesByName = set()
    nNames = []
    for name in names:
        nNames.append(f"q{name}")
    for state in states:
        if state.name in nNames:
            statesByName.add(state)
    return statesByName


# Algoritmo de subconjuntos para convertir un NFA a un DFA
# VIDEOS DE APOYO
# https://www.youtube.com/watch?v=WikU-ujoCqg
# https://www.youtube.com/watch?v=vt2x0W_jcPU
# https://www.youtube.com/watch?v=DjH7K7MZRAw&t=1427s

def subsetConstruction(NFA, expression):
    DFA = {}
    start = NFA.start
    newStates = {}
    simbolos = []
    for c in expression:
        if c not in simbolos and c not in ['|', '?', '*', '+']:
            simbolos.append(c)

    DFA = {"Estados": [], }
    for s in simbolos:
        if s != '&':
            DFA[s] = []

    # epsilon closure del estado inicial
    data = epsilonClosure(start)
    # Creamos el estado inicial del DFA
    valor = f"S{len(newStates)}"
    newStates[valor] = getFixedName(data)

    DFA['Estados'] = [valor]
    for STATE in enumerate(DFA['Estados']):
        ndata = getStatesByName(
            NFA.getAllStates(), newStates[STATE[1]].split(','))
        newSet = set()
        for state in ndata:
            newSet = newSet.union(epsilonClosure(state))
        data = ndata
        for s in simbolos:
            if s != '&':
                transiciones = getTransions(data, s)
                nData = set()
                for state in transiciones:
                    nData = nData.union(epsilonClosure(state))
                # print("nData",nData)
                nName = getFixedName(nData)
                # print(nName)
                if nName != "":
                    if nName not in newStates.values():
                        valor = f"S{len(newStates)}"

                        newStates[valor] = nName
                        DFA['Estados'].append(valor)
                        DFA[s].append(valor)
                    else:
                        for key in newStates:
                            if newStates[key] == nName:
                                DFA[s].append(key)
                else:
                    DFA[s].append("NONE")
    estadosAceptacion = []
    finalState = NFA.end.name.split('q')[1]
    for state in DFA['Estados']:
        if finalState in newStates[state].split(','):
            estadosAceptacion.append(state)

    DFA['Aceptacion'] = estadosAceptacion

    return DFA


# TODO Simulacion de AFN
def simulation():
    print('Simulation')


# Funcion para retornar pares de cadenas de estados
def state_pairs(table: dict):
    # subset construction already removed the non reachable states
    cadenas = []
    current_state_counter = 0
    next_state_counter = 0
    working = True
    while working:
        if (next_state_counter == len(table['Estados'])):
            next_state_counter = 0
        elif(current_state_counter == len(table["Estados"]) - 1):
            working = False
        pair = (
            table["Estados"][current_state_counter],
            table["Estados"][next_state_counter]
        )
        if (table["Estados"][current_state_counter] != table["Estados"][next_state_counter] and table["Estados"][current_state_counter] != "NONE" and table["Estados"][current_state_counter] != "NONE"):
            cadenas.append(pair)
        next_state_counter += 1

        if(next_state_counter == len(table["Estados"])):
            current_state_counter += 1

    return cadenas


def a_pairs(table: dict):
    # subset construction already removed the non reachable states
    cadenas = []
    current_state_counter = 0
    next_state_counter = 0
    working = True
    while working:
        if (next_state_counter == len(table['a'])):
            next_state_counter = 0
        elif(current_state_counter == len(table["a"]) - 1):
            working = False
        pair = (
            table["a"][current_state_counter],
            table["a"][next_state_counter]
        )
        if (table["a"][current_state_counter] != table["a"][next_state_counter]):
            cadenas.append(pair)
        next_state_counter += 1

        if(next_state_counter == len(table["a"])):
            current_state_counter += 1
    cadenas = list(set(cadenas))
    return cadenas


def b_pairs(table: dict):
    # subset construction already removed the non reachable states
    cadenas = []
    current_state_counter = 0
    next_state_counter = 0
    working = True
    while working:
        if (next_state_counter == len(table['b'])):
            next_state_counter = 0
        elif(current_state_counter == len(table["b"]) - 1):
            working = False
        pair = (
            table["b"][current_state_counter],
            table["b"][next_state_counter]
        )
        if (table["b"][current_state_counter] != table["b"][next_state_counter]):
            cadenas.append(pair)
        next_state_counter += 1

        if(next_state_counter == len(table["b"])):
            current_state_counter += 1
    # remove all repeated tuples from list
    cadenas = list(set(cadenas))
    return cadenas


def minimization(state_pairs, table):
    # Get all pairs that have the acceptance state as a first item
    first_is_AE = [pairs for pairs in state_pairs
                   if any(element == pairs[0] for element in table["Aceptacion"]) and any(element != pairs[1] for element in table["Aceptacion"])]
    # Get all pairs that have the acceptance state as a second item
    second_is_AE = [pairs for pairs in state_pairs
                    if any(element != pairs[0] for element in table["Aceptacion"]) and any(element == pairs[1] for element in table["Aceptacion"])]

    # Declare all posible matches on A and B transitions
    B_combinations = b_pairs(table)
    A_combinations = a_pairs(table)

    # combine both AE of distinguished chains in to a single list
    first_is_AE.extend(second_is_AE)
    # combine both A and B combinations in to a single list
    B_combinations.extend(A_combinations)

    # Asign new variable names
    dist_chains = first_is_AE
    ab_comb = B_combinations
