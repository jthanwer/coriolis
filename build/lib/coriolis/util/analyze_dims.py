def detect_grid(viz):
    detected = 0
    for coord in [viz.abs_name, viz.ord_name]:
        if 'lat' in coord.lower():
            detected += 1
        if 'lon' in coord.lower():
            detected += 1
    return True if detected == 2 else False
