import sys
import random
from antlr4 import *
from TPlusPlusLexer import TPlusPlusLexer
from TPlusPlusParser import TPlusPlusParser
from TPlusPlusVisitor import TPlusPlusVisitor
etiqueta = 'ta'
variables = ""
variables2 = ""
llistes = ""
temporals = ""
num_temp = 0

class EvalVisitor(TPlusPlusVisitor):
    def visitExpre(self, ctx):
        a = self.visit(ctx.expr(0))
        b = self.visit(ctx.expr(1))
        return a+b

    def visitFuncions(self, ctx):
        code = ""
        for funcio_ctx in ctx.funcio():
            code += self.visit(funcio_ctx)
        return code

    def visitReturn(self, ctx):
        a = ""
        if ctx.simples():
            a = self.visit(ctx.simples())
            a += f"""
SMN rETURN
STA
"""
        code = a
        code += f"""
JSR funcioretorn
"""

        return code

    def visitFuncio(self, ctx):

        a = self.visit(ctx.expr())
        code = f"""
{ctx.FUNC().getText()}:
""" + a
        return code



    def visitDef(self, ctx):
        global variables
        global variables2
        variable = ctx.VAR().getText()
        num = "00"
        if ctx.NUMBER():
            num = int(ctx.NUMBER().getText())
            num = hex(num)[2:].upper().zfill(2)
        if ctx.HEX4():
            variables2 += f"""
segment {ctx.HEX4().getText()}
{variable}: {num}
"""
        else:
            variables += f"""
{variable}: {num}
"""
        return ""

    def visitDefllista(self, ctx):
        global llistes
        variable = ctx.VAR().getText()
        num = "00"
        llistes += f"""
{variable}:
"""
        for i in range(int(ctx.NUMBER().getText())):
            llistes += f"{num} "
        return ""

    def visitAsigllista(self, ctx):
        global num_temp
        variable = ctx.VAR().getText()

        code = self.visit(ctx.op())
        code += f"""
SMN m
STA
"""
        code += self.visit(ctx.simples())
        code += f"""
SMN {variable}
TNB
ADD
SMN m
LDB
SMN {variable}
TAN
STB
"""
        num_temp = 0
        return code

    def visitParamasig(self, ctx):
        global num_temp

        code =f"""
SMN fUNCTIONS
LDA
SMN pila
TNB
ADD
INC
"""

        for i in range((int(ctx.UNDOSTRES().getText()[1]) * 2) - 1):
            code += "INC \n "


        code +="""SMN aUX
STA
"""
        code += self.visit(ctx.op())
        code += f"""
SMN aUX    
LDB
SMN pila
TBN
STA
"""
        num_temp = 0
        return code

    def visitAsig(self, ctx):
        global num_temp
        variable = ctx.VAR().getText()
        code = self.visit(ctx.op())
        code += f"""
SMN {variable}      
STA
"""
        num_temp = 0 #queeeee
        return code

    def visitFunc(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = f"""
SMN fUNCTIONS
LDA
INC
INC
INC
INC
INC
INC
INC
INC
STA

SMN pila
TNB
ADD
SMN {actual}
TMB
SMN pila
TAN
STB
        
INC
SMN {actual}
TNB
SMN pila
TAN
STB"""

        if ctx.VAR(1):
            code +="""
SMN fUNCTIONS
LDA
SMN pila
TNB
ADD
INC
INC
TAB
"""
            for i in range(1, 4):
                if ctx.VAR(i):
                    code += f"""SMN {ctx.VAR(i).getText()} 
LDA"""
                    code += """
SMN pila
TBN
STA
TBA
INC
INC
TAB
"""
        code += f"""
        JSR {ctx.FUNC().getText()}
        {actual}:
"""
        
        if ctx.VAR(0):
            code += f"""
SMN rETURN
LDA
SMN {ctx.VAR(0).getText()}
STA
"""
        code += f"""SMN fUNCTIONS
LDA
DEC
DEC
DEC
DEC
DEC
DEC
DEC
DEC
STA
STA
"""
        return code

    def visitDiv(self, ctx):
        global num_temp
        global etiqueta
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        actual = etiqueta
        etiqueta = etiqueta + 'a'

        code = self.visit(ctx.aritmetica(1))
        code += f""" 
SMN {temp}
STA
"""

        code += self.visit(ctx.aritmetica(0))
        code += f""" 
SMN r
STA
        
SMN m  
SEA 00      
STA
    
{actual}:
SMN {temp}
LDB

SMN m
LDA
INC
STA
        
SMN r
LDA
SUB
STA
        
BPL {actual} 
        
SMN m
LDA
DEC
"""
        return code

    def visitModul(self, ctx):
        global num_temp
        global etiqueta
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        actual = etiqueta
        etiqueta = etiqueta + 'a'

        code = self.visit(ctx.aritmetica(1))
        code += f""" 
SMN {temp}
STA
"""

        code += self.visit(ctx.aritmetica(0))
        code += f""" 
SMN r
STA
SMN m  
SEA 00      
STA
{actual}:
SMN {temp}
LDB

SMN m
LDA
INC
STA

SMN r
LDA
SUB
STA

BPL {actual} 
        
ADD
"""
        return code

    def visitMul(self, ctx):
        global num_temp
        global etiqueta
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        actual = etiqueta
        etiqueta = etiqueta + 'a'

        code = self.visit(ctx.aritmetica(1))

        code += f""" 
SMN {temp}
STA
"""

        code += self.visit(ctx.aritmetica(0))
        code += """
SMN m  
DEC
STA
"""

        code += f""" 
SMN r
SEA 00
STA

{actual}:
SMN {temp}
LDB

SMN r
LDA
ADD
STA

SMN m
LDA
DEC
STA
SEB 00
SUB
BPL {actual} 
SMN r
LDA
"""
        return code

    def visitSuma(self, ctx):
        global num_temp
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        code = self.visit(ctx.aritmetica(0))
        code += f"""
SMN {temp}
STA
"""
        code += self.visit(ctx.aritmetica(1))
        code += f"""
TAB
SMN {temp}
LDA
ADD
"""
        return code
    def visitResta(self, ctx):
        global num_temp
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        code = self.visit(ctx.aritmetica(0))
        code += f"""
SMN {temp}
STA
"""
        code += self.visit(ctx.aritmetica(1))
        code += f"""
TAB
SMN {temp}
LDA
SUB
"""
        return code

    def visitLogistica(self, ctx):
        code = self.visit(ctx.logic())
        return code
    def visitBool(self, ctx):
        code = self.visit(ctx.boolean())
        return code

    def visitAnd(self, ctx):
        global num_temp
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        code = self.visit(ctx.logic(0))
        code += f"""
SMN {temp}
STA
"""
        code += self.visit(ctx.logic(1))
        code += f"""
TAB
SMN {temp}
LDA
AND
"""
        return code


    def visitOr(self, ctx):
        global num_temp
        num_temp += 1
        temp = 't'
        for i in range(num_temp):
            temp = temp + 'P'
        code = self.visit(ctx.logic(0))
        code += f"""
SMN {temp}
STA
"""
        code += self.visit(ctx.logic(1))
        code += f"""
TAB
SMN {temp}
LDA
OR
"""
        return code

    def visitNot(self, ctx):

        code = self.visit(ctx.logic())
        code += """     
SEB 01
XOR
"""
        return code

    def visitMayorigual(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.aritmetica(1))
        code += """
SMN cOMP
STA
"""
        code += self.visit(ctx.aritmetica(0))
        code += f"""
SMN cOMP
LDB
SUB
SEA 00
BMI {actual}        
SEA 01
{actual}:
"""
        return code

    def visitMayor(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.aritmetica(0))
        code += """
SMN cOMP
STA
"""
        code += self.visit(ctx.aritmetica(1))
        code += f"""
SMN cOMP
LDB
SUB
SEA 01
BMI {actual}        
SEA 00
{actual}:
"""
        return code

    def visitMenorigual(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.aritmetica(0))
        code += """
SMN cOMP
STA
"""
        code += self.visit(ctx.aritmetica(1))
        code += f"""
SMN cOMP
LDB
SUB
SEA 00
BMI {actual}        
SEA 01
{actual}:
"""
        return code
    def visitMenor(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.aritmetica(1))
        code += """
SMN cOMP
STA
"""
        code += self.visit(ctx.aritmetica(0))
        code += f"""
SMN cOMP
LDB
SUB
SEA 01
BMI {actual}        
SEA 00
{actual}:
"""
        return code


    def visitIgual(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.aritmetica(1))
        code += """
SMN cOMP
STA
"""
        code += self.visit(ctx.aritmetica(0))
        code += f"""
SMN cOMP
LDB
SUB
SEA 01
BEQ {actual}        
SEA 00
{actual}:
"""
        return code
    def visitNoigual(self, ctx):
        global etiqueta
        actual = etiqueta
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.aritmetica(1))
        code += """
SMN cOMP
STA
"""
        code += self.visit(ctx.aritmetica(0))
        code += f"""
SMN cOMP
LDB
SUB
SEA 00
BEQ {actual}        
SEA 01
{actual}:
"""
        return code
    def visitFinal(self, ctx):
        code = self.visit(ctx.simples())
        return code

    def visitSimp(self, ctx):
        code = self.visit(ctx.aritmetica())
        return code

    def visitParen(self, ctx):
        code = self.visit(ctx.logic())
        return code
    def visitParenarit(self, ctx):
        code = self.visit(ctx.aritmetica())
        return code
    def visitPeça(self, ctx):
        code = self.visit(ctx.simples(1))
        code += f"""
TAB
ADD
TAB
"""
        code += self.visit(ctx.simples(0))
        code += f"""
LS3
ADD
TAB
"""
        code += self.visit(ctx.simples(2))
        code += f"""
ADD
SMN tETROMINOES
TAN
LDA
"""
        return code

    def visitPintar(self, ctx):
        left = ctx.simples(0).getText()
        if left.isdigit():
            left = int(left)
            if left > 19:
                raise Exception(f"Fila {left} no existent")
            h = hex(left*11)[2:].upper().zfill(2)
            code = f"""
SEA {h}"""
        else:

            code = f"""
SMN {left} 
LDA
LDB    
LS3
ADD
ADD 
ADD
"""

        right = ctx.simples(1).getText()
        if right.isdigit():
            right = int(right)
            if right > 9:
                raise Exception(f"Columna {right} no existent")
            h = hex(right)[2:].upper().zfill(2)
            code += f"""
SEB {h}"""
        else:
            code += f"""SMN {right}
LDB"""

        code += f"""
ADD
SEB 16
ADD"""

        color = ctx.simples(2).getText()
        if color.isdigit():
            color = int(color)
            if color > 7:
                raise Exception(f"Color no existent")
            col = hex(color)[2:].upper().zfill(2)
            code += f"""
SEB {col}"""
        else:
            code += f"""
SMN {color}
LDB"""
        code += f"""
SMN pLAYFIELD
TAN
STB       
"""
        return code
    def visitIf(self, ctx):
        global etiqueta
        actual = etiqueta
        actual2 = etiqueta + 'e'
        etiqueta = etiqueta + 'a'
        code = self.visit(ctx.logic())
        body_code = self.visit(ctx.expr(0))
        body_code2 = ""
        if ctx.expr(1):
            body_code2 = self.visit(ctx.expr(1))
        code += f"""
SEB 00
SUB  
BEQ {actual}
"""
        code += body_code
        code += f"""
JMP {actual2}
{actual}:
"""
        code +=  body_code2
        code += f"""{actual2}:
"""
        return code




    def visitRead(self, ctx):
        left = ctx.simples(0).getText()
        if left.isdigit():
            left = int(left)
            if left > 19:
                raise Exception(f"Fila {left} no existent")
            h = hex(left * 11)[2:].upper().zfill(2)
            code = f"""
SEA {h}"""
        else:

            code = f"""
SMN {left} 
LDA
LDB    
LS3
ADD
ADD 
ADD
"""

        right = ctx.simples(1).getText()
        if right.isdigit():
            right = int(right)
            if right > 9:
                raise Exception(f"Columna {right} no existent")
            h = hex(right)[2:].upper().zfill(2)
            code += f"""
SEB {h}"""
        else:
            code += f"""SMN {right}
LDB"""

        code += f"""
ADD
SEB 16
ADD"""
        code += f"""
SMN playfield
TAN
LDA       
"""
        return code

    def visitFor(self, ctx):
        global variables
        variable = ctx.VAR(0).getText()
        if variable.isdigit():
            raise Exception(f"No pots utilitzar un número per iterar en un bucle")
        if ctx.VAR(1):
            inicial = 0
            final = 1
        else:
            inicial = int(ctx.NUMBER(0).getText())
            final = int(ctx.NUMBER(1).getText())
        body_code = self.visit(ctx.expr())
        augment = "DEC"
        compara = "BPL"
        if inicial < final:
            augment = "INC"
            compara = "BMI"
            final += 1
        inicial = hex(inicial)[2:].upper().zfill(2)
        final = hex(final)[2:].upper().zfill(2)

        if ctx.VAR(1):
            final = f"""SMN {ctx.VAR(1).getText()}
LDB"""
        else:
            final = f"SEB {final}"

        variables += f"""
{variable}:   00 
"""
        output = f"""
SMN {variable}      
SEA {inicial}      
STA
inicifor{variable}: 
"""

        output += body_code
        output += f"continuefor{variable}:"
        output +=f"""
        {final}
SMN {variable} 
LDA
{augment}
STA
SUB
{compara} inicifor{variable} 
endfor{variable}:
"""
        return output

    def visitBucle(self, ctx):
            global variables
            variable = ctx.VAR().getText()
            if variable.isdigit():
                raise Exception(f"No pots utilitzar un número com a ID en un bucle")

            body_code = self.visit(ctx.expr())

            variables += f"""
{variable}:   00 
"""
            output = f"""
inicifor{variable}: 
"""

            output += body_code
            output += f"continuefor{variable}:"
            output += f"""
           
JMP inicifor{variable} 
endfor{variable}:
"""
            return output

    def visitBreak(self, ctx):
        variable = ctx.VAR().getText()
        return f"JMP endfor{variable} \n"

    def visitCont(self, ctx):
        variable = ctx.VAR().getText()
        return f"JMP continuefor{variable} \n"

    def visitReset(self, ctx):
        return """SMN drawFrame
SEA 01
STA
"""
    def visitNum(self, ctx):
        num = hex(int(ctx.NUMBER().getText()))[2:].upper().zfill(2)
        code = f"SEA {num}"
        return code

    def visitParam(self, ctx):
        code = f"""
SMN fUNCTIONS
LDA
SMN pila
TNB
ADD
INC
"""
        for i in range((int(ctx.UNDOSTRES().getText()[1]) *2) - 1):
            code += "INC \n"
        code += """TAN
LDA
"""
        return code

    def visitVar(self, ctx):
        code = f"""SMN {ctx.VAR().getText()}
LDA"""
        return code

    def visitLista(self, ctx):
        code = self.visit(ctx.simples())
        code += f"""
SMN {ctx.VAR().getText()}              
TNB                     
ADD                     
TAN                     
LDA"""
        return code

    def visitRandom(self, ctx):
        code = f"""
SEB 02
SMN seedLow
LDA
AND
SMN nextBit
STA
SMN seedHigh
LDA
AND
SMN nextBit
LDB
XOR
BEQ bit9Clear
SEA 80
bit9Clear:
STA                     

SMN seedHigh
LDA
SEB 01
AND
BEQ bit8Clear
SEB 80
bit8Clear:
SMN seedLow
LDA
RS1
OR
STA                     

SMN nextBit
LDB
SMN seedHigh
LDA
RS1
OR
STA                     

SMN frameCounter
LDB
XOR
SEB 1F
AND
TAB
LS3
SUB
RS5
"""
        return code

    def visitComenta(self, ctx):
        a = ctx.COMENTARI().getText()
        return a + "\n"
def main():
    global variables
    global variables2
    global llistes
    global temporals
    temporals += """
m:   00
r:   00
fUNCTIONS: 00  
rETURN: 00
aUX: 00
cARRY: 00
cOMP: 00
"""
    input_stream = FileStream("programa.txt", encoding='utf-8')
    lexer = TPlusPlusLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TPlusPlusParser(stream)
    tree = parser.expr()

    visitor = EvalVisitor()
    result = visitor.visit(tree)

    input_stream = FileStream("func.txt", encoding='utf-8')
    lexer = TPlusPlusLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TPlusPlusParser(stream)
    tree = parser.funcions()
    visitor = EvalVisitor()
    r_funciones = visitor.visit(tree)
    if r_funciones == None:
        r_funciones = ""
    numero = hex(random.randint(0, 255))[2:].upper().zfill(2)
    numero2 = hex(random.randint(0, 255))[2:].upper().zfill(2)

    asm_code =variables2 + "segment 0050" + variables + f"""
seedHigh:            {numero} 
seedLow:             {numero2}
nextBit:             00
segment 00FD
drawFrame:           00 
frameCounter:        00 
"""
    temporal = 't'
    for i in range(20):
        temporal = temporal +'P'
        temporals +=  f" {temporal}:   00"

    pila = """
pila: 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
"""
    asm_code += "segment 0100" + llistes + "\n segment 0270 \n" + temporals + "\n segment 0300 \n"+ pila + "\n segment 0400 \n"+f"""
JSR main"""
    if r_funciones != "" :
        asm_code += f"""
funcioretorn:
SMN fUNCTIONS
LDA
SMN pila
TNB
ADD
TAN
LDB
                
SMN notocar
TNA
INC
TAN
STB
                
SMN fUNCTIONS
LDA
SMN pila
TNB
ADD
INC
TAN
LDB
SMN notocar
TNA
INC
INC
TAN
STB
notocar: JSR notocar"""
    
    
    asm_code += f"""{r_funciones}
main: ; ---------------------------------------------------------------------------------------  
    
"""


    with open("../tetris.asm", "w") as f:
        f.write(asm_code)
        f.write(result)
        f.write("JMP main")
    print("Complete")

if __name__ == '__main__':
    main()

