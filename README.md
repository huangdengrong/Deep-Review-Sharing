# Deep-Review-Sharing: Towards Review-Based Software Improvement ,Where Software Projects  Without sufficient Reviews
# Introduction
Deep-Review-Sharing  is a user review recommendation system based on code cloning.
It is also an Eclipse plug-in system. Its implementation principle is mainly divided into two stages:
code clone and user comment recommendation. The code clone mainly  uses convolutional neural network.
User comment recommendation is mainly to recommend reasonable comments to the code entered by the user through the plugin.

In my repo Eclipse Rcp is used to realize the visualization of the user comment recommendation system. 
By calling python program in eclipse rcp, the entire recommendation system is implemented. 
Convolutional neural networks are mainly implemented in Python.
# Environment
This code has been tested on Windows 10/64 bit, python environment 3.6, and jdk version 1.8.

# Instructions for use
First open eclipse rcp (which is eclipse rcp is not ordinary eclipse), 
import MyRcpView project into eclipse, find META-INF, click MANIFEST.MF to enter the eclipse Overview page, 
and then find the Eclipse Application under Run as under the Run menu bar. 
Click to run the program. Will get the following interface, Input Code is the button for the user to enter their own code, 
Default Review is the comment corresponding to the code entered by the user, 
the default is to select the corresponding three-code corresponding to the user input code from the local data set.


Under window/Review Recommend is all the functions implemented by the system. 
Input Code is used for user  to input require comments. 
Output One Review is for user to input code recommend user comments for the previous code.
Output Two Review is for users to input code recommends the user comments corresponding to the first two codes, 
and Show Similarity Value is used to output the corresponding similarity value.
