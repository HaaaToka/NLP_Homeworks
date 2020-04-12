from bigram_hmm import HMM



def main():

    train_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\NERtagger\\train.txt"
    test_file_path = "E:\\Universite\\8yy\\497\\NLP_Homeworks\\NERtagger\\test.txt"

    bigram_hmm = HMM()

    sentences = bigram_hmm.dataset(train_file_path)

    bigram_hmm.HMM(sentences)


if __name__ == "__main__":
    main()   