import matplotlib.pyplot as plt


def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # TODO) Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [int(40/125*midterm + 60/100*final) for (midterm, final) in class_kr]
    midterm_en, final_en =zip(*class_en) 
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]
    
    # TODO) Plot midterm/final scores as points
    plt.scatter(midterm_kr,final_kr,color='red',label='Korean',s=10)
    plt.scatter(midterm_en, final_en,color='blue',label='English',s=40,marker='+')
    plt.grid()
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.legend()
    plt.xlim(0, 125)
    plt.ylim(0, 100)
    # TODO) Plot total scores as a histogram
    '''plt.hist(total_kr,color='r',alpha=0.7,label='Korean',bins=20,range=(0,100))
    plt.hist(total_en,color='b',alpha=0.7,label='English',bins=20,range=(0,100))
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.legend()
    plt.xlim([0, 100])'''
    plt.show()