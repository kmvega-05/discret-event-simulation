import random
import math

def generate_U():
    """Generate a random variable U uniformly distributed in [0, 1)."""
    return random.uniform(0, 1)

def generate_random_number(n : int):
    """Generate a random number in the range [1,n] with equal probability for each number"""
    u = generate_U()
    return math.floor(n * u) + 1

def generate_geometric_variable(p : float):
    """Generate a geometric random variable with probabilty p"""
    u  = generate_U()
    g = math.log(u) / math.log(1 - p)
    return math.floor(g) + 1

def generate_binomial_variable(n: int , p : float):
    """Generate a binomial random variable with parameters n and p.
    n : number of trials
    p : probability of success in each trial
    
    Uses the inverse transform method. By computing the cumulative distribution
    function until it exceeds a uniform random variable U."""
    
    i = 0               # current number of successes
    c = p / (1 - p)     # constant factor
    pf = (1 - p)**n     # P(X = 0)
    f = pf              # cumulative distribution function

    u = generate_U()    # uniform random variable in [0, 1)
    
    while u >= f :      
        pf = c * (n - i) / (i + 1) * pf 
        f  = f + pf
        i  = i + 1
    
    return i

def generate_poisson_variable(lam : float):
    """Generate a Poisson random variable with parameter lambda.
    
    Uses the inverse transform method. By computing the cumulative distribution
    function until it exceeds a uniform random variable U."""

    i = 0               # current number of occurrences
    pf = math.exp(-lam) # P(X = 0)
    f = pf              # cumulative distribution function

    u = generate_U()    # uniform random variable in [0, 1)
    
    while u >= f :      
        pf = lam / (i + 1) * pf 
        f  = f + pf
        i  = i + 1
    
    return i

def generate_exponential_variable(lam : float):
    """Generate an exponential random variable with parameter lambda."""
    u = generate_U()
    return -math.log(1 - u) / lam

def generate_poisson_process(lam : float, t : float):
    """Generate a Poisson process with parameter lambda up to time t.
    
    Returns a list of the arrival times."""
    
    arrival_times = []
    current_time = 0.0

    while True:
        inter_arrival_time = generate_exponential_variable(lam)
        current_time += inter_arrival_time
        
        if current_time >= t:
            break
        
        arrival_times.append(current_time)
    
    return arrival_times