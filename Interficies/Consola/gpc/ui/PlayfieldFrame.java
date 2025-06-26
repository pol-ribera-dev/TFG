package tetrominocomputer.gpc.ui;
import tetrominocomputer.util.Ui;


import static java.awt.EventQueue.invokeAndWait;
import static java.awt.EventQueue.isDispatchThread;
import java.awt.event.KeyEvent;
import java.awt.*;
import java.awt.event.*;

public class PlayfieldFrame extends javax.swing.JFrame implements ActionListener {
    TextField[] campos = new TextField[8];
    Label[] resultados = new Label[8];
    

    Button botonConvertir; 
    public PlayfieldFrame() {
        setTitle("Consola");
        setSize(300, 200);
        setLayout(new FlowLayout());
        setVisible(true);
        setLayout(new GridLayout(9, 2));

        for (int i = 0; i < 8; i++) {
            campos[i] = new TextField(10);
            resultados[i] = new Label("Resultat: --------");

            add(campos[i]);
            add(resultados[i]);
        }

        Button botonConvertir = new Button("Ejecutar");
        add(new Label("Números del 0-255"));
        add(botonConvertir);

        botonConvertir.addActionListener(this);


        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent we) {
                dispose();
            }
        });
    }
    
    private int[] nums = new int[8];
    private int[] valors = new int[8];

    public void update(final PlayfieldModel playfieldModel) {
        playfieldModel.setValors(valors);
        this.nums = playfieldModel.getNums();
    }


    public void actionPerformed(ActionEvent e) {
         for (int i = 0; i < 8; i++) {
            try {
                int numero = Integer.parseInt(campos[i].getText());
                if (numero < 0 || numero > 255) {
                    resultados[i].setText("Número fora de rang.");
                } else {
                    String binario = String.format("%8s", Integer.toBinaryString(numero)).replace(' ', '0');
                    valors[i] = numero;
                    resultados[i].setText("Resultat: " + nums[i]);
                }
            } catch (NumberFormatException ex) {
                resultados[i].setText("Entrada invàlida.");

            }
         }
    }

}
