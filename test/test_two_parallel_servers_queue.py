import unittest
import src.discret_events.two_parallel_servers_queue as twpsq
from src.utils import round_time_list, calculate_average_time_in_system

class TestSimulateTwoParallelServersQueue(unittest.TestCase):
    def test_basic_simulation(self):
        print("Testing two-parallel servers queue simulation...")
        lam = 1.0
        mu_1 = 2.0
        mu_2 = 1.5
        t = 5.0

        arrivals, departures, exceeded_time, c1, c2 = twpsq.simulate_two_paralel_servers_queue(lam, mu_1, mu_2, t)
        
        self.assertIsInstance(arrivals, list)
        self.assertIsInstance(departures, list)
        self.assertIsInstance(exceeded_time, float)
        self.assertGreaterEqual(len(arrivals), len(departures))
        self.assertGreaterEqual(exceeded_time, 0.0)

        print_two_parallel_server_queue_results(arrivals, departures,exceeded_time, c1, c2)

    def test_multipe_simulations(self):
        print("Testing multiple two-parallel-servers-queue simulations...")
        lmd = 1.0
        mu_1 = 2.0
        mu_2 = 1.5
        t = 5.0

        n = 1000 # simulations

        total_avg_time_on_system = 0.0
        total_exceeded_time = 0.0
        total_c1 = 0
        total_c2 = 0

        for _ in range(n):
            
            arrivals, departures, exceeded_time, c1 , c2 = twpsq.simulate_two_paralel_servers_queue(lmd, mu_1, mu_2, t)
            
            # Verifica que las listas no sean None
            self.assertIsNotNone(arrivals)
            self.assertIsNotNone(departures)
            self.assertIsInstance(arrivals, list)
            self.assertIsInstance(departures, list)
            self.assertIsInstance(exceeded_time, float)
            
            # Verifica que las llegadas y salidas tengan sentido
            self.assertGreaterEqual(len(arrivals), len(departures))
            self.assertGreaterEqual(exceeded_time, 0.0)

            total_avg_time_on_system += calculate_average_time_in_system(arrivals, departures)
            total_exceeded_time += exceeded_time
            total_c1 += c1
            total_c2 += c2
        
        print_multiple_two_parallel_server_queue_results(total_c1 / n, total_c2 / n , total_avg_time_on_system / n, total_exceeded_time / n , n)


def print_two_parallel_server_queue_results(arrivals : list, departures : list, exceeded_time : float, c_1 : int, c_2 : int):
    """Print the result of a two in series servers queue event"""
    print("------------------------------------------------------------------------")
    print("Simulation Results (Two-In-Series-Servers-Queue-Event)")
    
    print(f"Arrivals({len(arrivals)}): ")
    print(round_time_list(arrivals))

    print(f"Departures({len(departures)})")
    print(round_time_list(departures))

    print(f"Time exceeded after close: {exceeded_time:.2f}")

    avg_time = calculate_average_time_in_system(arrivals, departures)
    print(f"Average time in system for customer: {avg_time}")

    print(f"Customers attended(server 1) : {c_1}")
    print(f"Customers attended(server 2) : {c_2}")
    print("------------------------------------------------------------------------")

def print_multiple_two_parallel_server_queue_results(avg_c1 : float, avg_c2 : float , avg_time : float, avg_exceeded_time : float, n : int):
    print("------------------------------------------------------------------------")
    print("Multiple Simulations Results (Two-In-Series-Servers-Queue-Event)")
    print(f"Total Simulations : {n}")
    print(f"Average customers : {(avg_c1 + avg_c2):.2f}")
    print(f"Average time on system per customer : {avg_time:.2f}")
    print(f"Average time past after close : {avg_exceeded_time:.2f}")
    print(f"Average customers attended by server 1 : {avg_c1}")
    print(f"Average customers attended by server 2 : {avg_c2}")
    print("------------------------------------------------------------------------")


if __name__ == '__main__':
    unittest.main()