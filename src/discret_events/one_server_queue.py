from src.random_variable_generator import rvg
import math

def simulate_one_server_queue(lmd : float, mu : float, end_time : float):
    """Simulate a one-server queue with arrival rate lambda and service rate mu up to time end_time.
    Parameters:
      lmd : Poisson rate for the arrival times
      mu  : Exponential rate for the service time
      end_time : Time until the system will accept new arrivals

    Return :
        arrival_times -> list(float) : times of arrival times for each customer.
        departure_times -> list(float) : times of departure times for each customer.
        exceeded_time -> float : time past close time that the system remains attending customers."""

    # time variable
    t = 0.0     

    # SS = (n) : number of customers in the system
    n  = 0
    
    # Event List : (t_a , t_d) 
    t_a = rvg.generate_next_poisson_time(0, lmd)    # time for next arrival
    t_d = math.inf                              # time for next departure

    # Output Variables
    arrival_times = []      # list of arrival times for each customer
    departure_times = []    # list of departure times for each customer
    exceeded_time = 0.0     # time past after T that the last customer departs

    while True :
        
        # Next Event : Customer Arrival
        if t_a == min(t_a, t_d, end_time) :
            
            t = t_a   # update current time to next arrival
            n += 1    # update number of customers on the system

            t_a = rvg.generate_next_poisson_time(t, lmd) # generate the new arrival time

            # if the server is free the customer is attended
            if n == 1 :
                t_d = rvg.generate_next_poisson_time(t, mu)  # generate the new departure time
            
            # Collect arrival time of customer i
            arrival_times.append(t)
        
        # Next Event : Customer Departure
        elif n > 0 :     

            t = t_d     # update current time to next departure
            n -= 1      # update number of customers on the system 

            # No customers to be serviced
            if n == 0 :
                t_d = math.inf

            else:
                t_d = rvg.generate_next_poisson_time(t, mu) # generate next departure time

            # Collect departure time of customer i
            departure_times.append(t)

        # Next Event : System close
        else:
            
            # Collect exceeded time
            exceeded_time = max(0.0 , t - end_time)

            # Return output variables
            return arrival_times, departure_times, exceeded_time



