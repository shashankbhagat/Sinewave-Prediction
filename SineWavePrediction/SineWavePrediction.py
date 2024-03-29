
#from EarthQuake_phase_1 import EarthQuakePhase1
import numpy as np
import time
import random as rd
import pandas as pd
from matplotlib import pyplot as plt
import pickle
import os.path

class LSTM(object):
    """description of class"""
    def __init__(self, *args, **kwargs):
        np.random.seed(int(time.time()))
        #initialise weights
        #initially set forget gate to 1 to remember everything
        #using only one weight list instead of W and U
        self.Weights_forget_1=np.array(1)     #as per Felix lstm research to remember everything initially
        self.Weights_forget_2=np.array(1)     #as per Felix lstm research to remember everything initially 
        # weights initialised between -0.1 to 0.1 as per Felix research
        #self.Weights_input_1=np.array(np.random.uniform(-0.1,0.1))
        #self.Weights_input_2=np.array(np.random.uniform(-0.1,0.1))
        #self.Weights_output_1=np.array(np.random.uniform(-0.1,0.1))
        #self.Weights_output_2=np.array(np.random.uniform(-0.1,0.1))
        #self.Weights_A_1=np.array(np.random.uniform(-0.1,0.1))
        #self.Weights_A_2=np.array(np.random.uniform(-0.1,0.1))

        self.Weights_input_1=np.array(np.random.random())
        self.Weights_input_2=np.array(np.random.random())
        self.Weights_output_1=np.array(np.random.random())
        self.Weights_output_2=np.array(np.random.random())
        self.Weights_A_1=np.array(np.random.random())
        self.Weights_A_2=np.array(np.random.random())

        #weight gradients
        self.gradient_weights_forget_1=np.array(0)     
        self.gradient_weights_forget_2=np.array(0)        
        self.gradient_weights_input_1=np.array(0)
        self.gradient_weights_input_2=np.array(0)
        self.gradient_weights_output_1=np.array(0)
        self.gradient_weights_output_2=np.array(0)
        self.gradient_weights_A_1=np.array(0)
        self.gradient_weights_A_2=np.array(0)
        self.gradient_input_gate_bias=np.array(0)
        self.gradient_forget_gate_bias=np.array(0)
        self.gradient_input_A_gate_bias=np.array(0)
        self.gradient_output_gate_bias=np.array(0)

        #initialise biases
        #input and output gate bias should be -ve
        ##initially set forget gate to 1 to remember everything
        # as per felix, initialise input bias=0, forget bias=-2 and output bias=2
        #self.input_gate_bias=np.array(0)
        #self.forget_gate_bias=np.array(-2)
        #self.input_A_gate_bias=np.array(np.random.uniform(-0.1,0.1))
        #self.output_gate_bias=np.array(2)

        self.input_gate_bias=np.array(np.random.random())
        self.forget_gate_bias=np.array(1)
        self.input_A_gate_bias=np.array(np.random.random())
        self.output_gate_bias=np.array(np.random.random())
        #initialise weight matrix. Comprises of all weights(Z)
        self.weights_matrix=np.zeros((4,3))
        self.weights_matrix[0][0]=self.Weights_A_1; self.weights_matrix[0][1]=self.Weights_A_2; self.weights_matrix[0][2]=self.input_A_gate_bias;
        self.weights_matrix[1][0]=self.Weights_input_1; self.weights_matrix[1][1]=self.Weights_input_2; self.weights_matrix[1][2]=self.input_gate_bias;
        self.weights_matrix[2][0]=self.Weights_forget_1; self.weights_matrix[2][1]=self.Weights_forget_2; self.weights_matrix[2][2]=self.forget_gate_bias;
        self.weights_matrix[3][0]=self.Weights_output_1; self.weights_matrix[3][1]=self.Weights_output_2; self.weights_matrix[3][2]=self.output_gate_bias;
        
        #print(self.weights_matrix)
        #gates initialisation
        self.input_gate=[]
        self.forget_gate=[]
        self.input_A_gate=[]
        self.output_gate=[]
        self.cell_state=[]
        self.cell_state_previous=np.array(0)
        self.cell_state_current=np.array(0)
        self.deltas=[]
        self.input=0
        self.previous_output=np.array(0)
        self.cell_output=np.array(0)
        self.expected_cell_output=np.array(0)
        self.error=np.array(0)
        self.delta_output_gate=np.array(0)
        self.delta_cell_state=np.array(0)
        self.delta_input_gate=np.array(0)
        self.delta_input_A_gate=np.array(0)
        self.delta_forget_gate=np.array(0)
        self.delta_cell_output=np.array(0)
        self.delta_cumulative_error=np.array(0)

        #input matrix
        self.input_matrix=np.zeros(3)

        self.input_matrix_X=np.zeros((1,1))
        self.input_matrix_U=np.zeros((1,1))
        self.input_matrix_b=np.zeros((1,1))

        #variables needed for weights calculation
        self.delta_gate_list=np.zeros((4,1))
        return super().__init__(*args, **kwargs)
        
    pass

class LSTMNetwork():
    def __init__(self, cells,data,global_date_max):
        self.lstmCellsCnt=cells
        self.dataset=data
        self.global_date_max=global_date_max
        #self.expectedOutput=expectedOutput
        self.lstmCellObjList=[]
        self.lastPrediction=np.array(0)
        self.predictionResult=[]
        self.lastPredictionSet=[0 for i in range(cells)]
        return

    def initialiseLSTMCells(self):
        for i in range(self.lstmCellsCnt):
            self.lstmCellObjList.append(LSTM())

    def TrainNetwork(self):
        listPtr=0
        lastPrediction=np.array(0)
        temp_previous_output=np.array(0)
        temp_previous_cell_state=np.array(0)
        listPtr=0
        for cntr in range(30):#10
            listPtr=0
            print('Epoch# ',cntr,' running...')
            
            #for i in range(len(self.dataset)-1-self.lstmCellsCnt+1):
                #print('set#: ',i+1)
                #cellDataSet=self.dataset[listPtr:listPtr+self.lstmCellsCnt+1]

            while listPtr<len(self.dataset)-1:

                cellDataSet=self.dataset[listPtr:listPtr+self.lstmCellsCnt+1] #3 cause 2 lstm cells
                listPtr+=1
                temp_previous_output=np.array(0)
                temp_previous_cell_state=np.array(0)
                if len(cellDataSet)<(self.lstmCellsCnt+1):
                    break

                for j in range(self.lstmCellsCnt):
                    #if j==0:
                    #    print('prev cell state:',temp_previous_cell_state)
                    lstmCell=self.lstmCellObjList[j]
                    lstmCell.expected_cell_output=cellDataSet[j+1]
                                
                    lstmCell.previous_output=temp_previous_output           #initializing previous cell output
                    lstmCell.cell_state_previous=temp_previous_cell_state       #initializing previous cell state

                    temp_previous_output,temp_previous_cell_state=self.forwardPass(lstmCell,cellDataSet[j])    #forward pass
                    lstmCell.error= temp_previous_output-lstmCell.expected_cell_output    #error calculation
                    lstmCell.cell_state_current=temp_previous_cell_state        #current cell state
                    #print('error with cell# ',j+1,':',lstmCell.error,'\t input: ',cellDataSet[0]*15000,' \tpredicted:',temp_previous_output*15000)
                    #print('error with cell# ',j+1,':',lstmCell.error,'\t input: ',pd.to_datetime(cellDataSet[j]*self.global_date_max),' \tpredicted:',pd.to_datetime(temp_previous_output*self.global_date_max))
                    lastPrediction=temp_previous_output
                    self.lstmCellObjList[j]=lstmCell
                    if j<self.lstmCellsCnt-1:
                        self.lastPredictionSet[j]=lastPrediction

                self.backPropagate(self.lstmCellObjList,0)
                self.updateWeights(self.lstmCellObjList)
            
        return lastPrediction

    def updateWeights(self,lstmCellObjList):
        total_delta_W=np.zeros((4,1))
        total_delta_U=np.zeros((4,1))
        total_delta_b=np.zeros((4,1))
        total_delta=np.zeros((3,4))
        learning_rate=0.5
        for i in range(len(lstmCellObjList)):
            lstmCellObj=lstmCellObjList[i]
            total_delta_W+=np.dot(lstmCellObj.delta_gate_list,lstmCellObj.input_matrix_X)
            total_delta_U+=np.dot(lstmCellObj.delta_gate_list,lstmCellObj.input_matrix_U)
            #if i==0:
            #    total_delta_U+=np.array(0)                
            #else:
            #    total_delta_U+=np.dot(lstmCellObj.delta_gate_list,lstmCellObjList[i-1].input_matrix_U)

            total_delta_b+=np.dot(lstmCellObj.delta_gate_list,np.array(1))

            total_delta[0]=total_delta_W.T
            total_delta[1]=total_delta_U.T
            total_delta[2]=total_delta_b.T

            #lstmCellObj.weights_matrix=lstmCellObj.weights_matrix-np.dot(learning_rate,total_delta.T)

        for i in range(len(lstmCellObjList)):
            lstmCellObj=lstmCellObjList[i]
            lstmCellObj.weights_matrix=lstmCellObj.weights_matrix-np.dot(learning_rate,total_delta.T)
            
        return


    def backPropagate(self,lstmCellObjList,cellLocation):
        #print('back propagate cells#: ',len(lstmCellObjList))
        for cellLoc in range(len(lstmCellObjList)-1,-1,-1):     #back propagate the cell just forward propagated.
            lstmCellObj=lstmCellObjList[cellLoc]
            
            if cellLoc==len(lstmCellObjList)-1:
                backtrackObj=LSTM()
            else:
                backtrackObj=lstmCellObjList[cellLoc+1]
            
            #delta cell output
            #print('cumulative error(del t):',cellLoc,':',lstmCellObj.delta_cumulative_error)
            if cellLoc==len(lstmCellObjList)-1:
                lstmCellObj.delta_cell_output=lstmCellObj.error+np.array(0)
            else:                
                lstmCellObj.delta_cell_output=lstmCellObj.error+lstmCellObj.delta_cumulative_error

            #delta cell state
            if cellLoc==len(lstmCellObjList)-1:
                lstmCellObj.delta_cell_state=np.dot(lstmCellObj.delta_cell_output,np.dot(lstmCellObj.output_gate,np.array(1)-np.square(np.tanh(lstmCellObj.cell_state_current))))+np.array(0)
            else:
                lstmCellObj.delta_cell_state=np.dot(lstmCellObj.delta_cell_output,np.dot(lstmCellObj.output_gate,np.array(1)-np.square(np.tanh(lstmCellObj.cell_state_current))))+np.dot(backtrackObj.delta_cell_state,backtrackObj.forget_gate)

            #delta input A gate
            lstmCellObj.delta_input_A_gate=np.dot(lstmCellObj.delta_cell_state,np.dot(lstmCellObj.input_gate,np.array(1)-np.square(lstmCellObj.input_A_gate)))

            #delta input gate
            lstmCellObj.delta_input_gate=np.dot(lstmCellObj.delta_cell_state,np.dot(lstmCellObj.input_A_gate,np.dot(lstmCellObj.input_gate,np.array(1)-lstmCellObj.input_gate)))

            #delta forget gate
            if cellLoc==0:
                lstmCellObj.delta_forget_gate=0.0
            else:
                lstmCellObj.delta_forget_gate=np.dot(lstmCellObj.delta_cell_state,np.dot(lstmCellObj.cell_state_previous,np.dot(lstmCellObj.forget_gate,np.array(1)-lstmCellObj.forget_gate)))

            #delta output gate
            lstmCellObj.delta_output_gate=np.dot(lstmCellObj.delta_cell_output,np.dot(np.tanh(lstmCellObj.cell_state_current),np.dot(lstmCellObj.output_gate,np.array(1)-lstmCellObj.output_gate)))

            #delta cumulative error
            if cellLoc==len(lstmCellObjList)-1:
                lstmCellObj.delta_cumulative_error=np.array(0)

        #    self.weights_matrix=np.zeros((4,3))
        #self.weights_matrix[0][0]=self.Weights_A_1; self.weights_matrix[0][1]=self.Weights_A_2; self.weights_matrix[0][2]=self.input_A_gate_bias;
        #self.weights_matrix[1][0]=self.Weights_input_1; self.weights_matrix[1][1]=self.Weights_input_2; self.weights_matrix[1][2]=self.input_gate_bias;
        #self.weights_matrix[2][0]=self.Weights_forget_1; self.weights_matrix[2][1]=self.Weights_forget_2; self.weights_matrix[2][2]=self.forget_gate_bias;
        #self.weights_matrix[3][0]=self.Weights_output_1; self.weights_matrix[3][1]=self.Weights_output_2; self.weights_matrix[3][2]=self.output_gate_bias;
        
            lstmCellObj.delta_gate_list[0][0]=lstmCellObj.delta_input_A_gate
            lstmCellObj.delta_gate_list[1][0]=lstmCellObj.delta_input_gate
            lstmCellObj.delta_gate_list[2][0]=lstmCellObj.delta_forget_gate
            lstmCellObj.delta_gate_list[3][0]=lstmCellObj.delta_output_gate
            
            if cellLoc>0:
                weight_U_matrix=np.zeros((1,4))
                weight_U_matrix[0][0]=lstmCellObj.weights_matrix[0][1]  #lstmCellObj.Weights_A_2
                weight_U_matrix[0][1]=lstmCellObj.weights_matrix[1][1]   #lstmCellObj.Weights_input_2
                weight_U_matrix[0][2]=lstmCellObj.weights_matrix[2][1]  #lstmCellObj.Weights_forget_2
                weight_U_matrix[0][3]=lstmCellObj.weights_matrix[3][1]  #lstmCellObj.Weights_output_2

                
                
                lstmCellObjList[cellLoc-1].delta_cumulative_error=np.dot(weight_U_matrix,lstmCellObj.delta_gate_list)
                #lstmCellObj.delta_cumulative_error=np.dot(weight_U_matrix,lstmCellObj.delta_gate_list)
            
        return

    def forwardPass(self,lstmCell,current_input):
        #assemble input matrix        
        lstmCell.input_matrix=np.hstack((current_input,lstmCell.previous_output,1))
        lstmCell.input_matrix_X[0]=current_input
        lstmCell.input_matrix_U[0]=lstmCell.previous_output
        lstmCell.input_matrix_b[0]=1

        #forget gate computation
        complete_weights=np.hstack((lstmCell.weights_matrix[2][0],lstmCell.weights_matrix[2][1],lstmCell.weights_matrix[2][2]))
        complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)           
        lstmCell.forget_gate=self.sigmoid(np.dot(complete_weights.T,lstmCell.input_matrix))
        
        #input gate computation
        complete_weights=np.hstack((lstmCell.weights_matrix[1][0],lstmCell.weights_matrix[1][1],lstmCell.weights_matrix[1][2]))
        complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)
        lstmCell.input_gate=self.sigmoid(np.dot(complete_weights.T,lstmCell.input_matrix))

        #input A gate computation
        complete_weights=np.hstack((lstmCell.weights_matrix[0][0],lstmCell.weights_matrix[0][1],lstmCell.weights_matrix[0][2]))
        complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)
        lstmCell.input_A_gate=np.tanh(np.dot(complete_weights.T,lstmCell.input_matrix))

        #output gate computation
        complete_weights=np.hstack((lstmCell.weights_matrix[3][0],lstmCell.weights_matrix[3][1],lstmCell.weights_matrix[3][2]))
        complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)
        lstmCell.output_gate=self.sigmoid(np.dot(complete_weights.T,lstmCell.input_matrix))
                
        #cell state (Ct) computation
        lstmCell.cell_state=np.array((np.dot(lstmCell.forget_gate,lstmCell.cell_state_previous))+(np.dot(lstmCell.input_gate,lstmCell.input_A_gate)))
        
        #cell output (ht) computation
        lstmCell.cell_output=np.array(np.dot(lstmCell.output_gate,np.tanh(lstmCell.cell_state)))
        
        return np.array(lstmCell.cell_output),lstmCell.cell_state

    def sigmoid(self,inX):
        return 1/(1+np.exp(-inX))

    def predict(self,current_input,test_data):
        test_data=list(test_data)
        cnt=0
        i=0
        slidingPtr=0
        pred_val=np.array(0)
        prev_val=np.array(0)
        print('size: ',len(self.lstmCellObjList))
        threshold=int((pd.to_datetime('12/31/2017')+pd.Timedelta(days=365*80)).to_datetime64())
        cellCnt=len(self.lstmCellObjList)
        #while(pred_val<=threshold):
        while(slidingPtr<len(test_data)):
            #if current_input>=20:          #12312022:
            #    break
            prev_val=np.array(0)
            inputList=list(test_data[slidingPtr:slidingPtr+cellCnt]) #test_data[slidingPtr]  #list(test_data[slidingPtr:cellCnt+slidingPtr])
            #print('current input:',pd.to_datetime(current_input*self.global_date_max))
            if len(inputList)<cellCnt:
                break
            prev_val=np.array(0)
            for cnt in range(len(self.lstmCellObjList)):
                #assemble input matrix    
                lstmCell=self.lstmCellObjList[cnt]
                
                lstmCell.previous_output=prev_val
                #print('prev output:',lstmCell.previous_output)
                #lstmCell.input_matrix=np.hstack((current_input,lstmCell.previous_output,1))
                lstmCell.input_matrix=np.hstack((inputList[cnt],lstmCell.previous_output,1))
                lstmCell.input_matrix_X[0]=inputList[cnt] #current_input
                lstmCell.input_matrix_U[0]=lstmCell.previous_output
                lstmCell.input_matrix_b[0]=1

                #forget gate computation
                complete_weights=np.hstack((lstmCell.weights_matrix[2][0],lstmCell.weights_matrix[2][1],lstmCell.weights_matrix[2][2]))
                complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)           
                lstmCell.forget_gate=self.sigmoid(np.dot(complete_weights.T,lstmCell.input_matrix))
        
                #input gate computation
                complete_weights=np.hstack((lstmCell.weights_matrix[1][0],lstmCell.weights_matrix[1][1],lstmCell.weights_matrix[1][2]))
                complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)
                lstmCell.input_gate=self.sigmoid(np.dot(complete_weights.T,lstmCell.input_matrix))

                #input A gate computation
                complete_weights=np.hstack((lstmCell.weights_matrix[0][0],lstmCell.weights_matrix[0][1],lstmCell.weights_matrix[0][2]))
                complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)
                lstmCell.input_A_gate=np.tanh(np.dot(complete_weights.T,lstmCell.input_matrix))

                #output gate computation
                complete_weights=np.hstack((lstmCell.weights_matrix[3][0],lstmCell.weights_matrix[3][1],lstmCell.weights_matrix[3][2]))
                complete_weights=complete_weights.reshape(complete_weights.shape[0],-1)
                lstmCell.output_gate=self.sigmoid(np.dot(complete_weights.T,lstmCell.input_matrix))
                
                #cell state (Ct) computation
                lstmCell.cell_state=np.array((np.dot(lstmCell.forget_gate,lstmCell.cell_state_previous))+(np.dot(lstmCell.input_gate,lstmCell.input_A_gate)))
        
                #cell output (ht) computation
                lstmCell.cell_output=np.array(np.dot(lstmCell.output_gate,np.tanh(lstmCell.cell_state)))

                #previous output
                prev_val=lstmCell.cell_output
                pred_val=lstmCell.cell_output
                #prediction
                #print('input:',pd.to_datetime(inputList[0]*self.global_date_max),' predicted:',pd.to_datetime(lstmCell.cell_output*self.global_date_max))
                print('input:',(inputList[cnt]*self.global_date_max),' predicted:',(lstmCell.cell_output*self.global_date_max))
                #self.predictionResult.append(pred_val)

            print('#'*100)
            print('total prediction:',(pred_val*self.global_date_max))
            #print('total prediction:',pd.to_datetime(pred_val*15000))
            self.predictionResult.append(pred_val)
            #test_data.append(pred_val)
            print('*'*100)
            i+=1
            current_input=pred_val
            slidingPtr+=1
        
        return 


    pass


timeData=np.arange(0,50,0.1)
amp=np.sin(timeData)

maxVal=max(amp)
amp=np.divide(amp,maxVal)


#data=np.random.randint(1,15000,size=(21000,1))
#data.sort(axis=0)
#test_data=data[20000:]
#data=data[:20000]
#data=np.divide(data,15000)
#test_data=np.divide(test_data,15000)
#print(len(data),len(data)-10+1)
#print('input: ',data)
print('-'*100)
#lstmNet=LSTMNetwork(5,data,1)
lstmNet=LSTMNetwork(3,amp,maxVal) #25

if os.path.isfile('lstmTraining1.sb'):
    with open('lstmTraining.sb','rb') as lstmRead:
        lstmNet=pickle.load(lstmRead)
else:
    print('would init')
    lstmNet.initialiseLSTMCells()
    lstmNet.lastPrediction=lstmNet.TrainNetwork()
    #lstmNet.lastPrediction=lstmNet.TrainNetwork()

#save status of training in a file
with open('lstmTraining.sb','wb') as lstmWrite:
    pickle.dump(lstmNet,lstmWrite)


print('*'*100)
#print('total prediction:',pd.to_datetime(lstmNet.lastPrediction*lstmNet.global_date_max))
lstmNet.predict(lstmNet.lastPrediction,list(amp)) #list(data)+list(test_data)
#print('-'*100)
#for i in range(20):
#    print(pd.to_datetime(test_data[i]*global_date_max))

#plot graphs
plt.plot(list(amp),label='Training & Test Data')
#plt.plot(test_data,label='Test Data')

plt.plot(list(lstmNet.predictionResult),label='Predicted Data')
plt.legend()
plt.show(block=False)

plt.show()