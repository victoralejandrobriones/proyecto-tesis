import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Map;


public class data_analizer_routine {

	static float real_duration;
	static File[] files;
	public static void main(String[] args) {
		files = Filter.finder(args[0]);
		String current_file = args[1];
		real_duration = Float.valueOf(args[2]);
		ArrayList<String[]> file = readFileLines(current_file+".dat");
		Analizer analizer = new Analizer(file);
		ArrayList<Map<Float,ArrayList<Integer>>> patterns = analizer.find_patterns();
		
//		ArrayList<String[]> a_data_list = readFileLines(files[1].getPath()+".dat");
//		ArrayList<String[]> b_data_list = readFileLines(files[3].getPath()+".dat");
		
//		long startTime = System.currentTimeMillis();
//		Analizer a = new Analizer(a_data_list);
//		a.find_patterns();
//		Analizer b = new Analizer(b_data_list);
//		a.best_match(b.find_patterns());
//		System.out.println((System.currentTimeMillis() - startTime)/1000);
//		System.out.println(files[1].getPath()+" and "+files[3].getPath());

	}
	
	public void data_analizer(String current_file, int current_patterns){
		ArrayList<Tuple_data_analizer> patterns = new ArrayList<data_analizer_routine.Tuple_data_analizer>();
		int number = 0;
//		list_of_selections = []
		for(File file_name: files){
			if(!(file_name.getPath()+".dat").matches(current_file)){
				ArrayList<String[]> _file = readFileLines(file_name.getPath()+".dat");
				Analizer a = new Analizer(_file);
				patterns.add(new Tuple_data_analizer(file_name.getPath(), a));
			}
		}
//	    for next_file in patterns:
//	        matches = next_file[1].best_match(current_patterns)
//	        match_filter = []
//	        for match in matches:
//	            if float(match[0]) < float(match[1]):
//	                match_filter.append([match[1], match[0], len(match[2])])
//	        last = None
//	        dict_list = []
//	        match_dict = []
//	        for match in sorted(match_filter, key=itemgetter(0)):
//	            if last != match[0]:
//	                if last!= None:
//	                    match_dict.append({last:dict_list})
//	                last = match[0]
//	                dict_list = []
//	            dict_list.append([match[1], match[2]])
//	        selection = []
//	        for match in reversed(match_dict):
//	            selection.append(best_option(match))
//	        allow_time = real_duration
//	        allow_time = allow_time-(allow_time*.15)
//	        filter_selection = []
//	        for element in selection:
//	            if element[0] > allow_time:
//	                filter_selection.append(element)
//	        small_time = 0
//	        for sel in sorted(filter_selection, key=itemgetter(1)):
//	            if sel[2]!=0:
//	                if small_time == 0:
//	                    small_time = sel
//	                if small_time[1] > sel[1]:
//	                    small_time = sel
//	        list_of_selections.append([next_file[0],small_time])
//	    best_selection = None
//	    small_time = None
//	    for i in range(len(list_of_selections)):
//	        if small_time == None:
//	            small_time = list_of_selections[i][1][1]
//	        if small_time < list_of_selections[i][1][1]:
//	            small_time = list_of_selections[i][1][1]
//	            best_selection = list_of_selections[i][0]
//	    return best_selection
	}
//	
//	def best_option(match):
//	    matching = float(match.keys()[0])
//	    times = []
//	    intn = []
//	    for element in reversed(sorted(match[match.keys()[0]], key=itemgetter(1))):
//	        times.append(element[0])
//	        intn.append(element[1])
//	    max = 0
//	    sel_time = 0
//	    for i in range(len(intn)):
//	        if matching - times[i] > matching/3:
//	            if intn[i]>max:
//	                max = intn[i]
//	                sel_time = times[i]
//	    return matching, sel_time, max
	
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
