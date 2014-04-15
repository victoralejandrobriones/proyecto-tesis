import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class Analizer {
	int pattern_size = 20;
	ArrayList<Tuple_data_values> data_values = new ArrayList<Tuple_data_values>();
	ArrayList<Map<Float, ArrayList<Integer>>> patterns;
	public Analizer(ArrayList<String[]> data_list){
		for(String element[]: data_list){
			float value = Float.parseFloat(element[0]);
			int position = (int) Float.parseFloat(element[1]);
			this.data_values.add(new Tuple_data_values(value, position));
		}
	}

	public Map<Integer, ArrayList<Integer>> find_positions(){
		Map<Integer, ArrayList<Integer>> values = new HashMap<Integer, ArrayList<Integer>>();
		int checked[] = new int[this.data_values.size()];
		int element = 0;
		for(Tuple_data_values value: this.data_values){
			if(!checkFor((int) value.getPosition(), checked)){
				values.putAll(search((int) value.getPosition()));
				checked[element] = (int) value.getPosition();
				element+=1;
			}
		}
		return values;
	}

	public Map<Integer, ArrayList<Integer>> search(int pos){
		ArrayList<Integer> positions = new ArrayList<Integer>();
		for(int i = 0; i<this.data_values.size(); i++){
			if(pos==this.data_values.get(i).getPosition()){
				positions.add(i);
			}
		}
		Map<Integer, ArrayList<Integer>> map = new HashMap<Integer, ArrayList<Integer>>();
		map.put(new Integer(pos), positions);
		return map;
	}

	public ArrayList<Tuple_best_matches> best_match(ArrayList<Map<Float, ArrayList<Integer>>> patterns){
		ArrayList<Tuple_best_matches> best_matches = new ArrayList<Tuple_best_matches>();
		int iter = 0;
		for(Map<Float, ArrayList<Integer>> element : this.patterns){
			for(float key: element.keySet()){
				ArrayList<Integer> pattern = element.get(key);
				int p_size = pattern.size();
				if(p_size > pattern_size){
					for(Map<Float, ArrayList<Integer>> m_element : patterns){
						boolean validator[] = null;
						for(float m_key: m_element.keySet()){
							ArrayList<Integer> m_pattern = m_element.get(m_key);
							int m_size = m_pattern.size();
							int p_last = 0;
							int m_last = 0;
							int size = p_size <= m_size ? p_size : m_size;
							validator = new boolean[size];
							if(size > pattern_size){
								for(int i = 0; i<size; i++){
									if(i!=0){
										boolean value = (pattern.get(i) >= p_last) == (m_pattern.get(i) >= m_last);
										if(value == false){
											validator = null;
											break;
										}
									}
									else{
										p_last = pattern.get(i);
										m_last = m_pattern.get(i);
									}
								}
								if(validator != null){
									System.out.println(iter+" of "+this.patterns.size()+" "+size+" "+key+" "+m_key);
									best_matches.add(new Tuple_best_matches(key, m_key, validator));
								}
							}
						}
					}
				}
			}
		iter+=1;
		}
		return best_matches;
	}

	public ArrayList<Map<Float,ArrayList<Integer>>> find_patterns(){
		int chk_values [] = new int[this.data_values.size()];;
		int chk_positions [] = new int[this.data_values.size()];;
		patterns = new ArrayList<Map<Float,ArrayList<Integer>>>();
		Map<Integer, ArrayList<Integer>> positions = find_positions();
		for(int i = 0; i<data_values.size(); i++){
			int value = data_values.get(i).getPosition();
			if(!checkFor(value, chk_values) && !checkFor(i, chk_positions)){
				Map<Float, ArrayList<Integer>> c_patterns = new HashMap<Float, ArrayList<Integer>>();
				for(int j: positions.get(new Integer(value))){
					ArrayList<Integer> pattern = new ArrayList<Integer>();
					int k = 1;
					pattern.add(new Integer(value));
					while(!checkFor(j+k, positions.get(value))){
						if(j+k < data_values.size()){
							pattern.add(data_values.get(j+k).getPosition());
						}
						else
							break;
						k+=1;
					}
					c_patterns.put(data_values.get(j).getValue(), pattern);
				}
				patterns.add(c_patterns);
				chk_values[i] = value;
				chk_positions[i] = i;
			}
		}	
		return patterns;
	}

	private boolean checkFor(int value, int checked[]){
		for(int check: checked){
			if(value == check)
				return true;
		}
		return false;
	}

	private boolean checkFor(int value, ArrayList<Integer> checked) {
		for(int check: checked){
			if(value == check)
				return true;
		}		
		return false;
	}

	private class Tuple_data_values{
		float value;
		int position;

		public Tuple_data_values(float value, int position){
			this.value = value;
			this.position = position;
		}

		public float getValue(){
			return value;
		}
		public int getPosition(){
			return position;
		}
	}

}
