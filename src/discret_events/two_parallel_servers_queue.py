import math
import src.random_variable_generator as rvg
def simulate_two_paralel_servers_queue(lmd : float, mu_1 : float, mu_2 : float, end_time : float):
    """Simulate a two-parallel-servers queue with arrival rate lambda and service rates mu_1 and mu_2 up to time end_time.
    Parameters :
      lmd : Poisson rate for the arrival times
      mu_1  : Exponential rate for the service time (server 1)
      mu_2  : Exponential rate for the service time (server 2)
      end_time : Time until the system will accept new arrivals
    
    Return: 
      arrival_times -> list(float) : times of arrival times for each customer.
      departure_times -> list(float) : times of departure times for each customer.
      exceeded_time -> float : time past close time that the system remains attending customers.
      c_1 -> int : number of customers served by server 1
      c_2 -> int : number of customers served by server 2
    """
    
    # time variable 
    t = 0.0     # keeps track of current simulated time

    # System State(n, i_1 , i_2)
    # n : number of customers on the system
    # i_1 : customer being attend by server 1
    # i_2 : customer being attend by server 2
    SS = (0, -1, -1)

    # Even List(t_a, t_1, t_2)
    t_a = rvg.generate_next_poisson_time(0, lmd)     # time of next arrival
    t_1 = math.inf                                   # service completion time for server 1
    t_2 = math.inf                                   # service completion time for server 2

    # Output Variables
    c_1 = 0     # number of customers served by server 1
    c_2 = 0     # number of customers served by server 2
    n_a = 0     # number of arrivals

    arrival_times = []
    departure_times = {}

    while True :
        # Next Event : Customer Arrival
        if t_a == min(t_a , t_1, t_2 , end_time):
            t = t_a     # update current time to next arrival
            n_a += 1    # update number of arrivals

            t_a = rvg.generate_next_poisson_time(t,lmd)  # generate new arrival time
            customer = n_a -1                            # current customer

            # Determine wich server will attend the customer
            # if Server 1 is free it will attend the customer
            # if Server 2 is free it will attend the customer if Server 1 is busy
            # if both are busy the customer will wait
            i_1, t_1 = (customer, rvg.generate_next_poisson_time(t, mu_1)) if SS[1] == -1 else (SS[1] , t_1)
            i_2, t_2 = (customer, rvg.generate_next_poisson_time(t, mu_1)) if SS[2] == -1 and SS[1] != -1 else (SS[2] , t_2)

            SS = (SS[0] + 1 , i_1, i_2)  

            # Collect arrival time of customer i
            arrival_times.append(t)

        # Next Event : Service Completion (server 1)
        elif(t_1 <= t_2 and t_1 < math.inf):
            t = t_1           # update current time to time completion of server 1
            c_1 += 1          # update number of clients attended by server 1 
            customer = SS[1]  # current customer

            # update next completion time and customer (server 1)
            t_1 = math.inf if SS[0] <= 2 else rvg.generate_next_poisson_time(t, mu_1)
            next_customer = -1 if SS[0] <= 2 else max(SS[1], SS[2]) + 1

            SS = (SS[0] - 1 , next_customer , SS[2])

            departure_times[customer] = t

        # Next Event : Service Completion (server 2)
        elif(t_2 < t_1):
            t = t_2           # update current time to time completion of server 2
            c_2 += 1          # update number of clients attended by server 2 
            customer = SS[2]  # current customer

            # update next completion time and customer (server 2)
            t_2 = math.inf if SS[0] <= 2 else rvg.generate_next_poisson_time(t, mu_2)
            next_customer = -1 if SS[0] <= 2 else max(SS[1], SS[2]) + 1

            SS = (SS[0] - 1 , SS[1] , next_customer)

            departure_times[customer] = t

        # Event : System closed and no customers remaining
        else :
            exceeded_time = max(0.0, end_time - t)
            return arrival_times, convert_to_list(departure_times), exceeded_time, c_1, c_2


def convert_to_list(d : dict) :
    """Converts the departure times dictionary to a list"""
    return [d[i] for i in range(len(d))]


