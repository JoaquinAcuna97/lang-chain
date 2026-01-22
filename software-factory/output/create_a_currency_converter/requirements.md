# Requirements Specification

## Original Idea

Create a currency converter

## Final Requirements
### Functional
- The system can convert currencies from one to another.
- User input: amount and source/target currency
- System output: converted amount with target currency symbol

### Non-Functional
- Real-time conversion rates
- Multi-threading for performance
- Error handling for invalid inputs

### Assumptions
- Conversion rates will be obtained from a reliable API or database (assumed to be accurate)
- Users are aware of the exchange rates and any potential differences due to fees, etc.

### Constraints
- Limited by the reliability and accuracy of the used data source
- Exchange rate fluctuations may require periodic updates