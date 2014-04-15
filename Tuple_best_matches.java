public class Tuple_best_matches{
	float key;
	float m_key;
	boolean validator[];

	public Tuple_best_matches(float key, float m_key, boolean validator[]){
		this.key = key;
		this.m_key = m_key;
		this.validator = validator;
	}

	public float getKey(){
		return key;
	}
	public float getMKey(){
		return m_key;
	}
	public boolean[] getValidator(){
		return validator;
	}
}