from os import path
import pickle


def load_classifier():
    f = open('./classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


if __name__ == "__main__":
    if not path.isfile('./classifier.pickle'):
        print "You didn't generate the classifier"
        sys.exit(1)
    classifier = load_classifier()
    print "classifier loaded"
