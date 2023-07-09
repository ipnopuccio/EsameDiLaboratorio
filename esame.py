class ExamException(Exception):
    pass

class CSVTimeSeriesFile():

    def __init__(self, my_file):
        self.name = my_file
    
    def get_data(self):
        
        reader_my_file = self.open_my_file()

        my_data_file = self.read_my_file(reader_my_file)

        data = self.check_data_file(my_data_file)

        self.check_order(data)

        return data

    def open_my_file(self):
        try:
            open_my_file = open(self.name)
        except:
            raise ExamException("Impossibile aprire il file")        
        return open_my_file

    def read_my_file(self, reader_my_file):
        try:
            data = reader_my_file.read()
        except:
            raise ExamException("Impossibile leggere il file")
        return data.split("\n")

    def check_data_file(self, my_data):
        
        date_list=[]

        for item in my_data:

            data_split = item.split(',')
            valid_data = True

            try:
                n_passanger = int(data_split[1])
                
                if n_passanger < 0:
                    valid_data = False

            except:
                valid_data = False

            if '-' in data_split[0]:

                year = data_split[0].split('-')[0]
                month = data_split[0].split('-')[1]

                try:
                    int_year = int(year)
                    int_month = int(month)

                    if int_month<1 or int_month>12:
                        valid_data = False

                    if int_year < 1949 or int_year > 1960:
                        valid_data = False
                
                except:
                    valid_data = False
               
            else:
                valid_data = False

            if valid_data == True:
                date_list.append([data_split[0], n_passanger])

        return date_list

    def check_order(self,data):

        if not (len(data) < 2):
            date = data[0][0]

            for item in data[1:]:

                if(item[0] <= date):
                    raise ExamException("Errore: date non ordinate o con duplicati")
                date = item[0]

def compute_avg_monthly_difference(time_series, fy, ly):
    
    try:
        first_year=int(fy)
        last_year=int(ly)
    except: 
        raise ExamException("Errore: dati non confromi")

    if first_year >= last_year:
        raise ExamException("Errore: dati non conformi")

    monthly_values = []
    monthly_difference = last_year-first_year

    for i in range(monthly_difference + 1):

        this_year_list = [None] * 12

        for row in time_series:
            year = int(row[0].split('-')[0])

            if year == i + first_year:
                month = int(row[0].split('-')[1])
                this_year_list[month-1] = row[1]

        monthly_values.append(this_year_list)

    avg_diffs = []
    

    if monthly_difference == 1:

        for i in range(12):

            if monthly_values[0][i] != None and monthly_values[1][i] != None:
                avg_diffs.append(monthly_values[1][i]-monthly_values[0][i])

            else:
                avg_diffs.append(0)

    else:
        for i in range(12):
            total_diff = 0
            count_diff = 0

            for j in range(len(monthly_values) - 1):

                if monthly_values[j][i] != None and monthly_values[j + 1][i] != None:
                    total_diff +=  monthly_values[j + 1][i] - monthly_values[j][i]
                    count_diff += 1

                elif monthly_values[j][i] != None and monthly_values[j + 1][i] == None:
                    increment = 0
                    while(monthly_values[j + 1 + increment][i] == None):
                        increment += 1

                    total_diff +=  monthly_values[j + 1][i] - monthly_values[j][i]
                    count_diff += 1 

            if count_diff < 2:
                avg_diffs.append(0)
            
            else:
                avg_diffs.append(total_diff/count_diff)

    return avg_diffs

