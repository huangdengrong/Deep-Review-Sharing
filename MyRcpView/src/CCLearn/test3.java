package CCLearn;

import java.io.IOException;

import org.omg.CORBA.Any;



public class test3 {

//	 public static final Any deserialize(byte[] input) {
//	        int lastNotSpacePos = findLastNotSpacePos(input);
//	        com.jsoniter.JsonIterator iter = JsonIteratorPool.borrowJsonIterator();
//	        iter.reset(input, 0, lastNotSpacePos);
//	        try {
//	            Any val = iter.readAny();
//	            if (iter.head != lastNotSpacePos) {
//	                throw iter.reportError("deserialize", "trailing garbage found");
//	            }
//	            return val;
//	        } catch (ArrayIndexOutOfBoundsException e) {
//	            throw iter.reportError("deserialize", "premature end");
//	        } catch (IOException e) {
//	            throw new JsonException(e);
//	        } finally {
//	            JsonIteratorPool.returnJsonIterator(iter);
//	        }
//	    }
//
//	    private static int findLastNotSpacePos(byte[] input) {
//	        for (int i = input.length - 1; i >= 0; i--) {
//	            byte c = input[i];
//	            if (c != ' ' && c != '\t' && c != '\n' && c != '\r') {
//	                return i + 1;
//	            }
//	        }
//	        return 0;
//	    }
//
//	    public static void setMode(DecodingMode mode) {
//	        Config newConfig = JsoniterSpi.getDefaultConfig().copyBuilder().decodingMode(mode).build();
//	        JsoniterSpi.setDefaultConfig(newConfig);
//	        JsoniterSpi.setCurrentConfig(newConfig);
//	    }
}
