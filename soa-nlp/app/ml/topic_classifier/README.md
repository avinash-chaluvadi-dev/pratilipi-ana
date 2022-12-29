## **Topic(Reason For Call)Classifier**
<br>

**Topic Classifier** is a multi-label classifier that allows to classify each sentence into zero or more mutually non-exclusive class labels.

<br>

### **Software Requirements**
- - - -
1. OS(Windows, Linix, MacOs)
1. Python >= 3.6
1. CUDA > 10, cuDNN > 7.0(optional)

<br>

### **Application Requirements**
- - - -
1. [nltk](https://www.nltk.org/)
1. [Numpy](https://numpy.org/)
1. [Pandas](https://pandas.pydata.org/)
1. [PyTorch](https://pytorch.org/)
1. [Simple Transformers](https://simpletransformers.ai/)
1. [Scikit Multilearn](http://scikit.ml/)

You will also need to have software installed to run and execute a [Jupyter Notebook](https://jupyter.org/install.html).

<br>

### **Environment setup**
- - - -

**virtual environment** can be created using the below commands
```shell 
python -m venv venv
```

**Package requirements** can be installed using the below command
```shell 
pip install -r requirements.txt
```

<br>

### **Dataset**
- - - -
The topic classifier dataset consists of around **29K** data points, with each datapoint having 1 independent feature(Message) and 1 dependent feature(Label)
* Input is **Message/voicemail**
* Output is **Reason for Call** which can fall into alteast one of the below **TOPICS**
  1. **Access to Care**
  2. **Authorization**
  3. **Benefits**
  4. **Claim**
  5. **EE Benefits**
  6. **Grievance and/or Appeal**
  7. **ID Card**
  8. **Membership/Enrollment**
  9. **Monthly Premium**
  10. **Need Case Management**
  11. **No Reason Given**
  12. **Nurse Line**
  13. **OTC**
  14. **Provider**
  15. **RX/Pharmacy**
  16. **Transportation**
   
  <br>

* **Input Encoding**
    * There are various ways to encode text one of them is **word embeddings**, by taking the mean of all the word embeddings we get sentence embeddings.
  
  <br>

* **Output Encoding**
    * There are various ways to encode multi-label strings one of them is one hot encoding.


<br>

### **Code/Implementation**
- - - -

* #### **Training:**
    * **Preprocessing functions** has already been implemented, you will need to implement additional things as per requirement
    * Topic classifier code is provided in the train.ipynb notebook file. You will also be required to use the voicemail_data.xlxs dataset  file if it is stored on file-system modify the **Dataset Prepration** section to complete your work. While some classifiers has already been implemented to get you started, you will need to implement additional classifiers as per requirement.
    
    
    * To **RUN** the training code, In a terminal or command window, navigate to the top-level project directory(that contains this README) and run the below command:
    ```shell 
   ipython notebook boston_housing.ipynb
   ```
  
* #### **Serving:**
  * Topic Classifier package has 4 python modules
    1. utils.py&emsp;&emsp;&ensp;&emsp;--> utility module which holds general functions
    2. config.py&emsp;&emsp;&nbsp;    --> configuration parameters are stored in this module
    3. main.py &emsp;&emsp;&ensp;     --> entry point module for topic classifier serve component
    4. preprocess.py&ensp;--> preprocessing/text cleaning functions are placed in this module.
   
    <br>

  * Serving component of topic classifier has already been implemented, which takes input as either list of sentences or a single sentence and returns dictionary of inputs, output labels and confidence scores.
   
  * To **RUN** the training code, In a terminal or command window, navigate to the top-level project directory(that contains this README) and run the below command
   ```shell 
   python main.py --model="serve"
   ```
<br>

### **Results**
- - - -
- **SVM** is performing well when compared to other classifiers like **Naive Bayes**, **Random Forest** and **XGBoost**.
- **Evaluation Metrics:**
  1. SVM: 0.6455853615206963
  2. XGBoost: 0.5045301119204122
  3. Naive Bayes: 0.3020074613608101
  4. Random Forest: 0.5045301119204122


- **SVM Classification Report**

    |  Topic/Reason for Call  | precision |  recall  | f1-score | support |
    | :---------------------: | :-------: | :------: | :------: | :-----: |
    |     Access to Care      | 0.285714  | 0.098765 | 0.146789 |  81.0   |
    |      Authorization      | 0.722222  | 0.295455 | 0.419355 |  44.0   |
    |        Benefits         | 0.757576  | 0.416667 | 0.537634 |  180.0  |
    |          Claim          | 0.739726  | 0.724832 | 0.732203 |  149.0  |
    |       EE Benefits       | 0.666667  | 0.142857 | 0.235294 |  28.0   |
    | Grievance and/or Appeal | 0.677419  | 0.338710 | 0.451613 |  62.0   |
    |         ID Card         | 0.566265  | 0.691176 | 0.622517 |  68.0   |
    |  Membership/Enrollment  | 0.753623  | 0.722222 | 0.737589 |  216.0  |
    |     Monthly Premium     | 0.944444  | 0.596491 | 0.731183 |  57.0   |
    |  Need Case Management   | 0.000000  | 0.000000 | 0.000000 |  10.0   |
    |     No Reason Given     | 0.602941  | 0.878571 | 0.715116 |  140.0  |
    |       Nurse Line        | 0.928571  | 0.764706 | 0.838710 |  17.0   |
    |           OTC           | 0.826590  | 0.768817 | 0.796657 |  186.0  |
    |        Provider         | 0.786667  | 0.526786 | 0.631016 |  112.0  |
    |       RX/Pharmacy       | 0.800000  | 0.440000 | 0.567742 |  100.0  |
    |     Transportation      | 0.730263  | 0.792857 | 0.760274 |  140.0  |
