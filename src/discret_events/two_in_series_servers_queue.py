import math
import src.random_variable_generator as rvg
def simulate_two_in_series_servers_queue(lmd : float, mu_1 : float, mu_2 : float, end_time : float):
    """Simulate a two-in-series-server queue with arrival rate lambda, service rate mu_1 for sever 1 and mu_2 
    for server 2, up to time end_time.

    Parameters:
      lmd : Poisson rate for the arrival times
      mu_1  : Exponential rate for the service time (server 1)
      mu_2  : Exponential rate for the service time (server 2)
      end_time : Time until the system will accept new arrivals

    Return :
        arrival_times -> list(float) : times of arrival times for each customer.
        departure_times -> list(float) : times of departure times for each customer.
        exceeded_time -> float : time past close time that the system remains attending customers. """

    # time variable 
    t = 0.0     # keeps track of current simulated time

    # SS = (n1 , n2)
    n_1 = 0     # number of customers on server 1(including the one being attended)
    n_2 = 0     # number of customers on server 2(including the one being attended)

    # Even List(t_a, t_1, t_2)
    t_a = rvg.generate_next_poisson_time(0, lmd)     # time of next arrival
    t_1 = math.inf                                   # service completion time for server 1
    t_2 = math.inf                                   # service completion time for server 2

    # Output Variables
    arrival_times = []
    departure_times = []
    exceeded_time = 0.0    # time past after T that the last customer departs

    while True :

        # Next Event : Customer Arrival
        if t_a == min(t_a, t_1, t_2, end_time) : 
            
            t = t_a    # update current time to next arrival
            n_1 += 1   # update number of customers on server 1

            t_a = rvg.generate_next_poisson_time(t, lmd) # generate the time of next arrival

            # if the server 1 is free, the customer is attended
            if n_1 == 1 :
                t_1 = rvg.generate_next_poisson_time(t, mu_1)
            
            # Collect arrival time of customer i
            arrival_times.append(t)

        # Next Event : Service Completion (server 1)
        elif t_1 <= t_2 and n_1 > 0:

            t = t_1     # update current time to completion of server 1 work
            n_1 -= 1    # update number of customers on server 1
            n_2 += 1    # update number of customers on server 2

            # if there are customers waiting to use server 1 the next customer is attended if not the server stays inactive
            t_1 = math.inf if n_1 == 0 else rvg.generate_next_poisson_time(t, mu_1)
            

            # if server 2 is free, the customer is attended
            if n_2 == 1 :
                t_2 = rvg.generate_next_poisson_time(t, mu_2)

        # Next Event : Service Completion (server 2)
        elif t_2 < t_1 :
            t = t_2     # update current time to completion of server 2 work
            n_2 -= 1    # update number of customers on server 2

            # if there are customers waiting to use server 2 the next customer is attended if not 
            # the server stays inactive
            t_2 = math.inf if n_2 == 0 else rvg.generate_next_poisson_time(t, mu_2)
            
            # Collect departure time of customer i
            departure_times.append(t)
            
        # Next Event : System close
        elif n_1 + n_2 == 0:
            exceeded_time = max(0.0 , t - end_time)
            return arrival_times, departure_times, exceeded_time