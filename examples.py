#!/usr/bin/env python3
"""
Example: Using the Validation System
Demonstrates practical usage patterns for consulting outputs
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from validation_interface import ValidationInterface

def example_consulting_report():
    """Example: Validating a consulting recommendation"""
    
    # Sample consulting output
    consulting_output = """
    Based on our comprehensive market analysis, we recommend immediate expansion 
    into the Asian market. Data shows that 95% of similar companies have succeeded 
    with this strategy. The ROI is guaranteed to exceed 200% within 18 months.
    
    However, certain market conditions remain uncertain and require monitoring.
    Implementation should follow a phased approach, though some risks cannot be 
    fully quantified at this time. Historical data from 2019-2023 supports this 
    recommendation, with consistent growth patterns observed across all sectors.
    """
    
    # Sources that might back this up
    sources = [
        "Market research from 2019-2023 shows 60-80% success rate for Asian expansion.",
        "ROI varies between 50% and 300% depending on implementation strategy.",
        "Phased approach recommended by McKinsey study on market entry.",
        "Some sectors show inconsistent growth patterns in Asian markets."
    ]
    
    # Initialize validator
    validator = ValidationInterface()
    
    # Perform full validation
    result = validator.full_validate(
        consulting_output,
        sources=sources,
        scope="Strategic expansion recommendation",
        domain="consulting"
    )
    
    # Generate report
    report = validator.generate_report(result, format='markdown')
    
    print("="*60)
    print("CONSULTING OUTPUT VALIDATION")
    print("="*60)
    print(report)
    
    # Show how to iterate based on recommendations
    if not result.passed:
        print("\n" + "="*60)
        print("APPLYING RECOMMENDATIONS")
        print("="*60)
        
        # Revised version based on validation feedback
        revised_output = """
        Based on our comprehensive market analysis, we recommend a carefully 
        planned expansion into the Asian market. Market research indicates that 
        60-80% of similar companies have achieved positive outcomes with this 
        strategy, though success rates vary by sector and implementation approach.
        
        Expected ROI ranges from 50% to 300% within 18-24 months, with the median 
        outcome around 125%. These projections are based on historical data from 
        2019-2023, though we note that some sectors show inconsistent patterns.
        
        We acknowledge uncertainty in several areas:
        - Regulatory changes in target markets remain unpredictable
        - Currency fluctuation impacts are difficult to quantify precisely
        - Competitive responses cannot be fully anticipated
        
        We recommend a phased implementation approach, as validated by McKinsey 
        research, with clearly defined go/no-go decision points at each stage.
        """
        
        # Re-validate
        revised_result = validator.full_validate(
            revised_output,
            sources=sources,
            scope="Strategic expansion recommendation - Revised",
            domain="consulting"
        )
        
        print(f"\nOriginal Score: {result.overall_score*100:.1f}%")
        print(f"Revised Score: {revised_result.overall_score*100:.1f}%")
        print(f"Risk Reduction: {result.hallucination_risk} -> {revised_result.hallucination_risk}")
        print(f"Status: {'✅ Now Passing' if revised_result.passed else '❌ Still needs work'}")


def example_technical_documentation():
    """Example: Validating technical documentation"""
    
    technical_doc = """
    The system uses a proprietary algorithm that solves NP-hard optimization 
    problems in polynomial time. Performance benchmarks show 100% accuracy 
    across all test cases. The implementation is bug-free and requires no 
    maintenance.
    
    Architecture follows microservices patterns with some components still 
    under development. Scalability testing indicates the system can handle 
    unlimited concurrent users. Security has been validated using industry 
    best practices, though formal certification is pending.
    """
    
    sources = [
        "NP-hard problems cannot be solved in polynomial time unless P=NP.",
        "System testing showed 94% accuracy on standard benchmarks.",
        "Microservices architecture implemented with 12 services.",
        "Load testing successful up to 10,000 concurrent users."
    ]
    
    validator = ValidationInterface()
    result = validator.full_validate(technical_doc, sources, domain="technical")
    
    print("\n" + "="*60)
    print("TECHNICAL DOCUMENTATION VALIDATION")
    print("="*60)
    
    # Quick summary
    quick_result = validator.quick_validate(technical_doc, sources)
    print(f"Quick Check: {quick_result['score']}% - {quick_result['risk']} risk")
    print(f"Key Issues: {', '.join(quick_result['key_issues'])}")
    print(f"Recommendation: {quick_result['top_recommendation']}")


def example_batch_validation():
    """Example: Validating multiple outputs"""
    
    outputs = [
        "Our analysis definitively proves the strategy will succeed.",
        "Based on available data, we estimate a 70-80% probability of success, though several factors remain uncertain.",
        "The data suggests positive outcomes, but we cannot determine the exact magnitude without further analysis.",
    ]
    
    validator = ValidationInterface()
    results = validator.batch_validate(outputs)
    
    print("\n" + "="*60)
    print("BATCH VALIDATION RESULTS")
    print("="*60)
    
    for i, (output, result) in enumerate(zip(outputs, results), 1):
        print(f"\nOutput {i}: \"{output[:50]}...\"")
        print(f"  Score: {result['score']}%")
        print(f"  Risk: {result['risk']}")
        print(f"  Passed: {'✅' if result['passed'] else '❌'}")


def example_with_context_model_protocol():
    """Example: Integration with Context Model Protocol"""
    
    # This would integrate with your CMP from earlier
    output = """
    Following our Context Model Protocol pre-validation, this analysis 
    presents findings with explicit confidence levels:
    
    HIGH CONFIDENCE (>90%): Market size data from government sources shows 
    $2.3B current valuation with 12% CAGR over past 5 years.
    
    MEDIUM CONFIDENCE (75%): Competitive analysis suggests 3-4 major players 
    based on available public filings, though private competitors may exist.
    
    LOW CONFIDENCE (50%): Customer sentiment appears positive based on 
    limited survey data (n=127), but sample may not be representative.
    
    UNCERTAIN: Future regulatory changes could significantly impact 
    projections, but direction and magnitude cannot be determined.
    """
    
    validator = ValidationInterface()
    result = validator.full_validate(output, scope="Market Analysis with CMP")
    
    print("\n" + "="*60)
    print("CMP-ENHANCED OUTPUT VALIDATION")
    print("="*60)
    print(f"Score: {result.overall_score*100:.1f}%")
    print(f"Passes CMP Standards: {'✅ YES' if result.passed else '❌ NO'}")
    
    # Get statistics if running multiple validations
    stats = validator.get_statistics()
    if stats.get('total_validations', 0) > 0:
        print(f"\nCumulative Stats:")
        print(f"  Total Validations: {stats['total_validations']}")
        print(f"  Pass Rate: {stats['pass_rate']*100:.1f}%")
        print(f"  Average Score: {stats['average_score']*100:.1f}%")


if __name__ == "__main__":
    print("OUTPUT VALIDATION SYSTEM EXAMPLES")
    print("Based on 'Why Language Models Hallucinate' Paper")
    print("="*60 + "\n")
    
    # Run examples
    example_consulting_report()
    example_technical_documentation()
    example_batch_validation()
    example_with_context_model_protocol()
    
    print("\n" + "="*60)
    print("Examples completed. The validation system is ready for use.")
    print("Run 'python validate.py --help' for command-line usage.")
