package tetrominocomputer.gpc.ui;

public class PlayfieldModel {

    
    private int value;
    private int[] nums = new int[8];
    private int[] ascii = new int[30];
    public int[] getNums() {
        return nums;
    }
    public int[] getLletres() {
        return ascii;
    }
    public int isStartPressed() {
        return value;
    }

    public void setStartPressed(final int value) {
        this.value = value;
    }

    public void setLlista(final int[] asci) {
        this.ascii = asci;
    }    
}