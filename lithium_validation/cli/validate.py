#!/usr/bin/env python3
"""
Validation CLI - Command-line tool for output validation
Based on "Why Language Models Hallucinate" paper insights
"""

import argparse
import json
import sys
from pathlib import Path

# Import from the lithium_validation package
try:
    from lithium_validation.core.validation_interface import ValidationInterface
except ImportError:
    # Fallback for development
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from lithium_validation.core.validation_interface import ValidationInterface

def main():
    parser = argparse.ArgumentParser(
        description='Validate output for hallucination risk and quality issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick validate a text string
  lithium-validate --text "Your output text here"
  
  # Validate a file
  lithium-validate --file output.txt
  
  # Validate with source files for cross-checking
  lithium-validate --file output.txt --sources source1.txt source2.txt
  
  # Generate detailed report
  lithium-validate --file output.txt --report markdown
  
  # Get validation statistics
  lithium-validate --stats
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '--text', '-t',
        help='Text to validate (direct input)'
    )
    input_group.add_argument(
        '--file', '-f',
        help='Path to file containing text to validate'
    )
    
    # Source options
    parser.add_argument(
        '--sources', '-s',
        nargs='+',
        help='Source files for validation cross-checking'
    )
    
    # Output options
    parser.add_argument(
        '--report', '-r',
        choices=['json', 'markdown', 'text'],
        default='text',
        help='Report format (default: text)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (otherwise prints to stdout)'
    )
    
    # Other options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with all details'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show validation statistics from history'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.7,
        help='Passing score threshold (0-1, default: 0.7)'
    )
    
    args = parser.parse_args()
    
    # Initialize interface
    interface = ValidationInterface()
    
    # Handle statistics request
    if args.stats:
        stats = interface.get_statistics()
        print(json.dumps(stats, indent=2))
        return 0
    
    # Get content to validate
    if args.text:
        content = args.text
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {args.file}: {e}", file=sys.stderr)
            return 1
    else:
        print("Error: Must provide either --text or --file", file=sys.stderr)
        parser.print_help()
        return 1
    
    # Read sources if provided
    sources = []
    if args.sources:
        for source_path in args.sources:
            try:
                with open(source_path, 'r') as f:
                    sources.append(f.read())
            except Exception as e:
                print(f"Warning: Could not read source {source_path}: {e}", 
                     file=sys.stderr)
    
    # Perform validation
    if args.verbose:
        result = interface.full_validate(content, sources)
        output = interface.generate_report(result, args.report)
    else:
        result_dict = interface.quick_validate(content, sources)
        if args.report == 'json':
            output = json.dumps(result_dict, indent=2)
        else:
            # Simple text output for quick validation
            output = f"""
Validation Result:
  Score: {result_dict['score']}%
  Status: {'PASSED' if result_dict['passed'] else 'FAILED'}
  Risk: {result_dict['risk']}
  
Issues: {', '.join(result_dict['key_issues']) if result_dict['key_issues'] else 'None'}

Recommendation: {result_dict['top_recommendation'] or 'No specific recommendations'}
"""
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Results written to {args.output}")
        except Exception as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            return 1
    else:
        print(output)
    
    # Return appropriate exit code
    if args.verbose:
        return 0 if result.passed else 1
    else:
        return 0 if result_dict['passed'] else 1

def report():
    """Entry point for lithium-report command"""
    sys.argv.insert(1, '--report')
    sys.argv.insert(2, 'markdown')
    main()

if __name__ == "__main__":
    sys.exit(main())
