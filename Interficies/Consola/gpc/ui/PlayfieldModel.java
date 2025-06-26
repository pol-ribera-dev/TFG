package tetrominocomputer.gpc.ui;

public class PlayfieldModel {

    
    private int[] valors = new int[8];
    private int[] nums = new int[8];

    public int[] getNums() {
        return nums;
    }

    public int[] getValors() {
        return valors;
    }

    public void setValors(final int[] value) {
        this.valors = value;
    }
}