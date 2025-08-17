"""
Demonstration script for agent-to-agent communication.
"""
from dotenv import load_dotenv
from app.agents.a2a_communication import demonstrate_a2a_communication

# Load environment variables
load_dotenv()

def main():
    """Run the agent-to-agent communication demonstration."""
    print("=== Agent-to-Agent Communication Demonstration ===")
    
    examples = [
        {
            "query": "quantum computing",
            "context": "Focus on recent breakthroughs and potential applications."
        },
        {
            "query": "climate change mitigation strategies",
            "context": "What are the most promising approaches being developed?"
        },
        {
            "query": "advanced machine learning techniques",
            "context": "How do these compare to traditional algorithms?"
        }
    ]
    
    for i, example in enumerate(examples):
        print(f"\nExample {i+1}: {example['query']}")
        print(f"Context: {example['context']}")
        print("-" * 40)
        
        try:
            result = demonstrate_a2a_communication(
                example["query"], 
                example["context"]
            )
            
            print(f"Response from main agent:\n{result['response']}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 40)
        
    print("\nA2A communication demonstration completed.")

if __name__ == "__main__":
    main()