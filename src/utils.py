def round_time_list(time_list):
    """Round the times in a list to 2 decimal places."""
    return [round(t, 2) for t in time_list]

def calculate_average_time_in_system(arrival_times, departure_times):
    """Calculate the average time in system for clients who have departed."""
    customers = len(departure_times)
    
    if customers == 0:
        return 0.0
    
    return round((sum(departure_times) - sum(arrival_times)) / customers , 2)