def analyze_usage(cpu_usage):
    if cpu_usage < 5:
        return "underutilized"
    elif cpu_usage < 40:
        return "moderate"
    else:
        return "high"