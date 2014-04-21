import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class data_analizer_routine {

	static float real_duration;
	static File[] files;
	static String current_file;
	public static void main(String[] args) {
		files = Filter.finder(args[0]);
		current_file = args[1];
		real_duration = Float.valueOf(args[2]);

		ArrayList<String[]> file = readFileLines(current_file+".dat");
		Analizer analizer = new Analizer(file);
		ArrayList<Map<Float,ArrayList<Integer>>> patterns = analizer.find_patterns();
		data_analizer_routine self = new data_analizer_routine();
		String data = self.data_analizer(current_file+".dat", patterns);
		//		ArrayList<String[]> a_data_list = readFileLines(files[1].getPath()+".dat");
		//		ArrayList<String[]> b_data_list = readFileLines(files[3].getPath()+".dat");

		//		long startTime = System.currentTimeMillis();
		//		Analizer a = new Analizer(a_data_list);
		//		a.find_patterns();
		//		Analizer b = new Analizer(b_data_list);
		//		a.best_match(b.find_patterns());
		//		System.out.println((System.currentTimeMillis() - startTime)/1000);
		//		System.out.println(files[1].getPath()+" and "+files[3].getPath());
		System.out.println(data);
	}

	public String data_analizer(String current_file, ArrayList<Map<Float, ArrayList<Integer>>> current_patterns){
		ArrayList<Tuple_data_analizer> patterns = new ArrayList<data_analizer_routine.Tuple_data_analizer>();
		int number = 0;
		ArrayList<Tuple_selections> list_of_selections = new ArrayList<Tuple_selections>();
		for(File file_name: files){
			if(!(file_name.getPath()+".dat").matches(current_file)){
				ArrayList<String[]> _file = readFileLines(file_name.getPath()+".dat");
				Analizer a = new Analizer(_file);
				patterns.add(new Tuple_data_analizer(file_name.getPath(), a));
			}
		}
		for(Tuple_data_analizer next_file: patterns){
			Analizer a = next_file.getAnalizer();
			a.find_patterns();
			ArrayList<Tuple_best_matches> matches = a.best_match(current_patterns);
			ArrayList<Tuple_match_filter> match_filter = new ArrayList<Tuple_match_filter>();
			for(Tuple_best_matches match: matches){
				if(match.getKey() < match.getMKey()){
					match_filter.add(new Tuple_match_filter(match.getMKey(), match.getKey(), match.getValidator().length));
				}
			}
			float last = (float) -1.0;
			ArrayList<Tuple_match_filter> dict_list = new ArrayList<Tuple_match_filter>();
			Map<Float, ArrayList<Tuple_match_filter>> match_dict = new HashMap<Float, ArrayList<Tuple_match_filter>>();
			Collections.sort(match_filter);
			for(Tuple_match_filter match:match_filter){
				if(last!=match.getMKey()){
					if(last!=-1.0){
						match_dict.put(last, dict_list);
					}
					last = match.getMKey();
					dict_list = new ArrayList<Tuple_match_filter>();
				}

				dict_list.add(new Tuple_match_filter(-1, match.getKey(), match.getLength(), 1));
			}
			ArrayList<Tuple_matching> selection = new ArrayList<Tuple_matching>();
			for(float match:match_dict.keySet()){
				selection.add(best_option(match, match_dict.get(match)));
			}
			float allow_time = real_duration;
			allow_time = (float) (allow_time-(allow_time*.15));
			ArrayList<Tuple_matching>filter_selection = new ArrayList<Tuple_matching>();
			for(Tuple_matching element:selection){
				if(element.getMatching() > allow_time)
					filter_selection.add(element);	
			}
			Tuple_matching small_time = null;
			Collections.sort(filter_selection);
			for(Tuple_matching sel:filter_selection){
				if(sel.getMax() != 0){
					if(small_time == null)
						small_time = sel;
					if(small_time.getSelTime() > sel.getSelTime())
						small_time = sel;
				}
			}
			list_of_selections .add(new Tuple_selections(next_file.getFileName(), small_time));
		}
		String best_selection = new String();
		float small_time = 0;
		for(int i = 0; i < list_of_selections.size(); i++){
			if (small_time == 0)
				small_time = list_of_selections.get(i).getSmallTime().getSelTime();
			if (small_time <= list_of_selections.get(i).getSmallTime().getSelTime()){
				small_time = list_of_selections.get(i).getSmallTime().getSelTime();
				best_selection = new String();
				best_selection = best_selection.concat(list_of_selections.get(i).getFileName());
			}
		}
		return best_selection;
	}

	public Tuple_matching best_option(float matching, ArrayList<Tuple_match_filter> match){
		ArrayList<Float>times = new ArrayList<Float>();
		ArrayList<Integer> intn = new ArrayList<Integer>();
		Collections.sort(match);
		Collections.reverse(match);
		for(Tuple_match_filter element:match){
			times.add(element.getKey());
			intn.add(element.getLength());
		}
		float max = 0;
		float sel_time = 0;
		for(int i = 0; i<intn.size(); i++){
			if(matching - times.get(i) > matching / 3){
				if(intn.get(i)>max){
					max = intn.get(i);
					sel_time = times.get(i);
				}
			}
		}
		return new Tuple_matching(matching, sel_time, max);
	}

	public static ArrayList<String[]> readFileLines(String fileName){
		File file = new File(fileName);
		BufferedReader br;
		String line;
		ArrayList<String[]> list = new ArrayList<String[]>();
		try {
			br = new BufferedReader(new FileReader(file.getPath()));
			while ((line = br.readLine()) != null) {
				String [] data = line.split(", ");
				list.add(data);
			}
			br.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return list;
	}

	private class Tuple_data_analizer{

		String file_name;
		Analizer analizer;

		public Tuple_data_analizer(String file_name, Analizer analizer){
			this.file_name = file_name;
			this.analizer = analizer;
		}

		public String getFileName(){
			return file_name;
		}

		public Analizer getAnalizer(){
			return analizer;
		}
	}

	private class Tuple_match_filter implements Comparable<Tuple_match_filter>{

		float mKey;
		float key;
		int length;
		int comparator;

		public Tuple_match_filter(float mKey, float key, int length){
			this.mKey = mKey;
			this.key = key;
			this.length = length;
		}

		public Tuple_match_filter(float mKey, float key, int length, int comparator){
			this.mKey = mKey;
			this.key = key;
			this.length = length;
			this.comparator = comparator;
		}

		public float getMKey(){
			return mKey;
		}

		public float getKey(){
			return key;
		}
		public int getLength(){
			return length;
		}

		@Override
		public int compareTo(Tuple_match_filter o) {
			if(comparator==1)
				return (int) (key - o.getKey());
			else
				return (int) (mKey - o.getMKey());
		}
	}

	private class Tuple_matching implements Comparable<Tuple_matching>{

		float matching;
		float sel_time;
		float max;

		public Tuple_matching(float matching, float sel_time, float max){
			this.matching = matching;
			this.sel_time = sel_time;
			this.max = max;
		}

		public float getMatching(){
			return matching;
		}

		public float getSelTime(){
			return sel_time;
		}
		public float getMax(){
			return max;
		}

		@Override
		public int compareTo(Tuple_matching o) {
			return (int) (this.sel_time-o.getSelTime());
		}
	}
	
	private class Tuple_selections{

		String file_name;
		Tuple_matching small_time;

		public Tuple_selections(String file_name, Tuple_matching small_time){
			this.file_name = file_name;
			this.small_time = small_time;
		}

		public String getFileName(){
			return file_name;
		}

		public Tuple_matching getSmallTime(){
			return small_time;
		}
	}
	
	public static class Filter {
		public static File[] finder( String dirName){
			File dir = new File(dirName);
			return dir.listFiles(new FilenameFilter() { 
				public boolean accept(File dir, String filename){
					return filename.endsWith(".wav"); 
				}
			});
		}
	}
}
