import argparse
import sys
import json
import logging
from ocrapp.core.orchestrator import DocumentExtractor

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Smart Document Text Extraction App")
    parser.add_argument("file", help="Path to the document to process")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--json", action="store_true", help="Output only JSON format")
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    logger = logging.getLogger("cli")
    
    try:
        extractor = DocumentExtractor()
        
        result = extractor.process(args.file)
        
        if args.json:
            print(json.dumps({
                "source": result["source"],
                "score": result["score"],
                "text": result["text"]
            }, indent=2))
        else:
            print("\n" + "="*50)
            print(f"🥇 BEST EXTRACTOR: {result['source']}")
            print(f"📊 CONFIDENCE SCORE: {result['score']:.2f}")
            print("="*50 + "\n")
            print(result["text"])
            print("\n" + "="*50)
            print("DEBUG REPORT (All Extractor Scores):")
            for debug_info in result.get("debug", []):
                err = f" (Error: {debug_info['error']})" if "error" in debug_info else ""
                print(f" - {debug_info['source']}: {debug_info['score']}{err}")
            print("="*50 + "\n")
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
