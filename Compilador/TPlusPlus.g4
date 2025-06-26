grammar TPlusPlus;

FUNC : ('A'..'Z')+;
HEX4 : [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F];
VAR     :  ('a'..'z') ('A'..'Z')* ;
COMENTARI : ';' ('a'..'z'|'A'..'Z'|' '|'0'..'9')* ;
NUMBER  : [0-9]+ ;
UNDOSTRES: '(' [1-3] ')' ;
LPAREN  : '(' ;
RPAREN  : ')' ;
COMA  : ',' ;
WS      : [ \t\r\n]+ -> skip ;

program : funcions expr + EOF
        ;

funcions : (funcio)* ;

funcio : 'funcio' FUNC expr  'I' ;

expr    : VAR? 'ves' FUNC VAR? VAR? VAR? #Func
        | 'bucle' VAR expr 'I' #Bucle
        | 'per' VAR (NUMBER NUMBER| VAR) expr 'I' #For
        | 'si' logic expr 'I'(|'sino' expr 'I')  #If
        | 'var' VAR ('=' NUMBER)? ('memoria' HEX4)? #Def
        | 'llista' VAR NUMBER #Defllista
        | VAR '=' op #Asig
        | VAR '[' simples ']' '=' op #Asigllista
        | 'parametre' UNDOSTRES '=' op #Paramasig
        | expr expr # Expre
        | 'surt' VAR #Break
        | 'retorna' simples? #Return
        | 'continua' VAR #Cont
        | 'pinta' LPAREN simples COMA simples COMA simples RPAREN # Pintar
        | 'actualitza' #Reset
        | COMENTARI #Comenta
        ;

op : logic #Logistica
     | 'mira' LPAREN simples COMA simples RPAREN # Read
     | 'peça' simples simples simples #Peça
     | 'aleatori' #Random
     ;


logic: LPAREN logic RPAREN #Paren
     | 'no' logic #Not
     | logic 'i' logic  #And
     | logic 'o' logic  #Or
     | boolean #Bool
     ;


boolean:
     aritmetica '<' aritmetica #Menor
     | aritmetica '>' aritmetica #Mayor
     | aritmetica '<=' aritmetica #Menorigual
     | aritmetica '>=' aritmetica #Mayorigual
     | aritmetica '==' aritmetica #Igual
     | aritmetica '!=' aritmetica #Noigual
     | aritmetica #Simp
     ;

aritmetica: LPAREN aritmetica RPAREN #Parenarit
     | aritmetica '*' aritmetica #Mul
     | aritmetica '/' aritmetica #Div
     | aritmetica '+' aritmetica #Suma
     | aritmetica '-' aritmetica #Resta
     | aritmetica '%' aritmetica #Modul
     | simples #Final
;



simples : NUMBER # Num
        | VAR # Var
        | VAR'['simples']' #Lista
        | 'parametre' UNDOSTRES #Param
;