# Python Generators - ALX Backend Project

This project demonstrates advanced usage of Python generators for efficient data processing, memory management, and real-world applications involving large datasets and streaming data.

## Project Overview

The project focuses on leveraging Python's `yield` keyword to implement memory-efficient generators that can:
- Stream database rows one by one
- Process data in batches
- Implement lazy pagination
- Calculate aggregates without loading entire datasets into memory

## Learning Objectives

By completing this project, you will:
- Master Python generator functions and the `yield` keyword
- Handle large datasets efficiently without memory overload
- Implement batch processing and lazy loading techniques
- Simulate real-world streaming data scenarios
- Optimize performance for data-driven applications
- Integrate Python generators with SQL databases

## Project Structure

```
python-generators-0x00/
├── seed.py                    # Database setup and seeding
├── 0-stream_users.py         # Single-row streaming generator
├── 1-batch_processing.py     # Batch processing generators
├── 2-lazy_paginate.py        # Lazy pagination implementation
├── 4-stream_ages.py          # Memory-efficient aggregation
├── user_data.csv             # Sample data for testing
├── 0-main.py                 # Test script for database setup
├── 1-main.py                 # Test script for streaming
├── 2-main.py                 # Test script for batch processing
├── 3-main.py                 # Test script for lazy pagination
└── README.md                 # This file
```

## Requirements

- Python 3.x
- MySQL server
- `mysql-connector-python` package
- Basic understanding of SQL and database operations

## Installation

1. Install MySQL connector:
```bash
pip install mysql-connector-python
```

2. Update database credentials in all Python files:
```python
connection = mysql.connector.connect(
    host='localhost',
    user='your_username',  # Update this
    password='your_password',  # Update this
    database='ALX_prodev'
)
```

## Tasks Implementation

### Task 0: Database Setup (`seed.py`)
- `connect_db()`: Connects to MySQL server
- `create_database()`: Creates ALX_prodev database
- `connect_to_prodev()`: Connects to ALX_prodev database
- `create_table()`: Creates user_data table with required schema
- `insert_data()`: Populates table with CSV data

**Table Schema:**
```sql
CREATE TABLE user_data (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age DECIMAL(5,2) NOT NULL,
    INDEX idx_user_id (user_id)
)
```

### Task 1: Single-Row Streaming (`0-stream_users.py`)
- `stream_users()`: Generator that yields user data one by one
- Memory-efficient streaming from database
- Uses only one loop as required

### Task 2: Batch Processing (`1-batch_processing.py`)
- `stream_users_in_batches(batch_size)`: Yields data in batches
- `batch_processing(batch_size)`: Filters users over age 25
- Uses no more than 3 loops total

### Task 3: Lazy Pagination (`2-lazy_paginate.py`)
- `lazy_paginate(page_size)`: Implements lazy loading pagination
- `paginate_users(page_size, offset)`: Helper function for data fetching
- Only fetches next page when needed
- Uses only one loop as required

### Task 4: Memory-Efficient Aggregation (`4-stream_ages.py`)
- `stream_user_ages()`: Generator yielding user ages one by one
- `calculate_average_age()`: Computes average without loading full dataset
- Uses no more than two loops total
- Does not use SQL AVG function

## Usage Examples

### Database Setup
```bash
python 0-main.py
```

### Streaming Users
```bash
python 1-main.py
```

### Batch Processing
```bash
python 2-main.py | head -n 5
```

### Lazy Pagination
```bash
python 3-main.py | head -n 7
```

### Age Aggregation
```bash
python 4-stream_ages.py
```

## Key Features

### Memory Efficiency
- Generators process data on-demand
- No loading of entire datasets into memory
- Suitable for large-scale data processing

### Database Integration
- Direct SQL query execution
- Proper connection management
- Error handling for database operations

### Real-World Applications
- Streaming data processing
- Batch job processing
- Pagination for web applications
- Large dataset analytics

## Performance Benefits

1. **Memory Usage**: Constant memory usage regardless of dataset size
2. **Processing Speed**: On-demand data processing
3. **Scalability**: Handles large datasets efficiently
4. **Resource Management**: Automatic cleanup of database connections

## Testing

Each task includes test scripts that demonstrate:
- Proper generator implementation
- Memory-efficient data processing
- Correct output formatting
- Error handling capabilities

## Project Requirements Compliance

✅ All 5 tasks implemented
✅ Generator functions using `yield`
✅ Memory-efficient data processing
✅ Database integration with MySQL
✅ Proper error handling
✅ Test scripts provided
✅ README documentation
✅ CSV data file included

## Next Steps

1. Update MySQL credentials in all files
2. Install required dependencies
3. Run test scripts to verify functionality
4. Submit for ALX manual review

## Notes

- Update database credentials before running
- Ensure MySQL server is running
- Sample data is provided in `user_data.csv`
- All generators follow the specified constraints (loop limits, etc.)

---

**ALX Backend Python - Generators Project**  
*Deadline: September 8, 2025*
