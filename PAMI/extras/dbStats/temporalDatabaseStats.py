import statistics
import pandas as pd
import validators
from urllib.request import urlopen

class temporalDatabaseStats:
    """
    temporalDatabaseStats is class to get stats of database.

        Attributes:
        ----------
        inputFile : file
            input file path
        database : dict
            store time stamp and its transaction
        lengthList : list
            store size of all transaction
        timeStampCount : dict
            number of transactions per time stamp
        periodList : list
            all period list in the database
        sep : str
            separator in file. Default is tab space.

        Methods:
        -------
        run()
            execute readDatabase function
        readDatabase()
            read database from input file
        getDatabaseSize()
            get the size of database
        getMinimumTransactionLength()
            get the minimum transaction length
        getAverageTransactionLength()
            get the average transaction length. It is sum of all transaction length divided by database length.
        getMaximumTransactionLength()
            get the maximum transaction length
        getStandardDeviationTransactionLength()
            get the standard deviation of transaction length
        getSortedListOfItemFrequencies()
            get sorted list of item frequencies
        getSortedListOfTransactionLength()
            get sorted list of transaction length
        storeInFile(data, outputFile)
            store data into outputFile
        getMinimumPeriod()
            get the minimum period
        getAveragePeriod()
            get the average period
        getMaximumPeriod()
            get the maximum period
        getStandardDeviationPeriod()
            get the standard deviation period
        getNumberOfTransactionsPerTimestamp()
            get number of transactions per time stamp. This time stamp range is 1 to max period.
    """

    def __init__(self, inputFile, sep='\t'):
        """
        :param inputFile: input file name or path
        :type inputFile: str
        :param sep:
        """
        self.inputFile = inputFile
        self.database = {}
        self.lengthList = []
        self.timeStampCount = {}
        self.periodList = []
        self.sep = sep

    def run(self):
        self.readDatabase()

    def readDatabase(self):
        """
        read database from input file and store into database and size of each transaction.
        And store the period between transactions as list
        """
        numberOfTransaction = 0
        if isinstance(self.inputFile, pd.DataFrame):
            if self.inputFile.empty:
                print("its empty..")
            i = self.inputFile.columns.values.tolist()
            if 'ts' in i and 'Transactions' in i:
                self.database = self.inputFile.set_index('ts').T.to_dict(orient='records')[0]
            if 'ts' in i and 'Patterns' in i:
                self.database = self.inputFile.set_index('ts').T.to_dict(orient='records')[0]
            self.timeStampCount = self.inputFile.groupby('ts').count().T.to_dict(orient='records')[0]

        if isinstance(self.inputFile, str):
            if validators.url(self.inputFile):
                data = urlopen(self.inputFile)
                for line in data:
                    numberOfTransaction += 1
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self.sep)]
                    temp = [x for x in temp if x]
                    self.database[numberOfTransaction] = temp[1:]
                    self.timeStampCount[int(temp[0])] = self.timeStampCount.get(int(line[0]), 0)
                    self.timeStampCount[int(temp[0])] += 1
            else:
                try:
                    with open(self.inputFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            numberOfTransaction += 1
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self.sep)]
                            temp = [x for x in temp if x]
                            self.database[numberOfTransaction] = temp[1:]
                            self.timeStampCount[int(temp[0])] = self.timeStampCount.get(int(line[0]), 0)
                            self.timeStampCount[int(temp[0])] += 1
                except IOError:
                    print("File Not Found")
                    quit()
        self.lengthList = [len(s) for s in self.database.values()]
        timeStampList = sorted(list(self.database.keys()))
        preTimeStamp = 0
        for ts in timeStampList:
            self.periodList.append(int(ts)-preTimeStamp)
            preTimeStamp = ts

        # for line in self.Database:
        #     numberOfTransaction += 1
        #     self.database[numberOfTransaction] = line[1:]
        #     self.timeStampCount[int(line[0])] = self.timeStampCount.get(int(line[0]), 0)
        #     self.timeStampCount[int(line[0])] += 1
        # self.lengthList = [len(s) for s in self.database.values()]
        # timeStampList = sorted(list(self.timeStampCount.keys()))
        # preTimeStamp = 0
        # for ts in timeStampList:
        #     self.periodList.append(int(ts)-preTimeStamp)
        #     preTimeStamp = ts

    def getDatabaseSize(self):
        """
        get the size of database
        :return: data base size
        """
        return len(self.database)

    def getMinimumTransactionLength(self):
        """
        get the minimum transaction length
        :return: minimum transaction length
        """
        return min(self.lengthList)

    def getAverageTransactionLength(self):
        """
        get the average transaction length. It is sum of all transaction length divided by database length.
        :return: average transaction length
        """
        totalLength = sum(self.lengthList)
        return totalLength / len(self.database)

    def getMaximumTransactionLength(self):
        """
        get the maximum transaction length
        :return: maximum transaction length
        """
        return max(self.lengthList)

    def getStandardDeviationTransactionLength(self):
        """
        get the standard deviation transaction length
        :return: standard deviation transaction length
        """
        return statistics.pstdev(self.lengthList)

    def getVarianceTransactionLength(self):
        """
        get the variance transaction length
        :return: variance transaction length
        """
        return statistics.variance(self.lengthList)

    def getSparsity(self):
        # percentage of 0 dense dataframe
        """
        get the sparsity of database
        :return: database sparsity
        """
        matrixSize = self.getDatabaseSize()*len(self.getSortedListOfItemFrequencies())
        return (matrixSize - sum(self.getSortedListOfItemFrequencies().values())) / matrixSize

    def getTotalNumberOfItems(self):
        """
        get the number of items in database.
        :return: number of items
        """
        return len(self.getSortedListOfItemFrequencies())

    def getSortedListOfItemFrequencies(self):
        """
        get sorted list of item frequencies
        :return: item frequencies
        """
        itemFrequencies = {}
        for tid in self.database:
            for item in self.database[tid]:
                itemFrequencies[item] = itemFrequencies.get(item, 0)
                itemFrequencies[item] += 1
        return {k: v for k, v in sorted(itemFrequencies.items(), key=lambda x:x[1], reverse=True)}

    def getTransanctionalLengthDistribution(self):
        """
        get transaction length
        :return: transaction length
        """
        transactionLength = {}
        for length in self.lengthList:
            transactionLength[length] = transactionLength.get(length, 0)
            transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x: x[0])}

    def storeInFile(self, data, outputFile):
        """
        store data into outputFile
        :param data: input data
        :type data: dict
        :param outputFile: output file name or path to store
        :type outputFile: str
        """
        with open(outputFile, 'w') as f:
            for key, value in data.items():
                f.write(f'{key}\t{value}\n')

    def getMinimumPeriod(self):
        """
        get the minimum period
        :return: minimum period
        """
        return  min(self.periodList)

    def getAveragePeriod(self):
        """
        get the average period. It is sum of all period divided by number of period.
        :return: average period
        """
        totalPeriod = sum(self.periodList)
        return totalPeriod / len(self.periodList)

    def getMaximumPeriod(self):
        """
        get the maximum period
        :return: maximum period
        """
        return max(self.periodList)

    def getStandardDeviationPeriod(self):
        """
        get the standard deviation period
        :return: standard deviation period
        """
        return statistics.pstdev(self.periodList)

    def getNumberOfTransactionsPerTimestamp(self):
        """
        get number of transactions per time stamp
        :return: number of transactions per time stamp as dict
        """
        maxTS = max(list(self.timeStampCount.keys()))
        return {ts: self.timeStampCount.get(ts,0) for ts in range(1, maxTS+1)}

if __name__ == '__main__':
    data = {'ts': [1, 1, 3, 4, 5, 6, 7],

            'Transactions': [['a', 'd', 'e'], ['b', 'a', 'f', 'g', 'h'], ['b', 'a', 'd', 'f'], ['b', 'a', 'c'],
                             ['a', 'd', 'g', 'k'],

                             ['b', 'd', 'g', 'c', 'i'], ['b', 'd', 'g', 'e', 'j']]}

    data = pd.DataFrame.from_dict(data)
    obj = temporalDatabaseStats(data)
    obj = temporalDatabaseStats('https://www.u-aizu.ac.jp/~udayrage/datasets/temporalDatabases/temporal_T10I4D100K.csv')
    import PAMI.extras.graph.plotLineGraphFromDictionary as plt
    obj.run()
    print(f'Database size : {obj.getDatabaseSize()}')
    print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')
    print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
    print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
    print(f'Standard Deviation Transaction Size : {obj.getStandardDeviationTransactionLength()}')
    print(f'Variance : {obj.getVarianceTransactionLength()}')
    print(f'Sparsity : {obj.getSparsity()}')
    print(f'Number of items : {obj.getTotalNumberOfItems()}')
    print(f'Minimum period : {obj.getMinimumPeriod()}')
    print(f'Average period : {obj.getAveragePeriod()}')
    print(f'Maximum period : {obj.getMaximumPeriod()}')
    itemFrequencies = obj.getSortedListOfItemFrequencies()
    transactionLength = obj.getTransanctionalLengthDistribution()
    numberOfTransactionPerTimeStamp = obj.getNumberOfTransactionsPerTimestamp()
    # obj.storeInFile(itemFrequencies, 'itemFrequency.csv')
    # obj.storeInFile(transactionLength, 'transactionSize.csv')
    # obj.storeInFile(numberOfTransactionPerTimeStamp, 'numberOfTransaction.csv')
    plt.plotLineGraphFromDictionary(itemFrequencies, 100, 'itemFrequencies', 'item rank', 'frequency')
    plt.plotLineGraphFromDictionary(transactionLength, 100, 'transaction length', 'transaction length', 'frequency')
    plt.plotLineGraphFromDictionary(numberOfTransactionPerTimeStamp, 100)
