"""Example mixing wildcard and explicit imports."""
import sys
import os
from collections import Counter, defaultdict
from itertools import *  # Wildcard import mixed with explicit imports
from math import pi, e  # Explicit imports
from random import *  # Another wildcard


class DataAnalyzer:
    """Analyzer using mixed import styles."""
    
    def __init__(self):
        self.data = []
        self.counter = Counter()  # From explicit import
        self.groups = defaultdict(list)  # From explicit import
    
    def generate_data(self, size=100):
        """Generate random data using various imports."""
        seed(42)  # From random wildcard
        
        # Using itertools wildcard functions
        for i in count():  # From itertools
            if i >= size:
                break
            
            # Mix of explicit and wildcard
            value = uniform(0, 2 * pi)  # uniform from random*, pi from explicit
            self.data.append({
                'id': i,
                'value': value,
                'sin_value': sin(value),  # sin from random* (overwrites math.sin)
                'category': choice(['A', 'B', 'C', 'D']),  # From random*
                'timestamp': os.path.getmtime(sys.argv[0])  # Using explicit imports
            })
    
    def analyze_patterns(self):
        """Analyze data patterns using mixed imports."""
        # Using itertools functions
        sorted_data = sorted(self.data, key=lambda x: x['value'])
        
        # Group by category using itertools
        for key, group in groupby(sorted_data, key=lambda x: x['category']):
            group_list = list(group)
            self.groups[key] = group_list
            
            # Use combinations from itertools
            pairs = list(combinations(group_list[:5], 2))  # From itertools*
            
            # Analyze pairs
            for item1, item2 in pairs:
                diff = abs(item1['value'] - item2['value'])
                self.counter[f"{key}_pairs"] += 1
        
        # Using chain from itertools
        all_values = list(chain.from_iterable(
            [item['value'] for item in group] 
            for group in self.groups.values()
        ))
        
        # Statistics using both explicit and wildcard
        return {
            'mean': sum(all_values) / len(all_values),
            'sample': sample(all_values, min(10, len(all_values))),  # From random*
            'pi_ratio': sum(v for v in all_values if v > pi) / len(all_values),  # pi from explicit
            'e_ratio': sum(v for v in all_values if v > e) / len(all_values),  # e from explicit
            'permutations': len(list(permutations(range(4))))  # From itertools*
        }
    
    def create_batches(self, batch_size=10):
        """Create batches using itertools."""
        # Using islice from itertools wildcard
        shuffled = self.data.copy()
        shuffle(shuffled)  # From random*
        
        batches = []
        for i in range(0, len(shuffled), batch_size):
            batch = list(islice(shuffled, i, i + batch_size))  # From itertools*
            batches.append(batch)
        
        return batches
    
    def find_cycles(self):
        """Find cycles in data using itertools.cycle."""
        # Create a cycling iterator
        categories = cycle(['A', 'B', 'C'])  # From itertools*
        
        results = []
        for i, cat in enumerate(categories):
            if i >= 12:  # Only take first 12
                break
            results.append((i, cat))
        
        return results


def utility_functions():
    """Demonstrate usage of various imported functions."""
    # Using explicit imports
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Using math constants from explicit import
    print(f"Pi: {pi}, E: {e}")
    
    # Using random wildcard functions
    random_list = [randint(1, 100) for _ in range(10)]  # From random*
    print(f"Random integers: {random_list}")
    
    # Using itertools wildcard functions
    repeated = list(repeat('X', 5))  # From itertools*
    print(f"Repeated: {repeated}")
    
    # Product from itertools
    products = list(product([1, 2], ['a', 'b']))  # From itertools*
    print(f"Products: {products}")
    
    # Using Counter from explicit import
    cnt = Counter(random_list)
    print(f"Counts: {dict(cnt)}")


if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.generate_data(50)
    
    stats = analyzer.analyze_patterns()
    print(f"Statistics: {stats}")
    
    batches = analyzer.create_batches(10)
    print(f"Number of batches: {len(batches)}")
    
    cycles = analyzer.find_cycles()
    print(f"Cycles: {cycles}")
    
    print("\n=== Utility Demo ===")
    utility_functions() 
