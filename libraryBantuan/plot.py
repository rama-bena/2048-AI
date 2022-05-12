from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, rewards, degree=5, iterative=True):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Nilai')

    plt.plot(scores, label='score')
    plt.plot(rewards, label='reward')

    
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(rewards)-1, rewards[-1], str(rewards[-1]))
    
    plt.legend()

    if iterative:
        plt.show(block=False)
        plt.pause(.1)
    else:
        plt.show()