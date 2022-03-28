from datetime import datetime, date, timedelta
import decimal
from distutils.log import debug

def parse_jobblogg(file_name, with_comments=True):
  with open(file_name, encoding='utf-8', mode='r') as f:
    lines = f.readlines()
    entries = []
    date_format='%Y-%m-%dT%H:%M:%S%z'
    for i, line in enumerate(lines):
      splitted_line = line.split(",")
      if not len(splitted_line) > 1:
        continue
      if not with_comments:
        entries.append({"datetime": datetime.time.strptime(line.strip(), date_format)})
      if with_comments:
        date_part = splitted_line[0].strip()
        description = splitted_line[1].strip()
        entry_datetime = datetime.strptime(date_part, date_format)
        entries.append({"datetime": entry_datetime,
                        "description": description})   
    return entries
  
def format_entries(list_of_entries):
  entries = []
  debugprint = False
  for id, one_entry  in enumerate(list_of_entries):
    entry_datetime_from = one_entry.get("datetime")  
    time_from = entry_datetime_from.time()
    date_from = entry_datetime_from.date()
    description = one_entry.get("description")
    time_to = 0
    duration = 0
    entry_datetime_to = 0
    duration_total_seconds = 0
    
    if id < len(list_of_entries) - 1:
      entry_datetime_to = list_of_entries[id+1].get("datetime")
      time_to = entry_datetime_to.time()

    if entry_datetime_to != 0:
      duration = entry_datetime_to - entry_datetime_from
      duration_total_seconds = duration.total_seconds()
    
    
    if not debugprint:
      # print(f"type of duration: {type(duration)} methods: {dir(duration)} ")
      # print(f"total_seconds: {duration.total_seconds()}")
      debugprint = True
    
    entries.append({"date": date_from,
                    "details":
                    {"from": time_from,
                    "to": time_to,
                    "duration": duration,
                    "duration_decimal": decimal.Decimal(duration_total_seconds/3600),
                    "description": description}
                    })
  return entries

def print_filtered_entries(entries, date_filter_from, date_filter_to, csv=False):
  last_weekday = -1
  weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
  total_duration_of_day = []
  for i in entries:
    entry_date = i.get("date")
    if entry_date >= date_filter_from and entry_date < date_filter_to and i.get("details").get("description") != "EOD":
      if last_weekday != entry_date.weekday():
        if last_weekday != -1:
          print(f"\nTotal duration of day: {sum(total_duration_of_day):.2f}\n")
        total_duration_of_day = []
        print(f"\n{'#'*50}\n{entry_date} {weekdays[entry_date.weekday()]}\n{'#'*50}\n")
        keys = list(i.get('details').keys())
        print(f"{keys[0]+':':<15}{keys[1]+':':<15}{keys[2]+':':<15}{keys[3]+':':<20}{keys[4]+':'}")
    
      print(f"{str(i.get('details').get('from')):<15}{str(i.get('details').get('to')):<15}{str(i.get('details').get('duration')):<15}{str(round(float(i.get('details').get('duration_decimal')),2)).replace('.',','):<20}{i.get('details').get('description')}")
      total_duration_of_day.append(float(i.get('details').get('duration_decimal')))
      last_weekday = entry_date.weekday()
  print(f"\nTotal duration of day: {sum(total_duration_of_day):.2f}\n")
      
def get_last_specific_weekday(weekday_int):
  today = datetime.now()
  one_week_back = today - timedelta(days=7)
  
  for day_in_week in range(7):
    if one_week_back.weekday() == weekday_int:
      return one_week_back.date()
    print("backing one day")
    one_week_back = one_week_back - timedelta(days=1)
    day_in_week+=1
  
  
def get_previous_week_start():
  return get_last_specific_weekday(0)

def main():
  jobb_logg_file_name=r'C:\Users\HaraldEllingsen\iCloudDrive\iCloud~is~workflow~my~workflows\jobb-logg2.txt'
  entry_list = parse_jobblogg(jobb_logg_file_name, with_comments=True)
  
  date_from = get_previous_week_start()

  date_to = date_from + timedelta(days=7)
  
  print("Processing: " + jobb_logg_file_name)
  
  while True:
    print(f"Showing entries from {date_from} to {date_to}")
    result = input("Type 'n' to jump one week forward, 'p' to jump back one week, enter to continue: ")
    if result == 'n':
      date_from = date_from + timedelta(days=7)
      date_to = date_from + timedelta(days=7)
    elif result == 'p':
      date_from = date_from + timedelta(days=-7)
      date_to = date_from + timedelta(days=-7)
    elif not result:
      break
    
  print_filtered_entries(format_entries(entry_list), date_from, date_to, csv=True)
  
if __name__ == "__main__":
  main()