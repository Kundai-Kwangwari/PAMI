import statistics
import pandas as pd
import validators
from urllib.request import urlopen

class transactionalDatabaseStats:
    """
    transactionalDatabaseStats is class to get stats of database.

        Attributes:
        ----------
        inputFile : file
            input file path
        database : dict
            store time stamp and its transaction
        lengthList : list
            store length of all transaction
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
        getVarianceTransactionLength()
            get the variance of transaction length
        getSparsity()
            get the sparsity of database
        getSortedListOfItemFrequencies()
            get sorted list of item frequencies
        getSortedListOfTransactionLength()
            get sorted list of transaction length
        storeInFile(data, outputFile)
            store data into outputFile
    """
    def __init__(self, inputFile, sep='\t'):
        """
        :param inputFile: input file name or path
        :type inputFile: str
        """
        self.inputFile = inputFile
        self.lengthList = []
        self.sep = sep
        self.database = {}

    def run(self):
        self.readDatabase()

    def readDatabase(self):
        """
        read database from input file and store into database and size of each transaction.
        """
        #self.creatingItemSets()
        numberOfTransaction = 0
        if isinstance(self.inputFile, pd.DataFrame):
            if self.inputFile.empty:
                print("its empty..")
            i = self.inputFile.columns.values.tolist()
            if 'tid' in i and 'Transactions' in i:
                self.database = self.inputFile.set_index('tid').T.to_dict(orient='records')[0]
            if 'tid' in i and 'Patterns' in i:
                self.database = self.inputFile.set_index('tid').T.to_dict(orient='records')[0]
        if isinstance(self.inputFile, str):
            if validators.url(self.inputFile):
                data = urlopen(self.inputFile)
                for line in data:
                    numberOfTransaction += 1
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self.sep)]
                    temp = [x for x in temp if x]
                    self.database[numberOfTransaction] = temp
            else:
                try:
                    with open(self.inputFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            numberOfTransaction += 1
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self.sep)]
                            temp = [x for x in temp if x]
                            self.database[numberOfTransaction] = temp
                except IOError:
                    print("File Not Found")
                    quit()
        self.lengthList = [len(s) for s in self.database.values()]

    def getDatabaseSize(self):
        """
        get the size of database
        :return: data base size
        """
        return len(self.database)

    def getTotalNumberOfItems(self):
        """
        get the number of items in database.
        :return: number of items
        """
        return len(self.getSortedListOfItemFrequencies())

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

    def getNumberOfItems(self):
        """
        get the number of items in database.
        :return: number of items
        """
        return len(self.getSortedListOfItemFrequencies())

    def getSparsity(self):
        """
        get the sparsity of database. sparsity is percentage of 0 of database.
        :return: database sparsity
        """
        matrixSize = self.getDatabaseSize() * len(self.getSortedListOfItemFrequencies())
        return (matrixSize - sum(self.getSortedListOfItemFrequencies().values())) / matrixSize

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
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x:x[0])}

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

if __name__ == '__main__':
    data = {'tid': [1, 2, 3, 4, 5, 6, 7],

            'Transactions': [['a', 'd', 'e'], ['b', 'a', 'f', 'g', 'h'], ['b', 'a', 'd', 'f'], ['b', 'a', 'c'],
                             ['a', 'd', 'g', 'k'],

                             ['b', 'd', 'g', 'c', 'i'], ['b', 'd', 'g', 'e', 'j']]}

    data = pd.DataFrame.from_dict(data)
    import PAMI.extras.graph.plotLineGraphFromDictionary as plt
    #obj = transactionalDatabaseStats(data)
    obj = transactionalDatabaseStats('https://www.u-aizu.ac.jp/~udayrage/datasets/transactionalDatabases/transactional_T10I4D100K.csv')
    obj.run()
    print(f'Database size : {obj.getDatabaseSize()}')
    print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')
    print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
    print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
    print(f'Standard Deviation Transaction Size : {obj.getStandardDeviationTransactionLength()}')
    print(f'Variance in Transaction Sizes : {obj.getVarianceTransactionLength()}')
    print(f'Number of items : {obj.getNumberOfItems()}')
    itemFrequencies = obj.getSortedListOfItemFrequencies()
    transactionLength = obj.getTransanctionalLengthDistribution()
    #obj.storeInFile(itemFrequencies, 'itemFrequency.csv')
    #obj.storeInFile(transactionLength, 'transactionSize.csv')
    plt.plotLineGraphFromDictionary(itemFrequencies, 100, 'itemFrequencies', 'item rank', 'frequency')
    plt.plotLineGraphFromDictionary(transactionLength, 100, 'transaction length', 'transaction length', 'frequency')
