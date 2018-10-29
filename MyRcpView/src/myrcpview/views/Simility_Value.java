package myrcpview.views;

public class Simility_Value {
	private Double similarity;
	String name;
	public Simility_Value(String name,Double similarity) {
		this.name=name;
		this.similarity=similarity;
	}
	public Simility_Value() {
		
	}
	public Double getSimilarity() {
		return similarity;
	}
	public void setSimilarity(Double similarity) {
		this.similarity = similarity;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	
}
