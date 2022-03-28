def heatindex(temp, hum):
    fahrenheit = ((temp * 9 / 5) + 32)
    t2 = pow(fahrenheit, 2)
    h2 = pow(hum, 2)
    c1 = [-42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783e-03, -5.481717e-02, 1.22874e-03, 8.5282e-04,
          -1.99e-06]
    heatindex_f = c1[0] + (c1[1] * fahrenheit) + (c1[2] * hum) + (c1[3] * fahrenheit * hum) + (c1[4] * t2) + (
                c1[5] * h2) + (c1[6] * t2 * hum) + (c1[7] * fahrenheit * h2) + (c1[8] * t2 * h2)
    heatindex_celsius = (round(((heatindex_f - 32) * 5 / 9), 0))
    return heatindex_celsius


