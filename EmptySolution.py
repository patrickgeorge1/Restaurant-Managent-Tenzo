"""
Vitoga George Patrick, patrionpatrick@gmail.com
"""
import pandas as pd
import operator

def process_shifts(path_to_csv):
    data = pd.read_csv(path_to_csv)
    productivity = {x:0 for x in range(0, 24)}
    for _, row in data.iterrows():
        start_break, end_break, = format_hour_interval(row['break_notes'])
        start_shift,end_shift = format_hour_interval(row['start_time'] + "-" + row['end_time'])
        pay_rate = row['pay_rate']
        productivity = update_productivity(productivity, start_shift, end_shift, start_break, end_break, pay_rate)
    productivity = {map_hour_to_key(k):int(v) for (k,v) in productivity.items()}
    return productivity


def process_sales(path_to_csv):
    data = pd.read_csv(path_to_csv)
    productivity = {x:0 for x in range(0, 24)}
    for _, row in data.iterrows():
        time,_ = format_hour_interval(row["time"]+"- 00:00")
        productivity[time]+= row["amount"]
    productivity = {map_hour_to_key(k):v for (k,v) in productivity.items()}
    return productivity

def compute_percentage(shifts, sales):
    productivity = {map_hour_to_key(x):0 for x in range(0, 24)}
    for hour in sales.keys():
        if sales[hour] == 0:
            productivity[hour] = -shifts[hour]
        else:
            productivity[hour] = 100 * shifts[hour]/sales[hour]
    return productivity

def best_and_worst_hour(percentages):
    best_hour = max(percentages.items(), key=operator.itemgetter(1))[0]
    worst_hour = min(percentages.items(), key=operator.itemgetter(1))[0]
    return [best_hour,worst_hour]


def format_hour_interval(hour):
    arguments = hour.split("-")
    arguments =  [x.strip() for x in arguments]
    start_break,time_start,more_than_fix_start = convert_AmPm_hour_to_europe(arguments[0])
    end_break,time_end,more_than_fix_end = convert_AmPm_hour_to_europe(arguments[1])
    if time_end == "PM":
        end_break+= 12
    if time_start == "PM":
        start_break+= 12
    if time_start == "PM" and time_end == "":
        end_break+= 12
    if time_end == "PM" and time_start == "":
        start_break+= 12
    if more_than_fix_end == 1:
        end_break += 1
    if start_break == end_break:
        end_break+=1
    return start_break,end_break

def convert_AmPm_hour_to_europe(hour):
    time = ""
    more_than_fix = 0
    if hour.find('PM') != -1:
        time = "PM"
    if hour.find('AM') != -1:
        time = "AM"
    hour = hour.replace('AM', '').replace('PM', '').strip()
    if hour.find('.') != -1:
        parts = hour.split(".")
        if (parts[1] != '00'):
            more_than_fix = 1
        hour = parts[0]
    if hour.find(':') != -1:
        parts = hour.split(":")
        if (parts[1] != '00'):
            more_than_fix = 1
        hour = parts[0]
    hour = int(hour)
    return hour,time,more_than_fix

def update_productivity(productivity, start_shift, end_shift, start_break, end_break, pay_rate):
    # print( str(start_shift) + ' ' + str(end_shift) + ' ' + str(start_break) + ' ' + str(end_break) + ' ' +  str(pay_rate))
    condition_start = start_shift
    condition_end = end_shift
    if start_shift > end_shift:
        condition_end = 24
    while condition_start < condition_end:
        if condition_start < start_break or condition_start >= end_break:
            productivity[condition_start]+=pay_rate
        condition_start+=1
    return productivity

def map_hour_to_key(k):
    k = str(k)
    if len(k) < 2:
        k = '0'+ k
    return k+':00'
        
def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)


# Vitoga George Patrick, patrionpatrick@gmail.com
