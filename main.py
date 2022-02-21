from datetime import datetime, date, timedelta
from email import header
from time import sleep, time

from black import out

def parse_jobblogg(file_name, with_comments=True):
  with open(file_name, encoding='utf-8', mode='r') as f:
    lines = f.readlines()
    entries = []
    date_format='%Y-%m-%dT%H:%M:%S%z'
    for i, line in enumerate(lines):
      if not with_comments:
        entries.append({"datetime": datetime.time.strptime(line.strip(), date_format)})
      if with_comments:
        date_part = line.split(",")[0].strip()
        description = line.split(",")[1].strip()
        entry_datetime = datetime.strptime(date_part, date_format)
        entries.append({"datetime": entry_datetime,
                        "description": description})   
    return entries
  
def format_entries(list_of_entries):
  entries = []
  for id, one_entry  in enumerate(list_of_entries):
    entry_datetime_from = one_entry.get("datetime")  
    time_from = entry_datetime_from.time()
    date_from = entry_datetime_from.date()
    description = one_entry.get("description")
    time_to = 0
    duration = 0
    entry_datetime_to = 0
    
    if id < len(list_of_entries) - 1:
      entry_datetime_to = list_of_entries[id+1].get("datetime")
      time_to = entry_datetime_to.time()

    if entry_datetime_to != 0:
      duration = entry_datetime_to - entry_datetime_from
    
    entries.append({"date": date_from,
                    "details":
                    {"from": time_from,
                    "to": time_to,
                    "duration": duration,
                    "description": description}
                    })
  return entries

def print_filtered_entries(entries, date_filter_from, date_filter_to, csv=False):
  last_weekday = -1
  weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
  for i in entries:
    entry_date = i.get("date")
    if entry_date >= date_filter_from and entry_date < date_filter_to and i.get("details").get("description") != "EOD":
      current_weekday = entry_date.weekday()
      if last_weekday != current_weekday:
        print(f"\n{'#'*50}\n{entry_date} {weekdays[current_weekday]}\n{'#'*50}\n")
        keys = list(i.get('details').keys())
        print(f"{keys[0]+':':<15}{keys[1]+':':<15}{keys[2]+':':<15}{keys[3]+':'}")
      print(f"{str(i.get('details').get('from')):<15}{str(i.get('details').get('to')):<15}{str(i.get('details').get('duration')):<15}{i.get('details').get('description')}")
      last_weekday = current_weekday
      
      

def main():
  jobb_logg_file_name=r'C:\Users\HaraldEllingsen\iCloudDrive\iCloud~is~workflow~my~workflows\jobb-logg2.txt'
  entry_list = parse_jobblogg(jobb_logg_file_name, with_comments=True)
  
  date_from = date(2022, 2, 14)
  date_to = date_from + timedelta(days=7)
  
  print("Processing: " + jobb_logg_file_name)
  print(f"Showing entries from {date_from} to {date_to}")
  input()
  print_filtered_entries(format_entries(entry_list), date_from, date_to, csv=True)
  
if __name__ == "__main__":
  main()