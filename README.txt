En aquest projecte es crea un llenguatge de alt nivell per executar codi a partir d'una simulació de peces del Tetris.
Està tot explicat en la memòria del treball.

Aquesta és una extenció al treball fet per MeatFighter que es pot trobar a: https://meatfighter.com/tetromino-computer/

Passos per fer l'execució:

Fer clone de https://github.com/meatfighter/tetromino-computer

Substituir la carpeta gpc del repositori, per la de l'interfície que es desitgi utilitzar

Executar: mvn clean package (en $bash) (abans instal·lar les dependències)

Editar el main.py, l'adreça de sortida ha de ser tetromino-computer\code\asm\ i la d'entrada ha d'apuntar a un .txt amb codi Tetris++

Executar a la terminal: 

antlr4 -Dlanguage=Python3 -no-listener -visitor TPlusPlus.g4 (ANTLR4 ha d'estar instal·lat)

python main.py

java -cp target/tetromino-computer.jar tetrominocomputer.ts.LutsGenerator 

java -cp target/tetromino-computer.jar tetrominocomputer.asm.Assembler -a example.asm -b example.bin

java -cp target/tetromino-computer.jar tetrominocomputer.mc.CycleProgramsGenerator -b example.bin -l CYCLE_LEFT.mc -r CYCLE_RIGHT.mc 

java -cp target/tetromino-computer.jar tetrominocomputer.gpc.app.GeneralPurposeComputer -c tetrominocomputer.gpc.app.MCProcessorAndMemory -b example.bin -l CYCLE_LEFT.mc -r CYCLE_RIGHT.mc

