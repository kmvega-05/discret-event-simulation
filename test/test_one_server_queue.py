import unittest
import src.discret_events.one_server_queue as osq
from src.utils import round_time_list, calculate_average_time_in_system

class TestSimulateOneServerQueue(unittest.TestCase):
    def test_basic_simulation(self):
        print("Testing one-server queue simulation...")
        lam = 1.0
        mu = 2.0
        t = 5.0

        arrivals, departures, time_past = osq.simulate_one_server_queue(lam, mu, t)
        
        # Verifica que las listas no sean None
        self.assertIsNotNone(arrivals)
        self.assertIsNotNone(departures)
        self.assertIsInstance(arrivals, list)
        self.assertIsInstance(departures, list)
        self.assertIsInstance(time_past, float)
        
        # Verifica que las llegadas y salidas tengan sentido
        self.assertGreaterEqual(len(arrivals), len(departures))
        self.assertGreaterEqual(time_past, 0.0)

        print_one_server_queue_results(arrivals, departures, time_past)

    def test_multipe_simulations(self):
        print("Testing multiple one-server queue simulations...")
        lam = 1.0
        mu = 2.0
        t = 5.0

        n = 1000 # simulations

        total_avg_time_on_system = 0.0
        total_past_time = 0.0
        total_customers = 0

        for i in range(n):
            
            arrivals, departures, time_past = osq.simulate_one_server_queue(lam, mu, t)
            
            # Verifica que las listas no sean None
            self.assertIsNotNone(arrivals)
            self.assertIsNotNone(departures)
            self.assertIsInstance(arrivals, list)
            self.assertIsInstance(departures, list)
            self.assertIsInstance(time_past, float)
            
            # Verifica que las llegadas y salidas tengan sentido
            self.assertGreaterEqual(len(arrivals), len(departures))
            self.assertGreaterEqual(time_past, 0.0)

            total_customers += len(arrivals)
            total_avg_time_on_system += calculate_average_time_in_system(arrivals, departures)
            total_past_time += time_past


        print_multiple_one_server_queue_results(total_customers / n, total_avg_time_on_system / n, total_past_time / n , n)


def print_one_server_queue_results(arrivals : list, departures : list, time_past : float):
    """Print the result of a one server queue event"""
    print("------------------------------------------------------------------------")
    print("Simulation Results (One-Server-Queue-Event)")
    
    print(f"Arrivals({len(arrivals)}): ")
    print(round_time_list(arrivals))

    print(f"Departures({len(departures)})")
    print(round_time_list(departures))

    print(f"Time exceeded after close: {time_past:.2f}")

    avg_time = calculate_average_time_in_system(arrivals, departures)
    print(f"Average time in system for customer: {avg_time}")

    print("------------------------------------------------------------------------")

def print_multiple_one_server_queue_results(avg_customers : float , avg_time : float, avg_past_time : float, n : int):
    print("------------------------------------------------------------------------")
    print("Multiple Simulations Results (One-Server-Queue-Event)")
    print(f"Total Simulations : {n}")
    print(f"Average customers : {avg_customers:.2f}")
    print(f"Average time on system per customer : {avg_time:.2f}")
    print(f"Average time past after close : {avg_past_time:.2f}")
    print("------------------------------------------------------------------------")


if __name__ == '__main__':
    unittest.main()