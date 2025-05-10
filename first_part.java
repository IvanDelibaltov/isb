import java.io.File;
import java.io.PrintStream;
import java.security.SecureRandom;

class BinaryGenerator {
    private static final int SIZE = 128;
    private static final SecureRandom RAND = new SecureRandom();
    
    private static String createBits() {
        StringBuilder builder = new StringBuilder(SIZE);
        for (int index = 0; index < SIZE; index++) {
            builder.append(RAND.nextBoolean() ? '1' : '0');
        }
        return builder.toString();
    }
    
    private static void storeBits(String bits) {
        try (PrintStream out = new PrintStream(new File("BinaryData.dat"))) {
            out.print(bits);
            System.out.println("Binary data successfully stored");
        } catch (Exception e) {
            System.err.println("Storage failed: " + e.toString());
        }
    }
    
    public static void main(String[] arguments) {
        String binarySequence = createBits();
        storeBits(binarySequence);
    }
}