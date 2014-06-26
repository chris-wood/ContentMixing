import java.util.HashMap;
import java.util.ArrayList;
import java.util.Random;

public class ContentMixer
{

	public static byte[] XOR(byte[] b1, byte[] b2) throws Exception
	{
		if (b1.length != b2.length) throw new Exception("Blocks are not of the same length");
		byte[] br = new byte[b1.length];
		for (int i = 0; i < b1.length; i++)
		{
			br[i] = b1[i] ^ b2[i];
		}
		return br;
	}

	public static void main(String[] args) throws Exception
	{
		if (args.length != 4)
		{
			System.err.println("usage: java ContentMixer t n m k seed");
			System.err.println("    t - number of content items");
			System.err.println("    n - number of chunks in a piece of content");
			// System.err.println("    m - number of cover blocks");
			System.err.println("    k - number of bytes in each chunk/cover item");
			System.err.println("    seed - seed for the PRNG");
		}

		// Command line arguments
		int t = Integer.parseInt(args[0]);
		int n = Integer.parseInt(args[1]);
		// int m = Integer.parseInt(args[2]);
		int k = Integer.parseInt(args[3]);
		long seed = Long.parseLong(args[4]);

		// Create the PRNG
		Random prng = new Random(seed);

		// Populate the data items and their respective content blocks
		// Each content item is an array of content chunks
		ArrayList<ArrayList<byte[]>> contentItems = new ArrayList<ArrayList<byte[]>>();
		for (int i = 0; i < t; i++)
		{
			ArrayList<byte[]> chunks = new ArrayList<byte[]>();
			for (int j = 0; j < n; j++)
			{
				byte[] chunk = new byte[k];
				prng.nextBytes(chunk);
				chunks.add(chunk);
			}
			contentItems.add(chunks);
		}

		// // Create the cover blocks
		// ArrayList<byte[]> coverBlocks = new ArrayList<byte[]>();
		// for (int i = 0; i < m; i++)
		// {
		// 	byte[] chunk = new byte[k];
		// 	prng.nextBytes(chunk);
		// 	coverBlocks.add(chunk);
		// }

		//// TODO: compute all n*m combinations of content/cover chunks XOR'd and save them in a matrix addressable by content/chunk item for EACh file
		// this means that there will be t matrices of n*m*k bytes each to publish... how can we cut down that space requirement?...
		// will mixing across content items help? can we reduce the amount of cover blocks without impacting the privacy?

		// Mix each content block with the other content blocks - there are C(t*n, 2) total blocks that will result, and this number grows at a reasonable rate
		// item index #1, item index #2, item chunk #1 index, item chunk #2 index, arraylist of chunks XOR'd
		HashMap<Integer, HashMap<Integer, HashMap<Integer, HashMap<Integer, ArrayList<byte[]>>>>> mixMap = new HashMap<Integer, HashMap<Integer, HashMap<Integer, HashMap<Integer, ArrayList<byte[]>>>>>();
		



		
	}
}