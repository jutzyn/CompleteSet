#!/usr/bin/python
from __future__ import print_function
import sys
import os
import csv
import copy

grid_1     = [["RTK1   ",   50.0, 110.0, 10.0], \
              ["RTK2   ",   50.0, 120.0, 10.0], \
              ["RTK3   ",   40.0,  70.0, 10.0], \
              ["RTK4   ",   40.0,  80.0, 10.0], \
              ["RTK5   ",   40.0,  90.0, 10.0], \
              ["RTK6   ",   40.0, 100.0, 10.0], \
              ["RTK7   ",   40.0, 110.0, 10.0], \
              ["RTK8   ",   40.0, 120.0, 10.0], \
              ["RTK9   ",   40.0, 130.0, 10.0], \
              ["RTK10  ",   30.0,  70.0, 10.0], \
              ["RTK11  ",   30.0,  80.0, 10.0], \
              ["RTK12  ",   30.0,  90.0, 10.0], \
              ["RTK13  ",   30.0, 100.0, 10.0], \
              ["RTK14  ",   30.0, 110.0, 10.0], \
              ["RTK15  ",   30.0, 120.0, 10.0], \
              ["RTK16  ",   20.0,  80.0, 10.0], \
              ["RTK17  ",   20.0,  90.0, 10.0], \
              ["RTK18  ",   20.0, 100.0, 10.0], \
              ["RTK19  ",   20.0, 110.0, 10.0], \
              ["RTK20  ",   20.0, 120.0, 10.0], \
              ["RTK21  ",   10.0, 100.0, 10.0], \
              ["RTK22  ",   10.0, 110.0, 10.0]]

grid_2    =  [["RTK1   ",   50.0, 110.0, 10.0], \
              ["RTK2   ",   50.0, 120.0, 10.0], \
              ["RTK3   ",   40.0,  70.0, 10.0], \
              ["RTK4   ",   40.0,  80.0, 10.0], \
              ["RTK5   ",   40.0,  90.0, 10.0], \
              ["RTK6   ",   40.0, 100.0, 10.0], \
              ["RTK7   ",   40.0, 110.0, 10.0], \
              ["RTK8   ",   40.0, 120.0, 10.0], \
              ["RTK9   ",   40.0, 130.0, 10.0], \
              ["RTK10  ",   30.0,  70.0, 10.0], \
              ["RTK11  ",   30.0,  80.0, 10.0], \
              ["RTK12  ",   30.0,  90.0, 10.0], \
              ["RTK13  ",   30.0, 100.0, 10.0], \
              ["RTK14-1",   30.0, 110.0,  5.0], \
              ["RTK14-2",   30.0, 115.0,  5.0], \
              ["RTK14-3",   35.0, 110.0,  5.0], \
              ["RTK14-4",   35.0, 115.0,  5.0], \
              ["RTK15  ",   30.0, 120.0, 10.0], \
              ["RTK16  ",   20.0,  80.0, 10.0], \
              ["RTK17  ",   20.0,  90.0, 10.0], \
              ["RTK18_1",   20.0, 100.0,  5.0], \
              ["RTK18_2",   20.0, 105.0,  5.0], \
              ["RTK18_3",   25.0, 100.0,  5.0], \
              ["RTK18_4",   25.0, 105.0,  5.0], \
              ["RTK19_1",   20.0, 110.0,  5.0], \
              ["RTK19_2",   20.0, 115.0,  5.0], \
              ["RTK19_3",   25.0, 110.0,  5.0], \
              ["RTK19_4",   25.0, 115.0,  5.0], \
              ["RTK20  ",   20.0, 120.0, 10.0], \
              ["RTK21  ",   10.0, 100.0, 10.0], \
              ["RTK22  ",   10.0, 110.0, 10.0]]

grid_edge = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]

def myCheckFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def myCheckRow(row, line_count, in_lati_pos, in_longi_pos):
    total_col_num = len(row)
    if(total_col_num < 3):
        print("Only "+str(total_col_num)+" column! in line"+str(line_count)+" Seemed not a comma separated file, aborting .......")
        print(row)
        return False

    if(in_lati_pos > total_col_num or in_longi_pos > total_col_num):
        print("column number in "+str(line_count)+" is larger than maximum column, please check it .......")
        print(row)
        return False

    if(not myCheckFloat(row[in_lati_pos]) or not myCheckFloat(row[in_longi_pos])):
        print("latitude or longitude in line "+str(line_count)+" is not valid float, please check it .......")
        print("latitude column/field is "+row[in_lati_pos]+" and longitude column/field is "+row[in_longi_pos])
        return False
    return True

def isStationInGrid(s, g, len):
    if((s[0] > g[0] and s[0] < g[0] + len) and (s[1] > g[1] and s[1] < g[1] + len)):
        return True
    else:
        return False

def isStationCloseToGrid(s, g, len, step):

    if isStationInGrid(s, g, len):
       return False
    else:
        new_g = [0.0, 0.0]
        new_g[0] = g[0] - step     # adjust square grid/region co-ordinate 
        new_g[1] = g[1] - step     # adjust squqre grid/region co-ordinate
        new_len = len + step * 2
        return isStationInGrid(s, new_g, new_len)

def extendGrid(curr_grid):
    
    for tmp_grid in curr_grid:
        grid_stat=[[0, '']]
        for tmp_grid_edge in grid_edge: 
            grid_stat.append([0,''])
        tmp_grid.append(grid_stat)
    return

def getGridStats(curr_grid, row, latitude, longitude):

    shared_stats = [0] * (len(grid_edge))

    for tmp_grid in curr_grid:
        grid_latitude  = float(tmp_grid[1])
        grid_longitude = float(tmp_grid[2])
        grid_name = tmp_grid[0]
        grid_len  = tmp_grid[3]
        grid_stat = tmp_grid[4]
        
        if(isStationInGrid([latitude, longitude], [grid_latitude, grid_longitude], grid_len)):
            row.append(grid_name)
            grid_stat[0][0] += 1
            #grid_stat[0][1] = "#"
        else:
            edge_count = 0
            for tmp_grid_edge in grid_edge:
                edge_count += 1
                if(isStationCloseToGrid([latitude, longitude], [grid_latitude, grid_longitude], grid_len, tmp_grid_edge)):
                    #row.append(grid_name)
                    grid_stat[edge_count][0] += 1
                    shared_stats[edge_count - 1] += 1
    
    return shared_stats

def showGridStats(curr_grid):

    print("Grid/Region "+"Stations", end='')
    for tmp_grid_edge in grid_edge:
        print("\t"+str(tmp_grid_edge)+"dg",end='')
    print('')

    for tmp_grid in curr_grid:
        print(tmp_grid[0]+" \t", end='')
        edge_count = 0
        grid_stat = tmp_grid[4]
        for tmp_grid_edge in grid_edge:
            print(grid_stat[edge_count][0], "\t", end='')
            edge_count += 1
        print(grid_stat[edge_count][0])
    return

if(len(sys.argv) < 2):
    print("Following are command/script format: ")
    print("    "+sys.argv[0]+" yourcsvfile " + " or ")
    print("    "+sys.argv[0]+" yourcsvfile " + " column-number-of-latitude " + " column-number-of-longitude ")
    print("    for example: "+sys.argv[0]+" station_list.csv")
    print("    for example: "+sys.argv[0]+" station_list.csv " + " 7 " + " 8 ")
    exit()
elif(len(sys.argv) > 3 ):
    if(not sys.argv[2].isdigit() or not sys.argv[3].isdigit()):
        print("input column number invalid, please check it ........")
        exit()
    else:
        lati_pos = int(sys.argv[2])
        longi_pos = int(sys.argv[3])
else:
    lati_pos = 7   #default column/position number for latitude
    longi_pos = 8  #default column/position number for longitude
    (file, extension) = os.path.splitext(sys.argv[1])
    if(extension != '.csv'):
        print("file must be a CSV file!")
        exit()

total_shared_stats = [[0,0,0,0]]*len(grid_edge)

with open(sys.argv[1], 'r', encoding='UTF-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    valid_line_cnt = 0

    csv_writer_1 = csv.writer(open(file+'_with_grid_1'+extension, 'w+', encoding='utf-8-sig', newline=''))
    csv_writer_2 = csv.writer(open(file+'_with_grid_2'+extension, 'w+', encoding='utf-8-sig', newline=''))

    extendGrid(grid_1)
    extendGrid(grid_2)

    for row_1 in csv_reader:
        row_2 = copy.copy(row_1)
        line_count += 1
        if(myCheckRow(row_1, line_count, lati_pos, longi_pos)):
            latitude = float(row_1[lati_pos])
            longitude = float(row_1[longi_pos])
            valid_line_cnt += 1

            shared_stats_1 = getGridStats(grid_1,  row_1, latitude, longitude)
            shared_stats_2 = getGridStats(grid_2,  row_2, latitude, longitude)

            row_1.append(shared_stats_1)
            row_2.append(shared_stats_2)

            grid_edge_cnt = 0
            for tmp_grid_edge in grid_edge:
                if(shared_stats_1[grid_edge_cnt] == 1):
                    total_shared_stats[grid_edge_cnt][1] += 1
                elif(shared_stats_1[grid_edge_cnt] == 2):
                    total_shared_stats[grid_edge_cnt][2] += 1
                elif(shared_stats_1[grid_edge_cnt] == 3):
                    total_shared_stats[grid_edge_cnt][2] += 1
                else:
                    total_shared_stats[grid_edge_cnt][0] += 1

        elif(valid_line_cnt == 0):
            row_1.append("GridName")
            row_2.append("GridName")

        csv_writer_1.writerow(row_1)
        csv_writer_2.writerow(row_2)

csv_file.close()


print("-----------------------------------------------\r\n")
if(line_count > 1):
    print("Total "+str(line_count)+" lines processed!")
    print("and "+str(valid_line_cnt)+" lines' data are valid! \r\n")
    showGridStats(grid_1)
    print('')
    print(total_shared_stats)
    print('')
    showGridStats(grid_2)
else:
    print("No valid line processed, please check the original CSV file!!")
