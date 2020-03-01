#Commands to run:
1. #			Make all installs all the dependencies and run test with given path.
make all path="absolutepath"


OR 

1 #			First install all the dependencies
make dependencies

2 #			After installing all the dependenices just trun following command with absolute path.
make run path="absolutepath"

To generate new model run generateModel.py. It will require modify the file to give correct path to TrainingData.csv.
generateModel.py requires following packages to be imported.
1. pandas
2. sklearn
3. numpy
4. sklearn
5. scikit-learn
