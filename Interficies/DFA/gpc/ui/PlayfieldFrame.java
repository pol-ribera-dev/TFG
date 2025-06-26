package tetrominocomputer.gpc.ui;
import tetrominocomputer.util.Ui;


import static java.awt.EventQueue.invokeAndWait;
import static java.awt.EventQueue.isDispatchThread;
import java.awt.event.KeyEvent;
import java.awt.*;
import java.awt.event.*;

public class PlayfieldFrame extends javax.swing.JFrame implements ActionListener {
    int boto = 1;
    Label labelEntrada, labelResultado;
    TextField campoNumero;
    Button botonConvertir; 
    public PlayfieldFrame() {
        setTitle("DFA");
        setSize(300, 200);
        setLayout(new FlowLayout());
        setVisible(true);

        
        labelEntrada = new Label("Palabra:");
        campoNumero = new TextField(10);
        botonConvertir = new Button("Accepta?");
        labelResultado = new Label("Resultado binario: --------");

       
        add(labelEntrada);
        add(campoNumero);
        add(botonConvertir);
        add(labelResultado);

     
        botonConvertir.addActionListener(this);


        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent we) {
                dispose();
            }
        });
    }
    
    private int[] nums = new int[8];
    private int[] ascii = new int[30];


    public void update(final PlayfieldModel playfieldModel) {
        playfieldModel.setStartPressed(boto);
        boto = 0;
        playfieldModel.setLlista(ascii);
        this.nums = playfieldModel.getNums();
    }


    public void actionPerformed(ActionEvent e) {
    String entrada = campoNumero.getText();

    if (!entrada.matches("[ab]*")) {
        labelResultado.setText("Entrada inválida: solo se permiten 'a' y 'b'.");
        return;
    }
    for (int i = 0; i < ascii.length; i++) {
        ascii[i] = 0;
    }
    char[] caracteres = entrada.toCharArray();
    for (int i = 0; i < caracteres.length && i < ascii.length; i++) {
        ascii[i] = (int) caracteres[i];
    }
    boto = 1;
    if (nums[0] == 1){
            labelResultado.setText("Cadena válida");

    }
    else{
            labelResultado.setText("Cadena no válida");
    }
}

}
