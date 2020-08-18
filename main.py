from dataModel import Dataset

class Main:
    pass



if __name__ == "__main__":
    file = 'dataset\\dataset.csv'
    ds = Dataset(filepath=file)
    ds.dateFilter(start_date='1/3/2012',end_date='1/5/2012')