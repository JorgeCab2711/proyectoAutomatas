#  Proyecto de automatas
#  Universidad del Valle de Guatemala
#  Teoria de la computacion

#  Autores:
# - Alejandra Guzman 20262
# - Pablo Escobar 20936
# - Jorge Caballeros 20009

from Algorithms import Thompson



# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
# basado en el algoritmo de Shunting-yard 
def parseRegexToPostfix(regex):
    outputQueue = []
    operatorStack = []
    operatorPrecedence = {
        '*': 3,
        '?': 2,
        '|': 1,
        '+': 1,
        '(': 0,
        ')': 0
    }

    for char in regex:
        if char == '(':
            operatorStack.append(char)
        elif char == ')':
            while operatorStack[-1] != '(':
                outputQueue.append(operatorStack.pop())
            operatorStack.pop()
        elif char in operatorPrecedence:
            while operatorStack and operatorPrecedence[char] <= operatorPrecedence[operatorStack[-1]]:
                outputQueue.append(operatorStack.pop())
            operatorStack.append(char)
        else:
            outputQueue.append(char)

    while operatorStack:
        outputQueue.append(operatorStack.pop())

    return outputQueue
       

# Funcion para revisar que los parentesis esten balanceados
# param - cadena de caracteres
def revisarParentesis(cadena):
    count= 0  
    ans=False  
    for i in cadena:  
        if i == "(":  
            count += 1  
        elif i == ")":  
            count-= 1  
        if count < 0:  
            return ans  
    if count==0:  
        return not ans  
    return ans  

# Funcion para valida que la expresion regular es valida
# param - expresion regular 
def validarExpresionRegular(expresion):
    bandera = False
    caracteres = ["(", ")", "|", "*", "?","+"]
    for caracter in expresion:
        if caracter.isalnum() or caracter in caracteres:
            bandera = True
    return bandera and revisarParentesis(expresion)

   
# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
def createFixedRegex(regex):
    newRegex = ""
    for i in range(len(regex)):
        if i < len(regex) - 1:
            if (regex[i].isalnum() and regex[i + 1].isalnum()) or (regex[i].isalnum() and regex[i + 1] == "(") or (regex[i] == ")" and regex[i + 1].isalnum()) or (regex[i] == ")" and regex[i + 1] == "(") or (regex[i] == "*" and regex[i + 1].isalnum()) or (regex[i] == "*" and regex[i + 1] == "("):
                newRegex += regex[i]  + "?"
            else:
                newRegex += regex[i]
    newRegex += regex[len(regex) - 1]
    return newRegex


if __name__ == "__main__":
    # expresion = input("Ingrese la expresion regular: ")
    # cadena = input("Ingrese la cadena a evaluar: ")
    expresion = "a*b"

    # Expresion prueba
    # expresion = "a(a+b)*b"
    # expresion = "abc(a+b)*c(a|b)*"
    # expresion = "ab*c"


    if validarExpresionRegular(expresion):
        expresion = createFixedRegex(expresion)
        expresion = parseRegexToPostfix(expresion)
        Thompson(expresion)
        



